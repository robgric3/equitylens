# api/app/schemas/portfolio.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Base schema for portfolio data
class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    inception_date: date
    currency: str = "USD"

# Schema for creating a new portfolio
class PortfolioCreate(PortfolioBase):
    pass

# Schema for updating a portfolio
class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None

# Schema for position data
class PositionBase(BaseModel):
    symbol: str
    quantity: float
    entry_date: date
    entry_price: float
    exit_date: Optional[date] = None
    exit_price: Optional[float] = None

# Schema for creating a position
class PositionCreate(PositionBase):
    portfolio_id: int

# Schema for database representation
class PositionInDB(PositionBase):
    id: int
    portfolio_id: int
    created_at: date
    updated_at: date
    
    class Config:
        from_attributes = True


# Schema for database representation with positions
class PortfolioInDB(PortfolioBase):
    id: int
    created_at: date
    updated_at: date
    
    class Config:
        from_attributes = True

# Schema for portfolio with positions
class PortfolioWithPositions(PortfolioInDB):
    positions: List[PositionInDB] = []