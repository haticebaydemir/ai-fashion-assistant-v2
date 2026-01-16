/**
 * ProtectedRoute - Wrapper for authenticated-only routes
 */

import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    // Show loading spinner while checking authentication
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{
          color: 'white',
          fontSize: '1.5rem',
          textAlign: 'center'
        }}>
          <div style={{ marginBottom: '1rem' }}>🔐</div>
          <div>Loading...</div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to login, but save the attempted location
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
