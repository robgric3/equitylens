from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("equitylens-api")

# Import routers
from app.routers import (
    portfolios, 
    stocks, 
    risk, 
    performance, 
    factors, 
    optimization,
    users
)

# Create FastAPI app
app = FastAPI(
    title="EquityLens API",
    description="API for equity portfolio analytics and risk management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to EquityLens API",
        "docs": "/docs",
        "endpoints": {
            "portfolios": "/portfolios",
            "stocks": "/stocks",
            "risk": "/risk",
            "performance": "/performance",
            "factors": "/factors",
            "optimization": "/optimization",
        }
    }

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error. Please try again later."}
    )

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(portfolios.router, prefix="/portfolios", tags=["Portfolios"])
app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])
app.include_router(risk.router, prefix="/risk", tags=["Risk Analysis"])
app.include_router(performance.router, prefix="/performance", tags=["Performance"])
app.include_router(factors.router, prefix="/factors", tags=["Factor Analysis"])
app.include_router(optimization.router, prefix="/optimization", tags=["Portfolio Optimization"])

# Create database tables on startup if they don't exist
from app.db.base import Base
from app.db.session import engine

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the EquityLens API")
    try:
        # Create tables if they don't exist
        # In production, you would use Alembic migrations instead
        # This is just for development convenience
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or verified")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the EquityLens API")