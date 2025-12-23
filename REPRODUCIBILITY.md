# Reproducibility Guide

This guide explains how to reproduce results from this project.

## Environment Setup

1. Python version: Check `environment.json` for exact version
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

All experiments use configuration files in `configs/`.

Default configuration: `configs/default.yaml`

To run with a specific config:
```python
import yaml
with open('configs/default.yaml') as f:
    config = yaml.safe_load(f)
```

## Running Experiments

1. Start experiment:
   ```python
   tracker.start_experiment('my_experiment', config)
   ```

2. Run your code

3. Log metrics:
   ```python
   tracker.log_metric('recall@10', value)
   ```

4. End experiment:
   ```python
   tracker.end_experiment()
   ```

## Experiment Logs

All experiments are saved in `experiments/`.

Each experiment folder contains:
- `config.yaml`: Configuration used
- `experiment.json`: Metrics and artifacts

## Random Seeds

Set random seed for reproducibility:
```python
import numpy as np
import torch

seed = config['random_seed']
np.random.seed(seed)
torch.manual_seed(seed)
```

## Data Versions

Data files are tracked in the config under `data` section.
Make sure you're using the correct version.

## Results

Baseline results (Phase 5):
- Recall@10: 48%
- NDCG@10: 86.6%

To reproduce:
1. Use configs/default.yaml
2. Run evaluation notebook
3. Compare against baseline

## Troubleshooting

If results don't match:
1. Check Python version matches
2. Check package versions match requirements.txt
3. Check random seed is set correctly
4. Check data file versions
5. Check GPU vs CPU (some operations differ slightly)
