import React, { useState } from 'react';
import {
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Divider,
  Tooltip,
  IconButton,
  Tabs,
  Tab,
  ToggleButtonGroup,
  ToggleButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import { Info, ShowChart, BarChart, PieChart } from '@mui/icons-material';
import { BarChart as RechartsBarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Cell, LabelList, Tooltip as RechartsTooltip } from 'recharts';

const FactorExposure = ({ factorExposures, showDetails = false }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [chartType, setChartType] = useState('bar');
  
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  // Handle chart type change
  const handleChartTypeChange = (event, newChartType) => {
    if (newChartType !== null) {
      setChartType(newChartType);
    }
  };
  
  // Mock data if no factor exposures are available
  const mockFactorExposures = {
    overall_r_squared: 0.85,
    adjusted_r_squared: 0.82,
    factors: {
      Market: {
        exposure: 1.05,
        t_statistic: 8.2,
        p_value: 0.0001,
        significant: true
      },
      Size: {
        exposure: 0.25,
        t_statistic: 2.1,
        p_value: 0.038,
        significant: true
      },
      Value: {
        exposure: -0.15,
        t_statistic: -1.2,
        p_value: 0.22,
        significant: false
      },
      Momentum: {
        exposure: 0.12,
        t_statistic: 0.9,
        p_value: 0.36,
        significant: false
      },
      Quality: {
        exposure: 0.30,
        t_statistic: 2.4,
        p_value: 0.018,
        significant: true
      }
    },
    attribution: {
      total_return: 0.12,
      factor_contributions: {
        Market: {
          exposure: 1.05,
          factor_return: 0.07,
          contribution: 0.0735
        },
        Size: {
          exposure: 0.25,
          factor_return: 0.02,
          contribution: 0.005
        },
        Value: {
          exposure: -0.15,
          factor_return: -0.01,
          contribution: 0.0015
        },
        Momentum: {
          exposure: 0.12,
          factor_return: 0.03,
          contribution: 0.0036
        },
        Quality: {
          exposure: 0.30,
          factor_return: 0.04,
          contribution: 0.012
        }
      },
      specific_return: 0.015
    }
  };
  
  // Use real data if available, otherwise use mock data
  const data = factorExposures || mockFactorExposures;
  
  // Prepare data for charts
  const factorExposureData = Object.entries(data.factors || {}).map(([factor, details]) => ({
    factor,
    exposure: details.exposure,
    significant: details.significant,
    t_statistic: details.t_statistic,
    p_value: details.p_value
  }));
  
  // Prepare attribution data if available
  const attributionData = data.attribution ? Object.entries(data.attribution.factor_contributions || {}).map(([factor, details]) => ({
    factor,
    contribution: details.contribution,
    percentage: (details.contribution / data.attribution.total_return) * 100
  })) : [];
  
  // Add specific return to attribution data if available
  if (data.attribution) {
    attributionData.push({
      factor: 'Specific',
      contribution: data.attribution.specific_return,
      percentage: (data.attribution.specific_return / data.attribution.total_return) * 100
    });
  }
  
  // Color scheme for charts
  const factorColors = {
    Market: '#3f51b5',
    Size: '#4caf50',
    Value: '#f44336',
    Momentum: '#ff9800',
    Quality: '#9c27b0',
    Specific: '#607d8b'
  };
  
  if (!data) {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>Factor Analysis</Typography>
        <Typography color="text.secondary">Factor data not available</Typography>
      </Box>
    );
  }
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Factor Analysis</Typography>
        <Tooltip title="Factor analysis shows portfolio exposures to common market factors that drive returns">
          <IconButton size="small">
            <Info fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
      
      {showDetails && (
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          aria-label="factor analysis tabs"
          variant="fullWidth"
          sx={{ mb: 2 }}
        >
          <Tab label="Exposures" />
          <Tab label="Attribution" />
          <Tab label="Details" />
        </Tabs>
      )}
      
      {/* Factor Exposures Tab or Basic View */}
      {(!showDetails || activeTab === 0) && (
        <>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="subtitle1">Factor Exposures</Typography>
            {showDetails && (
              <ToggleButtonGroup
                value={chartType}
                exclusive
                onChange={handleChartTypeChange}
                size="small"
              >
                <ToggleButton value="bar">
                  <BarChart fontSize="small" />
                </ToggleButton>
                <ToggleButton value="table">
                  <ShowChart fontSize="small" />
                </ToggleButton>
              </ToggleButtonGroup>
            )}
          </Box>
          
          {chartType === 'bar' ? (
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <RechartsBarChart
                  data={factorExposureData}
                  margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="factor" 
                    angle={-45} 
                    textAnchor="end" 
                    tick={{ fontSize: 12 }}
                    tickMargin={10}
                  />
                  <YAxis label={{ value: 'Exposure', angle: -90, position: 'insideLeft' }} />
                  <RechartsTooltip 
                    formatter={(value, name, props) => [
                      value.toFixed(2),
                      'Factor Exposure'
                    ]}
                  />
                  <Bar dataKey="exposure" fill="#8884d8">
                    {factorExposureData.map((entry, index) => (
                      <Cell 
                        key={`cell-${index}`} 
                        fill={factorColors[entry.factor] || '#8884d8'} 
                        fillOpacity={entry.significant ? 1 : 0.5}
                        stroke={entry.significant ? '#333' : 'none'}
                        strokeWidth={entry.significant ? 1 : 0}
                      />
                    ))}
                    <LabelList dataKey="exposure" position="top" formatter={(value) => value.toFixed(2)} />
                  </Bar>
                </RechartsBarChart>
              </ResponsiveContainer>
            </Box>
          ) : (
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Factor</TableCell>
                    <TableCell align="right">Exposure</TableCell>
                    <TableCell align="right">t-statistic</TableCell>
                    <TableCell align="right">Significant</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {factorExposureData.map((row) => (
                    <TableRow key={row.factor}>
                      <TableCell component="th" scope="row">
                        {row.factor}
                      </TableCell>
                      <TableCell 
                        align="right"
                        sx={{ 
                          color: row.exposure > 0 ? 'success.main' : 'error.main',
                          fontWeight: Math.abs(row.exposure) > 0.3 ? 'bold' : 'normal'
                        }}
                      >
                        {row.exposure.toFixed(2)}
                      </TableCell>
                      <TableCell align="right">{row.t_statistic.toFixed(2)}</TableCell>
                      <TableCell align="right">
                        {row.significant ? 'Yes' : 'No'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          
          <Box mt={2}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>Model Fit</Typography>
                    <Typography variant="h6">R² = {(data.overall_r_squared * 100).toFixed(1)}%</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {data.overall_r_squared > 0.8 ? 'Strong' : data.overall_r_squared > 0.6 ? 'Moderate' : 'Weak'} explanatory power
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>Key Drivers</Typography>
                    {factorExposureData
                      .filter(factor => factor.significant)
                      .slice(0, 2)
                      .map((factor, index) => (
                        <Box key={index} display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
                          <Typography variant="body2">{factor.factor}</Typography>
                          <Typography 
                            variant="body2" 
                            fontWeight="medium"
                            color={factor.exposure > 0 ? 'success.main' : 'error.main'}
                          >
                            {factor.exposure.toFixed(2)}
                          </Typography>
                        </Box>
                      ))}
                    {factorExposureData.filter(factor => factor.significant).length === 0 && (
                      <Typography variant="body2" color="text.secondary">
                        No statistically significant factor exposures
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        </>
      )}
      
      {/* Factor Attribution Tab */}
      {showDetails && activeTab === 1 && data.attribution && (
        <>
          <Typography variant="subtitle1" gutterBottom>Return Attribution</Typography>
          
          <Box mb={3}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card variant="outlined">
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary">Total Return</Typography>
                    <Typography 
                      variant="h4" 
                      sx={{ 
                        color: data.attribution.total_return >= 0 ? 'success.main' : 'error.main',
                        fontWeight: 'bold' 
                      }}
                    >
                      {(data.attribution.total_return * 100).toFixed(2)}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={8}>
                <Card variant="outlined" sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="subtitle2" gutterBottom>Return Breakdown</Typography>
                    
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Factor Return</Typography>
                        <Typography 
                          variant="h6" 
                          color={
                            data.attribution.total_return - data.attribution.specific_return >= 0 ? 
                            'success.main' : 'error.main'
                          }
                        >
                          {((data.attribution.total_return - data.attribution.specific_return) * 100).toFixed(2)}%
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Specific Return</Typography>
                        <Typography 
                          variant="h6"
                          color={data.attribution.specific_return >= 0 ? 'success.main' : 'error.main'}
                        >
                          {(data.attribution.specific_return * 100).toFixed(2)}%
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
          
          <Box height={350}>
            <ResponsiveContainer width="100%" height="100%">
              <RechartsBarChart
                data={attributionData}
                margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
                layout="vertical"
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  type="number" 
                  domain={[0, Math.ceil(Math.max(...attributionData.map(d => d.contribution * 100)) * 1.2) / 100]}
                  tickFormatter={(value) => `${(value * 100).toFixed(1)}%`}
                />
                <YAxis dataKey="factor" type="category" width={100} />
                <RechartsTooltip 
                  formatter={(value, name, props) => [
                    `${(value * 100).toFixed(2)}%`,
                    'Contribution to Return'
                  ]}
                />
                <Bar dataKey="contribution" fill="#8884d8">
                  {attributionData.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={factorColors[entry.factor] || '#8884d8'}
                    />
                  ))}
                  <LabelList 
                    dataKey="contribution" 
                    position="right" 
                    formatter={(value) => `${(value * 100).toFixed(2)}%`} 
                  />
                </Bar>
              </RechartsBarChart>
            </ResponsiveContainer>
          </Box>
          
          <Box mt={3}>
            <Typography variant="subtitle2" gutterBottom>Factor Attribution Details</Typography>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Factor</TableCell>
                    <TableCell align="right">Exposure</TableCell>
                    <TableCell align="right">Factor Return</TableCell>
                    <TableCell align="right">Contribution</TableCell>
                    <TableCell align="right">% of Total</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.attribution && Object.entries(data.attribution.factor_contributions).map(([factor, details]) => (
                    <TableRow key={factor}>
                      <TableCell component="th" scope="row">{factor}</TableCell>
                      <TableCell align="right">{details.exposure.toFixed(2)}</TableCell>
                      <TableCell 
                        align="right"
                        sx={{ 
                          color: details.factor_return >= 0 ? 'success.main' : 'error.main'
                        }}
                      >
                        {(details.factor_return * 100).toFixed(2)}%
                      </TableCell>
                      <TableCell 
                        align="right"
                        sx={{ 
                          color: details.contribution >= 0 ? 'success.main' : 'error.main',
                          fontWeight: Math.abs(details.contribution) > 0.02 ? 'bold' : 'normal'
                        }}
                      >
                        {(details.contribution * 100).toFixed(2)}%
                      </TableCell>
                      <TableCell align="right">
                        {((details.contribution / data.attribution.total_return) * 100).toFixed(1)}%
                      </TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell component="th" scope="row">Specific</TableCell>
                    <TableCell align="right">-</TableCell>
                    <TableCell align="right">-</TableCell>
                    <TableCell 
                      align="right"
                      sx={{ 
                        color: data.attribution.specific_return >= 0 ? 'success.main' : 'error.main',
                        fontWeight: 'bold'
                      }}
                    >
                      {(data.attribution.specific_return * 100).toFixed(2)}%
                    </TableCell>
                    <TableCell align="right">
                      {((data.attribution.specific_return / data.attribution.total_return) * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </>
      )}
      
      {/* Factor Analysis Details Tab */}
      {showDetails && activeTab === 2 && (
        <>
          <Typography variant="subtitle1" gutterBottom>Model Insights</Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" gutterBottom>Factor Model Statistics</Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">R-Squared</Typography>
                      <Typography variant="body1">{(data.overall_r_squared * 100).toFixed(1)}%</Typography>
                    </Grid>
                    
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">Adjusted R-Squared</Typography>
                      <Typography variant="body1">{(data.adjusted_r_squared * 100).toFixed(1)}%</Typography>
                    </Grid>
                  </Grid>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <Typography variant="body2" paragraph>
                    The factor model explains <strong>{(data.overall_r_squared * 100).toFixed(1)}%</strong> of portfolio return variation, 
                    which is {
                      data.overall_r_squared > 0.8 ? 'very good' : 
                      data.overall_r_squared > 0.6 ? 'good' : 
                      data.overall_r_squared > 0.4 ? 'moderate' : 'relatively low'
                    }.
                  </Typography>
                  
                  <Typography variant="body2">
                    {data.overall_r_squared < 0.6 ? 
                      'This suggests the portfolio may have significant active bets or exposures to factors not captured in the model.' :
                      'This indicates the major risk factors in the portfolio are well captured by the model.'
                    }
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" gutterBottom>Factor Descriptions</Typography>
                  
                  <Box>
                    <Typography variant="body2" fontWeight="medium">Market</Typography>
                    <Typography variant="body2" paragraph>
                      Measures sensitivity to broad market movements. A value above 1.0 indicates higher volatility than the market.
                    </Typography>
                    
                    <Typography variant="body2" fontWeight="medium">Size</Typography>
                    <Typography variant="body2" paragraph>
                      Measures exposure to small vs. large companies. Positive values indicate tilt toward smaller companies.
                    </Typography>
                    
                    <Typography variant="body2" fontWeight="medium">Value</Typography>
                    <Typography variant="body2" paragraph>
                      Measures exposure to value vs. growth stocks. Positive values indicate tilt toward value stocks.
                    </Typography>
                    
                    <Typography variant="body2" fontWeight="medium">Quality</Typography>
                    <Typography variant="body2">
                      Measures exposure to companies with strong balance sheets and stable earnings. Positive values indicate higher quality.
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="subtitle2" gutterBottom>Statistical Significance</Typography>
                  
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Factor</TableCell>
                          <TableCell align="right">Exposure</TableCell>
                          <TableCell align="right">t-statistic</TableCell>
                          <TableCell align="right">p-value</TableCell>
                          <TableCell align="right">Significant</TableCell>
                          <TableCell>Interpretation</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {factorExposureData.map((row) => (
                          <TableRow key={row.factor}>
                            <TableCell component="th" scope="row">
                              {row.factor}
                            </TableCell>
                            <TableCell 
                              align="right"
                              sx={{ 
                                color: row.exposure > 0 ? 'success.main' : 'error.main',
                                fontWeight: Math.abs(row.exposure) > 0.3 ? 'bold' : 'normal'
                              }}
                            >
                              {row.exposure.toFixed(2)}
                            </TableCell>
                            <TableCell 
                              align="right"
                              sx={{ fontWeight: Math.abs(row.t_statistic) > 2 ? 'bold' : 'normal' }}
                            >
                              {row.t_statistic.toFixed(2)}
                            </TableCell>
                            <TableCell align="right">
                              {row.p_value < 0.001 ? '< 0.001' : row.p_value.toFixed(3)}
                            </TableCell>
                            <TableCell align="right">
                              {row.significant ? 'Yes' : 'No'}
                            </TableCell>
                            <TableCell>
                              {row.significant ? 
                                `Statistically significant ${row.exposure > 0 ? 'positive' : 'negative'} exposure` :
                                'Not statistically significant'
                              }
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                  
                  <Typography variant="body2" color="text.secondary" mt={2}>
                    Factors with absolute t-statistics greater than 2 and p-values less than 0.05 are considered statistically significant.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
};

export default FactorExposure;