import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Hepatology Clinical Tool", page_icon="🧪", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 MASH/MASLD Lifestyle Intervention Suite")
st.caption("Evidence-Based Precision Weight Loss for Fibrosis Regression")

# --- Sidebar: Patient Profile & References ---
with st.sidebar:
    st.header("Patient Profile")
    weight = st.number_input("Weight (kg)", 40.0, 250.0, 95.0)
    height = st.number_input("Height (cm)", 100.0, 250.0, 175.0)
    age = st.number_input("Age (years)", 18, 100, 45)
    gender = st.selectbox("Biological Sex", ["Male", "Female"])
    activity = st.select_slider("Activity Level", options=["Sedentary", "Lightly", "Moderately", "Very"])
    
    st.divider()
    st.markdown("### 📚 Key NEJM References")
    st.info("""
    - **Harrison et al. (2024):** Resmetirom (MAESTRO-NASH) - First FDA approved.
    - **Loomba et al. (2024):** Tirzepatide (SYNERGY-NASH) - 73% MASH resolution.
    - **Sanyal et al. (2025/26):** Semaglutide (ESSENCE) - Significant fibrosis regression.
    """)

# --- Logic: BMR & Targets ---
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

mult = {"Sedentary": 1.2, "Lightly": 1.375, "Moderately": 1.55, "Very": 1.725}
tdee = bmr * mult[activity]
target_kcal = tdee - 600
target_weight = weight * 0.90  # The 10% Gold Standard

# --- Display: Clinical Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Maintenance (TDEE)", f"{int(tdee)} kcal")
    st.caption("Standard energy requirements")

with col2:
    st.metric("Prescribed Daily Intake", f"{int(target_kcal)} kcal", "-600 kcal", delta_color="normal")
    st.caption("Target for 0.5kg/week loss")

with col3:
    st.metric("10% Weight Target", f"{target_weight:.1f} kg")
    st.caption("Threshold for Fibrosis Regression")

st.divider()

# --- Tabs: Intervention & Evidence ---
tab_plan, tab_evidence = st.tabs(["📋 Clinical Plan", "🔬 Scientific Evidence"])

with tab_plan:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Nutritional Prescription")
        st.write("- **Mediterranean Pattern:** High MUFA (Olive Oil), legumes, veggies.")
        st.write("- **Fructose Restriction:** Avoid sugar-sweetened beverages to reduce DNL.")
        st.write("- **Protein Goal:** 1.2 - 1.5g/kg to preserve lean mass during loss.")
    with c2:
        st.subheader("Physical Activity")
        st.write("- **Goal:** 150-200 min/week.")
        st.write("- **Resistance Training:** Twice weekly to improve insulin sensitivity.")

with tab_evidence:
    st.subheader("The '10% Rule' (Vilar-Gomez, Gastroenterology 2015)")
    st.write("Weight loss of ≥10% results in:")
    st.markdown("- **90%** MASH Resolution")
    st.markdown("- **45%** Fibrosis Regression (at least one stage)")
    st.success("This tool aligns with the latest AASLD (2024) and EASL (2024) Practice Guidance.")