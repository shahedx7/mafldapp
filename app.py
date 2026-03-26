import streamlit as st
import math

# --- Page Setup ---
st.set_page_config(page_title="MAFLD Consensus Support", page_icon="🇦🇺", layout="wide")

# --- MJA-Inspired Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus+Jakarta+Sans', sans-serif; background-color: #F8FAFC; }
    .main-header { color: #0F172A; font-weight: 800; font-size: 2.2rem; margin-bottom: 0; }
    .section-card { background: white; padding: 2rem; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
    .status-box { padding: 1rem; border-radius: 8px; font-weight: 600; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🇦🇺 MAFLD Clinical Decision Support</h1>', unsafe_allow_html=True)
st.caption("Derived from the MJA 2025 Consensus Statement Summary (Adams et al.)")

# --- Sidebar: Screening Criteria ---
with st.sidebar:
    st.header("Step 1: Screening")
    st.write("Does the patient have:")
    s1 = st.checkbox("Type 2 Diabetes")
    s2 = st.checkbox("Obesity (BMI ≥30)")
    s3 = st.multiselect("Metabolic Risk Factors", 
                        ["Waist >102cm(M)/>88cm(F)", "BP >130/85", "Triglycerides ≥1.7", "HDL <1.0(M)/<1.3(F)", "Pre-diabetes"])
    
    if s1 or s2 or len(s3) >= 2:
        st.success("✅ Assessment Recommended")
        screening_pass = True
    else:
        st.info("Assessment not routinely required")
        screening_pass = False

# --- Main Dashboard ---
if not screening_pass:
    st.warning("Please confirm patient eligibility in the sidebar to begin the clinical pathway.")
else:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Step 2: Fibrosis Risk (FIB-4)")
        c1, c2, c3, c4 = st.columns(4)
        age = c1.number_input("Age", 18, 100, 55)
        ast = c2.number_input("AST (U/L)", 1, 500, 35)
        alt = c3.number_input("ALT (U/L)", 1, 500, 40)
        plt = c4.number_input("Platelets (10⁹/L)", 1, 1000, 200)
        
        # FIB-4 Calc
        fib4 = (age * ast) / (plt * math.sqrt(alt))
        
        # Age-adjusted thresholds (Adams et al. 2025)
        low_threshold = 2.0 if age > 65 else 1.3
        
        if fib4 < low_threshold:
            st.markdown('<div class="status-box" style="background:#DCFCE7; color:#166534;">🟢 LOW RISK (F0-F2)</div>', unsafe_allow_html=True)
            action = "Repeat FIB-4 in 3 years. Focus on lifestyle."
        elif fib4 > 2.7:
            st.markdown('<div class="status-box" style="background:#FEE2E2; color:#991B1B;">🔴 HIGH RISK (Suspected F3-F4)</div>', unsafe_allow_html=True)
            action = "Urgent referral to Liver Specialist/Hepatologist."
        else:
            st.markdown('<div class="status-box" style="background:#FEF9C3; color:#854D0E;">🟡 INDETERMINATE</div>', unsafe_allow_html=True)
            action = "Perform second-line test (FibroScan/ELF) or refer if unavailable."
        
        st.write(f"**Recommendation:** {action}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Step 3: Holistic Health Assessment")
        st.write("Assessment for extra-hepatic conditions is mandatory:")
        st.checkbox("Cardiovascular Risk (CVD Check)")
        st.checkbox("Chronic Kidney Disease (eGFR/uACR)")
        st.checkbox("Obstructive Sleep Apnoea (STOP-Bang)")
        st.checkbox("Cancer Screening (Bowel/Breast/Cervical)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("Clinical Checklist")
        st.markdown("""
        - [ ] **First-line Diagnosis:** Liver Ultrasound [cite: 432]
        - [ ] **Rule out Alcohol:** Screening for harmful use [cite: 446]
        - [ ] **Viral Screen:** Hepatitis B/C if LFTs elevated [cite: 447]
        - [ ] **Iron Study:** Check for overload/HFE [cite: 449]
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("EMR Referral Summary")
        summary = f"MAFLD Assessment (MJA 2025 Guidelines)\nFIB-4: {fib4:.2f}\nRisk: {'High' if fib4>2.7 else 'Low' if fib4<low_threshold else 'Intermediate'}\nPlan: {action}"
        st.code(summary)
        st.markdown('</div>', unsafe_allow_html=True)
