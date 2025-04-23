# calculation_engine/performance/returns.py
import pandas as pd
import numpy as np

def calculate_portfolio_returns(portfolio_data, benchmark_data=None):
    """
    Calculate time series of portfolio returns
    
    Args:
        portfolio_data: Portfolio positions and prices
        benchmark_data: Optional benchmark prices
        
    Returns:
        DataFrame with portfolio returns and benchmark returns if provided
    """
    positions = portfolio_data['positions']
    prices = portfolio_data['prices']
    
    # Calculate position values over time
    position_values = pd.DataFrame()
    for idx, row in positions.iterrows():
        symbol = row['symbol']
        quantity = row['quantity']
        
        if symbol in prices.columns:
            position_values[symbol] = prices[symbol] * quantity
    
    # Calculate portfolio value over time
    portfolio_value = position_values.sum(axis=1)
    
    # Calculate daily returns
    portfolio_returns = portfolio_value.pct_change().dropna()
    
    result = pd.DataFrame({'portfolio_return': portfolio_returns})
    
    # Add benchmark if provided
    if benchmark_data is not None:
        # Calculate benchmark returns
        benchmark_returns = benchmark_data.pct_change().dropna()
        result['benchmark_return'] = benchmark_returns
        
    return result

def calculate_performance_metrics(portfolio_data, benchmark_id=None):
    """
    Calculate key performance metrics for a portfolio
    
    Args:
        portfolio_data: Portfolio positions and prices
        benchmark_id: Optional benchmark identifier
        
    Returns:
        Dict of performance metrics
    """
    # Get benchmark data if provided
    benchmark_data = None
    if benchmark_id is not None:
        # Replace with actual benchmark data retrieval
        pass
    
    # Calculate returns
    returns_df = calculate_portfolio_returns(portfolio_data, benchmark_data)
    
    # Calculate metrics
    total_return = (returns_df['portfolio_return'] + 1).prod() - 1
    annualized_return = (1 + total_return) ** (252 / len(returns_df)) - 1
    volatility = returns_df['portfolio_return'].std() * np.sqrt(252)
    sharpe_ratio = annualized_return / volatility
    
    # Calculate max drawdown
    cum_returns = (1 + returns_df['portfolio_return']).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns / running_max) - 1
    max_drawdown = drawdown.min()
    
    # Calculate benchmark-relative metrics if available
    tracking_error = None
    information_ratio = None
    if 'benchmark_return' in returns_df.columns:
        excess_returns = returns_df['portfolio_return'] - returns_df['benchmark_return']
        tracking_error = excess_returns.std() * np.sqrt(252)
        information_ratio = excess_returns.mean() * 252 / tracking_error
    
    return {
        'total_return': float(total_return),
        'annualized_return': float(annualized_return),
        'volatility': float(volatility),
        'sharpe_ratio': float(sharpe_ratio),
        'max_drawdown': float(max_drawdown),
        'tracking_error': float(tracking_error) if tracking_error is not None else None,
        'information_ratio': float(information_ratio) if information_ratio is not None else None,
    }