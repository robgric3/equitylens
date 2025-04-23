-- init-scripts/create_tables.sql
-- Create schemas
CREATE SCHEMA IF NOT EXISTS market_data;
CREATE SCHEMA IF NOT EXISTS portfolio_data;
CREATE SCHEMA IF NOT EXISTS factor_data;
CREATE SCHEMA IF NOT EXISTS risk_analytics;

-- TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Market data tables
CREATE TABLE IF NOT EXISTS market_data.daily_prices (
    symbol TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    PRIMARY KEY (symbol, date)
);

-- Convert to hypertable
SELECT create_hypertable('market_data.daily_prices', 'date', if_not_exists => TRUE);

-- Portfolio tables
CREATE TABLE IF NOT EXISTS portfolio_data.portfolios (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    inception_date DATE NOT NULL,
    currency TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_data.positions (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER REFERENCES portfolio_data.portfolios(id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    quantity NUMERIC NOT NULL,
    entry_date DATE NOT NULL,
    entry_price NUMERIC NOT NULL,
    exit_date DATE,
    exit_price NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Factor data tables
CREATE TABLE IF NOT EXISTS factor_data.factor_definitions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS factor_data.factor_values (
    factor_id TEXT REFERENCES factor_data.factor_definitions(id),
    date DATE NOT NULL,
    value NUMERIC NOT NULL,
    PRIMARY KEY (factor_id, date)
);

-- Risk analytics tables
CREATE TABLE IF NOT EXISTS risk_analytics.portfolio_risk_metrics (
    portfolio_id INTEGER REFERENCES portfolio_data.portfolios(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    volatility NUMERIC,
    beta NUMERIC,
    var_95 NUMERIC,
    var_99 NUMERIC,
    expected_shortfall NUMERIC,
    tracking_error NUMERIC,
    information_ratio NUMERIC,
    sharpe_ratio NUMERIC,
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (portfolio_id, date)
);

-- Create database for Airflow
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO equitylens;