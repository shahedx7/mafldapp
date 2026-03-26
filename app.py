import streamlit as st
import math

st.set_page_config(page_title="MAFLD Risk Stratifier", page_icon="⚖️", layout="centered")

st.title("⚖️ MASLD/MAFLD Clinical Risk Stratifier")
st.markdown("Automated Triage based on AASLD 2024 Practice Guidance")

# --- Inputs ---
with st.container():
    st.subheader("Patient Biochemistry")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age (years)", 18, 100, 55)
        plt = st.number_input("Platelets (10^9/L)", 1, 1000, 210)
    with c2:
        ast = st.number_input("AST (U/L)", 1, 500, 38)
        alt = st.number_input("ALT (U/L)", 1, 500, 42)

# --- Calculation ---
# FIB-4 Formula: (Age * AST) / (Platelets * sqrt(ALT))
fib4 = (age * ast) / (plt * math.sqrt(alt))

st.divider()

# --- Results Logic ---
st.subheader(f"Calculated FIB-4: {fib4:.2f}")

if fib4 < 1.30:
    st.success("🟢 LOW RISK: Advanced Fibrosis Unlikely")
    res_text = "Manage in Primary Care. Focus on CVD risk and metabolic health. Repeat FIB-4 in 2-3 years."
    status = "Low Risk"
elif 1.30 <= fib4 <= 2.67:
    st.warning("🟡 INTERMEDIATE RISK: Indeterminate Score")
    res_text = "Requires second-tier testing. Order VCTE (FibroScan) or ELF test to clarify fibrosis stage."
    status = "Intermediate Risk"
else:
    st.error("🔴 HIGH RISK: High Probability of Advanced Fibrosis (F3-F4)")
    res_text = "Refer to Hepatology for specialized evaluation and potential biopsy/treatment."
    status = "High Risk"

st.info(res_text)

# --- Referral Generator ---
st.divider()
st.subheader("📝 Referral Summary")
referral_note = f"""PATIENT TRIAGE SUMMARY:
- Age: {age}
- FIB-4 Score: {fib4:.2f}
- Classification: {status}
- Recommendation: {res_text}"""

st.code(referral_note, language="text")
st.caption("GPs can copy the above text directly into clinical notes or referral letters.")