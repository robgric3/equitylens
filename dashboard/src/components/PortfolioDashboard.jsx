// dashboard/src/components/PortfolioDashboard.jsx
import React, { useState, useEffect } from 'react';
import { Box, Grid, Typography, Paper, CircularProgress, Tab, Tabs } from '@mui/material';
import { useParams } from 'react-router-dom';
import { portfolioAPI, riskAPI } from '../services/api';
import PortfolioSummary from './portfolio/PortfolioSummary';
import PerformanceChart from './portfolio/PerformanceChart';
import PositionsTable from './portfolio/PositionsTable';
import RiskMetrics from './risk/RiskMetrics';
import FactorExposure from './factors/FactorExposure';
import { mockPortfolio, mockPerformance, mockRiskMetrics, mockFactorExposures } from '../mockData';


const PortfolioDashboard = () => {
  const { portfolioId } = useParams();
  const [portfolio, setPortfolio] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [positions, setPositions] = useState([]);
  const [riskMetrics, setRiskMetrics] = useState(null);
  const [factorExposures, setFactorExposures] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  // Then modify your useEffect to use mock data
useEffect(() => {
  const fetchPortfolioData = async () => {
    try {
      setLoading(true);
      
      // For development, use mock data
      const useMockData = true; // Toggle this when ready to test real API

      if (useMockData) {
        // Use mock data
        setPortfolio(mockPortfolio);
        setPositions(mockPortfolio.positions);
        setPerformance(mockPerformance);
        setRiskMetrics(mockRiskMetrics);
        setFactorExposures(mockFactorExposures);
        setLoading(false);
        return;
      }
      
      // Real API calls when ready
      const portfolioResponse = await portfolioAPI.getPortfolio(portfolioId);
      setPortfolio(portfolioResponse.data);
      
      if (portfolioResponse.data.positions) {
        setPositions(portfolioResponse.data.positions);
      }
      
      const performanceResponse = await portfolioAPI.getPortfolioPerformance(portfolioId);
      setPerformance(performanceResponse.data);
      
      const riskResponse = await riskAPI.getPortfolioRisk(portfolioId);
      setRiskMetrics(riskResponse.data);
      
      const factorResponse = await portfolioAPI.getFactorExposures(portfolioId);
      setFactorExposures(factorResponse.data);
      
      setLoading(false);
    } catch (err) {
      console.error('Error fetching portfolio data:', err);
      setError('Failed to load portfolio data. Please try again later.');
      setLoading(false);
    }
  };

  if (portfolioId) {
    fetchPortfolioData();
  }
}, [portfolioId]);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography color="error" variant="h6">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, padding: 3 }}>
      {portfolio && (
        <>
          <Typography variant="h4" gutterBottom>
            {portfolio.name}
          </Typography>
          
          <Typography variant="subtitle1" color="text.secondary" gutterBottom>
            {portfolio.description}
          </Typography>
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs value={activeTab} onChange={handleTabChange} aria-label="portfolio dashboard tabs">
              <Tab label="Overview" />
              <Tab label="Performance" />
              <Tab label="Positions" />
              <Tab label="Risk" />
              <Tab label="Factor Analysis" />
            </Tabs>
          </Box>
          
          {/* Overview Tab */}
          {activeTab === 0 && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 2, height: '100%' }}>
                  <PortfolioSummary portfolio={portfolio} performance={performance} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={8}>
                <Paper sx={{ p: 2 }}>
                  <PerformanceChart performance={performance} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                  <RiskMetrics riskMetrics={riskMetrics} />
                </Paper>
              </Grid>
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                  <FactorExposure factorExposures={factorExposures} />
                </Paper>
              </Grid>
            </Grid>
          )}
          
          {/* Performance Tab */}
          {activeTab === 1 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>Performance Analysis</Typography>
                  <PerformanceChart performance={performance} showDetails={true} />
                </Paper>
              </Grid>
              {/* Additional performance metrics components */}
            </Grid>
          )}
          
          {/* Positions Tab */}
          {activeTab === 2 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <PositionsTable positions={positions} />
                </Paper>
              </Grid>
            </Grid>
          )}
          
          {/* Risk Tab */}
          {activeTab === 3 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>Risk Analysis</Typography>
                  <RiskMetrics riskMetrics={riskMetrics} showDetails={true} />
                </Paper>
              </Grid>
              {/* Stress test results and other risk components */}
            </Grid>
          )}
          
          {/* Factor Analysis Tab */}
          {activeTab === 4 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="h6" gutterBottom>Factor Analysis</Typography>
                  <FactorExposure factorExposures={factorExposures} showDetails={true} />
                </Paper>
              </Grid>
              {/* Factor attribution and other components */}
            </Grid>
          )}
        </>
      )}
    </Box>
  );
};

export default PortfolioDashboard;