# Contributing Guidelines

This document outlines the coding standards and best practices for the EquityLens project. Following these guidelines ensures code consistency, readability, and maintainability across our portfolio analytics and risk management platform.

## Table of Contents

- [Python Standards](#python-standards)
- [JavaScript/React Standards](#javascriptreact-standards)
- [SQL Standards](#sql-standards)
- [Docker Standards](#docker-standards)
- [Git Workflow](#git-workflow)
- [Testing Requirements](#testing-requirements)
- [Documentation Guidelines](#documentation-guidelines)
- [Financial Calculation Standards](#financial-calculation-standards)

## Python Standards

### Naming Conventions

- **Variables and Functions**: Use `snake_case` (e.g., `portfolio_return`, `calculate_sharpe_ratio`)
- **Classes**: Use `PascalCase` (e.g., `PortfolioAnalyzer`, `RiskModel`)
- **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_API_RETRIES`, `RISK_FREE_RATE`)
- **Private Methods/Variables**: Use leading underscore (e.g., `_calculate_internal_metric`)
- **Modules**: Use `snake_case` for file names (e.g., `risk_metrics.py`)

### Formatting

- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **88 characters** (Black formatter standard)
- Use parentheses for line continuation
- Always use explicit line continuation inside parentheses rather than backslashes
- Add two blank lines before class definitions and one blank line before method definitions
- Use single quotes for simple strings, double quotes for strings with apostrophes or when string contains single quotes

### Documentation

- All functions must have docstrings following Google style format
- All classes must have docstrings explaining their purpose
- **Financial calculations must include formulas and references to academic sources**
- Include units (e.g., "returns percentage as decimal, not %")
- Document any assumptions made in financial calculations

### Imports

- Order imports as follows:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library-specific imports
- Separate import groups with a blank line
- Use absolute imports for clarity

```python
# Standard library
import datetime
import json
from typing import Dict, List, Optional

# Third-party libraries
import numpy as np
import pandas as pd
import requests
from fastapi import APIRouter, Depends, HTTPException

# Local modules
from app.core.database import get_db
from app.models.portfolio import Portfolio
```

### Error Handling

- Use specific exceptions rather than bare `except:`
- Log exceptions with context about what happened
- Financial calculation errors should provide clear diagnostics
- Always use `try`/`except` when dealing with external APIs or data sources

### Type Hints

- Use type hints for function parameters and return values
- Use `Optional` for parameters that might be None
- Use `Union` for parameters that might be of multiple types

### Example Function

```python
def calculate_tracking_error(
    portfolio_returns: pd.Series, 
    benchmark_returns: pd.Series,
    annualize: bool = True,
    trading_days_per_year: int = 252
) -> float:
    """
    Calculate tracking error (active risk) between portfolio and benchmark returns.
    
    Args:
        portfolio_returns: Daily portfolio returns as decimals (not percentages)
        benchmark_returns: Daily benchmark returns as decimals (not percentages)
        annualize: Whether to annualize the result
        trading_days_per_year: Number of trading days in a year
        
    Returns:
        Tracking error (annualized if annualize=True)
        
    Formula:
        TE = StdDev(Portfolio_Returns - Benchmark_Returns)
        Annualized by multiplying by sqrt(trading_days_per_year)
        
    Raises:
        ValueError: If return series have different lengths or contain invalid values
    """
    if len(portfolio_returns) != len(benchmark_returns):
        raise ValueError("Portfolio and benchmark return series must have same length")
        
    if len(portfolio_returns) == 0:
        raise ValueError("Empty returns series provided")
        
    try:
        # Calculate active returns
        active_returns = portfolio_returns - benchmark_returns
        
        # Calculate tracking error
        tracking_error = active_returns.std()
        
        # Annualize if requested
        if annualize:
            tracking_error = tracking_error * np.sqrt(trading_days_per_year)
            
        return tracking_error
    except Exception as e:
        logger.error(f"Error calculating tracking error: {e}")
        raise
```

## JavaScript/React Standards

### Naming Conventions

- **Variables and Functions**: Use `camelCase` (e.g., `calculateReturn`, `portfolioValue`)
- **Components**: Use `PascalCase` (e.g., `PortfolioChart`, `RiskMetricsPanel`)
- **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_PORTFOLIO_SIZE`, `DEFAULT_CHART_COLORS`)
- **Files**: Use `PascalCase` for component files, `camelCase` for utility files

### Component Structure

- Use functional components with hooks
- Keep components focused on a single responsibility
- Extract complex logic into custom hooks
- Use prop types or TypeScript for component props

### State Management

- Use React context for global state
- Use Redux for complex state management requirements
- Keep component state minimal and focused

### Styling

- Use CSS modules or styled-components
- Follow a consistent naming convention for CSS classes
- Use responsive design principles throughout

### Example Component

```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { LineChart, XAxis, YAxis, Tooltip, Line, ResponsiveContainer } from 'recharts';

import { formatCurrency, formatPercentage } from '../../utils/formatters';
import usePortfolioData from '../../hooks/usePortfolioData';
import './PerformanceChart.css';

/**
 * Component for displaying portfolio performance over time
 */
const PerformanceChart = ({ portfolioId, benchmark, timeRange }) => {
  const { data, isLoading, error } = usePortfolioData(portfolioId, timeRange);
  const [chartData, setChartData] = useState([]);
  
  useEffect(() => {
    if (data) {
      setChartData(formatChartData(data, benchmark));
    }
  }, [data, benchmark]);
  
  if (isLoading) return <div className="loading">Loading performance data...</div>;
  if (error) return <div className="error">Error loading data: {error.message}</div>;
  
  return (
    <div className="performance-chart">
      <h3 className="chart-title">Portfolio Performance</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis dataKey="date" />
          <YAxis tickFormatter={formatPercentage} />
          <Tooltip formatter={(value) => formatPercentage(value)} />
          <Line 
            type="monotone" 
            dataKey="portfolioReturn" 
            stroke="#8884d8" 
            name="Portfolio" 
          />
          <Line 
            type="monotone" 
            dataKey="benchmarkReturn" 
            stroke="#82ca9d" 
            name="Benchmark" 
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

PerformanceChart.propTypes = {
  portfolioId: PropTypes.string.isRequired,
  benchmark: PropTypes.string,
  timeRange: PropTypes.oneOf(['1M', '3M', '6M', '1Y', '3Y', '5Y', 'MAX'])
};

PerformanceChart.defaultProps = {
  benchmark: 'SPY',
  timeRange: '1Y'
};

export default PerformanceChart;
```

## SQL Standards

### Naming Conventions

- **Tables**: Use `snake_case`, plural (e.g., `daily_prices`, `portfolios`)
- **Columns**: Use `snake_case` (e.g., `adjusted_close`, `portfolio_value`)
- **Primary Keys**: Use `id` or `table_name_id`
- **Foreign Keys**: Use `referenced_table_singular_name_id` (e.g., `security_id`)
- **Indexes**: Use `idx_table_name_column_name` format

### Formatting

- Keywords in UPPERCASE (e.g., `SELECT`, `FROM`, `JOIN`)
- Commas at the end of lines, not the beginning
- Indentation for clauses (4 spaces)
- Aliases for table names (especially in complex queries)
- Each major clause (SELECT, FROM, WHERE, etc.) should start on a new line

### Documentation

- Comment blocks at the beginning of complex queries
- Comments explaining non-obvious joins or conditions
- Document performance considerations for complex queries
- Document time-series specific optimizations for TimescaleDB

### Example Query

```sql
-- Calculate the rolling portfolio value over time
-- Uses time-bucket functionality from TimescaleDB
-- Note: Aggregates portfolio value by week for performance
SELECT 
    p.portfolio_id,
    time_bucket('1 week', p.date) AS week,
    SUM(p.quantity * dp.adjusted_close) AS portfolio_value,
    AVG(p.quantity * dp.adjusted_close) AS avg_weekly_value,
    MIN(p.quantity * dp.adjusted_close) AS min_weekly_value,
    MAX(p.quantity * dp.adjusted_close) AS max_weekly_value
FROM 
    portfolio.positions p
JOIN 
    market_data.daily_prices dp ON p.symbol = dp.symbol AND p.date = dp.date
WHERE 
    p.portfolio_id = 'DEMO-001'
    AND p.date >= '2023-01-01'
GROUP BY 
    p.portfolio_id,
    time_bucket('1 week', p.date)
ORDER BY 
    week;
```

## Docker Standards

### Image Building

- Use specific versions for base images, not `latest`
- Use multi-stage builds where appropriate to reduce image size
- Include only necessary files in the Docker context

### Docker Compose

- Use descriptive service names
- Group environment variables logically
- Use environment files for sensitive information
- Include comments for non-obvious configuration options

### Example Docker Compose Service

```yaml
# API service for portfolio analytics
api:
  build:
    context: ./api
    dockerfile: Dockerfile
  container_name: equitylens_api
  depends_on:
    - timescaledb
  ports:
    - "8000:8000"
  volumes:
    - ./api:/app
  environment:
    # Database connection
    - DATABASE_URL=postgresql://equitylens:${POSTGRES_PASSWORD:-equitylens}@timescaledb:5432/equitylens
    # API configuration
    - LOG_LEVEL=info
    - ENABLE_CORS=true
    - MAX_WORKERS=4
    # Market data settings
    - YAHOO_FINANCE_RATE_LIMIT=2000  # Maximum API calls per hour
  restart: unless-stopped
```

## Git Workflow

### Branches

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/feature-name`: New features or enhancements
- `fix/bug-description`: Bug fixes
- `refactor/description`: Code refactoring without changing functionality

### Commit Messages

Follow the conventional commits specification:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(risk-metrics): add Value at Risk calculation

- Implemented historical VaR calculation with configurable confidence level
- Added parametric VaR as alternative methodology
- Created endpoint at /api/portfolios/{id}/risk/var
- Added unit tests with known test cases
```

## Testing Requirements

### Unit Tests

- Write tests for all financial calculations
- Test edge cases (empty portfolios, extreme market conditions, etc.)
- Aim for at least 80% code coverage
- Validate results against known academic benchmarks where possible

### Integration Tests

- Test data flows from market data to portfolio analytics
- Verify API endpoints return expected data
- Test database interactions with time-series data

### Frontend Tests

- Component tests with React Testing Library
- End-to-end tests with Cypress for critical workflows
- Visual regression tests for dashboard components

### Example Test

```python
def test_calculate_drawdown():
    """Test maximum drawdown calculation with known values."""
    # Arrange
    prices = pd.Series([100, 120, 90, 80, 85, 90, 85, 100])
    
    # Act
    result = calculate_maximum_drawdown(prices)
    
    # Assert
    expected_drawdown = 0.3333  # (120-80)/120
    np.testing.assert_almost_equal(result, expected_drawdown, decimal=4)
    
    # Test with empty series
    with pytest.raises(ValueError, match="Empty price series"):
        calculate_maximum_drawdown(pd.Series([]))
```

## Documentation Guidelines

### README.md

- Project overview and purpose
- Installation instructions
- Quick start guide
- Features list
- Configuration options
- Architecture diagram

### Code Comments

- Comment complex algorithms
- Explain why, not what (the code shows what, comments explain why)
- Document known limitations or edge cases
- Document any financial assumptions

### API Documentation

- Document all endpoints
- Include example requests and responses
- List all query parameters and their purpose
- Document expected performance characteristics

## Financial Calculation Standards

### General Principles

- All financial calculations must include citations to academic sources or industry standards
- Include edge case handling (e.g., division by zero in ratio calculations)
- Document time period assumptions (e.g., annualization factors)
- Use consistent conventions for returns (decimal vs. percentage)
- Implement validation checks for input data

### Risk Metrics

- Value at Risk (VaR) calculations must specify:
  - Confidence level (e.g., 95%, 99%)
  - Time horizon (e.g., 1-day, 10-day)
  - Methodology (historical, parametric, Monte Carlo)
- Performance metrics must specify:
  - Time period (e.g., trailing 1-year, 3-year)
  - Whether figures are annualized
  - Benchmark used for relative metrics

### Example Documentation

```python
def calculate_information_ratio(
    portfolio_returns: pd.Series, 
    benchmark_returns: pd.Series,
    annualize: bool = True,
    trading_days_per_year: int = 252
) -> float:
    """
    Calculate the Information Ratio of a portfolio.
    
    The Information Ratio measures portfolio active return per unit of active risk.
    
    Args:
        portfolio_returns: Daily portfolio returns as decimals
        benchmark_returns: Daily benchmark returns as decimals
        annualize: Whether to annualize the result
        trading_days_per_year: Number of trading days per year
        
    Returns:
        Information Ratio (annualized if annualize=True)
        
    Formula:
        IR = (Portfolio_Return - Benchmark_Return) / Tracking_Error
        
    References:
        Grinold, Richard C., and Ronald N. Kahn. "Active Portfolio Management." 
        McGraw-Hill, 2000, pp. 114-117.
        
    Notes:
        - Higher values indicate better risk-adjusted performance
        - Generally, IR > 0.5 is considered good, IR > 1.0 is excellent
        - Formula assumes consistent time frequency in both return series
    """
    # Implementation...
```

## Development Environment Setup

To enforce these standards, the project includes the following tools:

1. **Black**: Code formatter
   - Configuration in `pyproject.toml`
   - Run with `black .`

2. **isort**: Import sorter
   - Configuration in `pyproject.toml`
   - Run with `isort .`

3. **flake8**: Linter
   - Configuration in `setup.cfg`
   - Run with `flake8 .`

4. **mypy**: Type checker
   - Configuration in `mypy.ini`
   - Run with `mypy .`

5. **ESLint and Prettier**: For JavaScript/React
   - Configuration in `.eslintrc.js` and `.prettierrc`
   - Run with `eslint . --fix` and `prettier --write .`

6. **Pre-commit**: Git hooks
   - Configuration in `.pre-commit-config.yaml`
   - Install with `pre-commit install`

## Configuration Files

### pyproject.toml

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3
include_trailing_comma = true
```

### setup.cfg

```ini
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = .git,__pycache__,build,dist
```

### .pre-commit-config.yaml

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
    -   id: flake8
    
-   repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
    -   id: prettier
        types_or: [javascript, jsx, ts, tsx, json, css, markdown]
```