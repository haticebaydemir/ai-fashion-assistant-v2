import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { buildImageUrl } from '../utils/imageUrl';
import FavoriteButton from '../components/FavoriteButton';

export default function ChatPage() {
  const { isAuthenticated, user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId] = useState('user-' + Date.now());
  const [usePersonalization, setUsePersonalization] = useState(true);
  const [favoriteIds, setFavoriteIds] = useState(new Set()); // ✅ YENİ

  // ✅ Favorileri yükle
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchFavorites();
    }
  }, [isAuthenticated, user]);

  const fetchFavorites = async () => {
    try {
      const response = await api.get(`/users/${user.user_id}/favorites`);
      const favorites = response.data.favorites || [];
      const ids = new Set(favorites.map(f => f.product_id));
      setFavoriteIds(ids);
      
      // Update existing messages with favorite status
      setMessages(prevMessages => prevMessages.map(msg => ({
        ...msg,
        products: msg.products?.map(p => ({
          ...p,
          is_favorite: ids.has(p.product_id)
        }))
      })));
    } catch (error) {
      console.error('Fetch favorites error:', error);
    }
  };

  const addToFavorites = async (productId) => {
    if (!isAuthenticated) {
      alert('Please login to add favorites');
      return;
    }

    try {
      // Find product in current messages
      let product = null;
      for (const msg of messages) {
        if (msg.products) {
          product = msg.products.find(p => p.product_id === productId);
          if (product) break;
        }
      }

      if (!product) return;

      await api.post(`/users/${user.user_id}/favorites`, {
        product_id: productId,
        product_name: product.product_name,
        category: product.category || 'Unknown',
        color: product.color || 'Unknown',
        image_url: product.image_url
      });

      // Update favorite IDs
      setFavoriteIds(prev => new Set([...prev, productId]));

      // Update local state
      setMessages(messages.map(msg => ({
        ...msg,
        products: msg.products?.map(p =>
          p.product_id === productId
            ? { ...p, is_favorite: true }
            : p
        )
      })));

      alert('Added to favorites! ❤️');
    } catch (error) {
      console.error('Add to favorites error:', error);
      alert('Failed to add to favorites');
    }
  };

  // ✅ YENİ: Favoriden çıkar
  const removeFromFavorites = async (productId) => {
    if (!isAuthenticated) return;

    if (!window.confirm('Remove from favorites?')) return;

    try {
      await api.delete(`/users/${user.user_id}/favorites/${productId}`);

      // Update favorite IDs
      setFavoriteIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(productId);
        return newSet;
      });

      // Update local state
      setMessages(messages.map(msg => ({
        ...msg,
        products: msg.products?.map(p =>
          p.product_id === productId
            ? { ...p, is_favorite: false }
            : p
        )
      })));

      alert('Removed from favorites');
    } catch (error) {
      console.error('Remove from favorites error:', error);
      alert('Failed to remove from favorites');
    }
  };

  // ✅ YENİ: Toggle favorite (add veya remove)
  const toggleFavorite = async (productId) => {
    if (favoriteIds.has(productId)) {
      await removeFromFavorites(productId);
    } else {
      await addToFavorites(productId);
    }
  };

  const send = async () => {
    if (!input.trim()) return;

    setMessages([...messages, { role: 'user', content: input }]);
    const msg = input;
    setInput('');

    try {
      const res = await api.post('/chat/message', {
        session_id: sessionId,
        message: msg,
        include_search: true,
        use_personalization: isAuthenticated && usePersonalization
      });

      // ✅ Gelen ürünlere favorite durumunu ekle
      const productsWithFavorites = res.data.products?.map(p => ({
        ...p,
        is_favorite: favoriteIds.has(p.product_id)
      }));

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: res.data.response,
          products: productsWithFavorites,
          personalized: res.data.personalized
        }
      ]);
    } catch (e) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${e.response?.data?.detail || e.message}`
        }
      ]);
    }
  };

  return (
    <div style={{
      maxWidth: '900px',
      margin: '0 auto',
      padding: '2rem',
      height: 'calc(100vh - 100px)',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* Header with personalization toggle */}
      <div style={{
        background: 'rgba(255,255,255,0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '1rem',
        padding: '1rem 2rem',
        marginBottom: '1rem',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h2 style={{ margin: 0, color:"#535d8e" }}>Chat with AI</h2>

        {isAuthenticated && (
          <label style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            cursor: 'pointer',
            fontSize: '0.9rem'
          }}>
            <input
              type="checkbox"
              checked={usePersonalization}
              onChange={(e) => setUsePersonalization(e.target.checked)}
              style={{ cursor: 'pointer' }}
            />
            <span style={{color:"#535d8e"}}>✨ Personalized Results</span>
          </label>
        )}
      </div>

      {/* Messages */}
      <div style={{
        background: 'rgba(255,255,255,0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '1rem',
        padding: '2rem',
        flex: 1,
        overflowY: 'auto',
        marginBottom: '1rem',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)'
      }}>
        {!isAuthenticated && (
          <div style={{
            background: '#e3f2fd',
            padding: '1rem',
            borderRadius: '0.75rem',
            marginBottom: '1rem',
            fontSize: '0.9rem',
            border: '1px solid #90caf9'
          }}>
            💡 <strong>Tip:</strong> Login to get personalized recommendations
            based on your favorites and preferences!
          </div>
        )}

        {messages.length === 0 && (
          <div style={{
            textAlign: 'center',
            color: '#999',
            padding: '3rem 0',
            fontSize: '0.95rem'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💬</div>
            <p>Start a conversation! Ask me anything about fashion products.</p>
            {isAuthenticated && (
              <p style={{ marginTop: '0.5rem', color: '#667eea' }}>
                ✨ Personalization is active
              </p>
            )}
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              marginBottom: '1rem',
              padding: '1rem',
              background: m.role === 'user' ? '#667eea' : '#f5f5f5',
              color: m.role === 'user' ? 'white' : 'black',
              borderRadius: '1rem',
              maxWidth: '80%',
              marginLeft: m.role === 'user' ? 'auto' : '0'
            }}
          >
            <p>{m.content}</p>

            {m.personalized && (
              <div style={{
                fontSize: '0.75rem',
                marginTop: '0.5rem',
                padding: '0.25rem 0.5rem',
                background: 'rgba(168, 255, 120, 0.2)',
                borderRadius: '0.25rem',
                display: 'inline-block',
                color: m.role === 'user' ? 'white' : '#2e7d32'
              }}>
                ✨ Personalized for you
              </div>
            )}

            {m.products && (
              <div style={{
                marginTop: '1rem',
                display: 'flex',
                gap: '0.75rem',
                flexWrap: 'wrap'
              }}>
                {m.products.map(p => (
                  <div
                    key={p.product_id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '0.5rem',
                      background: 'rgba(255,255,255,0.2)',
                      borderRadius: '0.5rem',
                      fontSize: '0.8rem',
                      position: 'relative'
                    }}
                  >
                    {p.is_favorite && (
                      <div style={{
                        position: 'absolute',
                        top: '-6px',
                        right: '-6px',
                        background: '#ff4444',
                        color: 'white',
                        fontSize: '0.7rem',
                        padding: '2px 6px',
                        borderRadius: '10px',
                        fontWeight: 'bold'
                      }}>
                        ★
                      </div>
                    )}

                    <div style={{
                      width: 64,
                      height: 64,
                      flex: '0 0 64px',
                      borderRadius: '0.5rem',
                      overflow: 'hidden',
                      background: '#f6f6f6',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      {p.image_url ? (
                        <img
                          src={buildImageUrl(p.image_url)}
                          alt={p.product_name}
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover'
                          }}
                          onError={(e) => {
                            e.currentTarget.onerror = null;
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      ) : (
                        <div style={{ color: '#999', fontSize: '0.75rem' }}>
                          No image
                        </div>
                      )}
                    </div>

                    <div>
                      <div style={{ fontWeight: 600 }}>{p.product_name}</div>
                      <div style={{ fontSize: '0.75rem', color: '#666' }}>
                        Score: {p.personalized_score?.toFixed(3) || p.score?.toFixed(3) || 'N/A'}
                      </div>
                      {p.matches_color_pref && (
                        <div style={{
                          fontSize: '0.7rem',
                          color: '#2e7d32',
                          marginTop: '2px'
                        }}>
                          ✓ Matches your color
                        </div>
                      )}
                    </div>

                    <div style={{ marginLeft: 'auto' }}>
                      <FavoriteButton
                        productId={p.product_id}
                        isFavorite={p.is_favorite || false}
                        onToggle={toggleFavorite}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: '1rem' }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && send()}
          placeholder="Ask me anything..."
          style={{
            flex: 1,
            padding: '1rem',
            border: 'none',
            borderRadius: '1rem',
            fontSize: '1rem',
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
          }}
        />
        <button
          onClick={send}
          style={{
            padding: '1rem 2rem',
            background: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '1rem',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: 'bold',
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}