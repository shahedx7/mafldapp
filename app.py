import streamlit as st
import math

# --- Page Config ---
st.set_page_config(page_title="MAFLD Consensus 2025", page_icon="🇦🇺", layout="centered")

# --- Premium Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Plus+Jakarta+Sans', sans-serif;
        background-color: #F3F4F6;
    }
    
    /* Elegant Container */
    .clinical-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        border: 1px solid #F3F4F6;
        margin-bottom: 25px;
    }
    
    /* Section Headers */
    .step-label {
        color: #6366F1;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .main-title {
        color: #111827;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 30px;
    }

    /* Input Styling */
    .stNumberInput, .stMultiSelect {
        margin-bottom: 20px;
    }
    
    /* Result Cards */
    .result-card {
        padding: 24px;
        border-radius: 16px;
        margin-top: 20px;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="step-label">MJA 223 (5) Summary</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">🇦🇺 MAFLD Clinical Pathway</h1>', unsafe_allow_html=True)
st.markdown("---")

# --- STEP 1: ELIGIBILITY ---
st.markdown('<div class="clinical-container">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Step 01</div>', unsafe_allow_html=True)
st.subheader("Patient Screening Eligibility")
col_e1, col_e2 = st.columns(2)
with col_e1:
    diag_t2d = st.toggle("Type 2 Diabetes")
    diag_obese = st.toggle("Obesity (BMI ≥30)")
with col_e2:
    metabolic = st.multiselect("Metabolic Risk Factors (Rec 1)", 
                               ["Central Obesity", "Hypertension", "Hypertriglyceridemia", "Low HDL-C", "Pre-diabetes"])

eligible = diag_t2d or diag_obese or len(metabolic) >= 2
st.markdown('</div>', unsafe_allow_html=True)

if not eligible:
    st.info("Based on the MJA 2025 Consensus, routine screening is not currently indicated for this patient profile.")
else:
    # --- STEP 2: FIB-4 CALCULATION ---
    st.markdown('<div class="clinical-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">Step 02</div>', unsafe_allow_html=True)
    st.subheader("Liver Fibrosis Risk (FIB-4)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: age = st.number_input("Age", 18, 100, 55)
    with col2: ast = st.number_input("AST", 1, 500, 35)
    with col3: alt = st.number_input("ALT", 1, 500, 40)
    with col4: plt = st.number_input("PLT (10⁹/L)", 1, 1000, 200)
    
    fib4 = (age * ast) / (plt * math.sqrt(alt))
    
    # MJA 2025 Cut-offs (Rec 13)
    low_cut = 2.0 if age > 65 else 1.3
    
    if fib4 < low_cut:
        color, bg, status = "#166534", "#DCFCE7", "LOW RISK"
        plan = f"Repeat FIB-4 every 3 years (Rec 15). Focus on lifestyle and CVD risk."
    elif fib4 > 2.7:
        color, bg, status = "#991B1B", "#FEE2E2", "HIGH RISK"
        plan = "Suspected advanced fibrosis (F3-F4). Refer to Liver Specialist / Hepatology."
    else:
        color, bg, status = "#854D0E", "#FEF9C3", "INDETERMINATE"
        plan = "Perform second-line testing (VCTE/FibroScan) or ELF score (Rec 14)."

    st.markdown(f"""
        <div class="result-card" style="background-color: {bg}; border: 1px solid {color}33;">
            <p style="color: {color}; font-weight: 700; margin: 0; font-size: 0.85rem;">ASSESSMENT STATUS</p>
            <h2 style="color: {color}; margin: 5px 0;">{status} (FIB-4: {fib4:.2f})</h2>
            <p style="color: {color}; opacity: 0.8; margin: 0;">{plan}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- STEP 3: HOLISTIC CARE ---
    st.markdown('<div class="clinical-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">Step 03</div>', unsafe_allow_html=True)
    st.subheader("Extra-Hepatic Assessments (Rec 5 & 6)")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.checkbox("Cardiovascular Risk (CVD)")
        st.checkbox("Chronic Kidney Disease (CKD)")
    with col_h2:
        st.checkbox("Obstructive Sleep Apnoea")
        st.checkbox("Cancer Screening (Age-Appropriate)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- REFERENCES ---
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 0.75rem; margin-top: 50px;'>"
            "Source: Adams LA, et al. Assessment of MAFLD in primary care: a consensus statement summary. MJA 2025; 223 (5)."
            "</p>", unsafe_allow_html=True)
