import logging
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, date
import pandas as pd
import numpy as np
import uvicorn
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Import calculation modules
from portfolio import portfolio_analytics
from risk import risk_metrics, stress_testing
from performance import attribution, returns
from factors import factor_model, exposures
from optimization import efficient_frontier, constraints

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("calculation-engine")

# Create FastAPI app
app = FastAPI(
    title="EquityLens Calculation Engine",
    description="Service for performing computational finance calculations",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database connection from environment
DB_URL = os.getenv("DATABASE_URL", "postgresql://equitylens:equitylens_password@timescaledb:5432/equitylens_data")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Job tracking
calculation_jobs = {}

# Pydantic models for requests
class PortfolioRequest(BaseModel):
    portfolio_id: int
    start_date: date
    end_date: date = Field(default_factory=lambda: date.today())
    benchmark_id: Optional[str] = None
    include_positions: bool = True

class RiskAnalysisRequest(BaseModel):
    portfolio_id: int
    calculation_type: str = Field(..., description="Type of risk calculation: var, stress_test, etc.")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
class OptimizationRequest(BaseModel):
    portfolio_id: Optional[int] = None
    universe: List[str] = Field(default_factory=list)
    objective: str = "max_sharpe"
    constraints: Dict[str, Any] = Field(default_factory=dict)
    start_date: date
    end_date: date = Field(default_factory=lambda: date.today())

class FactorAnalysisRequest(BaseModel):
    portfolio_id: int
    factor_model: str = "fama_french_3"
    start_date: date
    end_date: date = Field(default_factory=lambda: date.today())

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float = 0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Portfolio analytics endpoint
@app.post("/portfolio-analytics", response_model=str)
async def run_portfolio_analytics(request: PortfolioRequest, background_tasks: BackgroundTasks):
    job_id = f"portfolio_{request.portfolio_id}_{datetime.now().timestamp()}"
    calculation_jobs[job_id] = {"status": "queued", "progress": 0, "result": None, "error": None}
    
    background_tasks.add_task(
        execute_portfolio_analytics,
        job_id,
        request.portfolio_id,
        request.start_date,
        request.end_date,
        request.benchmark_id,
        request.include_positions
    )
    
    return job_id

async def execute_portfolio_analytics(job_id, portfolio_id, start_date, end_date, benchmark_id, include_positions):
    calculation_jobs[job_id]["status"] = "running"
    try:
        # Get portfolio data from database
        with SessionLocal() as db:
            # This would be replaced with actual database queries
            calculation_jobs[job_id]["progress"] = 0.1
            
            # Run calculations
            portfolio_data = portfolio_analytics.get_portfolio_data(db, portfolio_id, start_date, end_date)
            calculation_jobs[job_id]["progress"] = 0.3
            
            performance_metrics = returns.calculate_performance_metrics(portfolio_data, benchmark_id)
            calculation_jobs[job_id]["progress"] = 0.6
            
            attribution_results = attribution.calculate_attribution(portfolio_data, benchmark_id)
            calculation_jobs[job_id]["progress"] = 0.9
            
            # Combine results
            result = {
                "portfolio_summary": portfolio_data.to_dict() if include_positions else {},
                "performance_metrics": performance_metrics,
                "attribution": attribution_results
            }
            
            calculation_jobs[job_id]["status"] = "completed"
            calculation_jobs[job_id]["progress"] = 1.0
            calculation_jobs[job_id]["result"] = result
            
    except Exception as e:
        logger.error(f"Error in portfolio analytics calculation: {e}", exc_info=True)
        calculation_jobs[job_id]["status"] = "failed"
        calculation_jobs[job_id]["error"] = str(e)

# Risk analysis endpoint
@app.post("/risk-analysis", response_model=str)
async def run_risk_analysis(request: RiskAnalysisRequest, background_tasks: BackgroundTasks):
    job_id = f"risk_{request.portfolio_id}_{datetime.now().timestamp()}"
    calculation_jobs[job_id] = {"status": "queued", "progress": 0, "result": None, "error": None}
    
    background_tasks.add_task(
        execute_risk_analysis,
        job_id,
        request.portfolio_id,
        request.calculation_type,
        request.parameters
    )
    
    return job_id

async def execute_risk_analysis(job_id, portfolio_id, calculation_type, parameters):
    calculation_jobs[job_id]["status"] = "running"
    try:
        with SessionLocal() as db:
            calculation_jobs[job_id]["progress"] = 0.1
            
            if calculation_type == "var":
                result = risk_metrics.calculate_var(db, portfolio_id, **parameters)
            elif calculation_type == "stress_test":
                result = stress_testing.run_stress_test(db, portfolio_id, **parameters)
            else:
                raise ValueError(f"Unknown calculation type: {calculation_type}")
            
            calculation_jobs[job_id]["status"] = "completed"
            calculation_jobs[job_id]["progress"] = 1.0
            calculation_jobs[job_id]["result"] = result
            
    except Exception as e:
        logger.error(f"Error in risk analysis calculation: {e}", exc_info=True)
        calculation_jobs[job_id]["status"] = "failed"
        calculation_jobs[job_id]["error"] = str(e)

# Portfolio optimization endpoint
@app.post("/optimization", response_model=str)
async def run_optimization(request: OptimizationRequest, background_tasks: BackgroundTasks):
    job_id = f"optimization_{request.objective}_{datetime.now().timestamp()}"
    calculation_jobs[job_id] = {"status": "queued", "progress": 0, "result": None, "error": None}
    
    background_tasks.add_task(
        execute_optimization,
        job_id,
        request.portfolio_id,
        request.universe,
        request.objective,
        request.constraints,
        request.start_date,
        request.end_date
    )
    
    return job_id

async def execute_optimization(job_id, portfolio_id, universe, objective, constraints, start_date, end_date):
    calculation_jobs[job_id]["status"] = "running"
    try:
        with SessionLocal() as db:
            calculation_jobs[job_id]["progress"] = 0.1
            
            # Get required data
            if portfolio_id:
                # Starting from existing portfolio
                universe_data = portfolio_analytics.get_portfolio_universe(db, portfolio_id, start_date, end_date)
            else:
                # Starting from provided universe
                universe_data = portfolio_analytics.get_symbols_data(db, universe, start_date, end_date)
                
            calculation_jobs[job_id]["progress"] = 0.3
            
            # Apply constraints
            constraint_set = constraints.build_constraint_set(universe_data, constraints)
            calculation_jobs[job_id]["progress"] = 0.5
            
            # Run optimization
            if objective == "max_sharpe":
                result = efficient_frontier.maximize_sharpe_ratio(universe_data, constraint_set)
            elif objective == "min_volatility":
                result = efficient_frontier.minimize_volatility(universe_data, constraint_set)
            elif objective == "max_return":
                result = efficient_frontier.maximize_return(universe_data, constraint_set)
            else:
                raise ValueError(f"Unknown objective: {objective}")
                
            calculation_jobs[job_id]["status"] = "completed"
            calculation_jobs[job_id]["progress"] = 1.0
            calculation_jobs[job_id]["result"] = result
            
    except Exception as e:
        logger.error(f"Error in optimization calculation: {e}", exc_info=True)
        calculation_jobs[job_id]["status"] = "failed"
        calculation_jobs[job_id]["error"] = str(e)

# Factor analysis endpoint
@app.post("/factor-analysis", response_model=str)
async def run_factor_analysis(request: FactorAnalysisRequest, background_tasks: BackgroundTasks):
    job_id = f"factor_{request.portfolio_id}_{datetime.now().timestamp()}"
    calculation_jobs[job_id] = {"status": "queued", "progress": 0, "result": None, "error": None}
    
    background_tasks.add_task(
        execute_factor_analysis,
        job_id,
        request.portfolio_id,
        request.factor_model,
        request.start_date,
        request.end_date
    )
    
    return job_id

async def execute_factor_analysis(job_id, portfolio_id, factor_model_name, start_date, end_date):
    calculation_jobs[job_id]["status"] = "running"
    try:
        with SessionLocal() as db:
            calculation_jobs[job_id]["progress"] = 0.1
            
            # Get portfolio and factor data
            portfolio_data = portfolio_analytics.get_portfolio_data(db, portfolio_id, start_date, end_date)
            calculation_jobs[job_id]["progress"] = 0.3
            
            # Get or calculate factor returns
            factor_returns = factor_model.get_factor_returns(db, factor_model_name, start_date, end_date)
            calculation_jobs[job_id]["progress"] = 0.5
            
            # Calculate exposures
            factor_exposures = exposures.calculate_exposures(portfolio_data, factor_returns)
            calculation_jobs[job_id]["progress"] = 0.7
            
            # Factor attribution
            factor_attribution = exposures.calculate_attribution(portfolio_data, factor_returns, factor_exposures)
            calculation_jobs[job_id]["progress"] = 0.9
            
            result = {
                "exposures": factor_exposures,
                "attribution": factor_attribution
            }
            
            calculation_jobs[job_id]["status"] = "completed"
            calculation_jobs[job_id]["progress"] = 1.0
            calculation_jobs[job_id]["result"] = result
            
    except Exception as e:
        logger.error(f"Error in factor analysis calculation: {e}", exc_info=True)
        calculation_jobs[job_id]["status"] = "failed"
        calculation_jobs[job_id]["error"] = str(e)

# Check job status
@app.get("/job/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    if job_id not in calculation_jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found"
        )
    
    job = calculation_jobs[job_id]
    return JobStatus(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        result=job["result"],
        error=job["error"]
    )

# Clean up old jobs (periodic task)
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_jobs())

async def cleanup_old_jobs():
    while True:
        try:
            current_time = datetime.now().timestamp()
            jobs_to_remove = []
            
            for job_id, job in calculation_jobs.items():
                job_time = float(job_id.split('_')[-1])
                # Remove completed or failed jobs older than 1 hour
                if (job["status"] in ["completed", "failed"]) and (current_time - job_time > 3600):
                    jobs_to_remove.append(job_id)
            
            for job_id in jobs_to_remove:
                del calculation_jobs[job_id]
                
            logger.info(f"Cleaned up {len(jobs_to_remove)} old calculation jobs")
        except Exception as e:
            logger.error(f"Error in job cleanup: {e}")
            
        await asyncio.sleep(3600)  # Run hourly

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)