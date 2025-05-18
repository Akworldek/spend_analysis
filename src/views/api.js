// api.js - API service for connecting React frontend to Django backend

import axios from 'axios';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token in requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Authentication services
export const authService = {
  login: async (username, password) => {
    const response = await apiClient.post('auth/login/', { username, password });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (username, password, email) => {
    const response = await apiClient.post('auth/register/', { username, password, email });
    if (response.data.token) {
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: async () => {
    await apiClient.post('auth/logout/');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

// Category services
export const categoryService = {
  getAll: async () => {
    const response = await apiClient.get('categories/');
    return response.data;
  },

  create: async (name) => {
    const response = await apiClient.post('categories/', { name });
    return response.data;
  },

  update: async (id, name) => {
    const response = await apiClient.put(`categories/${id}/`, { name });
    return response.data;
  },

  delete: async (id) => {
    await apiClient.delete(`categories/${id}/`);
  }
};

// Expense services
export const expenseService = {
  getAll: async (filters = {}) => {
    // Build query string from filters
    let queryParams = new URLSearchParams();

    if (filters.startDate) {
      queryParams.append('start_date', filters.startDate);
    }

    if (filters.endDate) {
      queryParams.append('end_date', filters.endDate);
    }

    if (filters.category && filters.category !== 'all') {
      queryParams.append('category', filters.category);
    }

    if (filters.search) {
      queryParams.append('search', filters.search);
    }

    const queryString = queryParams.toString();
    const url = queryString ? `expenses/?${queryString}` : 'expenses/';

    const response = await apiClient.get(url);
    return response.data;
  },

  getById: async (id) => {
    const response = await apiClient.get(`expenses/${id}/`);
    return response.data;
  },

  create: async (expense) => {
    const response = await apiClient.post('expenses/', expense);
    return response.data;
  },

  update: async (id, expense) => {
    const response = await apiClient.put(`expenses/${id}/`, expense);
    return response.data;
  },

  delete: async (id) => {
    await apiClient.delete(`expenses/${id}/`);
  },

  getSummary: async (filters = {}) => {
    // Build query string from filters
    let queryParams = new URLSearchParams();

    if (filters.startDate) {
      queryParams.append('start_date', filters.startDate);
    }

    if (filters.endDate) {
      queryParams.append('end_date', filters.endDate);
    }

    if (filters.category && filters.category !== 'all') {
      queryParams.append('category', filters.category);
    }

    if (filters.search) {
      queryParams.append('search', filters.search);
    }

    const queryString = queryParams.toString();
    const url = queryString ? `expenses/summary/?${queryString}` : 'expenses/summary/';

    const response = await apiClient.get(url);
    return response.data;
  },

  getMonthlyData: async () => {
    const response = await apiClient.get('expenses/monthly_summary/');
    return response.data;
  }
};

export default {
  auth: authService,
  categories: categoryService,
  expenses: expenseService
};