import React from 'react';
import { Typography, Box, Divider, Grid, Chip } from '@mui/material';
import { CalendarToday, AccountBalance, TrendingUp, Assessment } from '@mui/icons-material';

const PortfolioSummary = ({ portfolio, performance }) => {
  if (!portfolio) return <Typography>No portfolio data available</Typography>;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Portfolio Summary</Typography>
      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Box display="flex" alignItems="center" mb={1}>
            <CalendarToday fontSize="small" sx={{ mr: 1 }} />
            <Typography variant="body2" color="text.secondary">Inception Date</Typography>
          </Box>
          <Typography variant="body1">{portfolio.inception_date}</Typography>
        </Grid>

        <Grid item xs={6}>
          <Box display="flex" alignItems="center" mb={1}>
            <AccountBalance fontSize="small" sx={{ mr: 1 }} />
            <Typography variant="body2" color="text.secondary">Currency</Typography>
          </Box>
          <Typography variant="body1">{portfolio.currency}</Typography>
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      {performance ? (
        <>
          <Typography variant="subtitle1" gutterBottom>Performance Metrics</Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Box display="flex" alignItems="center" mb={1}>
                <TrendingUp fontSize="small" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">Total Return</Typography>
              </Box>
              <Typography variant="body1" color={performance.total_return >= 0 ? 'success.main' : 'error.main'}>
                {(performance.total_return * 100).toFixed(2)}%
              </Typography>
            </Grid>

            <Grid item xs={6}>
              <Box display="flex" alignItems="center" mb={1}>
                <Assessment fontSize="small" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">Sharpe Ratio</Typography>
              </Box>
              <Typography variant="body1">
                {performance.sharpe_ratio?.toFixed(2) || 'N/A'}
              </Typography>
            </Grid>

            {performance.annualized_return !== undefined && (
              <Grid item xs={6}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">Annualized Return</Typography>
                </Box>
                <Typography variant="body1" color={performance.annualized_return >= 0 ? 'success.main' : 'error.main'}>
                  {(performance.annualized_return * 100).toFixed(2)}%
                </Typography>
              </Grid>
            )}

            {performance.max_drawdown !== undefined && (
              <Grid item xs={6}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Typography variant="body2" color="text.secondary">Max Drawdown</Typography>
                </Box>
                <Typography variant="body1" color="error.main">
                  {(performance.max_drawdown * 100).toFixed(2)}%
                </Typography>
              </Grid>
            )}
          </Grid>
        </>
      ) : (
        <Typography color="text.secondary">Performance data not available</Typography>
      )}

      <Divider sx={{ my: 2 }} />

      <Box>
        <Typography variant="subtitle1" gutterBottom>Portfolio Statistics</Typography>
        <Box display="flex" flexWrap="wrap" gap={1}>
          <Chip 
            label={`${portfolio.positions?.length || 0} Positions`} 
            size="small" 
            color="primary" 
            variant="outlined" 
          />
          <Chip 
            label="Last Updated: Today" 
            size="small" 
            color="default" 
            variant="outlined" 
          />
        </Box>
      </Box>
    </Box>
  );
};

export default PortfolioSummary;