# House Prices (Ames) — Minimal, Reproducible ML

Predict Ames house sale prices with a clean scikit-learn pipeline and **OOF-validated blending**.

- **Competition:** Kaggle — *House Prices: Advanced Regression* (**RMSLE**)  
- **Validation:** RepeatedKFold **5×3** (shuffle=True, seed=42)  
- **Target transform:** `log1p` / `expm1` via `TransformedTargetRegressor`  
- **Best OOF:** **RMSLE = 0.11909** with a **blend** of **SVR (45%) + GBR (55%)**  
- **Public LB:** ~**125** (Top-150)

_Notebooks:_  
• [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb)  
• [notebooks/02_preprocessing.ipynb](notebooks/02_preprocessing.ipynb) — pipeline, tuning, OOF, blend, save models, submission

---

## Project Structure

    .
    ├─ datasets/           # Kaggle CSVs (not in git)
    ├─ models/             # saved models, weights, submissions (gitignored)
    ├─ notebooks/          # 01_eda, 02_preprocessing
    ├─ src/
    │   ├─ config.py       # column groups, engineered features
    │   └─ data_access.py  # (optional) data helper
    ├─ images/             # exported plots (optional)
    ├─ requirements.txt
    └─ README.md

---

## Quick Start

    python -m venv venv
    # Windows: venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    pip install -r requirements.txt

Download Kaggle `train.csv` / `test.csv` to `datasets/`. Or use data_loading function from src/data_access (requires Kaggle api)

Run notebooks in order:

1. `01_eda.ipynb`  
2. `02_preprocessing.ipynb` → computes OOF, learns blend weight, saves models and writes submission to:  
       models/<timestamp>_blend_rmsle/submission.csv

### Results (OOF, RMSLE)

| Model             | RMSLE   |
|-------------------|---------|
| SVR               | 0.12165 |
| Gradient Boosting | 0.12047 |
| Blend (45/55)     | 0.11909 |

---

Next Steps: 

Try LightGBM/CatBoost and a simple stacking meta (ridge).

Stress-test with GroupKFold by Neighborhood to gauge generalization.

Expand features (e.g., neighborhood medians, age×grade, porch flags).

Notes

Pipelines are leakage-safe, target modeled in log-space to match RMSLE. 
Final predictions are clipped at 0 to avoid negative inputs to log1p. 
Models and weights are saved under models/<timestamp>_blend_rmsle/. 

Acknowledgments: Kaggle House Prices – Advanced Regression Techniques. 
Built with scikit-learn, numpy, pandas, matplotlib.
