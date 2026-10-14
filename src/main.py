from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent  # Project root when this file is src/main.py
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
PROCESSED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Flight Intelligence | Delay Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- UI THEME -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #07111f 0%, #0a1728 55%, #101d31 100%); color: #edf4ff; }
[data-testid="stSidebar"] { background: #081321; border-right: 1px solid #1e344c; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f2f7ff !important; }
p, label, span, div { color: inherit; }
.hero {
  padding: 1.45rem 1.7rem; border-radius: 22px; margin-bottom: 1.1rem;
  background: linear-gradient(115deg, rgba(19,48,72,.98), rgba(15,31,52,.96));
  border: 1px solid rgba(79,209,197,.27); box-shadow: 0 16px 42px rgba(0,0,0,.18);
}
.eyebrow { color:#54d6c9; font-size:.78rem; font-weight:700; letter-spacing:.17em; text-transform:uppercase; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.25rem; font-weight:700; line-height:1.12; margin:.35rem 0 .6rem; }
.hero-sub { color:#b6c7da; font-size:1rem; max-width:850px; }
.kpi {
  background: linear-gradient(150deg, #12253a, #0e1b2d); border:1px solid #233d55;
  border-radius:17px; padding:1rem 1.1rem; min-height:112px;
}
.kpi-label { color:#a8bdd1; font-size:.83rem; font-weight:600; }
.kpi-value { color:#f4f8ff; font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; margin-top:.28rem; }
.kpi-note { color:#56d8c8; font-size:.76rem; margin-top:.15rem; }
.section-tag { color:#56d8c8; font-weight:700; letter-spacing:.12em; font-size:.75rem; text-transform:uppercase; }
div[data-testid="stMetric"] { background:#11243a; border:1px solid #28435d; padding:14px 16px; border-radius:15px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#102239; border-radius:10px 10px 0 0; padding:10px 18px; }
.stButton>button { border-radius:10px; border:1px solid #3cafa8; background:#1c8f89; color:white; font-weight:700; }
div[data-testid="stAlert"] { border-radius:12px; }
.small-muted { color:#91a7bd; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent  # Project root when this file is src/main.py
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
PROCESSED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Flight Intelligence | Delay Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- UI THEME -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #07111f 0%, #0a1728 55%, #101d31 100%); color: #edf4ff; }
[data-testid="stSidebar"] { background: #081321; border-right: 1px solid #1e344c; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #f2f7ff !important; }
p, label, span, div { color: inherit; }
.hero {
  padding: 1.45rem 1.7rem; border-radius: 22px; margin-bottom: 1.1rem;
  background: linear-gradient(115deg, rgba(19,48,72,.98), rgba(15,31,52,.96));
  border: 1px solid rgba(79,209,197,.27); box-shadow: 0 16px 42px rgba(0,0,0,.18);
}
.eyebrow { color:#54d6c9; font-size:.78rem; font-weight:700; letter-spacing:.17em; text-transform:uppercase; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:2.25rem; font-weight:700; line-height:1.12; margin:.35rem 0 .6rem; }
.hero-sub { color:#b6c7da; font-size:1rem; max-width:850px; }
.kpi {
  background: linear-gradient(150deg, #12253a, #0e1b2d); border:1px solid #233d55;
  border-radius:17px; padding:1rem 1.1rem; min-height:112px;
}
.kpi-label { color:#a8bdd1; font-size:.83rem; font-weight:600; }
.kpi-value { color:#f4f8ff; font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700; margin-top:.28rem; }
.kpi-note { color:#56d8c8; font-size:.76rem; margin-top:.15rem; }
.section-tag { color:#56d8c8; font-weight:700; letter-spacing:.12em; font-size:.75rem; text-transform:uppercase; }
div[data-testid="stMetric"] { background:#11243a; border:1px solid #28435d; padding:14px 16px; border-radius:15px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#102239; border-radius:10px 10px 0 0; padding:10px 18px; }
.stButton>button { border-radius:10px; border:1px solid #3cafa8; background:#1c8f89; color:white; font-weight:700; }
div[data-testid="stAlert"] { border-radius:12px; }
.small-muted { color:#91a7bd; font-size:.82rem; }
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#dce8f5", family="DM Sans"),
    margin=dict(l=20, r=20, t=55, b=25),
    xaxis=dict(gridcolor="#24384e", zerolinecolor="#24384e"),
    yaxis=dict(gridcolor="#24384e", zerolinecolor="#24384e"),
)

@st.cache_data(show_spinner=False)
def load_and_prepare_data():
    folders = ["janflights", "febflights", "marchflights"]
    frames = []
    for folder in folders:
        folder_path = RAW / folder
        if not folder_path.exists():
            raise FileNotFoundError(f"Missing folder: {folder_path}")
        csv_files = list(folder_path.rglob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV file found inside {folder_path}")
        for file in csv_files:
            part = pd.read_csv(file, low_memory=False)
            part.columns = part.columns.str.strip()
            frames.append(part)

    df = pd.concat(frames, ignore_index=True)
    required = [
        "FL_DATE", "OP_UNIQUE_CARRIER", "ORIGIN", "DEST", "CRS_DEP_TIME",
        "CRS_ARR_TIME", "ARR_DEL15", "CANCELLED", "DIVERTED", "DISTANCE"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Required columns missing from CSV: {missing}")

    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"], errors="coerce")
    df = df.dropna(subset=["FL_DATE"]).copy()

    numeric_columns = [
        "MONTH", "DAY_OF_MONTH", "CRS_DEP_TIME", "DEP_DELAY_NEW",
        "CRS_ARR_TIME", "ARR_DELAY_NEW", "ARR_DEL15", "CANCELLED",
        "DIVERTED", "DISTANCE"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["OP_UNIQUE_CARRIER", "ORIGIN", "DEST"]:
        df[col] = df[col].astype("string").str.strip()
        df.loc[df[col].isin(["", "nan", "None"]), col] = pd.NA

    raw_count = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = raw_count - len(df)

    def scheduled_hour(series):
        values = pd.to_numeric(series, errors="coerce")
        valid = values.between(0, 2359) & (values % 100 < 60)
        return (values // 100).where(valid)

    df["ScheduledDepHour"] = scheduled_hour(df["CRS_DEP_TIME"])
    df["ScheduledArrHour"] = scheduled_hour(df["CRS_ARR_TIME"])
    df["DayOfWeek"] = df["FL_DATE"].dt.dayofweek
    df["Month"] = df["FL_DATE"].dt.month
    df["MonthLabel"] = df["FL_DATE"].dt.strftime("%b %Y")

    # Preserve all operations for cancellation/diversion analysis.
    all_operations = df.copy()

    # ARR_DEL15 is evaluated only for non-cancelled, non-diverted flights
    # with a known binary arrival-delay label.
    flights = df[
        (df["CANCELLED"] == 0) &
        (df["DIVERTED"] == 0) &
        (df["ARR_DEL15"].isin([0, 1]))
    ].copy()
    flights["ARR_DEL15"] = flights["ARR_DEL15"].astype(int)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    all_operations.to_csv(PROCESSED / "cleaned_flights.csv", index=False)
    return all_operations, flights, duplicates_removed

@st.cache_resource(show_spinner="Training and evaluating models on your flight data...")
def train_models(_flights):
    flights = _flights.copy()
    available_months = sorted(flights["FL_DATE"].dt.to_period("M").unique())
    if len(available_months) < 3:
        raise ValueError("At least three months are required for chronological train/test evaluation.")

    train_months = available_months[:-1]
    test_month = available_months[-1]
    train_df = flights[flights["FL_DATE"].dt.to_period("M").isin(train_months)].copy()
    test_df = flights[flights["FL_DATE"].dt.to_period("M") == test_month].copy()

    # Keep model training responsive on a local machine.
    if len(train_df) > 200_000:
        train_df = train_df.sample(n=200_000, random_state=42)
    if len(test_df) > 100_000:
        test_df = test_df.sample(n=100_000, random_state=42)

    feature_columns = [
        "OP_UNIQUE_CARRIER", "ORIGIN", "DEST", "CRS_DEP_TIME",
        "CRS_ARR_TIME", "DISTANCE", "Month", "DayOfWeek",
        "DAY_OF_MONTH", "ScheduledDepHour", "ScheduledArrHour"
    ]
    feature_columns = [c for c in feature_columns if c in flights.columns]
    categorical = [c for c in ["OP_UNIQUE_CARRIER", "ORIGIN", "DEST"] if c in feature_columns]
    numeric = [c for c in feature_columns if c not in categorical]

    X_train, X_test = train_df[feature_columns], test_df[feature_columns]
    y_train, y_test = train_df["ARR_DEL15"], test_df["ARR_DEL15"]
    if y_train.nunique() < 2 or y_test.nunique() < 2:
        raise ValueError("Training and test partitions must contain both delay classes.")

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])
    preprocessor = ColumnTransformer([
        ("numeric", numeric_pipeline, numeric),
        ("categorical", categorical_pipeline, categorical)
    ])

    estimators = {
        "Logistic Regression": LogisticRegression(
            max_iter=500, class_weight="balanced", solver="saga", random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=15, min_samples_leaf=5,
            class_weight="balanced", random_state=42, n_jobs=-1
        )
    }

    results, fitted_models, reports, predictions_by_model, probabilities_by_model = [], {}, {}, {}, {}
    for name, estimator in estimators.items():
        pipeline = Pipeline([("preprocessor", preprocessor), ("model", estimator)])
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        probabilities = pipeline.predict_proba(X_test)[:, 1]

        results.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, predictions),
            "Precision": precision_score(y_test, predictions, zero_division=0),
            "Recall": recall_score(y_test, predictions, zero_division=0),
            "F1_Score": f1_score(y_test, predictions, zero_division=0),
            "ROC_AUC": roc_auc_score(y_test, probabilities)
        })
        fitted_models[name] = pipeline
        reports[name] = classification_report(
            y_test,
            predictions,
            target_names=["Not delayed", "Delayed 15+ minutes"],
            digits=2,
            zero_division=0,
            output_dict=True
        )
        predictions_by_model[name] = predictions
        probabilities_by_model[name] = probabilities

    results_df = pd.DataFrame(results).sort_values("F1_Score", ascending=False)
    return {
        "results": results_df,
        "models": fitted_models,
        "reports": reports,
        "predictions": predictions_by_model,
        "probabilities": probabilities_by_model,
        "y_test": y_test,
        "X_test": X_test,
        "feature_columns": feature_columns,
        "train_months": [str(m) for m in train_months],
        "test_month": str(test_month),
        "train_rows": len(train_df),
        "test_rows": len(test_df),
    }

def kpi_card(label, value, note=""):
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
        unsafe_allow_html=True
    )

def chart_theme(fig, height=360):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    return fig


# ----------------------------- SINGLE-PAGE DASHBOARD -----------------------------
try:
    with st.spinner("Loading flight data and evaluating models..."):
        operations, flights, duplicates_removed = load_and_prepare_data()
        model_bundle = train_models(flights)
except Exception as exc:
    st.error(f"Could not load or process the data: {exc}")
    st.info("Check the three CSV files inside data/raw/janflights, data/raw/febflights, and data/raw/marchflights.")
    st.stop()

results_df = model_bundle["results"]
best_name = results_df.iloc[0]["Model"]
delay_pct = flights["ARR_DEL15"].mean() * 100
cancel_pct = operations["CANCELLED"].mean() * 100
divert_pct = operations["DIVERTED"].mean() * 100
date_min = operations["FL_DATE"].min().strftime("%d %b %Y")
date_max = operations["FL_DATE"].max().strftime("%d %b %Y")

st.markdown(f"""
<div class="hero">
  <div class="eyebrow">DATA SCIENCE PROJECT • JAN–MAR 2026</div>
  <div class="hero-title">✈️ Flight Delay Analysis</div>
  <div class="hero-sub">Explore flight delay patterns, compare airlines, and evaluate two models that predict arrival delays of 15 minutes or more. Data: <b>{date_min} – {date_max}</b>.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 1. Dataset at a glance")
k1, k2, k3, k4 = st.columns(4)
with k1: kpi_card("TOTAL FLIGHTS", f"{len(operations):,}", "After removing duplicates")
with k2: kpi_card("DELAY RATE", f"{delay_pct:.1f}%", "Eligible flights delayed 15+ min")
with k3: kpi_card("CANCELLATION RATE", f"{cancel_pct:.2f}%", "Of all recorded flights")
with k4: kpi_card("DIVERSION RATE", f"{divert_pct:.2f}%", "Of all recorded flights")

st.markdown("### 2. Explore the data")
left, right = st.columns(2, gap="large")
with left:
    # Aggregate strictly by calendar month so the chart always has exactly 3 bars.
    monthly = flights.groupby(flights["FL_DATE"].dt.to_period("M")).agg(
        Flights=("ARR_DEL15", "size"), DelayRate=("ARR_DEL15", "mean")
    ).reset_index(names="MonthPeriod")
    monthly["Month"] = monthly["MonthPeriod"].dt.strftime("%B %Y")
    monthly["Delay rate (%)"] = monthly["DelayRate"] * 100
    month_order = ["January 2026", "February 2026", "March 2026"]
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("Month")
    fig = px.bar(
        monthly, x="Month", y="Delay rate (%)", text="Delay rate (%)",
        color="Month", category_orders={"Month": month_order},
        color_discrete_map={"January 2026": "#5bbdb1", "February 2026": "#2dd4bf", "March 2026": "#fb7185"},
        hover_data={"Flights": ":,"}, title="Monthly Arrival-Delay Rate"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="Month", yaxis_title="Delay rate (%)", showlegend=False,
                      xaxis={"type": "category", "tickangle": 0})
    st.plotly_chart(chart_theme(fig, 350), width="stretch")
with right:
    status = pd.DataFrame({
        "Arrival status": ["Not delayed 15+ min", "Delayed 15+ min"],
        "Flights": [(flights["ARR_DEL15"] == 0).sum(), (flights["ARR_DEL15"] == 1).sum()]
    })
    fig = px.pie(status, names="Arrival status", values="Flights", hole=.55,
                 title="Arrival-delay split",
                 color="Arrival status",
                 color_discrete_map={"Not delayed 15+ min": "#2dd4bf", "Delayed 15+ min": "#fb7185"})
    fig.update_traces(textposition="inside", textinfo="percent")
    st.plotly_chart(chart_theme(fig, 350), width="stretch")

carrier = flights.groupby("OP_UNIQUE_CARRIER").agg(
    Flights=("ARR_DEL15", "size"), DelayRate=("ARR_DEL15", "mean")
).reset_index()
carrier = carrier[carrier["Flights"] >= 500].copy()
carrier["Delay rate (%)"] = carrier["DelayRate"] * 100
carrier = carrier.sort_values("Delay rate (%)", ascending=False).head(12)
fig = px.bar(carrier.sort_values("Delay rate (%)"), x="Delay rate (%)", y="OP_UNIQUE_CARRIER",
             orientation="h", color="Delay rate (%)",
             color_continuous_scale=["#2dd4bf", "#fb7185"],
             title="Airlines with the highest observed delay rates (minimum 500 flights)",
             hover_data={"Flights": ":,"})
fig.update_coloraxes(showscale=False)
st.plotly_chart(chart_theme(fig, 420), width="stretch")

st.markdown("### 3. Machine-learning model comparison")
st.caption(
    f"Models train on {', '.join(model_bundle['train_months'])} and are tested on "
    f"{model_bundle['test_month']}. To keep the dashboard responsive, training uses "
    f"{model_bundle['train_rows']:,} rows and evaluation uses {model_bundle['test_rows']:,} rows."
)
pretty = results_df.copy()
metric_cols = ["Accuracy", "Precision", "Recall", "F1_Score", "ROC_AUC"]
for col in metric_cols:
    pretty[col] = (pretty[col] * 100).round(2)
pretty = pretty.rename(columns={
    "Accuracy": "Accuracy (%)", "Precision": "Precision (%)", "Recall": "Recall (%)",
    "F1_Score": "F1-score (%)", "ROC_AUC": "ROC-AUC (%)"
})
st.dataframe(pretty, width="stretch", hide_index=True)

chart_df = results_df.melt(id_vars="Model", value_vars=metric_cols,
                           var_name="Metric", value_name="Score")
chart_df["Score (%)"] = chart_df["Score"] * 100
fig = px.bar(chart_df, x="Metric", y="Score (%)", color="Model", barmode="group",
             color_discrete_map={"Logistic Regression": "#2dd4bf", "Random Forest": "#fb7185"},
             title="Performance metrics (%)", text="Score (%)")
fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
st.plotly_chart(chart_theme(fig, 380), width="stretch")

st.info(
    f"**Best model by delayed-flight F1-score: {best_name}.** "
    "Accuracy shows overall correctness; recall tells us how many delayed flights were detected; "
    "F1-score balances precision and recall."
)

model_choice = st.selectbox("View detailed results for", list(model_bundle["models"].keys()))
y_test = model_bundle["y_test"]
predictions = model_bundle["predictions"][model_choice]
with st.expander("Classification report and confusion matrix", expanded=True):
    report_text = classification_report(
        y_test, predictions,
        target_names=["Not delayed", "Delayed 15+ minutes"],
        digits=2, zero_division=0
    )
    st.code(report_text, language="text")
    cm = confusion_matrix(y_test, predictions, labels=[0, 1])
    fig = px.imshow(cm, text_auto=True, aspect="auto",
                    x=["Predicted not delayed", "Predicted delayed"],
                    y=["Actual not delayed", "Actual delayed"],
                    color_continuous_scale=[[0, "#102239"], [0.5, "#1c8f89"], [1, "#fb7185"]],
                    title="Confusion matrix")
    fig.update_layout(**PLOT_LAYOUT, height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")

st.markdown("### 4. Try a sample flight prediction")
st.caption("This is an estimate based on scheduled flight details and historical patterns, not a live airline or weather forecast.")
carriers = sorted(flights["OP_UNIQUE_CARRIER"].dropna().astype(str).unique())
airports = sorted(set(flights["ORIGIN"].dropna().astype(str)) | set(flights["DEST"].dropna().astype(str)))
a, b, c = st.columns(3)
with a:
    pred_carrier = st.selectbox("Airline", carriers)
    pred_origin = st.selectbox("Origin airport", airports, index=0)
with b:
    pred_dest = st.selectbox("Destination airport", airports, index=min(1, len(airports)-1))
    pred_month = st.selectbox("Month", [1, 2, 3], format_func=lambda m: {1:"January", 2:"February", 3:"March"}[m])
with c:
    pred_dep = st.slider("Scheduled departure hour", 0, 23, 9)
    pred_arr = st.slider("Scheduled arrival hour", 0, 23, 12)
pred_day = st.slider("Day of month", 1, 31, 15)
pred_weekday = st.selectbox("Day of week", list(range(7)),
                            format_func=lambda d: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][d])
distance_default = float(flights.loc[
    (flights["ORIGIN"] == pred_origin) & (flights["DEST"] == pred_dest), "DISTANCE"
].median()) if ((flights["ORIGIN"] == pred_origin) & (flights["DEST"] == pred_dest)).any() else 500.0
distance = st.number_input("Distance (miles)", min_value=1.0, max_value=7000.0,
                           value=max(1.0, min(7000.0, distance_default)), step=25.0)
if st.button("Estimate delay risk", width="stretch"):
    input_row = pd.DataFrame([{
        "OP_UNIQUE_CARRIER": pred_carrier, "ORIGIN": pred_origin, "DEST": pred_dest,
        "CRS_DEP_TIME": pred_dep * 100, "CRS_ARR_TIME": pred_arr * 100,
        "DISTANCE": distance, "Month": pred_month, "DayOfWeek": pred_weekday,
        "DAY_OF_MONTH": pred_day, "ScheduledDepHour": pred_dep, "ScheduledArrHour": pred_arr
    }])[model_bundle["feature_columns"]]
    probability = float(model_bundle["models"][best_name].predict_proba(input_row)[0, 1])
    x, y = st.columns(2)
    with x:
        st.metric("Estimated delay probability", f"{probability*100:.1f}%")
    with y:
        if probability >= 0.5:
            st.warning("Prediction: likely delayed by 15+ minutes")
        else:
            st.success("Prediction: likely not delayed by 15+ minutes")

st.markdown("---")
st.caption("Data source: U.S. BTS / TranStats On-Time Reporting. Workflow: data cleaning → exploration → model training → evaluation. For academic analysis only.")
