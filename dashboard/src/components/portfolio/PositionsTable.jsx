import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Paper,
  Typography,
  TextField,
  InputAdornment,
  Box,
  Chip
} from '@mui/material';
import { Search, TrendingUp, TrendingDown } from '@mui/icons-material';

const PositionsTable = ({ positions = [] }) => {
  const [orderBy, setOrderBy] = useState('market_value');
  const [order, setOrder] = useState('desc');
  const [search, setSearch] = useState('');
  
  // Handle sorting
  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };
  
  // Handle search
  const handleSearch = (event) => {
    setSearch(event.target.value);
  };
  
  // Filter positions based on search
  const filteredPositions = positions.filter(position => 
    position.symbol.toLowerCase().includes(search.toLowerCase())
  );
  
  // Sort positions
  const sortedPositions = React.useMemo(() => {
    if (!filteredPositions.length) return [];
    
    return [...filteredPositions].sort((a, b) => {
      if (orderBy === 'gain_loss_pct') {
        const aGain = ((a.current_price / a.entry_price) - 1) * 100;
        const bGain = ((b.current_price / b.entry_price) - 1) * 100;
        return order === 'asc' ? aGain - bGain : bGain - aGain;
      }
      
      const aValue = a[orderBy] || 0;
      const bValue = b[orderBy] || 0;
      
      return order === 'asc' ? aValue - bValue : bValue - aValue;
    });
  }, [filteredPositions, order, orderBy]);
  
  // Calculate totals
  const totalValue = React.useMemo(() => 
    positions.reduce((sum, position) => sum + (position.market_value || 0), 0),
    [positions]
  );
  
  if (!positions || positions.length === 0) {
    return (
      <Box>
        <Typography variant="h6" gutterBottom>Positions</Typography>
        <Typography>No positions found in this portfolio.</Typography>
      </Box>
    );
  }
  
  // Calculate gain/loss for a position
  const calculateGainLoss = (position) => {
    if (!position.entry_price || !position.current_price) return { amount: 0, percentage: 0 };
    
    const amount = (position.current_price - position.entry_price) * position.quantity;
    const percentage = ((position.current_price / position.entry_price) - 1) * 100;
    
    return { amount, percentage };
  };
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Positions</Typography>
        <TextField
          size="small"
          variant="outlined"
          placeholder="Search by symbol..."
          value={search}
          onChange={handleSearch}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Box>
      
      <TableContainer component={Paper} sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="positions table" size="small">
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={orderBy === 'symbol'}
                  direction={orderBy === 'symbol' ? order : 'asc'}
                  onClick={() => handleRequestSort('symbol')}
                >
                  Symbol
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'quantity'}
                  direction={orderBy === 'quantity' ? order : 'asc'}
                  onClick={() => handleRequestSort('quantity')}
                >
                  Quantity
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'entry_price'}
                  direction={orderBy === 'entry_price' ? order : 'asc'}
                  onClick={() => handleRequestSort('entry_price')}
                >
                  Entry Price
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'current_price'}
                  direction={orderBy === 'current_price' ? order : 'asc'}
                  onClick={() => handleRequestSort('current_price')}
                >
                  Current Price
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'market_value'}
                  direction={orderBy === 'market_value' ? order : 'asc'}
                  onClick={() => handleRequestSort('market_value')}
                >
                  Market Value
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">
                <TableSortLabel
                  active={orderBy === 'gain_loss_pct'}
                  direction={orderBy === 'gain_loss_pct' ? order : 'asc'}
                  onClick={() => handleRequestSort('gain_loss_pct')}
                >
                  Gain/Loss
                </TableSortLabel>
              </TableCell>
              <TableCell align="right">% of Portfolio</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedPositions.map((position) => {
              const gainLoss = calculateGainLoss(position);
              const portfolioPercentage = ((position.market_value || 0) / totalValue) * 100;
              
              return (
                <TableRow key={position.id || position.symbol}>
                  <TableCell component="th" scope="row">
                    {position.symbol}
                  </TableCell>
                  <TableCell align="right">{position.quantity}</TableCell>
                  <TableCell align="right">
                    ${position.entry_price?.toFixed(2) || 'N/A'}
                  </TableCell>
                  <TableCell align="right">
                    ${position.current_price?.toFixed(2) || 'N/A'}
                  </TableCell>
                  <TableCell align="right">
                    ${position.market_value?.toLocaleString('en-US') || 'N/A'}
                  </TableCell>
                  <TableCell align="right">
                    <Box display="flex" alignItems="center" justifyContent="flex-end">
                      {gainLoss.percentage >= 0 ? 
                        <TrendingUp fontSize="small" color="success" sx={{ mr: 0.5 }} /> : 
                        <TrendingDown fontSize="small" color="error" sx={{ mr: 0.5 }} />
                      }
                      <Typography
                        variant="body2"
                        color={gainLoss.percentage >= 0 ? 'success.main' : 'error.main'}
                      >
                        {gainLoss.percentage.toFixed(2)}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell align="right">
                    <Chip 
                      label={`${portfolioPercentage.toFixed(1)}%`} 
                      size="small"
                      color={
                        portfolioPercentage > 10 ? "error" : 
                        portfolioPercentage > 5 ? "warning" : "default"
                      }
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      
      <Box mt={2} display="flex" justifyContent="flex-end">
        <Typography variant="subtitle2">
          Total Portfolio Value: ${totalValue.toLocaleString('en-US')}
        </Typography>
      </Box>
    </Box>
  );
};

export default PositionsTable;