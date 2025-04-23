# calculation_engine/risk/stress_testing.py

def run_stress_test(db, portfolio_id, scenario_type, **kwargs):
    """
    Run a stress test on a portfolio
    
    Args:
        db: Database session
        portfolio_id: Portfolio identifier
        scenario_type: Type of stress scenario
        **kwargs: Additional scenario parameters
        
    Returns:
        Dictionary with stress test results
    """
    # Get portfolio data
    from calculation_engine.portfolio import portfolio_analytics
    portfolio_data = portfolio_analytics.get_portfolio_data(db, portfolio_id, 
                                                          start_date=None,
                                                          end_date=None)
    
    # Run appropriate stress test
    if scenario_type == 'historical':
        scenario_name = kwargs.get('scenario_name')
        return historical_scenario_test(portfolio_data, scenario_name)
    
    elif scenario_type == 'factor_shock':
        factor_shocks = kwargs.get('factor_shocks', {})
        return factor_shock_test(portfolio_data, factor_shocks)
    
    elif scenario_type == 'custom':
        asset_shocks = kwargs.get('asset_shocks', {})
        return custom_shock_test(portfolio_data, asset_shocks)
    
    else:
        raise ValueError(f"Unknown stress test scenario: {scenario_type}")

def historical_scenario_test(portfolio_data, scenario_name):
    """
    Run a historical scenario stress test
    
    Args:
        portfolio_data: Portfolio positions and prices
        scenario_name: Name of historical scenario
        
    Returns:
        Dictionary with stress test results
    """
    # Define historical scenarios (these would normally come from a database)
    scenarios = {
        'financial_crisis_2008': {
            'period': ('2008-09-01', '2008-11-30'),
            'description': '2008 Financial Crisis (Sep-Nov 2008)',
            'asset_returns': {
                # Example asset returns during this period
                'SPY': -0.30,  # S&P 500
                'QQQ': -0.35,  # NASDAQ
                'EEM': -0.40,  # Emerging Markets
                'TLT': 0.10,   # Long-Term Treasury
                'GLD': 0.05,   # Gold
                # Default for other assets
                '_default': -0.25
            }
        },
        'covid_crash_2020': {
            'period': ('2020-02-19', '2020-03-23'),
            'description': 'COVID-19 Market Crash (Feb-Mar 2020)',
            'asset_returns': {
                'SPY': -0.34,
                'QQQ': -0.28,
                'EEM': -0.33,
                'TLT': 0.15,
                'GLD': -0.05,
                '_default': -0.30
            }
        },
        'rate_shock_2022': {
            'period': ('2022-01-01', '2022-06-30'),
            'description': 'Interest Rate Shock (H1 2022)',
            'asset_returns': {
                'SPY': -0.20,
                'QQQ': -0.30,
                'TLT': -0.25,
                'HYG': -0.15,
                'SHY': -0.05,
                '_default': -0.15
            }
        }
    }
    
    # Check if scenario exists
    if scenario_name not in scenarios:
        raise ValueError(f"Unknown historical scenario: {scenario_name}")
    
    # Get scenario details
    scenario = scenarios[scenario_name]
    
    # Get portfolio positions and current values
    positions = portfolio_data['positions']
    prices = portfolio_data['prices']
    
    # Calculate current portfolio value
    portfolio_value = 0
    position_values = {}
    
    for idx, position in positions.iterrows():
        symbol = position['symbol']
        quantity = position['quantity']
        
        # Get latest price
        if symbol in prices.columns:
            latest_price = prices[symbol].iloc[-1]
            position_value = quantity * latest_price
            position_values[symbol] = {
                'symbol': symbol,
                'quantity': float(quantity),
                'current_price': float(latest_price),
                'current_value': float(position_value)
            }
            portfolio_value += position_value
    
    # Apply scenario shocks to each position
    stressed_values = {}
    total_stressed_value = 0
    
    for symbol, position in position_values.items():
        # Get scenario return for this asset (or default)
        if symbol in scenario['asset_returns']:
            shock_return = scenario['asset_returns'][symbol]
        else:
            shock_return = scenario['asset_returns']['_default']
        
        # Calculate stressed value
        stressed_price = position['current_price'] * (1 + shock_return)
        stressed_value = position['quantity'] * stressed_price
        
        stressed_values[symbol] = {
            'symbol': symbol,
            'current_value': float(position['current_value']),
            'shock_return': float(shock_return),
            'stressed_value': float(stressed_value),
            'value_change': float(stressed_value - position['current_value']),
            'pct_change': float(shock_return)
        }
        
        total_stressed_value += stressed_value
    
    # Calculate overall portfolio impact
    portfolio_change = total_stressed_value - portfolio_value
    portfolio_pct_change = portfolio_change / portfolio_value if portfolio_value > 0 else 0
    
    return {
        'scenario_name': scenario_name,
        'scenario_description': scenario['description'],
        'scenario_period': scenario['period'],
        'current_portfolio_value': float(portfolio_value),
        'stressed_portfolio_value': float(total_stressed_value),
        'absolute_change': float(portfolio_change),
        'percentage_change': float(portfolio_pct_change),
        'position_impacts': stressed_values
    }

def factor_shock_test(portfolio_data, factor_shocks):
    """
    Run a factor-based stress test
    
    Args:
        portfolio_data: Portfolio positions and prices
        factor_shocks: Dictionary of factor shock values
        
    Returns:
        Dictionary with stress test results
    """
    # This would normally use factor exposure data from the database
    # For now, implement a simplified version
    
    # Calculate current portfolio value
    positions = portfolio_data['positions']
    prices = portfolio_data['prices']
    
    # Get factor exposures for the portfolio
    # In a real implementation, this would be retrieved from the database
    # or calculated using the factor model
    
    # Sample factor betas for demonstration
    factor_betas = {
        'Market': 1.05,
        'Size': 0.2,
        'Value': -0.15,
        'Momentum': 0.1,
        'Quality': 0.25,
        'Volatility': -0.3
    }
    
    # Calculate portfolio value
    portfolio_value = 0
    position_values = {}
    
    for idx, position in positions.iterrows():
        symbol = position['symbol']
        quantity = position['quantity']
        
        # Get latest price
        if symbol in prices.columns:
            latest_price = prices[symbol].iloc[-1]
            position_value = quantity * latest_price
            position_values[symbol] = {
                'symbol': symbol,
                'quantity': float(quantity),
                'current_price': float(latest_price),
                'current_value': float(position_value)
            }
            portfolio_value += position_value
    
    # Calculate impact of factor shocks
    total_factor_impact = 0
    factor_impacts = {}
    
    for factor, shock in factor_shocks.items():
        if factor in factor_betas:
            # Impact = Factor Beta * Factor Shock
            impact = factor_betas[factor] * shock
            factor_impacts[factor] = {
                'factor': factor,
                'shock': float(shock),
                'beta': float(factor_betas[factor]),
                'impact': float(impact)
            }
            total_factor_impact += impact
    
    # Calculate overall portfolio impact
    stressed_value = portfolio_value * (1 + total_factor_impact)
    portfolio_change = stressed_value - portfolio_value
    portfolio_pct_change = portfolio_change / portfolio_value if portfolio_value > 0 else 0
    
    return {
        'scenario_type': 'factor_shock',
        'factor_shocks': factor_shocks,
        'current_portfolio_value': float(portfolio_value),
        'stressed_portfolio_value': float(stressed_value),
        'absolute_change': float(portfolio_change),
        'percentage_change': float(portfolio_pct_change),
        'factor_impacts': factor_impacts
    }

def custom_shock_test(portfolio_data, asset_shocks):
    """
    Run a custom asset-level stress test
    
    Args:
        portfolio_data: Portfolio positions and prices
        asset_shocks: Dictionary of asset-specific shock values
        
    Returns:
        Dictionary with stress test results
    """
    # Calculate current portfolio value and apply custom shocks
    positions = portfolio_data['positions']
    prices = portfolio_data['prices']
    
    # Calculate portfolio value
    portfolio_value = 0
    position_values = {}
    
    for idx, position in positions.iterrows():
        symbol = position['symbol']
        quantity = position['quantity']
        
        # Get latest price
        if symbol in prices.columns:
            latest_price = prices[symbol].iloc[-1]
            position_value = quantity * latest_price
            position_values[symbol] = {
                'symbol': symbol,
                'quantity': float(quantity),
                'current_price': float(latest_price),
                'current_value': float(position_value)
            }
            portfolio_value += position_value
    
    # Apply asset-specific shocks
    stressed_values = {}
    total_stressed_value = 0
    
    for symbol, position in position_values.items():
        # Get shock for this asset (or 0 if not specified)
        shock = asset_shocks.get(symbol, 0)
        
        # Calculate stressed value
        stressed_value = position['current_value'] * (1 + shock)
        
        stressed_values[symbol] = {
            'symbol': symbol,
            'current_value': float(position['current_value']),
            'shock': float(shock),
            'stressed_value': float(stressed_value),
            'value_change': float(stressed_value - position['current_value']),
            'pct_change': float(shock)
        }
        
        total_stressed_value += stressed_value
    
    # Calculate overall portfolio impact
    portfolio_change = total_stressed_value - portfolio_value
    portfolio_pct_change = portfolio_change / portfolio_value if portfolio_value > 0 else 0
    
    return {
        'scenario_type': 'custom_shock',
        'current_portfolio_value': float(portfolio_value),
        'stressed_portfolio_value': float(total_stressed_value),
        'absolute_change': float(portfolio_change),
        'percentage_change': float(portfolio_pct_change),
        'position_impacts': stressed_values
    }