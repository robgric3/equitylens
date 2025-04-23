# calculation_engine/risk/risk_metrics.py
import pandas as pd
import numpy as np
from scipy import stats

def calculate_var(db, portfolio_id, confidence_level=0.95, method='historical', lookback_days=252, **kwargs):
    """
    Calculate Value at Risk (VaR) for a portfolio
    
    Args:
        db: Database session
        portfolio_id: Portfolio identifier
        confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
        method: Calculation method ('historical', 'parametric', 'monte_carlo')
        lookback_days: Historical lookback period in trading days
        
    Returns:
        Dictionary with VaR results
    """
    # Get portfolio data
    from calculation_engine.portfolio import portfolio_analytics
    portfolio_data = portfolio_analytics.get_portfolio_data(db, portfolio_id, 
                                                          start_date=None,  # Will be calculated based on lookback
                                                          end_date=None)    # Current date
    
    # Calculate portfolio returns
    from calculation_engine.performance.returns import calculate_portfolio_returns
    returns_df = calculate_portfolio_returns(portfolio_data)
    
    # Limit to lookback period
    if len(returns_df) > lookback_days:
        returns_df = returns_df.iloc[-lookback_days:]
    
    if method == 'historical':
        # Historical simulation method
        var_result = calculate_historical_var(returns_df, confidence_level)
    
    elif method == 'parametric':
        # Parametric (variance-covariance) method
        var_result = calculate_parametric_var(returns_df, confidence_level)
    
    elif method == 'monte_carlo':
        # Monte Carlo simulation method
        num_simulations = kwargs.get('num_simulations', 10000)
        var_result = calculate_monte_carlo_var(returns_df, confidence_level, num_simulations)
    
    else:
        raise ValueError(f"Unknown VaR method: {method}")
    
    return var_result

def calculate_historical_var(returns_df, confidence_level=0.95):
    """
    Calculate historical VaR from return series
    
    Args:
        returns_df: DataFrame with portfolio returns
        confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
        
    Returns:
        Dictionary with VaR results
    """
    # Sort returns for percentile calculation
    sorted_returns = returns_df['portfolio_return'].sort_values()
    
    # Find the return at the specified percentile
    var_percentile = 1 - confidence_level
    var_value = sorted_returns.quantile(var_percentile)
    
    # Calculate Expected Shortfall (CVaR)
    cvar_value = sorted_returns[sorted_returns <= var_value].mean()
    
    # Return VaR and related metrics as positive values
    return {
        'var': float(-var_value),  # Convert to positive value
        'cvar': float(-cvar_value) if not pd.isna(cvar_value) else None,  # Convert to positive value
        'confidence_level': float(confidence_level),
        'method': 'historical',
        'observations': len(returns_df),
        'var_percentile': float(var_percentile),
        # Additional metrics
        'mean_return': float(returns_df['portfolio_return'].mean()),
        'volatility': float(returns_df['portfolio_return'].std()),
        'skewness': float(stats.skew(returns_df['portfolio_return'])),
        'kurtosis': float(stats.kurtosis(returns_df['portfolio_return']))
    }

def calculate_parametric_var(returns_df, confidence_level=0.95):
    """
    Calculate parametric VaR assuming normal distribution
    
    Args:
        returns_df: DataFrame with portfolio returns
        confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
        
    Returns:
        Dictionary with VaR results
    """
    # Calculate mean and standard deviation
    mean_return = returns_df['portfolio_return'].mean()
    std_return = returns_df['portfolio_return'].std()
    
    # Calculate Z-score for the given confidence level
    z_score = stats.norm.ppf(1 - confidence_level)
    
    # Calculate VaR
    var_value = -(mean_return + z_score * std_return)
    
    # Calculate CVaR (Expected Shortfall)
    # For normal distribution, CVaR = mean - std * pdf(z) / (1 - confidence_level)
    z_pdf = stats.norm.pdf(z_score)
    cvar_value = -(mean_return - std_return * z_pdf / (1 - confidence_level))
    
    return {
        'var': float(var_value),  # Already positive
        'cvar': float(cvar_value),  # Already positive
        'confidence_level': float(confidence_level),
        'method': 'parametric',
        'observations': len(returns_df),
        'var_percentile': float(1 - confidence_level),
        # Distribution parameters
        'mean_return': float(mean_return),
        'volatility': float(std_return),
        'z_score': float(z_score)
    }

def calculate_monte_carlo_var(returns_df, confidence_level=0.95, num_simulations=10000):
    """
    Calculate VaR using Monte Carlo simulation
    
    Args:
        returns_df: DataFrame with portfolio returns
        confidence_level: Confidence level (e.g., 0.95 for 95% VaR)
        num_simulations: Number of Monte Carlo simulations
        
    Returns:
        Dictionary with VaR results
    """
    # Calculate mean and standard deviation
    mean_return = returns_df['portfolio_return'].mean()
    std_return = returns_df['portfolio_return'].std()
    
    # Generate random normal returns
    np.random.seed(42)  # For reproducibility
    simulated_returns = np.random.normal(mean_return, std_return, num_simulations)
    
    # Calculate VaR
    var_percentile = 1 - confidence_level
    var_value = -np.percentile(simulated_returns, var_percentile * 100)
    
    # Calculate CVaR
    cvar_value = -np.mean(simulated_returns[simulated_returns <= -var_value])
    
    return {
        'var': float(var_value),  # Already positive
        'cvar': float(cvar_value),  # Already positive
        'confidence_level': float(confidence_level),
        'method': 'monte_carlo',
        'observations': len(returns_df),
        'simulations': num_simulations,
        'var_percentile': float(var_percentile),
        # Simulation parameters
        'mean_return': float(mean_return),
        'volatility': float(std_return)
    }

