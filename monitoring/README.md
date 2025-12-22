# Monitoring & Observability Guide

## Overview

Complete monitoring stack for AI Fashion Assistant v2.0.

## Architecture

```
Application → Prometheus → Grafana
     ↓            ↓            ↓
  Metrics      Storage    Visualization
```

## Components

### Prometheus
- **Port:** 9090
- **Purpose:** Time-series metrics storage
- **Scrape Interval:** 15s
- **Retention:** 15 days

### Grafana
- **Port:** 3000
- **Purpose:** Visualization & dashboards
- **Default Login:** admin/admin
- **Dashboards:** Pre-configured

## Key Metrics

### Request Metrics
- `http_requests_total`: Total request count
- `http_request_duration_seconds`: Request latency
- `http_requests_in_progress`: Concurrent requests

### Error Metrics
- `http_requests_total{status="5xx"}`: Server errors
- `http_requests_total{status="4xx"}`: Client errors

### System Metrics
- `node_cpu_seconds_total`: CPU usage
- `node_memory_MemAvailable_bytes`: Available memory
- `node_disk_io_time_seconds_total`: Disk I/O

### Redis Metrics
- `redis_commands_total`: Redis command count
- `redis_connected_clients`: Client connections
- `redis_memory_used_bytes`: Memory usage

## Alert Rules

### Critical Alerts
- **ServiceDown:** API unavailable >1min
- **HighErrorRate:** Error rate >5% for 5min
- **RedisDown:** Cache unavailable >1min

### Warning Alerts
- **HighLatency:** P95 latency >1s for 5min
- **HighCPUUsage:** CPU usage >80% for 10min
- **HighMemoryUsage:** Memory >85% for 10min

## Usage

### Start Monitoring
```bash
cd docker
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### Access Dashboards
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

### Query Examples

**Request rate:**
```promql
rate(http_requests_total[5m])
```

**P95 latency:**
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Error rate:**
```promql
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
```

## SLA Targets

### Availability
- **Target:** 99.9% (43.8 minutes downtime/month)
- **Measurement:** `up` metric

### Latency
- **P50:** <100ms
- **P95:** <500ms
- **P99:** <1000ms

### Error Rate
- **Target:** <1%
- **Critical:** >5%

## Troubleshooting

### Prometheus not scraping
1. Check `/metrics` endpoint accessibility
2. Verify network connectivity
3. Check Prometheus targets page

### Grafana dashboard empty
1. Verify Prometheus data source
2. Check time range selection
3. Verify metrics exist in Prometheus

### High latency
1. Check CPU/Memory usage
2. Review slow queries
3. Check Redis cache hit rate
4. Profile application code
