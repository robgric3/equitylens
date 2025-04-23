# calculation_engine/optimization/constraints.py

def build_constraint_set(universe_data, constraints_dict):
    """
    Build a set of constraints for portfolio optimization
    
    Args:
        universe_data: DataFrame of security prices
        constraints_dict: Dictionary of constraints from API request
        
    Returns:
        Processed constraint set for optimizer
    """
    constraint_set = {}
    
    # Process sector constraints
    if 'sectors' in constraints_dict:
        sectors = constraints_dict['sectors']
        sector_mapping = {}
        sector_upper = {}
        sector_lower = {}
        
        # Get list of securities
        securities = universe_data.columns
        
        # This would normally come from database
        # For now, assign dummy sectors as a placeholder
        sectors_list = ['Technology', 'Healthcare', 'Financials', 'Consumer', 'Energy']
        import random
        random.seed(42)  # For reproducibility
        
        # Assign random sectors for demonstration
        for security in securities:
            sector = random.choice(sectors_list)
            if sector not in sector_mapping:
                sector_mapping[sector] = []
            sector_mapping[sector].append(security)
        
        for sector_const in sectors:
            sector_name = sector_const['name']
            if 'max' in sector_const:
                sector_upper[sector_name] = sector_const['max']
            if 'min' in sector_const:
                sector_lower[sector_name] = sector_const['min']
        
        constraint_set['sector_constraints'] = {
            'sector_mapping': sector_mapping,
            'sector_upper': sector_upper,
            'sector_lower': sector_lower
        }
    
    # Process position constraints
    if 'positions' in constraints_dict:
        positions = constraints_dict['positions']
        
        position_constraints = {
            'min_weight': positions.get('min_weight', 0.0),
            'max_weight': positions.get('max_weight', 1.0),
            'security_limits': {}
        }
        
        # Process security-specific constraints
        if 'securities' in positions:
            for security in positions['securities']:
                symbol = security['symbol']
                limits = {}
                
                if 'min' in security:
                    limits['min'] = security['min']
                if 'max' in security:
                    limits['max'] = security['max']
                
                if limits:
                    position_constraints['security_limits'][symbol] = limits
        
        constraint_set['position_constraints'] = position_constraints
    
    # Process return target if specified
    if 'target_return' in constraints_dict:
        constraint_set['target_return'] = constraints_dict['target_return']
    
    return constraint_set