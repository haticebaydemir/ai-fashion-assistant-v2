import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Search, Image as ImageIcon, Sparkles, Heart } from 'lucide-react';
import api from '../services/api';

export default function SearchPage() {
  const { user } = useAuth();
  const [searchType, setSearchType] = useState('text');
  const [query, setQuery] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [personalized, setPersonalized] = useState(true);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (searchType === 'text') {
        // ✅ Text search - URLSearchParams kullan
        const params = new URLSearchParams();
        params.append('query', query);
        params.append('k', '20');
        params.append('personalized', personalized);
        
        const response = await api.post('/search/text', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        setResults(response.data.results || []);
        
      } else if (searchType === 'image' && imageFile) {
        // ✅ Image search - FormData
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('k', '20');
        formData.append('personalized', personalized);
        
        const response = await api.post('/search/image', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResults(response.data.results || []);
        
      } else if (searchType === 'multimodal' && query && imageFile) {
        // ✅ Multimodal search - FormData
        const formData = new FormData();
        formData.append('query', query);
        formData.append('image', imageFile);
        formData.append('k', '20');
        formData.append('alpha', '0.7');
        formData.append('personalized', personalized);
        
        const response = await api.post('/search/multimodal', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResults(response.data.results || []);
        
      } else {
        alert('Please provide required inputs');
        setLoading(false);
        return;
      }
    } catch (error) {
      console.error('Search error:', error);
      console.log('Error details:', error.response?.data);
      alert('Search failed: ' + (error.response?.data?.error || error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const addToFavorites = async (productId) => {
    if (!user) {
      alert('Please login to add favorites');
      return;
    }

    try {
      const product = results.find(r => r.product_id === productId);

      await api.post(`/users/${user.user_id}/favorites`, {
        product_id: productId,
        product_name: product.product_name,
        category: product.category,
        color: product.color,
        image_url: product.image_url
      });

      setResults(results.map(r =>
        r.product_id === productId
          ? { ...r, is_favorite: true }
          : r
      ));

      alert('Added to favorites! ❤️');
    } catch (error) {
      console.error('Add to favorites error:', error);
      alert('Failed to add to favorites');
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem', fontSize: '2rem' }}>
        <Search style={{ display: 'inline', marginRight: '0.5rem' }} size={32} />
        Product Search
      </h1>

      {/* Search Type Tabs */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <button
          onClick={() => setSearchType('text')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: searchType === 'text' ? '#646cff' : '#1a1a1a',
            borderRadius: '8px',
            border: 'none',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          <Search size={18} style={{ marginRight: '0.5rem', display: 'inline' }} />
          Text Search
        </button>
        <button
          onClick={() => setSearchType('image')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: searchType === 'image' ? '#646cff' : '#1a1a1a',
            borderRadius: '8px',
            border: 'none',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          <ImageIcon size={18} style={{ marginRight: '0.5rem', display: 'inline' }} />
          Image Search
        </button>
        <button
          onClick={() => setSearchType('multimodal')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: searchType === 'multimodal' ? '#646cff' : '#1a1a1a',
            borderRadius: '8px',
            border: 'none',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          <Sparkles size={18} style={{ marginRight: '0.5rem', display: 'inline' }} />
          Multimodal
        </button>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} style={{ marginBottom: '2rem' }}>
        {(searchType === 'text' || searchType === 'multimodal') && (
          <div style={{ marginBottom: '1rem' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for products (e.g., black dress, running shoes)..."
              style={{ width: '100%', padding: '1rem', fontSize: '1rem' }}
              required={searchType === 'text'}
            />
          </div>
        )}

        {(searchType === 'image' || searchType === 'multimodal') && (
          <div style={{ marginBottom: '1rem' }}>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              style={{ marginBottom: '1rem' }}
              required={searchType === 'image'}
            />
            {imagePreview && (
              <img
                src={imagePreview}
                alt="Preview"
                style={{ maxWidth: '200px', maxHeight: '200px', borderRadius: '8px' }}
              />
            )}
          </div>
        )}

        {user && (
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <input
                type="checkbox"
                checked={personalized}
                onChange={(e) => setPersonalized(e.target.checked)}
              />
              <Sparkles size={16} />
              Use personalization
            </label>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '1rem 2rem',
            backgroundColor: '#646cff',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {/* Results */}
      {results.length > 0 && (
        <div>
          <h2 style={{ marginBottom: '1rem' }}>
            Results ({results.length})
            {personalized && user && <Sparkles size={20} style={{ marginLeft: '0.5rem', display: 'inline', color: '#646cff' }} />}
          </h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
            gap: '1.5rem'
          }}>
            {results.map((result) => (
              <div
                key={result.product_id}
                style={{
                  border: '1px solid #333',
                  borderRadius: '12px',
                  padding: '1rem',
                  backgroundColor: '#1a1a1a',
                  position: 'relative'
                }}
              >
                {result.is_favorite && (
                  <Heart
                    size={20}
                    fill="#ff4444"
                    color="#ff4444"
                    style={{ position: 'absolute', top: '1rem', right: '1rem' }}
                  />
                )}
                {result.image_url ? (
                  <img
                    src={result.image_url}
                    alt={result.product_name}
                    style={{
                      width: '100%',
                      height: '250px',
                      objectFit: 'cover',
                      borderRadius: '8px',
                      marginBottom: '1rem'
                    }}
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/250x250?text=No+Image';
                    }}
                  />
                ) : (
                  <div style={{
                    width: '100%',
                    height: '250px',
                    backgroundColor: '#333',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '1rem'
                  }}>
                    <ImageIcon size={48} color="#666" />
                  </div>
                )}
                <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
                  {result.product_name}
                </h3>
                <p style={{ fontSize: '0.875rem', color: '#999', marginBottom: '0.5rem' }}>
                  {result.category} • {result.gender} • {result.color}
                </p>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.875rem', color: '#646cff' }}>
                    Score: {(result.personalized_score || result.score).toFixed(3)}
                  </span>
                  {user && !result.is_favorite && (
                    <button
                      onClick={() => addToFavorites(result.product_id)}
                      style={{
                        padding: '0.5rem',
                        backgroundColor: 'transparent',
                        border: '1px solid #646cff',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center'
                      }}
                      title="Add to favorites"
                    >
                      <Heart size={16} />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}