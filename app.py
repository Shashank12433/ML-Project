import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="OrderPulse AI · Delivery Prediction Dashboard",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom Executive Dark Glassmorphism Theme & Keyframe Micro-Interactions
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
    --bg-primary: #070B14;
    --bg-card: rgba(15, 23, 42, 0.72);
    --bg-card-hover: rgba(22, 33, 58, 0.88);
    --border-subtle: rgba(148, 163, 184, 0.14);
    --border-accent: rgba(249, 115, 22, 0.45);
    --accent-primary: #F97316;
    --accent-secondary: #FB923C;
    --accent-cyan: #38BDF8;
    --emerald: #10B981;
    --rose: #F43F5E;
    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Global Typography & App Canvas */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(249, 115, 22, 0.11) 0%, transparent 38%),
        radial-gradient(circle at 88% 14%, rgba(56, 189, 248, 0.09) 0%, transparent 40%),
        radial-gradient(circle at 50% 95%, rgba(16, 185, 129, 0.06) 0%, transparent 45%),
        linear-gradient(180deg, #070B14 0%, #0B1120 100%);
    color: var(--text-main);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 28, 0.92) !important;
    border-right: 1px solid var(--border-subtle);
    backdrop-filter: blur(16px);
}

/* Keyframe Animations */
@keyframes fadeSlideUp {
    0% {
        opacity: 0;
        transform: translateY(16px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes popReveal {
    0% {
        opacity: 0;
        transform: scale(0.96) translateY(12px);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

@keyframes pulseBeacon {
    0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.65);
    }
    50% {
        transform: scale(1.15);
        box-shadow: 0 0 0 7px rgba(16, 185, 129, 0);
    }
}

@keyframes shimmerSweep {
    0% {
        transform: translateX(-120%) skewX(-20deg);
    }
    100% {
        transform: translateX(260%) skewX(-20deg);
    }
}

@keyframes growWidth {
    0% {
        width: 0%;
    }
}

@keyframes drawRing {
    from {
        stroke-dashoffset: 282.74;
    }
}

/* Hero Banner */
.hero-shell {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.88) 0%, rgba(30, 41, 59, 0.68) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 20px 45px -20px rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(16px);
    animation: fadeSlideUp 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.hero-shell::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #F97316, #38BDF8, transparent);
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 13px;
    border-radius: 999px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.32);
    color: #6EE7B7;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
    animation: pulseBeacon 2s infinite;
}

.hero-title {
    font-size: 2.05rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.18;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #94A3B8;
    font-size: 0.98rem;
    margin: 0;
    max-width: 780px;
    line-height: 1.55;
}

/* Top KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

@media (max-width: 900px) {
    .kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 18px 20px;
    backdrop-filter: blur(12px);
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.28s ease, box-shadow 0.28s ease;
    animation: fadeSlideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.kpi-card:nth-child(1) { animation-delay: 0.05s; }
.kpi-card:nth-child(2) { animation-delay: 0.12s; }
.kpi-card:nth-child(3) { animation-delay: 0.19s; }
.kpi-card:nth-child(4) { animation-delay: 0.26s; }

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(249, 115, 22, 0.45);
    box-shadow: 0 14px 30px -12px rgba(249, 115, 22, 0.22);
}

.kpi-label {
    font-size: 0.76rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94A3B8;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.02em;
    font-family: 'JetBrains Mono', monospace;
}

.kpi-foot {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 4px;
}

/* Form & Container Styling */
div[data-testid="stForm"] {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
    padding: 24px 26px;
    backdrop-filter: blur(14px);
    box-shadow: 0 16px 36px -18px rgba(0, 0, 0, 0.7);
    transition: border-color 0.3s ease;
}

div[data-testid="stForm"]:hover {
    border-color: rgba(148, 163, 184, 0.28);
}

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.95rem;
    font-weight: 700;
    color: #F1F5F9;
    padding-bottom: 10px;
    margin-bottom: 14px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.14);
}

.section-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 8px;
    background: rgba(249, 115, 22, 0.16);
    border: 1px solid rgba(249, 115, 22, 0.35);
    color: #FB923C;
    font-size: 0.85rem;
}

/* Animated Primary Submit & Download Buttons */
div[data-testid="stFormSubmitButton"] > button,
div[data-testid="stDownloadButton"] > button {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #F97316 0%, #EA580C 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    letter-spacing: 0.01em !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 12px !important;
    padding: 0.72rem 1.4rem !important;
    box-shadow: 0 10px 24px -6px rgba(249, 115, 22, 0.48) !important;
    transition: all 0.28s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

div[data-testid="stFormSubmitButton"] > button::after,
div[data-testid="stDownloadButton"] > button::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 45%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.32), transparent);
    transform: translateX(-140%) skewX(-20deg);
}

div[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 16px 32px -6px rgba(249, 115, 22, 0.65) !important;
    background: linear-gradient(135deg, #FB923C 0%, #F97316 100%) !important;
}

div[data-testid="stFormSubmitButton"] > button:hover::after,
div[data-testid="stDownloadButton"] > button:hover::after {
    animation: shimmerSweep 0.85s ease forwards;
}

div[data-testid="stFormSubmitButton"] > button:active,
div[data-testid="stDownloadButton"] > button:active {
    transform: translateY(1px) scale(0.985) !important;
}

/* Secondary Preset & Demo Buttons */
div[data-testid="stButton"] > button {
    background: rgba(30, 41, 59, 0.75) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(148, 163, 184, 0.22) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    transition: all 0.22s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    border-color: rgba(249, 115, 22, 0.55) !important;
    background: rgba(249, 115, 22, 0.14) !important;
    color: #FFFFFF !important;
    box-shadow: 0 8px 20px -8px rgba(249, 115, 22, 0.4) !important;
}

div[data-testid="stButton"] > button:active {
    transform: scale(0.97) !important;
}

/* Input Hover & Focus Glow */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(15, 23, 42, 0.9) !important;
    border-color: rgba(148, 163, 184, 0.22) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover {
    border-color: rgba(249, 115, 22, 0.5) !important;
}

div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: #F97316 !important;
    box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2) !important;
}

/* Styled Navigation Tabs */
button[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: #94A3B8 !important;
    padding: 10px 18px !important;
    border-radius: 10px 10px 0 0 !important;
    transition: all 0.22s ease !important;
}

button[data-baseweb="tab"]:hover {
    color: #F8FAFC !important;
    background: rgba(255, 255, 255, 0.04) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FB923C !important;
    background: rgba(249, 115, 22, 0.08) !important;
}

/* Animated Prediction Result Card */
.result-card {
    animation: popReveal 0.52s cubic-bezier(0.22, 1, 0.36, 1) both;
    border-radius: 20px;
    padding: 26px 28px;
    margin-top: 18px;
    backdrop-filter: blur(16px);
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 26px;
    align-items: center;
}

@media (max-width: 720px) {
    .result-card {
        grid-template-columns: 1fr;
        text-align: center;
    }
}

.result-yes {
    background: linear-gradient(135deg, rgba(6, 78, 59, 0.42) 0%, rgba(15, 23, 42, 0.88) 100%);
    border: 1px solid rgba(16, 185, 129, 0.45);
    box-shadow: 0 20px 45px -18px rgba(16, 185, 129, 0.35);
}

.result-no {
    background: linear-gradient(135deg, rgba(136, 19, 55, 0.42) 0%, rgba(15, 23, 42, 0.88) 100%);
    border: 1px solid rgba(244, 63, 94, 0.45);
    box-shadow: 0 20px 45px -18px rgba(244, 63, 94, 0.35);
}

.gauge-wrap {
    position: relative;
    width: 124px;
    height: 124px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.gauge-svg {
    transform: rotate(-90deg);
    width: 124px;
    height: 124px;
}

.gauge-progress {
    animation: drawRing 1.05s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.gauge-center {
    position: absolute;
    text-align: center;
}

.gauge-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1.1;
}

.gauge-sub {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-top: 2px;
}

.verdict-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.tag-yes {
    background: rgba(16, 185, 129, 0.18);
    color: #6EE7B7;
    border: 1px solid rgba(16, 185, 129, 0.35);
}

.tag-no {
    background: rgba(244, 63, 94, 0.18);
    color: #FDA4AF;
    border: 1px solid rgba(244, 63, 94, 0.35);
}

.verdict-headline {
    font-size: 1.45rem;
    font-weight: 800;
    color: #F8FAFC;
    margin: 0 0 6px 0;
}

.verdict-desc {
    font-size: 0.9rem;
    color: #CBD5E1;
    margin: 0 0 16px 0;
}

.prob-row {
    margin-bottom: 10px;
}

.prob-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 5px;
}

.prob-track {
    width: 100%;
    height: 9px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.9);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.prob-fill-yes {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #059669, #34D399);
    animation: growWidth 0.95s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.prob-fill-no {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #E11D48, #FB7185);
    animation: growWidth 0.95s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
}

.info-chip {
    font-size: 0.76rem;
    font-weight: 600;
    color: #CBD5E1;
    background: rgba(30, 41, 59, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.18);
    padding: 4px 10px;
    border-radius: 8px;
}

/* Insight Breakdown Card */
.insight-box {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 16px;
    animation: fadeSlideUp 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Artifact & Dataset Loaders
# ---------------------------------------------------------------------------
@st.cache_resource
def load_artifacts(pkl_path: str = "ML_Project_pred.pkl"):
    bundle = joblib.load(pkl_path)
    return bundle["model"], bundle["OE"], bundle["OHE"]


@st.cache_data
def load_dataset(csv_path: str = "online food delivery dataset.csv"):
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        return pd.DataFrame()


model, oe, ohe = load_artifacts()
raw_dataset = load_dataset()

geo_lookup = {}
if not raw_dataset.empty:
    geo_df = (
        raw_dataset[["Pin code", "latitude", "longitude"]]
        .drop_duplicates(subset=["Pin code"])
        .sort_values("Pin code")
    )
    geo_lookup = geo_df.set_index("Pin code").to_dict(orient="index")

FEEDBACK_DISPLAY = {"Positive": "Positive", "Negative": "Negative "}
OCCUPATION_DISPLAY = {
    "Student": "Student",
    "Employee": "Employee",
    "Self Employed": "Self Employeed",
    "Housewife": "House wife",
}


def get_coords_for_pin(pin: int):
    coords = geo_lookup.get(int(pin), {"latitude": 12.9766, "longitude": 77.5993})
    return float(coords["latitude"]), float(coords["longitude"])


def build_sample_batch_df() -> pd.DataFrame:
    rows = [
        {"Age": 22, "Gender": "Female", "Marital Status": "Single", "Occupation": "Student", "Monthly Income": "No Income", "Educational Qualifications": "Post Graduate", "Family size": 4, "Customer Type": "Frequent", "Feedback": "Positive", "Pin code": 560001},
        {"Age": 24, "Gender": "Female", "Marital Status": "Single", "Occupation": "Student", "Monthly Income": "Below Rs.10000", "Educational Qualifications": "Graduate", "Family size": 3, "Customer Type": "Regular", "Feedback": "Positive", "Pin code": 560009},
        {"Age": 28, "Gender": "Male", "Marital Status": "Married", "Occupation": "Employee", "Monthly Income": "More than 50000", "Educational Qualifications": "Post Graduate", "Family size": 4, "Customer Type": "Frequent", "Feedback": "Positive", "Pin code": 560038},
        {"Age": 26, "Gender": "Female", "Marital Status": "Single", "Occupation": "Employee", "Monthly Income": "25001 to 50000", "Educational Qualifications": "Graduate", "Family size": 2, "Customer Type": "Regular", "Feedback": "Positive", "Pin code": 560076},
        {"Age": 30, "Gender": "Male", "Marital Status": "Married", "Occupation": "Self Employeed", "Monthly Income": "More than 50000", "Educational Qualifications": "Graduate", "Family size": 5, "Customer Type": "Frequent", "Feedback": "Positive", "Pin code": 560066},
        {"Age": 25, "Gender": "Female", "Marital Status": "Married", "Occupation": "House wife", "Monthly Income": "No Income", "Educational Qualifications": "Graduate", "Family size": 4, "Customer Type": "Regular", "Feedback": "Positive", "Pin code": 560011},
        {"Age": 21, "Gender": "Male", "Marital Status": "Single", "Occupation": "Student", "Monthly Income": "No Income", "Educational Qualifications": "Graduate", "Family size": 2, "Customer Type": "Regular", "Feedback": "Negative ", "Pin code": 560046},
        {"Age": 21, "Gender": "Male", "Marital Status": "Single", "Occupation": "Student", "Monthly Income": "No Income", "Educational Qualifications": "Graduate", "Family size": 2, "Customer Type": "Regular", "Feedback": "Negative ", "Pin code": 560032},
        {"Age": 22, "Gender": "Male", "Marital Status": "Married", "Occupation": "Employee", "Monthly Income": "No Income", "Educational Qualifications": "Graduate", "Family size": 2, "Customer Type": "New", "Feedback": "Negative ", "Pin code": 560046},
        {"Age": 22, "Gender": "Male", "Marital Status": "Married", "Occupation": "Student", "Monthly Income": "More than 50000", "Educational Qualifications": "Post Graduate", "Family size": 4, "Customer Type": "New", "Feedback": "Negative ", "Pin code": 560046},
    ]
    for r in rows:
        lat, lon = get_coords_for_pin(r["Pin code"])
        r["latitude"] = lat
        r["longitude"] = lon
    return pd.DataFrame(rows)[
        [
            "Age",
            "Gender",
            "Marital Status",
            "Occupation",
            "Monthly Income",
            "Educational Qualifications",
            "Family size",
            "Customer Type",
            "latitude",
            "longitude",
            "Pin code",
            "Feedback",
        ]
    ]


def build_feature_matrix(input_df: pd.DataFrame) -> pd.DataFrame:
    df = input_df.copy()
    df["Feedback"] = df["Feedback"].replace({"Negative": "Negative "})
    df["Occupation"] = df["Occupation"].replace(
        {
            "Self Employed": "Self Employeed",
            "Housewife": "House wife",
        }
    )

    ohe_cols = list(ohe.feature_names_in_)
    oe_cols = list(oe.feature_names_in_)

    ohe_encoded = pd.DataFrame(
        ohe.transform(df[ohe_cols]),
        columns=ohe.get_feature_names_out(),
    )
    oe_encoded = pd.DataFrame(
        oe.transform(df[oe_cols]),
        columns=oe_cols,
    )

    neutral_idx = float(np.median(model._fit_X[:, 0]))
    idx_series = pd.Series(np.full(len(df), neutral_idx), name="index")

    return pd.concat(
        [
            idx_series.reset_index(drop=True),
            ohe_encoded.reset_index(drop=True),
            idx_series.reset_index(drop=True),
            oe_encoded.reset_index(drop=True),
        ],
        axis=1,
    )


def render_prediction_card(pred: int, probs: np.ndarray, profile: dict) -> str:
    is_yes = pred == 1
    conf = float(probs[1] if is_yes else probs[0])
    yes_pct = float(probs[1]) * 100
    no_pct = float(probs[0]) * 100

    circumference = 282.74
    dash_offset = circumference * (1.0 - conf)
    stroke_color = "#10B981" if is_yes else "#F43F5E"
    card_cls = "result-card result-yes" if is_yes else "result-card result-no"
    tag_cls = "verdict-tag tag-yes" if is_yes else "verdict-tag tag-no"
    tag_text = "High Conversion Likelihood · Class 1" if is_yes else "Churn / Non-Order Risk · Class 0"
    headline = "Likely to Place Order (Yes)" if is_yes else "Unlikely to Place Order (No)"
    desc = (
        "Nearest-neighbor behavioral & geo-demographic patterns strongly favor order completion."
        if is_yes
        else "Nearest-neighbor profile matches customers who did not complete or repeat an order."
    )

    return (
        f'<div class="{card_cls}">'
        f'<div class="gauge-wrap">'
        f'<svg class="gauge-svg" viewBox="0 0 100 100">'
        f'<circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.09)" stroke-width="9"></circle>'
        f'<circle class="gauge-progress" cx="50" cy="50" r="45" fill="none" stroke="{stroke_color}" '
        f'stroke-width="9" stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{dash_offset:.2f}"></circle>'
        f'</svg>'
        f'<div class="gauge-center">'
        f'<div class="gauge-pct">{conf * 100:.0f}%</div>'
        f'<div class="gauge-sub">Confidence</div>'
        f'</div>'
        f'</div>'
        f'<div>'
        f'<span class="{tag_cls}">{tag_text}</span>'
        f'<h3 class="verdict-headline">{headline}</h3>'
        f'<p class="verdict-desc">{desc}</p>'
        f'<div class="prob-row">'
        f'<div class="prob-meta"><span>Order Probability · Yes (1)</span><span>{yes_pct:.1f}%</span></div>'
        f'<div class="prob-track"><div class="prob-fill-yes" style="width: {yes_pct:.1f}%;"></div></div>'
        f'</div>'
        f'<div class="prob-row">'
        f'<div class="prob-meta"><span>Non-Order Probability · No (0)</span><span>{no_pct:.1f}%</span></div>'
        f'<div class="prob-track"><div class="prob-fill-no" style="width: {no_pct:.1f}%;"></div></div>'
        f'</div>'
        f'<div class="chip-row">'
        f'<span class="info-chip">Age {profile["Age"]} · {profile["Gender"]}</span>'
        f'<span class="info-chip">{profile["Occupation_UI"]}</span>'
        f'<span class="info-chip">{profile["Monthly Income"]}</span>'
        f'<span class="info-chip">{profile["Customer Type"]} · {profile["Feedback_UI"]} Feedback</span>'
        f'<span class="info-chip">PIN {profile["Pin code"]}</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Session State Defaults & Quick-Fill Presets
# ---------------------------------------------------------------------------
init_lat, init_lon = get_coords_for_pin(560001)
DEFAULT_STATE = {
    "age": 24,
    "gender": "Female",
    "marital_status": "Single",
    "occupation_label": "Student",
    "income": "Below Rs.10000",
    "education": "Graduate",
    "family_size": 3,
    "customer_type": "Regular",
    "feedback_label": "Positive",
    "pin_code": 560001,
    "latitude": init_lat,
    "longitude": init_lon,
    "last_synced_pin": 560001,
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "use_demo_batch" not in st.session_state:
    st.session_state["use_demo_batch"] = False


def apply_preset(preset_type: str):
    if preset_type == "high":
        lat, lon = get_coords_for_pin(560001)
        st.session_state.update(
            {
                "age": 22,
                "gender": "Female",
                "marital_status": "Single",
                "occupation_label": "Student",
                "income": "No Income",
                "education": "Post Graduate",
                "family_size": 4,
                "customer_type": "Frequent",
                "feedback_label": "Positive",
                "pin_code": 560001,
                "latitude": lat,
                "longitude": lon,
                "last_synced_pin": 560001,
            }
        )
        st.toast("Loaded High-Retention Customer profile (Predicts Yes)", icon="✨")
    elif preset_type == "risk":
        lat, lon = get_coords_for_pin(560046)
        st.session_state.update(
            {
                "age": 21,
                "gender": "Male",
                "marital_status": "Single",
                "occupation_label": "Student",
                "income": "No Income",
                "education": "Graduate",
                "family_size": 2,
                "customer_type": "Regular",
                "feedback_label": "Negative",
                "pin_code": 560046,
                "latitude": lat,
                "longitude": lon,
                "last_synced_pin": 560046,
            }
        )
        st.toast("Loaded At-Risk / Churn Customer profile (Predicts No)", icon="⚠️")
    else:
        st.session_state.update(DEFAULT_STATE)
        st.toast("Reset form to default values", icon="🔄")


# ---------------------------------------------------------------------------
# Sidebar Telemetry Panel
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛵 OrderPulse AI")
    st.caption("Bengaluru Online Food Delivery Intelligence")
    st.divider()
    st.markdown("**Model Artifact**")
    st.code("ML_Project_pred.pkl", language="text")
    st.markdown(
        f"- **Estimator:** `KNeighborsClassifier`\n"
        f"- **Neighbors ($k$):** `{model.n_neighbors}` ({model.weights})\n"
        f"- **Distance Metric:** `{model.effective_metric_}`\n"
        f"- **Input Vector:** `{model.n_features_in_}` aligned features\n"
        f"- **Encoders:** `OneHotEncoder` + `OrdinalEncoder`"
    )
    st.divider()
    st.markdown("**Demo Walkthrough**")
    st.info(
        "1. Click **High-Retention Profile** → predicts **Yes (80%)**.\n"
        "2. Click **At-Risk Profile** → predicts **No (60%)**.\n"
        "3. Open **Batch CSV Scoring** and upload `sample_batch_customers.csv` or click **Load Sample Batch CSV**."
    )


# ---------------------------------------------------------------------------
# Hero Header & Top KPI Strip
# ---------------------------------------------------------------------------
train_samples = model._fit_X.shape[0]
train_pos_rate = float(np.mean(model._y == 1)) * 100
pin_count = len(oe.categories_[5])

hero_html = (
    '<div class="hero-shell">'
    '<div class="status-pill"><span class="status-dot"></span>Live KNN Inference Engine · 27-Feature Pipeline</div>'
    '<h1 class="hero-title">Online Food Delivery Order Predictor</h1>'
    '<p class="hero-sub">Interactive customer conversion &amp; reorder intelligence powered by your trained '
    'K-Nearest Neighbors classifier, dual categorical/ordinal encoders, and Bengaluru pin-code telemetry.</p>'
    '</div>'
    '<div class="kpi-grid">'
    '<div class="kpi-card">'
    '<div class="kpi-label">Classifier Architecture</div>'
    f'<div class="kpi-value">KNN (k={model.n_neighbors})</div>'
    '<div class="kpi-foot">Uniform Euclidean voting</div>'
    '</div>'
    '<div class="kpi-card">'
    '<div class="kpi-label">Training Cohort</div>'
    f'<div class="kpi-value">{train_samples} Rows</div>'
    f'<div class="kpi-foot">{train_pos_rate:.1f}% positive order rate</div>'
    '</div>'
    '<div class="kpi-card">'
    '<div class="kpi-label">Feature Engineering</div>'
    f'<div class="kpi-value">{model.n_features_in_} Dims</div>'
    '<div class="kpi-foot">19 OHE + 6 OE + 2 Index</div>'
    '</div>'
    '<div class="kpi-card">'
    '<div class="kpi-label">Geo Coverage</div>'
    f'<div class="kpi-value">{pin_count} PINs</div>'
    '<div class="kpi-foot">Auto-synced Lat / Lon</div>'
    '</div>'
    '</div>'
)
st.markdown(hero_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Main Dashboard Tabs
# ---------------------------------------------------------------------------
tab_single, tab_batch, tab_insights = st.tabs(
    [
        "🎯 Single Customer Prediction",
        "📂 Batch CSV Scoring",
        "📊 Dataset & Model Insights",
    ]
)

# === TAB 1: SINGLE CUSTOMER PREDICTION ===
with tab_single:
    p_col1, p_col2, p_col3, _ = st.columns([1.45, 1.35, 1.0, 2.2])
    with p_col1:
        st.button("✨ High-Retention Profile", on_click=apply_preset, args=("high",), use_container_width=True)
    with p_col2:
        st.button("⚠️ At-Risk Profile", on_click=apply_preset, args=("risk",), use_container_width=True)
    with p_col3:
        st.button("🔄 Reset", on_click=apply_preset, args=("reset",), use_container_width=True)

    with st.form("prediction_form"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                '<div class="section-header"><span class="section-badge">1</span>Demographics &amp; Household</div>',
                unsafe_allow_html=True,
            )
            age = st.number_input("Age", min_value=15, max_value=80, step=1, key="age")
            gender = st.selectbox("Gender", options=list(ohe.categories_[0]), key="gender")
            marital_status = st.selectbox("Marital Status", options=list(ohe.categories_[1]), key="marital_status")
            occupation_label = st.selectbox(
                "Occupation", options=list(OCCUPATION_DISPLAY.keys()), key="occupation_label"
            )
            education = st.selectbox(
                "Educational Qualifications", options=list(ohe.categories_[3]), key="education"
            )
            family_size = st.number_input("Family Size", min_value=1, max_value=15, step=1, key="family_size")

        with col2:
            st.markdown(
                '<div class="section-header"><span class="section-badge">2</span>Engagement &amp; Bengaluru Zone</div>',
                unsafe_allow_html=True,
            )
            income = st.selectbox("Monthly Income", options=list(oe.categories_[1]), key="income")
            customer_type = st.selectbox("Customer Type", options=list(ohe.categories_[4]), key="customer_type")
            feedback_label = st.selectbox(
                "Latest Customer Feedback", options=list(FEEDBACK_DISPLAY.keys()), key="feedback_label"
            )

            known_pins = [int(p) for p in oe.categories_[5]]
            pin_code = st.selectbox("Pin Code (Bengaluru)", options=known_pins, key="pin_code")

            if st.session_state["last_synced_pin"] != pin_code:
                new_lat, new_lon = get_coords_for_pin(pin_code)
                st.session_state["latitude"] = new_lat
                st.session_state["longitude"] = new_lon
                st.session_state["last_synced_pin"] = pin_code

            geo_c1, geo_c2 = st.columns(2)
            with geo_c1:
                latitude = st.number_input("Latitude", format="%.4f", key="latitude")
            with geo_c2:
                longitude = st.number_input("Longitude", format="%.4f", key="longitude")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Run Reorder Prediction", use_container_width=True)

    if submitted:
        # Sync coordinates if user changed Pin Code right before clicking submit
        if st.session_state["last_synced_pin"] != pin_code:
            latitude, longitude = get_coords_for_pin(pin_code)

        with st.status("Executing feature engineering & KNN scoring...", expanded=False) as status:
            time.sleep(0.25)
            input_row = pd.DataFrame(
                [
                    {
                        "Gender": gender,
                        "Marital Status": marital_status,
                        "Occupation": OCCUPATION_DISPLAY[occupation_label],
                        "Educational Qualifications": education,
                        "Customer Type": customer_type,
                        "Feedback": FEEDBACK_DISPLAY[feedback_label],
                        "Age": age,
                        "Monthly Income": income,
                        "Family size": family_size,
                        "latitude": latitude,
                        "longitude": longitude,
                        "Pin code": pin_code,
                    }
                ]
            )
            X_ready = build_feature_matrix(input_row)
            pred = int(model.predict(X_ready)[0])
            probs = model.predict_proba(X_ready)[0]
            status.update(label="Prediction complete · 27 features scored", state="complete", expanded=False)

        st.toast(f"Predicted Outcome: {'Yes (1)' if pred == 1 else 'No (0)'}", icon="✅" if pred == 1 else "⚠️")

        profile_summary = {
            "Age": age,
            "Gender": gender,
            "Occupation_UI": occupation_label,
            "Monthly Income": income,
            "Customer Type": customer_type,
            "Feedback_UI": feedback_label,
            "Pin code": pin_code,
        }
        st.markdown(render_prediction_card(pred, probs, profile_summary), unsafe_allow_html=True)


# === TAB 2: BATCH CSV SCORING ===
with tab_batch:
    st.markdown(
        '<div class="insight-box">'
        '<h4 style="margin:0 0 6px 0; color:#F8FAFC;">Batch Customer Scoring Pipeline</h4>'
        '<p style="margin:0; color:#94A3B8; font-size:0.9rem;">Upload a CSV containing customer attributes—or load the '
        '10-customer sample cohort below—to encode, align, and score all rows simultaneously.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    sample_input_df = build_sample_batch_df()

    b_col1, b_col2, _ = st.columns([1.6, 1.5, 2.9])
    with b_col1:
        if st.button("⚡ Load & Score Sample CSV (10 Rows)", use_container_width=True):
            st.session_state["use_demo_batch"] = True
            st.toast("Loaded 10-customer sample batch CSV", icon="📂")
    with b_col2:
        st.download_button(
            "📥 Download Sample Input CSV",
            data=sample_input_df.to_csv(index=False).encode("utf-8"),
            file_name="sample_batch_customers.csv",
            mime="text/csv",
            use_container_width=True,
        )

    uploaded_file = st.file_uploader("Or upload your own CSV matching dataset schema", type=["csv"])

    batch_df = None
    if uploaded_file is not None:
        st.session_state["use_demo_batch"] = False
        batch_df = pd.read_csv(uploaded_file)
    elif st.session_state.get("use_demo_batch", False):
        batch_df = sample_input_df.copy()

    if batch_df is not None:
        required_cols = list(ohe.feature_names_in_) + list(oe.feature_names_in_)
        missing = [c for c in required_cols if c not in batch_df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            with st.spinner("Encoding and scoring batch records..."):
                X_batch = build_feature_matrix(batch_df)
                preds = model.predict(X_batch)
                probs = model.predict_proba(X_batch)[:, 1]

            results_df = batch_df.copy()
            results_df["Predicted_Output"] = np.where(preds == 1, "Yes", "No")
            results_df["Yes_Probability"] = np.round(probs, 4)

            yes_count = int(np.sum(preds == 1))
            no_count = int(np.sum(preds == 0))
            avg_conf = float(np.mean(np.where(preds == 1, probs, 1.0 - probs))) * 100

            batch_kpis = (
                '<div class="kpi-grid" style="margin-top: 14px;">'
                f'<div class="kpi-card"><div class="kpi-label">Records Scored</div><div class="kpi-value">{len(results_df)}</div><div class="kpi-foot">100% schema matched</div></div>'
                f'<div class="kpi-card"><div class="kpi-label">Predicted Yes</div><div class="kpi-value" style="color:#34D399;">{yes_count}</div><div class="kpi-foot">{yes_count / len(results_df) * 100:.1f}% of cohort</div></div>'
                f'<div class="kpi-card"><div class="kpi-label">Predicted No (At-Risk)</div><div class="kpi-value" style="color:#FB7185;">{no_count}</div><div class="kpi-foot">{no_count / len(results_df) * 100:.1f}% of cohort</div></div>'
                f'<div class="kpi-card"><div class="kpi-label">Mean Confidence</div><div class="kpi-value">{avg_conf:.1f}%</div><div class="kpi-foot">5-NN neighborhood vote</div></div>'
                '</div>'
            )
            st.markdown(batch_kpis, unsafe_allow_html=True)

            st.dataframe(
                results_df,
                use_container_width=True,
                column_config={
                    "Yes_Probability": st.column_config.ProgressColumn(
                        "Yes Probability",
                        help="Estimated probability of customer placing/repeating an order",
                        min_value=0.0,
                        max_value=1.0,
                        format="%.2f",
                    )
                },
            )

            st.download_button(
                "⬇️ Download Scored Predictions CSV",
                data=results_df.to_csv(index=False).encode("utf-8"),
                file_name="food_delivery_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )


# === TAB 3: DATASET & MODEL INSIGHTS ===
with tab_insights:
    if raw_dataset.empty:
        st.warning("Place `online food delivery dataset.csv` in the app folder to view historical cohort analytics.")
    else:
        i_col1, i_col2 = st.columns(2, gap="large")

        with i_col1:
            st.markdown(
                '<div class="insight-box">'
                '<h4 style="margin:0 0 12px 0; color:#F8FAFC;">Order Conversion by Customer Feedback</h4>',
                unsafe_allow_html=True,
            )
            fb_rates = (
                raw_dataset.assign(Feedback_Clean=raw_dataset["Feedback"].str.strip())
                .groupby("Feedback_Clean")["Output"]
                .apply(lambda s: (s == "Yes").mean() * 100)
                .sort_values(ascending=False)
            )
            bars_html = ""
            for label, rate in fb_rates.items():
                fill_cls = "prob-fill-yes" if rate >= 50 else "prob-fill-no"
                bars_html += (
                    f'<div class="prob-row">'
                    f'<div class="prob-meta"><span>{label} Feedback</span><span>{rate:.1f}% Order Rate</span></div>'
                    f'<div class="prob-track"><div class="{fill_cls}" style="width:{rate:.1f}%;"></div></div>'
                    f'</div>'
                )
            st.markdown(bars_html + "</div>", unsafe_allow_html=True)

        with i_col2:
            st.markdown(
                '<div class="insight-box">'
                '<h4 style="margin:0 0 12px 0; color:#F8FAFC;">Order Conversion by Customer Segment</h4>',
                unsafe_allow_html=True,
            )
            seg_rates = (
                raw_dataset.groupby("Customer Type")["Output"]
                .apply(lambda s: (s == "Yes").mean() * 100)
                .sort_values(ascending=False)
            )
            seg_html = ""
            for label, rate in seg_rates.items():
                seg_html += (
                    f'<div class="prob-row">'
                    f'<div class="prob-meta"><span>{label} Customers</span><span>{rate:.1f}% Order Rate</span></div>'
                    f'<div class="prob-track"><div class="prob-fill-yes" style="width:{rate:.1f}%;"></div></div>'
                    f'</div>'
                )
            st.markdown(seg_html + "</div>", unsafe_allow_html=True)

        st.markdown("#### Feature Engineering & Pipeline Schema")
        schema_df = pd.DataFrame(
            [
                {
                    "Pipeline Stage": "1. Index Slot A",
                    "Transformer": "Median Training Index (194.5)",
                    "Input Columns": "index",
                    "Output Dims": 1,
                },
                {
                    "Pipeline Stage": "2. Nominal Encoding",
                    "Transformer": "OneHotEncoder (sparse_output=False)",
                    "Input Columns": "Gender, Marital Status, Occupation, Education, Customer Type, Feedback",
                    "Output Dims": 19,
                },
                {
                    "Pipeline Stage": "3. Index Slot B",
                    "Transformer": "Median Training Index (194.5)",
                    "Input Columns": "index",
                    "Output Dims": 1,
                },
                {
                    "Pipeline Stage": "4. Ordinal & Geo Encoding",
                    "Transformer": "OrdinalEncoder (unknown_value=-1)",
                    "Input Columns": "Age, Monthly Income, Family size, latitude, longitude, Pin code",
                    "Output Dims": 6,
                },
            ]
        )
        st.dataframe(schema_df, hide_index=True, use_container_width=True)