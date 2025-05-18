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

const API_URL = process.env.REACT_APP_API_URL || '';

// Helper function for making authenticated API requests
const fetchWithAuth = async (url, options = {}) => {
  // Set default headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Include credentials for session-based authentication
  const config = {
    ...options,
    headers,
    credentials: 'include',
  };

  const response = await fetch(`${API_URL}${url}`, config);

  // Handle 401 Unauthorized - redirect to login
  if (response.status === 401) {
    window.location.href = '/auth/login/';
    return null;
  }

  // For non-204 (No Content) responses, parse JSON
  if (response.status !== 204) {
    return await response.json();
  }

  return null;
};

// Authentication API
export const authAPI = {
  login: async (username, password) => {
    const response = await fetch(`${API_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include',
    });
    return response.ok;
  },

  register: async (username, password1, password2) => {
    const response = await fetch(`${API_URL}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password1, password2 }),
    });
    return response.ok;
  },

  logout: async () => {
    await fetch(`${API_URL}/auth/logout/`, {
      method: 'POST',
      credentials: 'include',
    });
    window.location.href = '/';
  },

  getProfile: async () => {
    return await fetchWithAuth('/api/profile/');
  },

  updateProfile: async (userData) => {
    return await fetchWithAuth('/api/profile/update/', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  },
};

// Transactions API
export const transactionsAPI = {
  getAll: async () => {
    return await fetchWithAuth('/api/transactions/');
  },

  getById: async (id) => {
    return await fetchWithAuth(`/api/transactions/${id}/`);
  },

  create: async (transaction) => {
    return await fetchWithAuth('/api/transactions/', {
      method: 'POST',
      body: JSON.stringify(transaction),
    });
  },

  update: async (id, transaction) => {
    return await fetchWithAuth(`/api/transactions/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(transaction),
    });
  },

  delete: async (id) => {
    return await fetchWithAuth(`/api/transactions/${id}/`, {
      method: 'DELETE',
    });
  },

  uploadCSV: async (formData) => {
    return await fetch(`${API_URL}/api/upload-csv/`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    }).then(response => response.json());
  },
};

// Categories API
export const categoriesAPI = {
  getAll: async () => {
    return await fetchWithAuth('/api/categories/');
  },

  getById: async (id) => {
    return await fetchWithAuth(`/api/categories/${id}/`);
  },

  create: async (category) => {
    return await fetchWithAuth('/api/categories/', {
      method: 'POST',
      body: JSON.stringify(category),
    });
  },

  update: async (id, category) => {
    return await fetchWithAuth(`/api/categories/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(category),
    });
  },

  delete: async (id) => {
    return await fetchWithAuth(`/api/categories/${id}/`, {
      method: 'DELETE',
    });
  },
};

// Analysis API
export const analysisAPI = {
  getSummary: async (startDate, endDate) => {
    let url = '/api/summary/';
    if (startDate || endDate) {
      url += '?';
      if (startDate) url += `start_date=${startDate}&`;
      if (endDate) url += `end_date=${endDate}`;
    }
    return await fetchWithAuth(url);
  },

  getMonthlySpending: async (year) => {
    const url = year ? `/api/monthly/?year=${year}` : '/api/monthly/';
    return await fetchWithAuth(url);
  },
};

export default {
  auth: authAPI,
  categories: categoryService,
  expenses: expenseService,
  transactions: transactionsAPI,
  categories: categoriesAPI,
  analysis: analysisAPI,
};