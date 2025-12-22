#!/usr/bin/env python3
"""
Performance Analytics Script
AI Fashion Assistant v2.0
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

PROMETHEUS_URL = "http://localhost:9090"

def query_prometheus(query, start, end, step='1m'):
    """Query Prometheus API."""
    params = {
        'query': query,
        'start': start.isoformat(),
        'end': end.isoformat(),
        'step': step
    }
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params=params)
    return response.json()

def get_request_rate(hours=24):
    """Get request rate for last N hours."""
    end = datetime.now()
    start = end - timedelta(hours=hours)
    query = 'rate(http_requests_total[5m])'
    return query_prometheus(query, start, end)

def get_error_rate(hours=24):
    """Get error rate for last N hours."""
    end = datetime.now()
    start = end - timedelta(hours=hours)
    query = 'rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])'
    return query_prometheus(query, start, end)

def get_latency_percentiles(hours=24):
    """Get latency percentiles."""
    end = datetime.now()
    start = end - timedelta(hours=hours)
    
    percentiles = {}
    for p in [50, 95, 99]:
        query = f'histogram_quantile({p/100}, rate(http_request_duration_seconds_bucket[5m]))'
        percentiles[f'p{p}'] = query_prometheus(query, start, end)
    
    return percentiles

def generate_report():
    """Generate performance report."""
    print("\n📊 PERFORMANCE ANALYTICS REPORT")
    print("=" * 80)
    
    # Request rate
    print("\n1. Request Rate (24h)")
    rate_data = get_request_rate()
    print(f"   Current: {rate_data} req/s")
    
    # Error rate
    print("\n2. Error Rate (24h)")
    error_data = get_error_rate()
    print(f"   Current: {error_data}%")
    
    # Latency
    print("\n3. Latency Percentiles (24h)")
    latency_data = get_latency_percentiles()
    for p, data in latency_data.items():
        print(f"   {p}: {data}ms")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    generate_report()
