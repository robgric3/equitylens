import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { 
  CssBaseline, 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Container, 
  Button,
  Paper
} from '@mui/material';
import PortfolioDashboard from './components/PortfolioDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
                EquityLens
              </Link>
            </Typography>
            <Button color="inherit" component={Link} to="/portfolio/1">
              Sample Portfolio
            </Button>
          </Toolbar>
        </AppBar>
        
        <Container component="main" sx={{ flexGrow: 1, paddingY: 3 }}>
          <Routes>
            <Route path="/portfolio/:portfolioId" element={<PortfolioDashboard />} />
            <Route path="/" element={<HomePage />} />
          </Routes>
        </Container>
        
        <Box component="footer" sx={{ py: 2, bgcolor: 'background.paper' }}>
          <Container maxWidth="lg">
            <Typography variant="body2" color="text.secondary" align="center">
              EquityLens © {new Date().getFullYear()} - Equity Portfolio Analytics & Risk Platform
            </Typography>
          </Container>
        </Box>
      </Box>
    </Router>
  );
}

function HomePage() {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '70vh'
    }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 4, 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center',
          maxWidth: 800,
          mx: 'auto'
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Welcome to EquityLens
        </Typography>
        
        <Typography variant="h6" color="text.secondary" align="center" paragraph>
          A professional-grade portfolio analytics and risk management system focused 
          exclusively on equity markets.
        </Typography>
        
        <Typography variant="body1" paragraph align="center">
          EquityLens combines modern portfolio theory with factor-based analysis 
          to provide institutional-quality insights at a fraction of the cost.
        </Typography>
        
        <Box sx={{ mt: 4 }}>
          <Button 
            variant="contained" 
            color="primary" 
            size="large" 
            component={Link} 
            to="/portfolio/1"
          >
            View Sample Portfolio
          </Button>
        </Box>
        
        <Box sx={{ mt: 6, width: '100%' }}>
          <Typography variant="h6" gutterBottom>Key Features:</Typography>
          <ul>
            <li>Portfolio construction and optimization</li>
            <li>Performance attribution analysis</li>
            <li>Multi-factor risk modeling</li>
            <li>Stress testing and scenario analysis</li>
            <li>Factor exposure visualization</li>
          </ul>
        </Box>
      </Paper>
    </Box>
  );
}

export default App;