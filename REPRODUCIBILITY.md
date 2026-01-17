# Reproducibility Guide - AI Fashion Assistant v2.5

**Complete guide to reproducing all results from v2.0 through v2.5**

This document provides step-by-step instructions to reproduce:
- Search performance metrics (NDCG, Recall, MRR)
- RAG pipeline results
- AI agent evaluations
- Personalization metrics
- User study results (SUS 84.50)
- Full-stack application deployment

---

## 📋 Quick Navigation

- [Environment Setup](#environment-setup)
- [v2.0 Baseline Results](#v20-baseline-results)
- [v2.1 Visual Attributes](#v21-visual-attributes)
- [v2.2 RAG Pipeline](#v22-rag-pipeline)
- [v2.3 AI Agents](#v23-ai-agents)
- [v2.4 Personalization](#v24-personalization)
- [v2.4.5 Multimodal RAG](#v245-multimodal-rag)
- [v2.5 User Study](#v25-user-study)
- [Full-Stack Application](#full-stack-application)

---

## Environment Setup

### Prerequisites

```bash
# Python version
Python 3.10 or higher

# Check environment.json for exact versions
cat environment.json
```

### Installation

```bash
# Clone repository
git clone https://github.com/haticebaydemir/ai-fashion-assistant-v2.git
cd ai-fashion-assistant-v2

# Install core dependencies
pip install -r requirements.txt
```

### Configuration

All experiments use configuration files in `configs/`.

Default configuration: `configs/default.yaml`

To run with a specific config:
```python
import yaml
with open('configs/default.yaml') as f:
    config = yaml.safe_load(f)
```

### Random Seeds

Set random seed for reproducibility:
```python
import numpy as np
import torch

seed = config.get('random_seed', 42)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
```

---

## 🎯 Version-Specific Reproduction

### v2.0 Baseline Results

**Target Metrics:**
- NDCG@10: 97.43%
- MRR: 100%
- Recall@10: 51.11%
- Response time: <50ms

**Steps:**

1. Navigate to baseline directory:
```bash
cd v2.0-baseline/
```

2. Follow setup instructions:
```bash
# See v2.0-baseline/README.md for details
```

3. Run evaluation notebooks:
```bash
# Open Jupyter
jupyter notebook

# Navigate to:
research/notebooks/phase9_evaluation/

# Run all evaluation notebooks sequentially
```

4. Check results:
```bash
# Results saved in:
evaluation/results/

# Key files:
# - baseline_metrics.csv
# - fusion_metrics.csv
# - performance_comparison.png
```

**Expected Time:** 2-3 hours (includes model downloads)

**Variance:** ±0.5% on metrics due to FAISS approximation

---

### v2.1 Visual Attributes

**Target Results:**
- 307,720 attributes extracted
- 95.4% product coverage
- 10 semantic categories
- Avg 6.93 attributes per product

**Steps:**

1. Navigate to v2.1 directory:
```bash
cd v2.1-core-ml-plus/
```

2. Run attribute extraction:
```bash
jupyter notebook notebooks/01_visual_attributes_extraction.ipynb
```

3. Check results:
```bash
# Output file:
evaluation/results/product_attributes.csv

# Verify:
# - Total rows: 307,720
# - Unique products with attributes: ~42,388 (95.4%)
# - Categories: 10 (pattern, fit, length, etc.)
```

**Expected Time:** 1-2 hours

**Note:** CLIP inference requires GPU for faster processing (CPU: 4-6 hours)

---

### v2.2 RAG Pipeline

**Target Metrics:**
- Average RAG score: 0.714
- Response time: 0.89s
- 30 test queries evaluated

**Steps:**

1. Set up environment:
```bash
cd v2.2-rag-langchain/

# Set GROQ API key
export GROQ_API_KEY="your_api_key_here"
# Or create .env file
```

2. Run evaluation:
```bash
jupyter notebook notebooks/03_evaluation.ipynb
```

3. Check results:
```bash
evaluation/results/
├── evaluation_results.csv      # Per-query scores
├── evaluation_stats.json       # Summary statistics
├── category_performance.csv    # By category
└── score_distribution.png      # Visualization
```

**Expected Time:** 30 minutes

**API Requirements:**
- GROQ API key (free tier: 14,400 requests/day)
- Results may vary ±5% due to LLM non-determinism

**Troubleshooting:**
- Rate limit: Wait or use free tier limit
- API errors: Check GROQ_API_KEY environment variable

---

### v2.3 AI Agents

**Target Metrics:**
- Success rate: 100%
- Tool usage rate: 100%
- Avg response time: 2.6s
- Memory efficiency: 92%

**Steps:**

1. Setup:
```bash
cd v2.3-ai-agents-langchain/

# Ensure GROQ_API_KEY is set
echo $GROQ_API_KEY
```

2. Run comprehensive evaluation:
```bash
jupyter notebook notebooks/04_final_evaluation.ipynb
```

3. Verify results:
```bash
evaluation/results/
├── final_evaluation_results.csv
├── final_evaluation_complete.png
├── v2.3_final_summary.json
└── conversation_memory_results.json

# Check metrics match:
# - success_rate: 1.0 (100%)
# - tool_usage_rate: 1.0 (100%)
# - avg_response_time: ~2.6s
```

**Expected Time:** 1 hour

**Note:** 
- LangChain 0.1.20 required
- Results consistent across runs for same inputs

---

### v2.4 Personalization

**Target Metrics:**
- Preference match: 76.7%
- Personalization latency: 11.92ms
- Coverage: 100%
- Personalization rate: 83.3%

**Steps:**

1. Navigate and run:
```bash
cd v2.4-complete/

jupyter notebook notebooks/02_personalization_engine.ipynb
```

2. Check outputs:
```bash
evaluation/results/
├── personalization_metrics.csv     # Per-user metrics
├── recommendations_U001.csv        # User 1 recommendations
├── recommendations_U002.csv        # User 2 recommendations
└── recommendations_U003.csv        # User 3 recommendations

# Verify:
# - Avg preference_match: 76.7%
# - Avg latency: 11.92ms
# - Coverage: 100%
```

**Expected Time:** 30 minutes

**Data Requirements:**
- Test user profiles in `data/users/`
- Pre-computed embeddings from v2.0

---

### v2.4.5 Multimodal RAG

**Target Metrics:**
- Response time: 0.64s (28% faster than v2.2)
- Visual keywords: 7.6 per response
- Visual keyword rate: 100%
- Multimodal unique products: 6.0

**Steps:**

1. Run all notebooks sequentially:
```bash
cd v2.4.5-multimodal-rag/

# Run notebooks in order:
jupyter notebook notebooks/01_multimodal_rag_architecture.ipynb
jupyter notebook notebooks/02_image_query_processing.ipynb
jupyter notebook notebooks/03_multimodal_retrieval.ipynb
jupyter notebook notebooks/04_visual_aware_rag.ipynb
jupyter notebook notebooks/05_evaluation_metrics.ipynb
jupyter notebook notebooks/06_final_documentation.ipynb
```

2. Verify results:
```bash
evaluation/results/
├── rag_quality_metrics.json
├── performance_visualization.png
├── v2.4.5_comprehensive_results.xlsx
└── final_summary.json

# Check key metrics:
# - avg_response_time: 0.642s
# - avg_visual_keywords: 7.6
# - visual_keyword_rate: 1.0 (100%)
```

**Expected Time:** 2 hours

**Note:** Requires CLIP model and GROQ API

---

### v2.5 User Study

**Target Results:**
- SUS Score: 84.50 (Grade A)
- 92% usage intent
- n=25 participants

**Reproduction Options:**

#### Option A: Analyze Existing Data (Recommended)

1. Read comprehensive report:
```bash
cat USER_STUDY_RESULTS.md
```

2. Verify calculations:
```python
# SUS Calculation
# Odd questions (1,3,5,7,9): score = answer - 1
# Even questions (2,4,6,8,10): score = 5 - answer
# Total SUS = sum(all_scores) * 2.5

# Example for one participant:
scores = [
    (4 - 1),  # Q1
    (5 - 2),  # Q2
    (5 - 1),  # Q3
    (5 - 1),  # Q4
    (4 - 1),  # Q5
    (5 - 2),  # Q6
    (5 - 1),  # Q7
    (5 - 2),  # Q8
    (4 - 1),  # Q9
    (5 - 2),  # Q10
]
sus_score = sum(scores) * 2.5
print(f"SUS Score: {sus_score}")  # Should be 80-100 for good UX
```

3. Check raw data (if provided):
```bash
# If you have access to:
data/user_study/responses.csv
```

**Expected Time:** 1 hour (data analysis)

#### Option B: Run New User Study

1. Deploy full-stack application (see next section)

2. Recruit 20-30 participants

3. Create Google Forms with SUS questions:
```
Scale: 1 (Strongly Disagree) to 5 (Strongly Agree)

Q1: I think I would like to use this system frequently
Q2: I found the system unnecessarily complex
Q3: I thought the system was easy to use
Q4: I think I would need technical support to use this
Q5: I found the various functions well integrated
Q6: I thought there was too much inconsistency
Q7: I imagine most people would learn quickly
Q8: I found the system very cumbersome to use
Q9: I felt very confident using the system
Q10: I needed to learn a lot before I could use this
```

4. Calculate SUS:
```python
def calculate_sus(responses):
    """
    responses: list of 10 answers (1-5)
    """
    odd_sum = sum(responses[i] - 1 for i in [0,2,4,6,8])
    even_sum = sum(5 - responses[i] for i in [1,3,5,7,9])
    sus = (odd_sum + even_sum) * 2.5
    return sus

# Example:
participant_responses = [4, 2, 5, 1, 4, 2, 5, 1, 4, 1]
print(calculate_sus(participant_responses))  # Output: 85.0
```

5. Analyze results:
```python
import pandas as pd
import numpy as np

# Load responses
df = pd.read_csv('responses.csv')

# Calculate SUS for each participant
df['sus_score'] = df.apply(lambda row: calculate_sus(row[['Q1','Q2',...,'Q10']].values), axis=1)

# Statistics
print(f"Mean SUS: {df['sus_score'].mean():.2f}")
print(f"Median SUS: {df['sus_score'].median():.2f}")
print(f"Std Dev: {df['sus_score'].std():.2f}")

# Grade distribution
def sus_grade(score):
    if score >= 80.3: return 'A'
    if score >= 68: return 'B'
    if score >= 52: return 'C'
    if score >= 25: return 'D'
    return 'F'

df['grade'] = df['sus_score'].apply(sus_grade)
print(df['grade'].value_counts())
```

**Expected Time:** 1-2 weeks (full study)

**Variance:** ±5 points normal for SUS

---

## 🚀 Full-Stack Application

**Target:** Deploy working application matching screenshots

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup

```bash
cd AI-Fashion-fullstack/backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy data files
# Option 1: Use batch script (Windows)
copy_data.bat

# Option 2: Manual copy (Linux/Mac)
# Copy embeddings/ and models/ from v2.0-baseline/
cp -r ../../v2.0-baseline/embeddings/ ./data/
cp -r ../../v2.0-baseline/models/ ./data/

# Set environment variables
cp .env.example .env

# Edit .env file:
# MONGODB_URI=mongodb://localhost:27017/  # or MongoDB Atlas URI
# GROQ_API_KEY=your_groq_key
# JWT_SECRET=your_secret_key

# Start backend
uvicorn main:app --reload
```

**Backend should be running on:** http://localhost:8000

### Frontend Setup

```bash
cd AI-Fashion-fullstack/frontend

# Install dependencies
npm install

# Set environment
cp .env.example .env

# Edit .env:
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

**Frontend should be running on:** http://localhost:5173

### Verification Checklist

✅ **Backend Health Check:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

✅ **Test Search:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blue dress", "limit": 5}'
# Expected: JSON with 5 products
```

✅ **Frontend Tests:**
1. Open http://localhost:5173
2. Register new user → Should work
3. Login → Should redirect to home
4. Search "blue dress" → Should return results in <1s
5. Try image search → Should work
6. Use chat → Should get AI responses
7. Add favorites → Should persist
8. Update profile → Should save

### Common Issues

**Issue: MongoDB connection failed**
```
ServerSelectionTimeoutError
```
**Solution:**
- Check MongoDB is running: `mongod --version`
- Verify MONGODB_URI in .env
- For Atlas: Check IP whitelist

**Issue: FAISS dimension mismatch**
```
AssertionError: Dimension mismatch
```
**Solution:**
- Ensure embeddings are from correct version
- Check search_engine.py padding logic

**Issue: GROQ API errors**
```
Rate limit exceeded
```
**Solution:**
- Check GROQ_API_KEY is valid
- Free tier: 14,400 requests/day
- Wait or upgrade plan

**Expected Time:** 1-2 hours (first-time setup)

---

## 📊 Expected Results Summary

| Version | Key Metric | Expected Result | Variance |
|---------|------------|-----------------|----------|
| v2.0 | NDCG@10 | 97.43% | ±0.5% |
| v2.1 | Attributes | 307K | ±100 |
| v2.2 | RAG Score | 0.714 | ±0.05 |
| v2.3 | Success Rate | 100% | 0% |
| v2.4 | Preference Match | 76.7% | ±5% |
| v2.4.5 | Response Time | 0.64s | ±0.1s |
| v2.5 | SUS Score | 84.50 | ±5 |

### Variance Notes

- **Search metrics (v2.0, v2.1):** Very stable, ±0.5% expected
- **LLM-based metrics (v2.2, v2.3):** ±5% due to non-determinism
- **User study (v2.5):** ±5 points normal for SUS
- **Timing metrics:** ±10% depending on hardware

---

## 🔬 Advanced Reproduction

### Running Experiments

1. Start experiment:
```python
from src.utils import ExperimentTracker

tracker = ExperimentTracker()
tracker.start_experiment('my_experiment', config)
```

2. Run your code

3. Log metrics:
```python
tracker.log_metric('recall@10', value)
tracker.log_metric('ndcg@10', value)
```

4. End experiment:
```python
tracker.end_experiment()
```

### Experiment Logs

All experiments saved in `experiments/` directory.

Each folder contains:
- `config.yaml`: Configuration used
- `experiment.json`: Metrics and artifacts
- `logs/`: Detailed logs

### Data Versions

Data files tracked in config under `data` section.

Ensure correct versions:
```python
# Check data hash
import hashlib

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# Verify
expected_hash = config['data']['hash']
actual_hash = hash_file('data/meta_ssot.csv')
assert expected_hash == actual_hash, "Data file mismatch!"
```

---

## 🐛 Troubleshooting

### Python Version Mismatch

**Symptom:** Package installation errors

**Solution:**
```bash
python --version  # Check version
# Should be 3.10+

# If different, use pyenv or conda
conda create -n fashion python=3.10
conda activate fashion
```

### Package Version Conflicts

**Symptom:** Import errors

**Solution:**
```bash
# Use exact versions
pip install -r requirements.txt --force-reinstall

# Check installed versions
pip list
```

### GPU vs CPU Differences

**Symptom:** Slightly different results

**Solution:**
- Expected: Some operations differ between GPU/CPU
- Variance: Usually <1%
- For exact reproduction: Use same hardware type

### Results Don't Match Exactly

**Checklist:**
1. ✅ Python version matches?
2. ✅ Package versions match requirements.txt?
3. ✅ Random seed set correctly?
4. ✅ Data file versions correct?
5. ✅ GPU vs CPU noted?
6. ✅ LLM variance expected (<5%)?

**If still different:**
- Document variance in issues
- Provide system info (Python, OS, hardware)
- Share config and logs

---

## 📖 Additional Resources

### Documentation
- Main README: Comprehensive overview
- Version READMEs: Specific to each version
- CHANGELOG: Version history
- USER_STUDY_RESULTS: Detailed SUS analysis

### Code Examples
- `v2.0-baseline/research/notebooks/`: 30+ examples
- `v2.1-core-ml-plus/notebooks/`: Visual attributes
- `v2.2-rag-langchain/notebooks/`: RAG pipeline
- All notebooks fully documented

### Support
- GitHub Issues: Report problems
- README FAQ: Common questions
- Code comments: Inline documentation

---

## 🎯 Reproducibility Checklist

Before starting:
- [ ] Python 3.10+ installed
- [ ] Git repository cloned
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB running (if testing full-stack)
- [ ] GROQ API key set (if testing LLM features)

For each version:
- [ ] Navigate to correct directory
- [ ] Read version README
- [ ] Run notebooks in sequence
- [ ] Verify results match expected
- [ ] Document any variances

After completion:
- [ ] All metrics within expected variance
- [ ] Full-stack application deployed
- [ ] Screenshots match documentation
- [ ] Issues reported (if any)

---

## ✅ Success Criteria

Reproduction successful if:
- ✅ All metrics within expected variance
- ✅ Full-stack application runs
- ✅ No critical errors
- ✅ Documentation clear and helpful

---

**Last Updated:** January 17, 2026  
**Version:** 2.5  
**Maintainer:** Hatice Baydemir  
**Contact:** GitHub Issues

---

*For detailed API documentation, see individual version READMEs.*
