# calculation_engine/optimization/efficient_frontier.py
import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt import objective_functions

def prepare_optimization_data(prices_df):
    """
    Prepare price data for optimization
    
    Args:
        prices_df: DataFrame of daily prices for securities
        
    Returns:
        Tuple of (expected returns, covariance matrix)
    """
    # Calculate expected returns (use mean historical return)
    mu = expected_returns.mean_historical_return(prices_df)
    
    # Calculate sample covariance matrix
    S = risk_models.sample_cov(prices_df)
    
    return mu, S

def maximize_sharpe_ratio(universe_data, constraint_set=None):
    """
    Optimize portfolio for maximum Sharpe ratio
    
    Args:
        universe_data: DataFrame of security prices
        constraint_set: Dictionary of constraints
        
    Returns:
        Dictionary with optimization results
    """
    # Prepare data
    mu, S = prepare_optimization_data(universe_data)
    
    # Create efficient frontier object
    ef = EfficientFrontier(mu, S)
    
    # Apply constraints if provided
    if constraint_set:
        apply_constraints(ef, constraint_set)
    
    # Find maximum Sharpe portfolio
    weights = ef.max_sharpe()
    
    # Get cleaned weights (removes tiny weights)
    cleaned_weights = ef.clean_weights()
    
    # Get performance metrics
    metrics = get_portfolio_metrics(ef, mu, S, cleaned_weights)
    
    return {
        'weights': {k: float(v) for k, v in cleaned_weights.items() if v > 0.0001},
        'expected_return': float(metrics['expected_return']),
        'volatility': float(metrics['volatility']),
        'sharpe_ratio': float(metrics['sharpe_ratio']),
        'portfolio_value': 1.0,  # Normalized to 1.0
        'weights_sum': float(sum(cleaned_weights.values())),
        'optimization_type': 'max_sharpe'
    }

def minimize_volatility(universe_data, constraint_set=None):
    """
    Optimize portfolio for minimum volatility
    
    Args:
        universe_data: DataFrame of security prices
        constraint_set: Dictionary of constraints
        
    Returns:
        Dictionary with optimization results
    """
    # Prepare data
    mu, S = prepare_optimization_data(universe_data)
    
    # Create efficient frontier object
    ef = EfficientFrontier(mu, S)
    
    # Apply constraints if provided
    if constraint_set:
        apply_constraints(ef, constraint_set)
    
    # Find minimum volatility portfolio
    weights = ef.min_volatility()
    
    # Get cleaned weights (removes tiny weights)
    cleaned_weights = ef.clean_weights()
    
    # Get performance metrics
    metrics = get_portfolio_metrics(ef, mu, S, cleaned_weights)
    
    return {
        'weights': {k: float(v) for k, v in cleaned_weights.items() if v > 0.0001},
        'expected_return': float(metrics['expected_return']),
        'volatility': float(metrics['volatility']),
        'sharpe_ratio': float(metrics['sharpe_ratio']),
        'portfolio_value': 1.0,  # Normalized to 1.0
        'weights_sum': float(sum(cleaned_weights.values())),
        'optimization_type': 'min_volatility'
    }

def maximize_return(universe_data, constraint_set=None, target_volatility=None):
    """
    Optimize portfolio for maximum return
    
    Args:
        universe_data: DataFrame of security prices
        constraint_set: Dictionary of constraints
        target_volatility: Optional target volatility constraint
        
    Returns:
        Dictionary with optimization results
    """
    # Prepare data
    mu, S = prepare_optimization_data(universe_data)
    
    # Create efficient frontier object
    ef = EfficientFrontier(mu, S)
    
    # Apply constraints if provided
    if constraint_set:
        apply_constraints(ef, constraint_set)
    
    # Find maximum return portfolio (with optional volatility target)
    if target_volatility is not None:
        weights = ef.efficient_risk(target_volatility)
    else:
        # Without volatility constraint, max return is just 100% in highest return asset
        # We'll use a high target volatility as a stand-in
        weights = ef.efficient_risk(2.0)  # Very high volatility target
    
    # Get cleaned weights (removes tiny weights)
    cleaned_weights = ef.clean_weights()
    
    # Get performance metrics
    metrics = get_portfolio_metrics(ef, mu, S, cleaned_weights)
    
    return {
        'weights': {k: float(v) for k, v in cleaned_weights.items() if v > 0.0001},
        'expected_return': float(metrics['expected_return']),
        'volatility': float(metrics['volatility']),
        'sharpe_ratio': float(metrics['sharpe_ratio']),
        'portfolio_value': 1.0,  # Normalized to 1.0
        'weights_sum': float(sum(cleaned_weights.values())),
        'optimization_type': 'max_return'
    }

def apply_constraints(ef, constraint_set):
    """
    Apply constraints to an efficient frontier object
    
    Args:
        ef: EfficientFrontier object
        constraint_set: Dictionary of constraints
    """
    # Apply sector constraints if provided
    if 'sector_constraints' in constraint_set:
        sector_constraints = constraint_set['sector_constraints']
        sector_mapper = {}
        
        # Build sector mapper
        for sector, symbols in sector_constraints['sector_mapping'].items():
            for symbol in symbols:
                sector_mapper[symbol] = sector
        
        # Add sector constraints
        sector_lower = sector_constraints.get('sector_lower', {})
        sector_upper = sector_constraints.get('sector_upper', {})
        
        ef.add_sector_constraints(sector_mapper, sector_lower, sector_upper)
    
    # Apply position constraints if provided
    if 'position_constraints' in constraint_set:
        position_constraints = constraint_set['position_constraints']
        
        # Set portfolio-wide limits
        min_weight = position_constraints.get('min_weight', 0.0)
        max_weight = position_constraints.get('max_weight', 1.0)
        
        ef.add_constraint(lambda x: x >= min_weight)
        ef.add_constraint(lambda x: x <= max_weight)
        
        # Set security-specific limits
        for symbol, limits in position_constraints.get('security_limits', {}).items():
            if 'min' in limits:
                ef.add_constraint(lambda x, sym=symbol: x[sym] >= limits['min'])
            if 'max' in limits:
                ef.add_constraint(lambda x, sym=symbol: x[sym] <= limits['max'])
    
    # Apply target return constraint if provided
    if 'target_return' in constraint_set:
        target_return = constraint_set['target_return']
        ef.add_constraint(lambda x: ef.portfolio_return(x) >= target_return)

def get_portfolio_metrics(ef, mu, S, weights):
    """
    Calculate key portfolio metrics from optimized weights
    
    Args:
        ef: EfficientFrontier object
        mu: Expected returns
        S: Covariance matrix
        weights: Portfolio weights
        
    Returns:
        Dictionary of portfolio performance metrics
    """
    # Calculate expected return
    expected_return = ef.portfolio_performance(verbose=False)[0]
    
    # Calculate volatility
    volatility = ef.portfolio_performance(verbose=False)[1]
    
    # Calculate Sharpe ratio
    sharpe_ratio = ef.portfolio_performance(verbose=False)[2]
    
    return {
        'expected_return': expected_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }

