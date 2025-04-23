// dashboard/src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Portfolio API calls
export const portfolioAPI = {
  getPortfolios: () => axiosInstance.get('/portfolios'),
  getPortfolio: (id) => axiosInstance.get(`/portfolios/${id}`),
  createPortfolio: (data) => axiosInstance.post('/portfolios', data),
  updatePortfolio: (id, data) => axiosInstance.put(`/portfolios/${id}`, data),
  deletePortfolio: (id) => axiosInstance.delete(`/portfolios/${id}`),
};

// Stock API calls
export const stockAPI = {
  getStocks: (params) => axiosInstance.get('/stocks', { params }),
  getStockHistory: (symbol, params) => 
    axiosInstance.get(`/stocks/${symbol}/history`, { params }),
};

// Risk analysis API calls
export const riskAPI = {
  getPortfolioRisk: (portfolioId) => 
    axiosInstance.get(`/risk/portfolio/${portfolioId}`),
  runStressTest: (portfolioId, scenario) => 
    axiosInstance.post(`/risk/stress-test/${portfolioId}`, { scenario }),
};

// Authentication API calls
export const authAPI = {
  login: (credentials) => axiosInstance.post('/users/login', credentials),
  register: (userData) => axiosInstance.post('/users/register', userData),
  getProfile: () => axiosInstance.get('/users/me'),
};

export default {
  portfolio: portfolioAPI,
  stock: stockAPI,
  risk: riskAPI,
  auth: authAPI,
};