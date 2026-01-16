import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import List, Dict


def bm25_retrieve(corpus: List[str], queries: List[str], k: int = 10) -> List[List[int]]:
    tokenized = [doc.split() for doc in corpus]
    bm25 = BM25Okapi(tokenized)
    results = []
    for q in queries:
        q_tok = q.split()
        scores = bm25.get_scores(q_tok)
        topk = np.argsort(scores)[::-1][:k]
        results.append(topk.tolist())
    return results


def tfidf_retrieve(corpus: List[str], queries: List[str], k: int = 10) -> List[List[int]]:
    vect = TfidfVectorizer().fit(corpus)
    doc_mat = vect.transform(corpus)
    q_mat = vect.transform(queries)
    results = []
    for i in range(q_mat.shape[0]):
        sims = linear_kernel(q_mat[i:i+1], doc_mat).flatten()
        topk = np.argsort(sims)[::-1][:k]
        results.append(topk.tolist())
    return results


def rrf_aggregate(ranked_lists: List[List[int]], k: int = 10, c: int = 60) -> List[int]:
    # Reciprocal Rank Fusion: sum 1 / (c + rank)
    scores = {}
    for rlist in ranked_lists:
        for rank, doc in enumerate(rlist):
            scores[doc] = scores.get(doc, 0) + 1.0 / (c + rank + 1)
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in sorted_docs][:k]


def topk_to_ranked_lists(topk_all_methods: Dict[str, List[List[int]]], k: int = 10):
    # converts dict of method->list_of_queries->[ids] into per-query lists of lists
    num_queries = len(next(iter(topk_all_methods.values())))
    per_query_lists = []
    for qi in range(num_queries):
        lists = []
        for method, lists_all in topk_all_methods.items():
            lists.append(lists_all[qi])
        per_query_lists.append(lists)
    return per_query_lists
