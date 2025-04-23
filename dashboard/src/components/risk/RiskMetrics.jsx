import React, { useState } from 'react';
import {
  Typography,
  Box,
  Grid,
  Paper,
  Divider,
  Tooltip,
  IconButton,
  Tabs,
  Tab,
  LinearProgress,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip 
} from '@mui/material';
import {
  Info,
  Warning,
  ShowChart,
  Security,
  ErrorOutline,
  Speed,
  ArrowDropDown,
  ArrowDropUp
} from '@mui/icons-material';

const RiskMetrics = ({ riskMetrics, showDetails = false }) => {
  const [activeTab, setActiveTab] = useState(0);
  
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  // If no risk metrics are available, show placeholder
  if (!riskMetrics) {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>Risk Analysis</Typography>
        <Typography color="text.secondary">Risk metrics not available</Typography>
      </Box>
    );
  }
  
  // Generate mock data for demo purposes
  const mockRiskData = {
    volatility: riskMetrics.volatility || 0.15,
    var: riskMetrics.var || {
      value: 0.08,
      confidence_level: 0.95,
      method: 'historical'
    },
    max_drawdown: riskMetrics.max_drawdown || -0.12,
    beta: riskMetrics.beta || 0.9,
    sharpe_ratio: riskMetrics.sharpe_ratio || 0.75,
    tracking_error: riskMetrics.tracking_error || 0.05,
    information_ratio: riskMetrics.information_ratio || 0.4,
    downside_deviation: riskMetrics.downside_deviation || 0.08,
    sortino_ratio: riskMetrics.sortino_ratio || 0.85,
    concentration_risk: {
      top_holding_pct: 0.15,
      top_5_holdings_pct: 0.45,
      sector_concentration: [
        { name: 'Technology', weight: 0.35 },
        { name: 'Financials', weight: 0.20 },
        { name: 'Healthcare', weight: 0.15 },
        { name: 'Consumer Discretionary', weight: 0.12 },
        { name: 'Industrials', weight: 0.08 },
        { name: 'Other', weight: 0.10 }
      ]
    },
    stress_test_results: [
      { scenario: '2008 Financial Crisis', impact: -0.32 },
      { scenario: 'COVID-19 Crash', impact: -0.25 },
      { scenario: 'Rate Hike 100bps', impact: -0.08 },
      { scenario: 'Tech Selloff', impact: -0.15 }
    ]
  };
  
  // Combine mock data with real data
  const data = { ...mockRiskData, ...riskMetrics };
  
  // Helper function to determine risk level color
  const getRiskColor = (value, thresholds) => {
    if (value <= thresholds.low) return 'success.main';
    if (value <= thresholds.medium) return 'warning.main';
    return 'error.main';
  };
  
  // Helper function to format numbers as percentages
  const formatPercent = (value) => {
    if (value === undefined || value === null) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Risk Metrics</Typography>
        <Tooltip title="Risk metrics are calculated based on historical data and may not predict future performance">
          <IconButton size="small">
            <Info fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
      
      {showDetails && (
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          aria-label="risk metrics tabs"
          variant="fullWidth"
          sx={{ mb: 2 }}
        >
          <Tab label="Summary" />
          <Tab label="VaR" />
          <Tab label="Concentration" />
          <Tab label="Stress Tests" />
        </Tabs>
      )}
      
      {/* Summary Tab or Basic View */}
      {(!showDetails || activeTab === 0) && (
        <Grid container spacing={2}>
          <Grid item xs={12} md={showDetails ? 12 : 6}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>Volatility & Drawdown</Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">Volatility</Typography>
                    <Typography 
                      variant="h6"
                      color={getRiskColor(data.volatility, { low: 0.1, medium: 0.2 })}
                    >
                      {formatPercent(data.volatility)}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">Max Drawdown</Typography>
                    <Typography variant="h6" color="error.main">
                      {formatPercent(data.max_drawdown)}
                    </Typography>
                  </Grid>
                </Grid>
                
                <Divider sx={{ my: 1.5 }} />
                
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">VaR (95%)</Typography>
                    <Typography variant="h6" color="warning.main">
                      {formatPercent(data.var?.value || data.var)}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">Beta</Typography>
                    <Box display="flex" alignItems="center">
                      <Typography variant="h6">
                        {data.beta?.toFixed(2) || 'N/A'}
                      </Typography>
                      {data.beta && (
                        <Box ml={0.5}>
                          {data.beta > 1 ? 
                            <ArrowDropUp color="error" /> : 
                            <ArrowDropDown color="success" />
                          }
                        </Box>
                      )}
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
          
          {!showDetails && (
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" gutterBottom>Risk-Adjusted Returns</Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
                      <Typography 
                        variant="h6"
                        color={getRiskColor(data.sharpe_ratio, { low: 0.5, medium: 1 })}
                      >
                        {data.sharpe_ratio?.toFixed(2) || 'N/A'}
                      </Typography>
                    </Grid>
                    
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">Information Ratio</Typography>
                      <Typography variant="h6">
                        {data.information_ratio?.toFixed(2) || 'N/A'}
                      </Typography>
                    </Grid>
                  </Grid>
                  
                  <Divider sx={{ my: 1.5 }} />
                  
                  <Box>
                    <Typography variant="body2" color="text.secondary" gutterBottom>Top Sector Exposure</Typography>
                    <Box display="flex" alignItems="center">
                      <Typography variant="body2" fontWeight="medium">
                        {data.concentration_risk?.sector_concentration?.[0]?.name || 'Technology'}
                      </Typography>
                      <Box ml={1}>
                        <Chip 
                          label={formatPercent(data.concentration_risk?.sector_concentration?.[0]?.weight || 0.35)} 
                          size="small"
                          color={
                            (data.concentration_risk?.sector_concentration?.[0]?.weight || 0.35) > 0.3 ? 
                            "warning" : "default"
                          }
                        />
                      </Box>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}
          
          {showDetails && (
            <>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>Risk-Adjusted Returns</Typography>
                    
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
                        <Typography 
                          variant="h6"
                          color={getRiskColor(data.sharpe_ratio, { low: 0.5, medium: 1 })}
                        >
                          {data.sharpe_ratio?.toFixed(2) || 'N/A'}
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Sortino Ratio</Typography>
                        <Typography 
                          variant="h6"
                          color={getRiskColor(data.sortino_ratio, { low: 0.5, medium: 1 })}
                        >
                          {data.sortino_ratio?.toFixed(2) || 'N/A'}
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    <Divider sx={{ my: 1.5 }} />
                    
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Information Ratio</Typography>
                        <Typography variant="h6">
                          {data.information_ratio?.toFixed(2) || 'N/A'}
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Tracking Error</Typography>
                        <Typography variant="h6">
                          {formatPercent(data.tracking_error)}
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>Concentration Risk</Typography>
                    
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Top Holding</Typography>
                        <Typography 
                          variant="h6"
                          color={getRiskColor(data.concentration_risk?.top_holding_pct || 0, { low: 0.05, medium: 0.1 })}
                        >
                          {formatPercent(data.concentration_risk?.top_holding_pct)}
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Top 5 Holdings</Typography>
                        <Typography 
                          variant="h6"
                          color={getRiskColor(data.concentration_risk?.top_5_holdings_pct || 0, { low: 0.3, medium: 0.5 })}
                        >
                          {formatPercent(data.concentration_risk?.top_5_holdings_pct)}
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    <Divider sx={{ my: 1.5 }} />
                    
                    <Typography variant="body2" color="text.secondary" gutterBottom>Sector Concentration</Typography>
                    <Box>
                      {(data.concentration_risk?.sector_concentration || [])
                        .slice(0, 2)
                        .map((sector, index) => (
                          <Box key={index} mb={0.5}>
                            <Typography variant="body2">{sector.name}</Typography>
                            <Box display="flex" alignItems="center">
                              <LinearProgress
                                variant="determinate"
                                value={sector.weight * 100}
                                sx={{ 
                                  flexGrow: 1, 
                                  mr: 1,
                                  height: 8,
                                  borderRadius: 1,
                                  backgroundColor: 'grey.200',
                                  '& .MuiLinearProgress-bar': {
                                    backgroundColor: sector.weight > 0.3 ? 'warning.main' : 'primary.main',
                                  }
                                }}
                              />
                              <Typography variant="body2">{formatPercent(sector.weight)}</Typography>
                            </Box>
                          </Box>
                        ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </>
          )}
        </Grid>
      )}
      
      {/* VaR Tab */}
      {showDetails && activeTab === 1 && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>Value at Risk (VaR) Analysis</Typography>
            
            <Box mb={3}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box textAlign="center" p={2} bgcolor="grey.100" borderRadius={1}>
                    <Typography variant="body2" color="text.secondary">VaR (95% Confidence)</Typography>
                    <Typography variant="h4" color="error.main" fontWeight="bold">
                      {formatPercent(data.var?.value || data.var)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Method: {data.var?.method || 'Historical'}
                    </Typography>
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={8}>
                  <Typography variant="body2" paragraph>
                    With 95% confidence, the portfolio's loss will not exceed {formatPercent(data.var?.value || data.var)} over a one-day period. 
                    This means there is a 5% chance that the portfolio could lose more than this amount.
                  </Typography>
                  
                  <Typography variant="body2">
                    The VaR calculation uses the {data.var?.method || 'historical'} method, which {
                      data.var?.method === 'parametric' ? 
                        'assumes returns follow a normal distribution.' :
                      data.var?.method === 'monte_carlo' ?
                        'simulates thousands of possible market scenarios.' :
                        'analyzes actual historical returns without assuming a specific distribution.'
                    }
                  </Typography>
                </Grid>
              </Grid>
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="subtitle2" gutterBottom>Additional Risk Metrics</Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Box p={1}>
                  <Typography variant="body2" color="text.secondary">Expected Shortfall (CVaR)</Typography>
                  <Typography variant="h6" color="error.main">
                    {formatPercent(data.cvar || data.var?.value * 1.3 || 0.1)}
                  </Typography>
                  <Typography variant="caption" display="block">
                    Average loss in worst 5% cases
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box p={1}>
                  <Typography variant="body2" color="text.secondary">Volatility</Typography>
                  <Typography variant="h6" color={getRiskColor(data.volatility, { low: 0.1, medium: 0.2 })}>
                    {formatPercent(data.volatility)}
                  </Typography>
                  <Typography variant="caption" display="block">
                    Annualized standard deviation
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box p={1}>
                  <Typography variant="body2" color="text.secondary">Downside Deviation</Typography>
                  <Typography variant="h6">
                    {formatPercent(data.downside_deviation)}
                  </Typography>
                  <Typography variant="caption" display="block">
                    Volatility of negative returns only
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Box p={1}>
                  <Typography variant="body2" color="text.secondary">Max Drawdown</Typography>
                  <Typography variant="h6" color="error.main">
                    {formatPercent(data.max_drawdown)}
                  </Typography>
                  <Typography variant="caption" display="block">
                    Largest peak-to-trough decline
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
      
      {/* Concentration Tab */}
      {showDetails && activeTab === 2 && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>Concentration Risk</Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Security Concentration</Typography>
                
                <Box mb={2}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Top Holding: {formatPercent(data.concentration_risk?.top_holding_pct)}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={data.concentration_risk?.top_holding_pct * 100 || 15}
                    sx={{ 
                      height: 10,
                      borderRadius: 1,
                      mb: 2,
                      backgroundColor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getRiskColor(
                          data.concentration_risk?.top_holding_pct || 0, 
                          { low: 0.05, medium: 0.1 }
                        ),
                      }
                    }}
                  />
                  
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Top 5 Holdings: {formatPercent(data.concentration_risk?.top_5_holdings_pct)}
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={data.concentration_risk?.top_5_holdings_pct * 100 || 45}
                    sx={{ 
                      height: 10,
                      borderRadius: 1,
                      backgroundColor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getRiskColor(
                          data.concentration_risk?.top_5_holdings_pct || 0, 
                          { low: 0.3, medium: 0.5 }
                        ),
                      }
                    }}
                  />
                </Box>
                
                <Typography variant="body2" mt={2}>
                  {data.concentration_risk?.top_holding_pct > 0.1 ? (
                    <Box display="flex" alignItems="center">
                      <Warning color="warning" sx={{ mr: 1 }} />
                      <Typography variant="body2">
                        High concentration in top holding may increase specific risk.
                      </Typography>
                    </Box>
                  ) : (
                    <Box display="flex" alignItems="center">
                      <Info color="info" sx={{ mr: 1 }} />
                      <Typography variant="body2">
                        Security concentration is within acceptable levels.
                      </Typography>
                    </Box>
                  )}
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Sector Allocation</Typography>
                
                {(data.concentration_risk?.sector_concentration || []).map((sector, index) => (
                  <Box key={index} mb={1}>
                    <Box display="flex" justifyContent="space-between">
                      <Typography variant="body2">{sector.name}</Typography>
                      <Typography variant="body2" fontWeight="medium">
                        {formatPercent(sector.weight)}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={sector.weight * 100}
                      sx={{ 
                        height: 8,
                        borderRadius: 1,
                        backgroundColor: 'grey.200',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: sector.weight > 0.3 ? 'warning.main' : 'primary.main',
                        }
                      }}
                    />
                  </Box>
                ))}
                
                <Typography variant="body2" mt={2}>
                  {data.concentration_risk?.sector_concentration?.[0]?.weight > 0.3 ? (
                    <Box display="flex" alignItems="center">
                      <Warning color="warning" sx={{ mr: 1 }} />
                      <Typography variant="body2">
                        High exposure to {data.concentration_risk?.sector_concentration?.[0]?.name} 
                        may increase sector-specific risk.
                      </Typography>
                    </Box>
                  ) : (
                    <Box display="flex" alignItems="center">
                      <Info color="info" sx={{ mr: 1 }} />
                      <Typography variant="body2">
                        Sector allocation is relatively diversified.
                      </Typography>
                    </Box>
                  )}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
      
      {/* Stress Tests Tab */}
      {showDetails && activeTab === 3 && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="subtitle1" gutterBottom>Stress Test Scenarios</Typography>
            
            <Typography variant="body2" paragraph>
              These scenarios show how the portfolio might perform under various market conditions.
              The impact is shown as potential percentage loss based on historical or simulated events.
            </Typography>
            
            <Grid container spacing={2}>
              {(data.stress_test_results || []).map((scenario, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">{scenario.scenario}</Typography>
                    <Box display="flex" alignItems="center" mt={1}>
                      <Typography 
                        variant="h5" 
                        color="error.main"
                        sx={{ fontWeight: 'bold' }}
                      >
                        {formatPercent(scenario.impact)}
                      </Typography>
                      
                      <Box ml={2} flex={1}>
                        <LinearProgress
                          variant="determinate"
                          value={Math.abs(scenario.impact) * 100}
                          sx={{ 
                            height: 10,
                            borderRadius: 1,
                            backgroundColor: 'grey.200',
                            '& .MuiLinearProgress-bar': {
                              backgroundColor: 'error.main',
                            }
                          }}
                        />
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" mt={1}>
                      {Math.abs(scenario.impact) > 0.3 ? (
                        "Severe impact - consider risk mitigation strategies"
                      ) : Math.abs(scenario.impact) > 0.15 ? (
                        "Moderate impact - monitor closely in similar conditions"
                      ) : (
                        "Limited impact - portfolio shows resilience"
                      )}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
            
            <Box mt={3} bgcolor="grey.100" p={2} borderRadius={1}>
              <Typography variant="subtitle2" gutterBottom>Risk Assessment Summary</Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <ShowChart fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Historical Volatility" 
                    secondary={`The portfolio has ${data.volatility < 0.15 ? 'lower' : 'higher'} than market volatility, indicating ${data.volatility < 0.15 ? 'lower' : 'higher'} risk.`} 
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <ErrorOutline fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Drawdown Risk" 
                    secondary={`Maximum historical drawdown of ${formatPercent(data.max_drawdown)} suggests ${Math.abs(data.max_drawdown) > 0.2 ? 'significant' : 'moderate'} downside risk.`} 
                  />
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Security fontSize="small" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Concentration Risk" 
                    secondary={`${data.concentration_risk?.top_5_holdings_pct > 0.5 ? 'High' : 'Moderate'} concentration in top holdings and ${data.concentration_risk?.sector_concentration?.[0]?.weight > 0.3 ? 'high' : 'moderate'} sector exposure.`} 
                  />
                </ListItem>
              </List>
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default RiskMetrics;