# dags/market_data_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import logging
import os
from sqlalchemy import create_engine, text

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define DAG
dag = DAG(
    'market_data_pipeline',
    default_args=default_args,
    description='Extract daily market data for equity portfolio analysis',
    schedule_interval='0 18 * * 1-5',  # Run at 6 PM on weekdays
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['equitylens', 'market_data'],
)

# Define the list of tickers to track
# In a production environment, this would be dynamically loaded from the database
TICKERS = [
    # US Large Cap Tech
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
    
    # US Financials
    'JPM', 'BAC', 'WFC', 'GS', 'MS',
    
    # US Healthcare
    'JNJ', 'PFE', 'MRK', 'UNH', 'ABBV',
    
    # US Consumer
    'PG', 'KO', 'PEP', 'WMT', 'MCD',
    
    # UK Stocks (FTSE 100)
    'BP.L', 'HSBA.L', 'GSK.L', 'ULVR.L', 'RIO.L'
]

def extract_market_data(**kwargs):
    """
    Extract market data for a list of tickers and store in TimescaleDB
    """
    execution_date = kwargs['execution_date']
    # If we're running on a weekend, don't try to get market data
    if execution_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        logger.info("Skipping market data extraction on weekend")
        return "Skipped (weekend)"
    
    start_date = execution_date - timedelta(days=5)  # Get a few days of history in case of backfilling
    end_date = execution_date + timedelta(days=1)  # Include execution date
    
    logger.info(f"Extracting market data from {start_date} to {end_date}")
    
    # Connect to the database
    db_url = os.environ.get(
        'DATABASE_URL', 
        'postgresql://equitylens:equitylens_password@timescaledb:5432/equitylens_data'
    )
    engine = create_engine(db_url)
    
    # Download data for all tickers at once
    try:
        data = yf.download(
            TICKERS,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            group_by='ticker',
            auto_adjust=True,
            threads=True
        )
        
        logger.info(f"Downloaded data for {len(TICKERS)} tickers")
        
        # Process each ticker's data
        for ticker in TICKERS:
            try:
                if ticker in data.columns.levels[0]:
                    ticker_data = data[ticker].copy()
                    
                    # Skip if no data
                    if ticker_data.empty:
                        logger.warning(f"No data for {ticker}, skipping")
                        continue
                    
                    # Reset index to get date as a column
                    ticker_data.reset_index(inplace=True)
                    
                    # Rename columns to match database schema
                    ticker_data.rename(columns={
                        'Date': 'date',
                        'Open': 'open',
                        'High': 'high',
                        'Low': 'low',
                        'Close': 'close',
                        'Volume': 'volume',
                    }, inplace=True)
                    
                    # Add symbol column
                    ticker_data['symbol'] = ticker
                    
                    # Select and order columns to match database schema
                    ticker_data = ticker_data[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]
                    
                    # Write to database using SQLAlchemy
                    ticker_data.to_sql(
                        'daily_prices',
                        engine,
                        schema='market_data',
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    
                    logger.info(f"Inserted {len(ticker_data)} rows for {ticker}")
                else:
                    logger.warning(f"No data for {ticker}, skipping")
            except Exception as e:
                logger.error(f"Error processing {ticker}: {e}")
        
        return f"Processed {len(TICKERS)} tickers"
    except Exception as e:
        logger.error(f"Error downloading market data: {e}")
        raise

def calculate_technical_indicators(**kwargs):
    """
    Calculate technical indicators based on the latest market data
    """
    execution_date = kwargs['execution_date']
    
    # Connect to the database
    db_url = os.environ.get(
        'DATABASE_URL', 
        'postgresql://equitylens:equitylens_password@timescaledb:5432/equitylens_data'
    )
    engine = create_engine(db_url)
    
    # For each ticker, calculate technical indicators
    for ticker in TICKERS:
        try:
            # Get the last 200 days of data for this ticker
            query = text("""
                SELECT date, close
                FROM market_data.daily_prices
                WHERE symbol = :symbol
                ORDER BY date DESC
                LIMIT 200
            """)
            
            with engine.connect() as conn:
                result = conn.execute(query, {"symbol": ticker})
                data = pd.DataFrame(result.fetchall(), columns=result.keys())
            
            if data.empty:
                logger.warning(f"No price data for {ticker}, skipping")
                continue
                
            # Sort by date ascending for calculations
            data.sort_values('date', inplace=True)
            
            # Calculate indicators
            # 1. Simple Moving Averages
            data['sma_20'] = data['close'].rolling(window=20).mean()
            data['sma_50'] = data['close'].rolling(window=50).mean()
            data['sma_200'] = data['close'].rolling(window=200).mean()
            
            # 2. Relative Strength Index (RSI)
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['rsi_14'] = 100 - (100 / (1 + rs))
            
            # Get only the latest day with complete indicators
            latest_data = data.dropna(subset=['sma_200', 'rsi_14']).iloc[-1:].copy()
            
            if latest_data.empty:
                logger.warning(f"Insufficient data for {ticker} indicators, skipping")
                continue
                
            # Add ticker
            latest_data['symbol'] = ticker
            
            # Format for database
            latest_data = latest_data[['symbol', 'date', 'sma_20', 'sma_50', 'sma_200', 'rsi_14']]
            
            # Insert into technical indicators table
            latest_data.to_sql(
                'technical_indicators',
                engine,
                schema='market_data',
                if_exists='append',
                index=False,
                method='multi'
            )
            
            logger.info(f"Calculated indicators for {ticker}")
        except Exception as e:
            logger.error(f"Error calculating indicators for {ticker}: {e}")
    
    return "Technical indicators calculated"

# Define tasks
create_tables_task = PostgresOperator(
    task_id='create_tables_if_not_exist',
    postgres_conn_id='equitylens_db',
    sql="""
    -- Create schema if not exists
    CREATE SCHEMA IF NOT EXISTS market_data;
    
    -- Create extension if not exists
    CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
    
    -- Create daily prices table if not exists
    CREATE TABLE IF NOT EXISTS market_data.daily_prices (
        symbol TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume BIGINT,
        PRIMARY KEY (symbol, date)
    );
    
    -- Convert to hypertable if not already
    SELECT create_hypertable('market_data.daily_prices', 'date', 
                            if_not_exists => TRUE, 
                            migrate_data => TRUE);
                            
    -- Create technical indicators table if not exists
    CREATE TABLE IF NOT EXISTS market_data.technical_indicators (
        symbol TEXT NOT NULL,
        date TIMESTAMP NOT NULL,
        sma_20 NUMERIC,
        sma_50 NUMERIC,
        sma_200 NUMERIC,
        rsi_14 NUMERIC,
        PRIMARY KEY (symbol, date)
    );
    
    -- Convert to hypertable if not already
    SELECT create_hypertable('market_data.technical_indicators', 'date', 
                            if_not_exists => TRUE, 
                            migrate_data => TRUE);
    """,
    dag=dag,
)

extract_data_task = PythonOperator(
    task_id='extract_market_data',
    python_callable=extract_market_data,
    provide_context=True,
    dag=dag,
)

calculate_indicators_task = PythonOperator(
    task_id='calculate_technical_indicators',
    python_callable=calculate_technical_indicators,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
create_tables_task >> extract_data_task >> calculate_indicators_task