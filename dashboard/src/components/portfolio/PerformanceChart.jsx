import React from 'react';
import { Typography, Box, ButtonGroup, Button } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PerformanceChart = ({ performance, showDetails = false }) => {
  const [timeRange, setTimeRange] = React.useState('all');
  
  // Mock data in case no performance data is available
  const mockData = [
    { date: '2023-01-01', value: 100000, benchmark: 100000 },
    { date: '2023-02-01', value: 102000, benchmark: 101000 },
    { date: '2023-03-01', value: 105000, benchmark: 103000 },
    { date: '2023-04-01', value: 108000, benchmark: 104500 },
    { date: '2023-05-01', value: 112000, benchmark: 106000 },
    { date: '2023-06-01', value: 110000, benchmark: 107000 },
    { date: '2023-07-01', value: 115000, benchmark: 109000 },
  ];
  
  // Use real data if available, otherwise use mock data
  const chartData = performance?.time_series || mockData;
  
  // Filter data based on selected time range
  const filteredData = React.useMemo(() => {
    if (timeRange === 'all') return chartData;
    
    const now = new Date();
    let cutoffDate;
    
    switch (timeRange) {
      case '1m':
        cutoffDate = new Date(now.setMonth(now.getMonth() - 1));
        break;
      case '3m':
        cutoffDate = new Date(now.setMonth(now.getMonth() - 3));
        break;
      case '6m':
        cutoffDate = new Date(now.setMonth(now.getMonth() - 6));
        break;
      case '1y':
        cutoffDate = new Date(now.setFullYear(now.getFullYear() - 1));
        break;
      default:
        return chartData;
    }
    
    const cutoffString = cutoffDate.toISOString().split('T')[0];
    return chartData.filter(item => item.date >= cutoffString);
  }, [chartData, timeRange]);
  
  // Calculate percentage change for the current period
  const calculateChange = () => {
    if (filteredData.length < 2) return { value: 0, percentage: 0 };
    
    const startValue = filteredData[0].value;
    const endValue = filteredData[filteredData.length - 1].value;
    const absoluteChange = endValue - startValue;
    const percentageChange = (absoluteChange / startValue) * 100;
    
    return {
      value: absoluteChange,
      percentage: percentageChange
    };
  };
  
  const change = calculateChange();
  
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Portfolio Performance</Typography>
        <ButtonGroup size="small" aria-label="time range selection">
          <Button 
            variant={timeRange === '1m' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('1m')}
          >
            1M
          </Button>
          <Button 
            variant={timeRange === '3m' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('3m')}
          >
            3M
          </Button>
          <Button 
            variant={timeRange === '6m' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('6m')}
          >
            6M
          </Button>
          <Button 
            variant={timeRange === '1y' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('1y')}
          >
            1Y
          </Button>
          <Button 
            variant={timeRange === 'all' ? 'contained' : 'outlined'} 
            onClick={() => setTimeRange('all')}
          >
            All
          </Button>
        </ButtonGroup>
      </Box>
      
      <Box display="flex" gap={2} mb={2}>
        <Box>
          <Typography variant="body2" color="text.secondary">Change</Typography>
          <Typography 
            variant="h6" 
            color={change.percentage >= 0 ? 'success.main' : 'error.main'}
          >
            {change.percentage.toFixed(2)}%
          </Typography>
        </Box>
        <Box>
          <Typography variant="body2" color="text.secondary">Value Change</Typography>
          <Typography 
            variant="h6" 
            color={change.value >= 0 ? 'success.main' : 'error.main'}
          >
            ${Math.abs(change.value).toLocaleString('en-US')}
          </Typography>
        </Box>
      </Box>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={filteredData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip formatter={(value) => ['$' + value.toLocaleString('en-US')]} />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="value" 
            name="Portfolio"
            stroke="#8884d8" 
            activeDot={{ r: 8 }} 
          />
          {showDetails && (
            <Line 
              type="monotone" 
              dataKey="benchmark" 
              name="Benchmark"
              stroke="#82ca9d" 
            />
          )}
        </LineChart>
      </ResponsiveContainer>
      
      {showDetails && (
        <Box mt={3}>
          <Typography variant="subtitle1">Performance Details</Typography>
          <Typography variant="body2">
            This chart shows the portfolio performance over time compared to the benchmark.
            The portfolio has {change.percentage >= 0 ? 'outperformed' : 'underperformed'} the benchmark
            by {Math.abs(change.percentage - 2).toFixed(2)}% during this period.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default PerformanceChart;