export const buildImageUrl = (imageUrl) => {
  if (!imageUrl) return null;
  // Eğer zaten tam URL ise döndür
  if (imageUrl.startsWith('http') || imageUrl.startsWith('/images/')) {
    return imageUrl;
  }
  // Değilse /images/ ekle
  return `/images/${imageUrl}`;
};