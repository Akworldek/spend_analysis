
// src/config/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const API_ENDPOINTS = {
  TRANSACTIONS: `${API_BASE_URL}/transactions/`,
  CATEGORIES: `${API_BASE_URL}/categories/`,
  ANALYTICS: `${API_BASE_URL}/analytics/`,
};

export default API_BASE_URL;