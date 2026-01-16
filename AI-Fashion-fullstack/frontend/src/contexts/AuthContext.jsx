/**
 * Authentication Context - Global user state management
 * Manages user authentication state, login, logout, and token refresh
 */

import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load user from token on mount
  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await api.get('/auth/me');
          setUser(response.data);
        } catch (err) {
          console.error('Failed to load user:', err);
          // Token might be expired
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await api.post('/auth/login', { email, password });
      const { access_token, refresh_token } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      // Set auth header for future requests
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Fetch user info
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);

      return { success: true };
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const register = async (name, email, password) => {
    try {
      setError(null);
      const response = await api.post('/auth/register', { name, email, password });
      const { access_token, refresh_token } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      // Set auth header
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Fetch user info
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);

      return { success: true };
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Registration failed';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      // Clear tokens and user state
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete api.defaults.headers.common['Authorization'];
      setUser(null);
    }
  };

  const refreshToken = async () => {
    try {
      const refresh_token = localStorage.getItem('refresh_token');
      if (!refresh_token) {
        throw new Error('No refresh token');
      }

      const response = await api.post('/auth/refresh', { refresh_token });
      const { access_token, refresh_token: new_refresh_token } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', new_refresh_token);

      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      return true;
    } catch (err) {
      console.error('Token refresh failed:', err);
      await logout();
      return false;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    refreshToken,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export default AuthContext;
