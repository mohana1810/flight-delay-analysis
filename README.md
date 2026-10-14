# Flight Delay Analysis and Prediction

A Data Science project that analyzes U.S. flight delays, explores trends across airlines and months, and compares machine learning models to predict arrival delays of 15 minutes or more.

## Dashboard Preview

![Flight Delay Analysis Dashboard](assets/flight-delay-dashboard.png)

## Project Overview

This project analyzes U.S. flight data from January to March 2026 to identify delay patterns and evaluate predictive models.

- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Monthly and airline delay analysis
- Data visualization
- Model training and evaluation
- Sample flight delay prediction

## Key Statistics

| Metric | Result |
|---|---:|
| Flight records analyzed | 1,671,127 |
| Arrival-delay rate | 21.8% |
| Cancellation rate | 3.29% |
| Diversion rate | 0.26% |
| Data period | Jan–Mar 2026 |

## Machine Learning Models

- **Logistic Regression**
- **Random Forest**

The models are evaluated using accuracy, precision, recall, F1-score, and ROC-AUC. In the current evaluation, **Random Forest has the higher F1-score and recall for delayed flights**, while Logistic Regression has higher overall accuracy. This illustrates why accuracy alone may not be sufficient when comparing models for an imbalanced target.


The target variable is `ARR_DEL15`:

- `0` — Arrival delay under 15 minutes
- `1` — Arrival delay of 15 minutes or more

## Tech Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Streamlit
- Plotly
- Joblib

## Project Structure

```text
flight-delay-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── reports/
│   └── figures/
├── src/
│   └── main.py
├── assets/
│   └── flight-delay-dashboard.png
├── requirements.txt
└── README.md
```

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/mohana1810/flight-delay-analysis.git
cd flight-delay-analysis
```

**2. Create and activate a virtual environment**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```powershell
python -m pip install -r requirements.txt
```

**4. Run the dashboard**

```powershell
python -m streamlit run src/main.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Data Source

U.S. Bureau of Transportation Statistics (BTS) — Airline On-Time Performance Data.

[Official BTS TranStats Data Index](https://www.transtats.bts.gov/DataIndex.asp)

The project uses monthly flight data for January–March 2026.

## Project Developer

**J. Mohana**  
B.Tech — Computer Science Engineering (AI & Machine Learning)

---
