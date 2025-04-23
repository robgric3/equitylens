# dags/system_monitoring.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import json
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'system_health_monitoring',
    default_args=default_args,
    description='Monitor system health for EquityLens',
    schedule_interval='0 * * * *',  # Run hourly
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['equitylens', 'monitoring'],
)

# Check API health
check_api_health = SimpleHttpOperator(
    task_id='check_api_health',
    http_conn_id='equitylens_api',
    endpoint='health',
    method='GET',
    response_check=lambda response: response.json()['status'] == 'healthy',
    log_response=True,
    dag=dag,
)

# Check Calculation Engine health
check_calculation_engine_health = SimpleHttpOperator(
    task_id='check_calculation_engine_health',
    http_conn_id='equitylens_calculation_engine',
    endpoint='health',
    method='GET',
    response_check=lambda response: response.json()['status'] == 'healthy',
    log_response=True,
    dag=dag,
)

# Check database health
check_database_health = PostgresOperator(
    task_id='check_database_health',
    postgres_conn_id='equitylens_db',
    sql='SELECT 1;',
    dag=dag,
)

# Check data freshness
check_data_freshness = PostgresOperator(
    task_id='check_data_freshness',
    postgres_conn_id='equitylens_db',
    sql="""
    SELECT 
        CASE 
            WHEN MAX(date) > NOW() - INTERVAL '2 days' THEN 1
            ELSE 0
        END as is_fresh
    FROM market_data.daily_prices
    WHERE symbol = 'SPY';
    """,
    dag=dag,
)

def process_monitoring_results(**kwargs):
    """Process the results of the monitoring tasks"""
    ti = kwargs['ti']
    
    try:
        api_result = ti.xcom_pull(task_ids='check_api_health')
        calc_engine_result = ti.xcom_pull(task_ids='check_calculation_engine_health')
        db_result = ti.xcom_pull(task_ids='check_database_health')
        data_freshness = ti.xcom_pull(task_ids='check_data_freshness')
        
        all_healthy = all([
            api_result is not None,
            calc_engine_result is not None,
            db_result is not None,
            data_freshness and data_freshness[0][0] == 1
        ])
        
        if all_healthy:
            logging.info("All systems are healthy")
        else:
            logging.error("Some systems are unhealthy!")
            
            if api_result is None:
                logging.error("API health check failed")
            
            if calc_engine_result is None:
                logging.error("Calculation Engine health check failed")
            
            if db_result is None:
                logging.error("Database health check failed")
            
            if not data_freshness or data_freshness[0][0] != 1:
                logging.error("Data freshness check failed - market data may be stale")
        
        return all_healthy
    except Exception as e:
        logging.error(f"Error processing monitoring results: {e}")
        return False

process_results = PythonOperator(
    task_id='process_monitoring_results',
    python_callable=process_monitoring_results,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
[check_api_health, check_calculation_engine_health, check_database_health, check_data_freshness] >> process_results