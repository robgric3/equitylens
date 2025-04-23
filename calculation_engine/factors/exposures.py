def calculate_exposures(portfolio_data, factor_returns):
    """
    Calculate portfolio's factor exposures
    
    Args:
        portfolio_data: Portfolio positions and prices
        factor_returns: Factor returns time series
        
    Returns:
        Dictionary of factor exposures and statistics
    """
    # Calculate portfolio returns
    from calculation_engine.performance.returns import calculate_portfolio_returns
    portfolio_returns = calculate_portfolio_returns(portfolio_data)
    
    # Align dates between portfolio returns and factor returns
    aligned_data = pd.merge(
        portfolio_returns, 
        factor_returns,
        left_index=True,
        right_index=True,
        how='inner'
    )
    
    if len(aligned_data) < 20:
        raise ValueError("Insufficient data for factor analysis (need at least 20 observations)")
    
    # Prepare data for regression
    y = aligned_data['portfolio_return'].values
    
    # For Fama-French 3-factor model
    if 'mkt_rf' in aligned_data.columns and 'smb' in aligned_data.columns and 'hml' in aligned_data.columns:
        X = aligned_data[['mkt_rf', 'smb', 'hml']].values
        factor_names = ['Market', 'Size', 'Value']
    # For Fama-French 5-factor model
    elif 'rmw' in aligned_data.columns and 'cma' in aligned_data.columns:
        X = aligned_data[['mkt_rf', 'smb', 'hml', 'rmw', 'cma']].values
        factor_names = ['Market', 'Size', 'Value', 'Profitability', 'Investment']
    else:
        # Custom set of factors
        factor_cols = [col for col in aligned_data.columns if col != 'portfolio_return']
        X = aligned_data[factor_cols].values
        factor_names = factor_cols
    
    # Add constant for regression
    X_with_const = sm.add_constant(X)
    
    # Run regression
    model = sm.OLS(y, X_with_const)
    results = model.fit()
    
    # Extract exposures (betas) and statistics
    exposures = results.params[1:]  # Skip the constant term
    t_values = results.tvalues[1:]  # t-statistics
    p_values = results.pvalues[1:]  # p-values
    r_squared = results.rsquared
    adj_r_squared = results.rsquared_adj
    
    # Map exposures to factor names
    exposure_dict = {
        'overall_r_squared': float(r_squared),
        'adjusted_r_squared': float(adj_r_squared),
        'factors': {}
    }
    
    for i, factor_name in enumerate(factor_names):
        exposure_dict['factors'][factor_name] = {
            'exposure': float(exposures[i]),
            't_statistic': float(t_values[i]),
            'p_value': float(p_values[i]),
            'significant': bool(p_values[i] < 0.05)
        }
    
    return exposure_dict

def calculate_attribution(portfolio_data, factor_returns, factor_exposures):
    """
    Calculate factor attribution of returns
    
    Args:
        portfolio_data: Portfolio positions and prices
        factor_returns: Factor returns time series
        factor_exposures: Previously calculated factor exposures
        
    Returns:
        Dictionary with factor attribution analysis
    """
    # Calculate portfolio returns
    from calculation_engine.performance.returns import calculate_portfolio_returns
    portfolio_returns = calculate_portfolio_returns(portfolio_data)
    
    # Align dates
    aligned_data = pd.merge(
        portfolio_returns, 
        factor_returns,
        left_index=True,
        right_index=True,
        how='inner'
    )
    
    # Calculate factor contributions to return
    factor_names = list(factor_exposures['factors'].keys())
    factor_betas = {name: factor_exposures['factors'][name]['exposure'] for name in factor_names}
    
    attribution = {
        'total_return': float(portfolio_returns['portfolio_return'].sum()),
        'factor_contributions': {},
        'specific_return': 0.0,
        'period_breakdown': []
    }
    
    # Map factor names to dataframe columns
    factor_cols = []
    for name in factor_names:
        if name == 'Market':
            factor_cols.append('mkt_rf')
        elif name == 'Size':
            factor_cols.append('smb')
        elif name == 'Value':
            factor_cols.append('hml')
        elif name == 'Profitability':
            factor_cols.append('rmw')
        elif name == 'Investment':
            factor_cols.append('cma')
        else:
            factor_cols.append(name.lower())
    
    # Calculate factor contributions
    total_factor_contribution = 0.0
    for i, name in enumerate(factor_names):
        col = factor_cols[i]
        beta = factor_betas[name]
        
        # Factor contribution is beta * factor return
        factor_return = aligned_data[col].sum()
        contribution = beta * factor_return
        total_factor_contribution += contribution
        
        attribution['factor_contributions'][name] = {
            'exposure': float(beta),
            'factor_return': float(factor_return),
            'contribution': float(contribution)
        }
    
    # Specific (idiosyncratic) return is what's not explained by factors
    specific_return = attribution['total_return'] - total_factor_contribution
    attribution['specific_return'] = float(specific_return)
    
    # Add monthly breakdown for more detailed analysis
    monthly_data = aligned_data.copy()
    monthly_data.index = pd.to_datetime(monthly_data.index)
    monthly_returns = monthly_data.resample('M').apply(
        lambda x: (1 + x).prod() - 1 if x.name == 'portfolio_return' else x.sum()
    )
    
    for idx, row in monthly_returns.iterrows():
        month_contrib = {
            'period': idx.strftime('%Y-%m'),
            'portfolio_return': float(row['portfolio_return']),
            'factor_contributions': {}
        }
        
        month_factor_contrib = 0.0
        for i, name in enumerate(factor_names):
            col = factor_cols[i]
            beta = factor_betas[name]
            contrib = beta * row[col]
            month_factor_contrib += contrib
            
            month_contrib['factor_contributions'][name] = float(contrib)
        
        month_contrib['specific_return'] = float(row['portfolio_return'] - month_factor_contrib)
        attribution['period_breakdown'].append(month_contrib)
    
    return attribution