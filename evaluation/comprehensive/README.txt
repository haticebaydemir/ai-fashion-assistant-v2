Comprehensive Evaluation Metrics
============================================================

This evaluation goes beyond basic Recall/NDCG to measure
multiple aspects of recommendation quality.

Ranking Quality:
  MAP - mean average precision (higher = better)
  Recall@K - fraction of relevant items retrieved
  Success@K - at least one relevant item found

Diversity:
  ILS - intra-list similarity (lower = more diverse)
  cat_diversity - unique categories ratio (higher = better)

Novelty:
  novelty - average item novelty (1 - popularity)
  Higher = recommending less obvious items

Files:
  - comprehensive_metrics.csv: per-query metrics
  - metrics_summary.json: aggregated statistics
