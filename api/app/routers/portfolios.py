# api/app/routers/portfolios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.schemas.portfolio import (
    PortfolioCreate, 
    PortfolioUpdate, 
    PortfolioInDB,
    PortfolioWithPositions
)
from app.db.session import get_db
from app.crud.portfolio import (
    create_portfolio, 
    get_portfolio, 
    get_portfolios, 
    update_portfolio,
    delete_portfolio
)

router = APIRouter()

@router.post("/", response_model=PortfolioInDB, status_code=status.HTTP_201_CREATED)
def create_new_portfolio(portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    """Create a new portfolio"""
    return create_portfolio(db=db, portfolio=portfolio)

@router.get("/{portfolio_id}", response_model=PortfolioWithPositions)
def read_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Get a specific portfolio by ID"""
    db_portfolio = get_portfolio(db=db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return db_portfolio

@router.get("/", response_model=List[PortfolioInDB])
def read_portfolios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get list of portfolios"""
    portfolios = get_portfolios(db=db, skip=skip, limit=limit)
    return portfolios

@router.put("/{portfolio_id}", response_model=PortfolioInDB)
def update_existing_portfolio(
    portfolio_id: int, 
    portfolio: PortfolioUpdate, 
    db: Session = Depends(get_db)
):
    """Update a portfolio"""
    db_portfolio = get_portfolio(db=db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return update_portfolio(db=db, portfolio_id=portfolio_id, portfolio=portfolio)

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Delete a portfolio"""
    db_portfolio = get_portfolio(db=db, portfolio_id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    delete_portfolio(db=db, portfolio_id=portfolio_id)
    return None