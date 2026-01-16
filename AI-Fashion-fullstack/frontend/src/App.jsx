/**
 * App.jsx - Main application with authentication and routing
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import SearchPage from './pages/SearchPage';
import ChatPage from './pages/ChatPage';
import FavoritesPage from './pages/FavoritesPage';
import ProfilePage from './pages/ProfilePage';

// Components
import ProtectedRoute from './components/ProtectedRoute';

// Navigation Component
function Navigation() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav style={{
      background: 'rgba(255,255,255,0.1)',
      backdropFilter: 'blur(10px)',
      padding: '1rem 2rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: '1px solid rgba(255,255,255,0.2)'
    }}>
      <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
        <Link
          to="/"
          style={{
            color: 'white',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '1.2rem'
          }}
        >
          🛍️ AI Fashion
        </Link>
        <Link to="/search" style={{ color: 'white', textDecoration: 'none' }}>
          Search
        </Link>
        <Link to="/chat" style={{ color: 'white', textDecoration: 'none' }}>
          Chat
        </Link>
        {isAuthenticated && (
          <>
            <Link to="/favorites" style={{ color: 'white', textDecoration: 'none' }}>
              Favorites
            </Link>
            <Link to="/profile" style={{ color: 'white', textDecoration: 'none' }}>
              Profile
            </Link>
          </>
        )}
      </div>

      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        {isAuthenticated ? (
          <>
            <span style={{ color: 'white', fontSize: '0.9rem' }}>
              👋 {user?.name}
            </span>
            <button
              onClick={logout}
              style={{
                padding: '0.5rem 1rem',
                background: 'rgba(255,255,255,0.2)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '0.5rem',
                cursor: 'pointer',
                fontSize: '0.9rem'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link
              to="/login"
              style={{
                padding: '0.5rem 1rem',
                background: 'rgba(255,255,255,0.2)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '0.5rem',
                textDecoration: 'none',
                fontSize: '0.9rem'
              }}
            >
              Login
            </Link>
            <Link
              to="/register"
              style={{
                padding: '0.5rem 1rem',
                background: 'white',
                color: '#667eea',
                border: 'none',
                borderRadius: '0.5rem',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: '600'
              }}
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

// Home Component
function Home() {
  const { isAuthenticated, user } = useAuth();

  return (
    <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'white' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
        AI Fashion Assistant
      </h1>
      <p style={{ fontSize: '1.2rem', marginBottom: '2rem' }}>
        {isAuthenticated
          ? `Welcome back, ${user?.name}! 👋`
          : 'v2.5 with Authentication & Personalization'}
      </p>

      <div style={{
        display: 'flex',
        gap: '1rem',
        justifyContent: 'center',
        flexWrap: 'wrap',
        marginBottom: '3rem'
      }}>
        <Feature icon="🔍" title="Text Search" desc="Semantic search with MPNet" />
        <Feature icon="🖼️" title="Image Search" desc="Visual search with CLIP" />
        <Feature icon="🔀" title="Multimodal" desc="Combine text + image" />
        <Feature icon="💬" title="Chat" desc="Conversational AI agent" />
        <Feature icon="🤖" title="RAG" desc="Llama-3.3-70B powered" />
        <Feature
          icon="👤"
          title="Personalization"
          desc={isAuthenticated ? 'Your preferences active' : 'Login to enable'}
          highlight={isAuthenticated}
        />
      </div>

      {!isAuthenticated && (
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          backdropFilter: 'blur(10px)',
          padding: '2rem',
          borderRadius: '1rem',
          maxWidth: '600px',
          margin: '0 auto',
          border: '1px solid rgba(255,255,255,0.2)'
        }}>
          <h3 style={{ marginBottom: '1rem' }}>🎯 Unlock Personalization</h3>
          <p style={{ marginBottom: '1.5rem', fontSize: '0.95rem', lineHeight: '1.6' }}>
            Create an account to get personalized recommendations based on your
            favorites, search history, and style preferences!
          </p>
          <Link
            to="/register"
            style={{
              display: 'inline-block',
              padding: '0.875rem 2rem',
              background: 'white',
              color: '#667eea',
              textDecoration: 'none',
              borderRadius: '0.75rem',
              fontWeight: '600',
              fontSize: '1rem'
            }}
          >
            Get Started →
          </Link>
        </div>
      )}
    </div>
  );
}

// Feature Card Component
function Feature({ icon, title, desc, highlight }) {
  return (
    <div style={{
      background: highlight
        ? 'rgba(255,255,255,0.2)'
        : 'rgba(255,255,255,0.1)',
      backdropFilter: 'blur(10px)',
      padding: '2rem',
      borderRadius: '1rem',
      minWidth: '200px',
      border: highlight
        ? '2px solid rgba(255,255,255,0.4)'
        : '1px solid rgba(255,255,255,0.2)',
      transition: 'transform 0.2s',
      cursor: 'default'
    }}>
      <div style={{ fontSize: '3rem' }}>{icon}</div>
      <h3 style={{ margin: '1rem 0 0.5rem' }}>{title}</h3>
      <p style={{ opacity: 0.8, fontSize: '0.9rem' }}>{desc}</p>
      {highlight && (
        <div style={{
          marginTop: '0.5rem',
          color: '#a8ff78',
          fontSize: '0.85rem',
          fontWeight: '600'
        }}>
          ✓ Active
        </div>
      )}
    </div>
  );
}

// Main App Component
export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div style={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        }}>
          <Navigation />
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Semi-Protected Routes (work better with auth) */}
            <Route path="/search" element={<SearchPage />} />
            <Route path="/chat" element={<ChatPage />} />

            {/* Fully Protected Routes */}
            <Route
              path="/favorites"
              element={
                <ProtectedRoute>
                  <FavoritesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}
