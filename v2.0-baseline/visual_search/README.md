# Görsel Arama Sistemi

CLIP tabanlı görsel arama implementasyonu.

## Özellikler

- Görsel yükleme ve preprocessing
- CLIP image encoding (512-dim)
- FAISS similarity search
- Batch processing desteği
- ~100ms toplam gecikme

## Kullanım

```python
from visual_search import VisualSearchEngine

# Initialize
engine = VisualSearchEngine(model, preprocessor, device)

# Build index
engine.build_index(embeddings, product_ids)

# Search
results, scores = engine.search('query_image.jpg', k=10)
```

## Demo

```bash
python visual_search_demo.py --image test.jpg --k 10
```

## Performans

- Encoding: ~50ms
- Search: ~1ms
- Total: ~51ms (target: <100ms) ✓

## Gelecek İyileştirmeler

1. Gerçek ürün görselleri ile test
2. GPU batch processing
3. Model quantization
4. Streamlit UI
5. Kullanıcı testleri
