# api/app/crud/portfolio.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.models.portfolio import Portfolio, Position
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PositionCreate

# Portfolio CRUD operations
def get_portfolio(db: Session, portfolio_id: int):
    """Get a single portfolio by ID"""
    return db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

def get_portfolios(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of portfolios with pagination"""
    return db.query(Portfolio).offset(skip).limit(limit).all()

def create_portfolio(db: Session, portfolio: PortfolioCreate):
    """Create a new portfolio"""
    db_portfolio = Portfolio(
        name=portfolio.name,
        description=portfolio.description,
        inception_date=portfolio.inception_date,
        currency=portfolio.currency
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def update_portfolio(db: Session, portfolio_id: int, portfolio: PortfolioUpdate):
    """Update an existing portfolio"""
    db_portfolio = get_portfolio(db, portfolio_id)
    
    # Only update fields that are provided
    update_data = portfolio.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_portfolio, key, value)
    
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def delete_portfolio(db: Session, portfolio_id: int):
    """Delete a portfolio"""
    db_portfolio = get_portfolio(db, portfolio_id)
    db.delete(db_portfolio)
    db.commit()
    return db_portfolio

# Position CRUD operations
def get_positions(db: Session, portfolio_id: int, skip: int = 0, limit: int = 100):
    """Get positions for a portfolio"""
    return db.query(Position).filter(
        Position.portfolio_id == portfolio_id
    ).offset(skip).limit(limit).all()

def create_position(db: Session, position: PositionCreate):
    """Add a position to a portfolio"""
    db_position = Position(
        portfolio_id=position.portfolio_id,
        symbol=position.symbol,
        quantity=position.quantity,
        entry_date=position.entry_date,
        entry_price=position.entry_price,
        exit_date=position.exit_date,
        exit_price=position.exit_price
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position