import streamlit as st
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="MASLD Precision Triage",
    page_icon="🧬",
    layout="centered"
)

# --- High-End Custom CSS ---
st.markdown("""
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F9FAFB;
    }

    /* Professional Card Styling */
    .clinical-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 20px;
    }

    /* Custom Header */
    .main-header {
        color: #111827;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 5px;
    }

    /* Status Badges */
    .badge {
        padding: 8px 16px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-green { background-color: #DCFCE7; color: #166534; }
    .badge-yellow { background-color: #FEF9C3; color: #854d0e; }
    .badge-red { background-color: #FEE2E2; color: #991b1b; }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<h1 class="main-header">🧬 MASLD Precision Triage</h1>', unsafe_allow_html=True)
st.markdown("<p style='color: #6B7280; font-size: 1.1rem;'>Strategic referral pathway based on AASLD 2024 Practice Guidance</p>", unsafe_allow_html=True)

# --- Input Section (Clean Layout) ---
st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0;'>Patient Lab Metrics</h4>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", 18, 100, 58, help="Patient's current age")
    plt = st.number_input("Platelets (10⁹/L)", 1, 1000, 185)
with col2:
    ast = st.number_input("AST (U/L)", 1, 500, 42)
    alt = st.number_input("ALT (U/L)", 1, 500, 39)
st.markdown('</div>', unsafe_allow_html=True)

# --- Calculation ---
fib4 = (age * ast) / (plt * math.sqrt(alt))

# --- Results Section ---
st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
st.markdown("<h4>Clinical Assessment Score</h4>", unsafe_allow_html=True)

res_col1, res_col2 = st.columns([1, 1.5])

with res_col1:
    st.markdown(f"<h1 style='color: #1F2937; margin:0;'>{fib4:.2f}</h1>", unsafe_allow_html=True)
    st.caption("FIB-4 Index Result")

with res_col2:
    if fib4 < 1.30:
        st.markdown('<span class="badge badge-green">LOW RISK</span>', unsafe_allow_html=True)
        st.markdown("**Management Plan:** Primary Care follow-up. Focus on metabolic health and weight management.")
        tag, color = "Low Risk", "#166534"
    elif 1.30 <= fib4 <= 2.67:
        st.markdown('<span class="badge badge-yellow">INDETERMINATE</span>', unsafe_allow_html=True)
        st.markdown("**Management Plan:** Supplemental testing required. Suggest VCTE (FibroScan) or ELF Score.")
        tag, color = "Indeterminate", "#854d0e"
    else:
        st.markdown('<span class="badge badge-red">HIGH RISK</span>', unsafe_allow_html=True)
        st.markdown("**Management Plan:** Immediate Hepatology referral. High suspicion for F3-F4 advanced fibrosis.")
        tag, color = "High Risk", "#991b1b"

st.markdown('</div>', unsafe_allow_html=True)

# --- Interactive Referral Block ---
st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
st.markdown("<h4>Integration Summary</h4>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.9rem; color: #6B7280;'>Copy the following for EMR clinical notes:</p>", unsafe_allow_html=True)

ref_text = f"MASLD TRIAGE: FIB-4 Score {fib4:.2f} ({tag}). Recommendation: {tag} pathway."
st.code(ref_text, language="text")
st.markdown('</div>', unsafe_allow_html=True)

# --- Institutional Footer ---
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 0.8rem;'>V1.2 Clinical Support Module | Verified against AASLD 2024</p>", unsafe_allow_html=True)
