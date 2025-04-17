# EquityLens: Equity Portfolio Analytics & Risk Platform

A professional-grade portfolio analytics and risk management system focused exclusively on equity markets, providing institutional-quality analysis at a fraction of the cost.

![Project Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10-green)

## Overview

EquityLens is a comprehensive platform for constructing, analyzing, and risk-testing equity portfolios. It combines modern portfolio theory with factor-based analysis to provide institutional-quality insights without the enterprise price tag. The system enables portfolio managers, analysts, and individual investors to make data-driven investment decisions through robust quantitative methods.

The platform focuses exclusively on equity securities to provide deep analytical capabilities while maintaining a manageable scope and implementation timeline.

## Features

### Portfolio Construction & Management
- **Position tracking**: Full historical position management with proper handling of corporate actions
- **Multi-portfolio support**: Create and compare multiple portfolio strategies
- **Optimization engine**: Mean-variance optimization with customizable constraints
- **Rebalancing frameworks**: Rules-based, threshold-based, and calendar-driven rebalancing strategies
- **What-if analysis**: Pre-trade impact analysis and portfolio simulation

### Factor Analysis
- **Multi-factor modeling**: Implementation of Fama-French factors with extensibility
- **Factor exposure visualization**: Breakdown of portfolio exposures across factors
- **Custom factor creation**: Define and test proprietary factors
- **Style analysis**: Returns-based and holdings-based style analysis
- **Factor attribution**: Decompose performance into factor contributions

### Risk Analytics
- **Market risk metrics**: Beta, volatility, correlation, tracking error, information ratio
- **Value at Risk (VaR)**: Historical, parametric, and Monte Carlo methodologies
- **Stress testing engine**: Historical scenarios and custom stress test creation
- **Concentration analysis**: Sector, industry, geographic, and individual security exposure
- **Tail risk assessment**: Expected shortfall (CVaR) and higher moment analysis

### Performance Analysis
- **Return calculations**: Time-weighted and money-weighted return methodologies
- **Attribution analysis**: Sector, industry, and security selection attribution
- **Benchmark comparison**: Multiple benchmark support with custom benchmark creation
- **Performance visualization**: Interactive charting of relative and absolute performance
- **Historical analytics**: Rolling period analysis with statistical significance testing

## Architecture

EquityLens employs a modern, modular architecture designed for performance, extensibility, and maintainability:

### Core Components
1. **Data Layer**: TimescaleDB for time-series data with proper handling of point-in-time information
2. **Calculation Engine**: Vectorized Python modules for computational efficiency
3. **API Layer**: FastAPI service providing consistent access to all platform capabilities
4. **Orchestration Layer**: Airflow for scheduled processes and data pipelines
5. **Visualization Layer**: React-based dashboard with interactive components

### System Design

```
┌────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Data Sources  │────▶│  Data Pipeline  │────▶│  TimescaleDB    │
└────────────────┘     │  (Airflow DAGs) │     │  (Time-Series)  │
                       └─────────────────┘     └────────┬────────┘
                                                        │
┌────────────────┐     ┌─────────────────┐             │
│  Dashboard     │◀───▶│  API Layer      │◀────────────┘
│  (React)       │     │  (FastAPI)      │
└────────────────┘     └────────┬────────┘
                                │
                       ┌────────▼────────┐
                       │ Calculation     │
                       │ Engine (Python) │
                       └─────────────────┘
```

## Technology Stack

EquityLens leverages industry-standard open-source technologies to create a professional platform without enterprise costs:

### Backend Infrastructure
- **Python 3.10+**: Core programming language for financial calculations
- **TimescaleDB**: Specialized PostgreSQL extension optimized for time-series data
- **FastAPI**: High-performance API framework with automatic documentation
- **Apache Airflow**: Workflow orchestration for data pipelines
- **Redis**: In-memory cache for performance-critical calculations
- **Docker**: Containerization for consistent deployment

### Calculation Engine
- **NumPy/pandas**: Numerical computing and data manipulation
- **scikit-learn**: Machine learning for anomaly detection and clustering
- **statsmodels**: Statistical models for hypothesis testing and time-series analysis
- **pyportfolioopt**: Modern portfolio optimization algorithms
- **Numba**: JIT compilation for performance-critical numerical calculations

### Frontend
- **React**: Component-based UI library
- **Redux**: State management for complex applications
- **Victory/Recharts**: Interactive financial charting
- **Material-UI**: Professional UI component library
- **React-Table**: Data grid for portfolio analysis

### Data Sources
- **Yahoo Finance API**: Free equity pricing data with historical coverage
- **Alpha Vantage**: Basic financial data (limited API calls on free tier)
- **Financial Modeling Prep**: Fundamental data (limited on free tier)
- **FRED API**: Economic indicators from Federal Reserve
- **SEC EDGAR**: Regulatory filings data through web scraping

## Project Structure

```
equitylens/
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── models/
│       ├── routers/
│       └── services/
├── calculation_engine/
│   ├── portfolio/
│   ├── risk/
│   ├── performance/
│   ├── factors/
│   └── optimization/
├── airflow/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── dags/
│       ├── market_data_pipeline.py
│       ├── factor_calculation_pipeline.py
│       └── portfolio_analytics_pipeline.py
├── dashboard/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── store/
├── database/
│   ├── init-scripts/
│   └── migrations/
└── docs/
    ├── architecture/
    ├── user_guide/
    └── api_reference/
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.10+
- Node.js 16+

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/equitylens.git
   cd equitylens
   ```

2. Create a `.env` file with required API keys and configuration:
   ```
   ALPHA_VANTAGE_API_KEY=your_free_tier_key
   FINANCIAL_MODELING_PREP_API_KEY=your_free_tier_key
   POSTGRES_PASSWORD=your_secure_password
   ```

3. Build and start the containers:
   ```
   docker-compose up -d
   ```

4. Access the components:
   - Dashboard: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Airflow UI: http://localhost:8080

## Data Management

### Data Sources
EquityLens uses a combination of free and low-cost data sources to minimize expenses:

1. **Market Data**: Yahoo Finance API (free) with fallback to Alpha Vantage (free tier)
2. **Fundamental Data**: Financial Modeling Prep API (free tier) and SEC EDGAR web scraping
3. **Factor Data**: Calculated internally using raw market data
4. **Classification Data**: Static industry/sector mappings with manual updates

### Data Pipeline
The system employs a robust data management process:

1. **Extraction**: Daily scheduled retrieval of pricing and factor data
2. **Validation**: Statistical checks to identify anomalies and ensure quality
3. **Transformation**: Calculation of derived metrics and proper handling of corporate actions
4. **Loading**: Optimized storage in TimescaleDB with appropriate indices
5. **Caching**: Frequently accessed data cached in Redis for performance

## Key Capabilities

### Portfolio Construction
- Create portfolios by uploading holdings or manual entry
- Set investment constraints (sector limits, max position sizes)
- Optimize for various objectives (max Sharpe, min volatility, target return)
- Implement custom portfolio construction methodologies

### Risk Analysis
- Calculate standard metrics (volatility, Sharpe ratio, drawdown)
- Implement multiple VaR methodologies with custom confidence intervals
- Perform historical stress tests (2008 Crisis, 2020 COVID crash)
- Analyze factor exposures and their contribution to risk

### Performance Attribution
- Break down returns by sectors, industries, and securities
- Attribute performance to investment decisions vs market movements
- Compare against multiple benchmarks
- Analyze rolling performance over various time periods

### Interactive Analysis
- Filter and group portfolio data dynamically
- Create custom visualizations of portfolio characteristics
- Export analysis results in various formats
- Save and share analysis configurations

## Deployment Options

### Local Development
- Full system runs on a standard development machine
- Docker containers handle service isolation
- Volume mounts for rapid development iteration

### Low-Cost Production
- AWS Free Tier eligible setup
- Digital Ocean basic droplet ($5-10/month)
- Raspberry Pi self-hosting option

### Scaling Considerations
- Separate DB and application tiers as complexity grows
- Implement calculation job queue for intensive operations
- Consider read replicas for data-intensive workloads

## Future Enhancements

- **Machine learning integration**: Anomaly detection and pattern recognition
- **Alternative data sources**: Sentiment analysis and ESG metrics
- **Options analytics**: Basic equity options analysis and strategy building
- **Portfolio optimization enhancements**: Black-Litterman and robust optimization methods
- **Multi-user support**: Authentication and authorization for team use

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Financial algorithms based on academic research and industry best practices
- Inspired by institutional portfolio management systems
- Built with open-source tools and community resources