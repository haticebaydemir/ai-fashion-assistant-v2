import { Heart } from 'lucide-react';

export default function FavoriteButton({ productId, isFavorite, onToggle }) {
  return (
    <button
      onClick={() => onToggle(productId)}
      style={{
        padding: '0.5rem',
        backgroundColor: 'transparent',
        border: '1px solid #646cff',
        borderRadius: '6px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center'
      }}
    >
      <Heart size={16} fill={isFavorite ? '#ff4444' : 'none'} color={isFavorite ? '#ff4444' : 'currentColor'} />
    </button>
  );
}
