import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Heart, Trash2, Image as ImageIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function FavoritesPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchFavorites();
  }, [user, navigate]);

  const fetchFavorites = async () => {
    try {
      const response = await api.get(`/users/${user.user_id}/favorites`);
      setFavorites(response.data.favorites || []);
    } catch (error) {
      console.error('Fetch favorites error:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeFavorite = async (productId) => {
    if (!window.confirm('Remove from favorites?')) return;

    try {
      await api.delete(`/users/${user.user_id}/favorites/${productId}`);
      setFavorites(favorites.filter(f => f.product_id !== productId));
    } catch (error) {
      console.error('Remove favorite error:', error);
    }
  };

  if (loading) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading...</div>;
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem', fontSize: '2rem' }}>
        <Heart style={{ display: 'inline', marginRight: '0.5rem' }} size={32} fill="#ff4444" color="#ff4444" />
        My Favorites ({favorites.length})
      </h1>

      {favorites.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem', color: '#999' }}>
          <Heart size={64} style={{ marginBottom: '1rem', opacity: 0.3 }} />
          <p>No favorites yet. Start searching and add products you like!</p>
          <button
            onClick={() => navigate('/search')}
            style={{
              marginTop: '1rem',
              padding: '1rem 2rem',
              backgroundColor: '#646cff',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            Go to Search
          </button>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
          gap: '1.5rem'
        }}>
          {favorites.map((fav) => (
            <div
              key={fav.product_id}
              style={{
                border: '1px solid #333',
                borderRadius: '12px',
                padding: '1rem',
                backgroundColor: '#1a1a1a',
                position: 'relative'
              }}
            >
              <Heart
                size={20}
                fill="#ff4444"
                color="#ff4444"
                style={{ position: 'absolute', top: '1rem', left: '1rem', zIndex: 1 }}
              />
              <button
                onClick={() => removeFavorite(fav.product_id)}
                style={{
                  position: 'absolute',
                  top: '1rem',
                  right: '1rem',
                  padding: '0.5rem',
                  backgroundColor: 'rgba(255, 68, 68, 0.2)',
                  border: '1px solid #ff4444',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  zIndex: 1
                }}
              >
                <Trash2 size={16} color="#ff4444" />
              </button>

              {fav.image_url ? (
                <img
                  src={fav.image_url}
                  alt={fav.product_name}
                  style={{
                    width: '100%',
                    height: '250px',
                    objectFit: 'cover',
                    borderRadius: '8px',
                    marginBottom: '1rem'
                  }}
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
              ) : null}
              <div style={{
                width: '100%',
                height: '250px',
                backgroundColor: '#333',
                borderRadius: '8px',
                display: fav.image_url ? 'none' : 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '1rem'
              }}>
                <ImageIcon size={48} color="#666" />
              </div>  

              <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
                {fav.product_name}
              </h3>
              <p style={{ fontSize: '0.875rem', color: '#999', marginBottom: '0.5rem' }}>
                {fav.category} • {fav.color}
              </p>
              <p style={{ fontSize: '0.75rem', color: '#666' }}>
                Added: {new Date(fav.added_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
