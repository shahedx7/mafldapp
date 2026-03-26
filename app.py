import streamlit as st
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="MASLD Risk Stratifier",
    page_icon="🩺",
    layout="centered"
)

# --- Custom CSS for a Professional Look ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #fcfcfc;
    }
    /* Headers */
    h1 {
        color: #004a99;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Metric Card Styling */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #004a99;
    }
    /* Instructions & Info Boxes */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004a99;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- App Header ---
st.title("🩺 MASLD Clinical Triage Tool")
st.markdown("**Primary Care Referral Pathway | Based on AASLD 2024 Guidelines**")
st.divider()

# --- Input Section in a clean card ---
with st.expander("📝 Enter Patient Lab Data", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (years)", 18, 100, 55)
        plt = st.number_input("Platelets (10⁹/L)", 1, 1000, 210)
    with col2:
        ast = st.number_input("AST (U/L)", 1, 500, 38)
        alt = st.number_input("ALT (U/L)", 1, 500, 42)

# --- Calculation ---
fib4 = (age * ast) / (plt * math.sqrt(alt))

# --- Results Dashboard ---
st.subheader("Clinical Assessment")
c1, c2 = st.columns([1, 2])

with c1:
    st.metric(label="Calculated FIB-4", value=f"{fib4:.2f}")

with c2:
    if fib4 < 1.30:
        st.success("### 🟢 LOW RISK\n**Advanced Fibrosis Unlikely**")
        recommendation = "Manage in Primary Care. Focus on CVD risk. Repeat FIB-4 in 24 months."
        tag = "LOW_RISK"
    elif 1.30 <= fib4 <= 2.67:
        st.warning("### 🟡 INTERMEDIATE RISK\n**Indeterminate Score**")
        recommendation = "Requires second-tier testing (e.g., VCTE/FibroScan) to clarify fibrosis stage."
        tag = "INDETERMINATE"
    else:
        st.error("### 🔴 HIGH RISK\n**Advanced Fibrosis Likely (F3-F4)**")
        recommendation = "Direct Referral to Hepatology for specialized evaluation."
        tag = "HIGH_RISK"

st.info(f"**Recommendation:** {recommendation}")

# --- Referral Export Tool ---
st.divider()
st.subheader("📋 Referral Summary for EMR")
summary = f"""[MASLD TRIAGE REPORT]
-------------------------
Age: {age} | PLT: {plt} | AST: {ast} | ALT: {alt}
Calculated FIB-4 Index: {fib4:.2f}
Classification: {tag}
Clinical Plan: {recommendation}
-------------------------
Generated via MASLD-Triage-v1.0"""

st.code(summary, language="text")

# --- Footer References ---
st.caption("Reference: AASLD Practice Guidance on MASLD (2024). Not a substitute for clinical judgment.")
