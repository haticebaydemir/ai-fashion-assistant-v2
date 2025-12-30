# Data Schemas

This directory contains standardized schemas for all data in the project.

## Purpose

Schemas ensure data consistency and catch errors early.

## Files

- `schemas.json`: Machine-readable schema definitions
- `schemas.yaml`: Human-readable schema definitions
- `validator.py`: Python validation utilities

## Schemas

### product

Product catalog data

**Required fields:**
- `product_id` (int): Unique product identifier
- `name` (str): Product name
- `category` (str): Product category

### query

Search query data

**Required fields:**
- `query_id` (int): Unique query identifier
- `query_text` (str): Query text

### ground_truth

Query-product relevance judgments

**Required fields:**
- `query_id` (int): Query identifier
- `product_id` (int): Product identifier
- `relevance` (int): Relevance score (0-3)

### embedding

Vector embeddings

**Required fields:**
- `item_id` (int): Item identifier
- `embedding_type` (str): 'text' or 'image'
- `embedding` (list[float]): Vector embedding
- `model_name` (str): Model used for embedding

