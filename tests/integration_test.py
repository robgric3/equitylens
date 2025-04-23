# tests/integration_test.py
import requests
import json
import time
import pandas as pd
from datetime import datetime, timedelta

API_URL = "http://localhost:8000"
CALC_ENGINE_URL = "http://localhost:8001"

def test_api_health():
    """Test API health endpoint"""
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ API health check passed")

def test_calculation_engine_health():
    """Test calculation engine health endpoint"""
    response = requests.get(f"{CALC_ENGINE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Calculation engine health check passed")

def create_test_portfolio():
    """Create a test portfolio with positions"""
    portfolio_data = {
        "name": "Test Integration Portfolio",
        "description": "Portfolio created for integration testing",
        "inception_date": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        "currency": "USD"
    }
    
    response = requests.post(f"{API_URL}/portfolios", json=portfolio_data)
    assert response.status_code == 201
    portfolio = response.json()
    portfolio_id = portfolio["id"]
    print(f"✅ Created test portfolio with ID: {portfolio_id}")
    
    # Add positions to the portfolio
    positions = [
        {"symbol": "AAPL", "quantity": 100, "entry_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"), "entry_price": 150.0},
        {"symbol": "MSFT", "quantity": 50, "entry_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"), "entry_price": 250.0},
        {"symbol": "GOOGL", "quantity": 20, "entry_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"), "entry_price": 1800.0},
        {"symbol": "AMZN", "quantity": 15, "entry_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"), "entry_price": 3000.0},
        {"symbol": "TSLA", "quantity": 30, "entry_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"), "entry_price": 700.0},
    ]
    
    for position in positions:
        position["portfolio_id"] = portfolio_id
        response = requests.post(f"{API_URL}/portfolios/{portfolio_id}/positions", json=position)
        assert response.status_code == 201
    
    print(f"✅ Added {len(positions)} positions to test portfolio")
    return portfolio_id

def test_portfolio_analytics(portfolio_id):
    """Test portfolio analytics calculation"""
    request_data = {
        "portfolio_id": portfolio_id,
        "start_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Start the calculation job
    response = requests.post(f"{CALC_ENGINE_URL}/portfolio-analytics", json=request_data)
    assert response.status_code == 200
    job_id = response.json()
    print(f"✅ Started portfolio analytics calculation with job ID: {job_id}")
    
    # Poll for job completion
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        response = requests.get(f"{CALC_ENGINE_URL}/job/{job_id}")
        assert response.status_code == 200
        job_status = response.json()
        
        if job_status["status"] == "completed":
            print(f"✅ Portfolio analytics calculation completed")
            return job_status["result"]
        elif job_status["status"] == "failed":
            assert False, f"Portfolio analytics calculation failed: {job_status['error']}"
        
        attempt += 1
        time.sleep(1)
    
    assert False, "Portfolio analytics calculation timed out"

def test_risk_analysis(portfolio_id):
    """Test risk analysis calculation"""
    request_data = {
        "portfolio_id": portfolio_id,
        "calculation_type": "var",
        "parameters": {
            "confidence_level": 0.95,
            "method": "historical",
            "lookback_days": 252
        }
    }
    
    # Start the calculation job
    response = requests.post(f"{CALC_ENGINE_URL}/risk-analysis", json=request_data)
    assert response.status_code == 200
    job_id = response.json()
    print(f"✅ Started risk analysis calculation with job ID: {job_id}")
    
    # Poll for job completion
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        response = requests.get(f"{CALC_ENGINE_URL}/job/{job_id}")
        assert response.status_code == 200
        job_status = response.json()
        
        if job_status["status"] == "completed":
            print(f"✅ Risk analysis calculation completed")
            return job_status["result"]
        elif job_status["status"] == "failed":
            assert False, f"Risk analysis calculation failed: {job_status['error']}"
        
        attempt += 1
        time.sleep(1)
    
    assert False, "Risk analysis calculation timed out"

def test_factor_analysis(portfolio_id):
    """Test factor analysis calculation"""
    request_data = {
        "portfolio_id": portfolio_id,
        "factor_model": "fama_french_3",
        "start_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Start the calculation job
    response = requests.post(f"{CALC_ENGINE_URL}/factor-analysis", json=request_data)
    assert response.status_code == 200
    job_id = response.json()
    print(f"✅ Started factor analysis calculation with job ID: {job_id}")
    
    # Poll for job completion
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        response = requests.get(f"{CALC_ENGINE_URL}/job/{job_id}")
        assert response.status_code == 200
        job_status = response.json()
        
        if job_status["status"] == "completed":
            print(f"✅ Factor analysis calculation completed")
            return job_status["result"]
        elif job_status["status"] == "failed":
            assert False, f"Factor analysis calculation failed: {job_status['error']}"
        
        attempt += 1
        time.sleep(1)
    
    assert False, "Factor analysis calculation timed out"

def test_optimization(portfolio_id):
    """Test portfolio optimization"""
    request_data = {
        "portfolio_id": portfolio_id,
        "objective": "max_sharpe",
        "constraints": {
            "positions": {
                "min_weight": 0.05,
                "max_weight": 0.30
            }
        },
        "start_date": (datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Start the calculation job
    response = requests.post(f"{CALC_ENGINE_URL}/optimization", json=request_data)
    assert response.status_code == 200
    job_id = response.json()
    print(f"✅ Started portfolio optimization with job ID: {job_id}")
    
    # Poll for job completion
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        response = requests.get(f"{CALC_ENGINE_URL}/job/{job_id}")
        assert response.status_code == 200
        job_status = response.json()
        
        if job_status["status"] == "completed":
            print(f"✅ Portfolio optimization completed")
            return job_status["result"]
        elif job_status["status"] == "failed":
            assert False, f"Portfolio optimization failed: {job_status['error']}"
        
        attempt += 1
        time.sleep(1)
    
    assert False, "Portfolio optimization timed out"

def run_integration_test():
    """Run full integration test"""
    print("Starting EquityLens integration test...")
    
    # Test health endpoints
    test_api_health()
    test_calculation_engine_health()
    
    # Create test portfolio
    portfolio_id = create_test_portfolio()
    
    # Test portfolio analytics
    analytics_result = test_portfolio_analytics(portfolio_id)
    print(f"Portfolio performance metrics: {json.dumps(analytics_result['performance_metrics'], indent=2)}")
    
    # Test risk analysis
    risk_result = test_risk_analysis(portfolio_id)
    print(f"Portfolio risk metrics: {json.dumps(risk_result, indent=2)}")
    
    # Test factor analysis
    factor_result = test_factor_analysis(portfolio_id)
    print(f"Factor exposures: {json.dumps(factor_result['exposures']['factors'], indent=2)}")
    
    # Test optimization
    optimization_result = test_optimization(portfolio_id)
    print(f"Optimized weights: {json.dumps(optimization_result['weights'], indent=2)}")
    
    print("🎉 Integration test completed successfully!")

if __name__ == "__main__":
    run_integration_test()