export const mockPortfolio = {
    id: 1,
    name: "Tech Growth Portfolio",
    description: "A growth-oriented portfolio focused on technology and innovation",
    inception_date: "2023-01-01",
    currency: "USD",
    created_at: "2023-01-01",
    updated_at: "2023-04-10",
    positions: [
      {
        id: 1,
        symbol: "AAPL",
        quantity: 100,
        entry_date: "2023-01-01",
        entry_price: 150.75,
        current_price: 175.25,
        market_value: 17525
      },
      {
        id: 2,
        symbol: "MSFT",
        quantity: 50,
        entry_date: "2023-01-01",
        entry_price: 250.50,
        current_price: 275.80,
        market_value: 13790
      },
      {
        id: 3,
        symbol: "GOOGL",
        quantity: 20,
        entry_date: "2023-01-01",
        entry_price: 2300.00,
        current_price: 2450.00,
        market_value: 49000
      },
      {
        id: 4,
        symbol: "AMZN",
        quantity: 15,
        entry_date: "2023-01-01",
        entry_price: 3200.00,
        current_price: 3300.00,
        market_value: 49500
      },
      {
        id: 5,
        symbol: "NVDA",
        quantity: 40,
        entry_date: "2023-01-01",
        entry_price: 220.00,
        current_price: 270.00,
        market_value: 10800
      }
    ]
  };
  
  export const mockPerformance = {
    total_return: 0.12,
    annualized_return: 0.15,
    volatility: 0.18,
    sharpe_ratio: 0.83,
    max_drawdown: -0.08,
    tracking_error: 0.05,
    information_ratio: 0.62,
    time_series: [
      { date: "2023-01-01", value: 100000, benchmark: 100000 },
      { date: "2023-01-15", value: 101500, benchmark: 100800 },
      { date: "2023-02-01", value: 102000, benchmark: 101200 },
      { date: "2023-02-15", value: 101200, benchmark: 100500 },
      { date: "2023-03-01", value: 105000, benchmark: 103000 },
      { date: "2023-03-15", value: 106500, benchmark: 104200 },
      { date: "2023-04-01", value: 108000, benchmark: 104500 },
      { date: "2023-04-15", value: 110000, benchmark: 105200 },
      { date: "2023-05-01", value: 112000, benchmark: 106000 }
    ]
  };
  
  export const mockRiskMetrics = {
    volatility: 0.18,
    var: {
      value: 0.08,
      confidence_level: 0.95,
      method: "historical",
      cvar: 0.12
    },
    max_drawdown: -0.08,
    beta: 1.15,
    sharpe_ratio: 0.83,
    tracking_error: 0.05,
    information_ratio: 0.62,
    downside_deviation: 0.08,
    sortino_ratio: 0.94,
    concentration_risk: {
      top_holding_pct: 0.15,
      top_5_holdings_pct: 0.45,
      sector_concentration: [
        { name: "Technology", weight: 0.65 },
        { name: "Consumer Discretionary", weight: 0.15 },
        { name: "Communication Services", weight: 0.12 },
        { name: "Healthcare", weight: 0.05 },
        { name: "Financials", weight: 0.03 }
      ]
    },
    stress_test_results: [
      { scenario: "2008 Financial Crisis", impact: -0.28 },
      { scenario: "COVID-19 Crash", impact: -0.32 },
      { scenario: "Rate Hike 100bps", impact: -0.12 },
      { scenario: "Tech Selloff", impact: -0.25 }
    ]
  };
  
  export const mockFactorExposures = {
    overall_r_squared: 0.82,
    adjusted_r_squared: 0.78,
    factors: {
      Market: {
        exposure: 1.15,
        t_statistic: 8.5,
        p_value: 0.0001,
        significant: true
      },
      Size: {
        exposure: -0.22,
        t_statistic: -1.8,
        p_value: 0.072,
        significant: false
      },
      Value: {
        exposure: -0.42,
        t_statistic: -3.2,
        p_value: 0.002,
        significant: true
      },
      Momentum: {
        exposure: 0.35,
        t_statistic: 2.6,
        p_value: 0.009,
        significant: true
      },
      Quality: {
        exposure: 0.18,
        t_statistic: 1.5,
        p_value: 0.134,
        significant: false
      }
    },
    attribution: {
      total_return: 0.12,
      factor_contributions: {
        Market: {
          exposure: 1.15,
          factor_return: 0.05,
          contribution: 0.0575
        },
        Size: {
          exposure: -0.22,
          factor_return: 0.02,
          contribution: -0.0044
        },
        Value: {
          exposure: -0.42,
          factor_return: -0.03,
          contribution: 0.0126
        },
        Momentum: {
          exposure: 0.35,
          factor_return: 0.04,
          contribution: 0.014
        },
        Quality: {
          exposure: 0.18,
          factor_return: 0.01,
          contribution: 0.0018
        }
      },
      specific_return: 0.0285
    }
  };