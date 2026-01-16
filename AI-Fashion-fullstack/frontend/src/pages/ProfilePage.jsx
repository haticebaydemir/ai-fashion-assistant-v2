import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { User, Save, Mail } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function ProfilePage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // State
  const [profile, setProfile] = useState({
    style: [],
    size: '',
    colors: [],
    budget: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Options
  const styleOptions = ['casual', 'formal', 'sportswear', 'streetwear', 'elegant', 'bohemian'];
  const sizeOptions = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
  const colorOptions = ['black', 'white', 'blue', 'red', 'green', 'yellow', 'pink', 'navy', 'gray', 'brown'];

  // Load profile on mount
  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchProfile();
  }, [user, navigate]);

  const fetchProfile = async () => {
    try {
      const response = await api.get(`/users/${user.user_id}/profile`);
      if (response.data.profile) {
        const loadedProfile = response.data.profile;
        
        setProfile({
          style: Array.isArray(loadedProfile.style) ? loadedProfile.style : [],
          size: typeof loadedProfile.size === 'string' ? loadedProfile.size : '',
          colors: Array.isArray(loadedProfile.colors) ? loadedProfile.colors : [],
          budget: loadedProfile.budget || ''
        });
      }
    } catch (error) {
      console.error('Fetch profile error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStyleToggle = (style) => {
    setProfile(prev => ({
      ...prev,
      style: prev.style.includes(style)
        ? prev.style.filter(s => s !== style)
        : [...prev.style, style]
    }));
  };

  const handleSizeSelect = (size) => {
    setProfile(prev => ({
      ...prev,
      size: size
    }));
  };

  const handleColorToggle = (color) => {
    setProfile(prev => ({
      ...prev,
      colors: prev.colors.includes(color)
        ? prev.colors.filter(c => c !== color)
        : [...prev.colors, color]
    }));
  };

  const handleBudgetChange = (e) => {
    setProfile(prev => ({
      ...prev,
      budget: e.target.value
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      await api.put(`/users/${user.user_id}/profile`, {
        style: profile.style,
        size: profile.size,
        colors: profile.colors,
        budget: profile.budget
      });
      
      alert('Profile updated successfully! ✅');
    } catch (error) {
      console.error('Save profile error:', error);
      alert('Failed to save profile: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div style={{ 
        padding: '2rem', 
        textAlign: 'center',
        fontSize: '1.2rem'
      }}>
        Loading profile...
      </div>
    );
  }

  return (
    <div style={{ 
      padding: '2rem', 
      maxWidth: '800px', 
      margin: '0 auto' 
    }}>
      <h1 style={{ 
        marginBottom: '2rem', 
        fontSize: '2rem',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      }}>
        <User size={32} />
        My Profile
      </h1>

      <form onSubmit={handleSave}>
        {/* Account Information */}
        <div style={{
          backgroundColor: '#1a1a1a',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '1px solid #333'
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            marginBottom: '1rem',
            color: '#fff'
          }}>
            Account Information
          </h2>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem', 
            color: '#999' 
          }}>
            <Mail size={18} />
            <span>{user.email}</span>
          </div>
        </div>

        {/* Style Preferences */}
        <div style={{
          backgroundColor: '#1a1a1a',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '1px solid #333'
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            marginBottom: '1rem',
            color: '#fff'
          }}>
            Style Preferences
          </h2>
          <div style={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: '0.75rem' 
          }}>
            {styleOptions.map(style => (
              <button
                key={style}
                type="button"
                onClick={() => handleStyleToggle(style)}
                style={{
                  padding: '0.5rem 1rem',
                  backgroundColor: profile.style.includes(style) ? '#646cff' : '#2a2a2a',
                  border: '1px solid ' + (profile.style.includes(style) ? '#646cff' : '#444'),
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  transition: 'all 0.2s',
                  fontSize: '0.95rem'
                }}
                onMouseEnter={(e) => {
                  if (!profile.style.includes(style)) {
                    e.target.style.backgroundColor = '#333';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!profile.style.includes(style)) {
                    e.target.style.backgroundColor = '#2a2a2a';
                  }
                }}
              >
                {style}
              </button>
            ))}
          </div>
        </div>

        {/* Size */}
        <div style={{
          backgroundColor: '#1a1a1a',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '1px solid #333'
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            marginBottom: '1rem',
            color: '#fff'
          }}>
            Size
          </h2>
          <div style={{ 
            display: 'flex', 
            gap: '0.75rem',
            flexWrap: 'wrap'
          }}>
            {sizeOptions.map(size => (
              <button
                key={size}
                type="button"
                onClick={() => handleSizeSelect(size)}
                style={{
                  padding: '0.5rem 1rem',
                  backgroundColor: profile.size === size ? '#646cff' : '#2a2a2a',
                  border: '1px solid ' + (profile.size === size ? '#646cff' : '#444'),
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  fontSize: '0.95rem',
                  minWidth: '60px'
                }}
                onMouseEnter={(e) => {
                  if (profile.size !== size) {
                    e.target.style.backgroundColor = '#333';
                  }
                }}
                onMouseLeave={(e) => {
                  if (profile.size !== size) {
                    e.target.style.backgroundColor = '#2a2a2a';
                  }
                }}
              >
                {size}
              </button>
            ))}
          </div>
        </div>

        {/* Favorite Colors */}
        <div style={{
          backgroundColor: '#1a1a1a',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '1px solid #333'
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            marginBottom: '1rem',
            color: '#fff'
          }}>
            Favorite Colors
          </h2>
          <div style={{ 
            display: 'flex', 
            flexWrap: 'wrap', 
            gap: '0.75rem' 
          }}>
            {colorOptions.map(color => (
              <button
                key={color}
                type="button"
                onClick={() => handleColorToggle(color)}
                style={{
                  padding: '0.5rem 1rem',
                  backgroundColor: profile.colors.includes(color) ? '#646cff' : '#2a2a2a',
                  border: '1px solid ' + (profile.colors.includes(color) ? '#646cff' : '#444'),
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer',
                  textTransform: 'capitalize',
                  transition: 'all 0.2s',
                  fontSize: '0.95rem'
                }}
                onMouseEnter={(e) => {
                  if (!profile.colors.includes(color)) {
                    e.target.style.backgroundColor = '#333';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!profile.colors.includes(color)) {
                    e.target.style.backgroundColor = '#2a2a2a';
                  }
                }}
              >
                {color}
              </button>
            ))}
          </div>
        </div>

        {/* Budget */}
        <div style={{
          backgroundColor: '#1a1a1a',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          border: '1px solid #333'
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            marginBottom: '1rem',
            color: '#fff'
          }}>
            Budget
          </h2>
          <select
            value={profile.budget}
            onChange={handleBudgetChange}
            style={{
              width: '100%',
              padding: '0.75rem',
              backgroundColor: '#2a2a2a',
              border: '1px solid #444',
              borderRadius: '8px',
              color: 'white',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            <option value="">Select budget range</option>
            <option value="low">Budget-friendly ($ - $$)</option>
            <option value="medium">Mid-range ($$ - $$$)</option>
            <option value="high">Premium ($$$ - $$$$)</option>
            <option value="luxury">Luxury ($$$$+)</option>
          </select>
        </div>

        {/* Save Button */}
        <button
          type="submit"
          disabled={saving}
          style={{
            width: '100%',
            padding: '1rem',
            backgroundColor: saving ? '#555' : '#646cff',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1rem',
            cursor: saving ? 'not-allowed' : 'pointer',
            opacity: saving ? 0.7 : 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
            transition: 'all 0.2s',
            fontWeight: '600'
          }}
          onMouseEnter={(e) => {
            if (!saving) {
              e.target.style.backgroundColor = '#5558e0';
            }
          }}
          onMouseLeave={(e) => {
            if (!saving) {
              e.target.style.backgroundColor = '#646cff';
            }
          }}
        >
          <Save size={20} />
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </form>
    </div>
  );
}
