import streamlit as st
import pandas as pd
import pickle

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Dropout Predictor Pro", layout="centered", page_icon="🎓")

# ─────────────────────────────────────────────
# 🎨 CUSTOM CSS (BIG + CLEAN + PRETTY)
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(to right, #eef2f7, #f8fafc);
}

/* Title */
h1 {
    font-size: 48px !important;
    font-weight: 800;
    color: #1e293b;
    text-align: center;
}

/* Subheaders */
h3 {
    font-size: 24px !important;
    font-weight: 600;
    color: #334155;
}

/* Labels */
label {
    font-size: 18px !important;
    font-weight: 500;
}

/* Text Input */
.stTextInput input {
    font-size: 20px !important;
    padding: 12px !important;
    border-radius: 10px !important;
}

/* Radio buttons */
.stRadio label {
    font-size: 16px !important;
}

/* Sliders */
.stSlider label {
    font-size: 16px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    border-radius: 12px;
    background: linear-gradient(90deg, #6366f1, #4f46e5);
    color: white;
    border: none;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: scale(1.03);
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Result Box */
.result-box {
    padding: 25px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    text-align: center;
}

/* Metric */
[data-testid="stMetric"] {
    font-size: 22px;
    padding: 20px;
    border-radius: 12px;
    background: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
model = pickle.load(open("model.pkl", "rb"))

features = [
    'Marital status','Application mode','Application order','Course',
    'Daytime/evening attendance','Previous qualification','Nacionality',
    "Mother's qualification","Father's qualification","Mother's occupation",
    "Father's occupation",'Displaced','Educational special needs','Debtor',
    'Tuition fees up to date','Gender','Scholarship holder',
    'Age at enrollment','International',
    'Curricular units 1st sem (credited)',
    'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)',
    'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)',
    'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)',
    'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)',
    'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)',
    'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate','Inflation rate','GDP'
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🎓 Student Dropout Risk Predictor")
st.markdown("### Smart AI system to detect at-risk students early")

st.divider()

# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
st.subheader("📊 Student Information")

col1, col2 = st.columns(2)

with col1:
    age_input = st.text_input("Age", placeholder="Enter age (e.g., 20)")
    try:
        age = int(age_input)
    except:
        age = 0

    s1 = st.slider("Semester 1 Passed Subjects", 0, 6, 3)

with col2:
    s2 = st.slider("Semester 2 Passed Subjects", 0, 6, 3)

st.subheader("💰 Financial Details")

col3, col4, col5 = st.columns(3)

with col3:
    scholarship = st.radio("Scholarship", ["Yes", "No"])

with col4:
    debtor = st.radio("Debt", ["Yes", "No"])

with col5:
    fees = st.radio("Fees Paid", ["Yes", "No"])

# Convert
scholarship = 1 if scholarship == "Yes" else 0
debtor = 1 if debtor == "Yes" else 0
fees = 1 if fees == "Yes" else 0

# ─────────────────────────────────────────────
# DATAFRAME
# ─────────────────────────────────────────────
data = {col: 0 for col in features}
df = pd.DataFrame([data])

df["Age at enrollment"] = age
df["Scholarship holder"] = scholarship
df["Debtor"] = debtor
df["Tuition fees up to date"] = fees
df["Curricular units 1st sem (approved)"] = s1
df["Curricular units 2nd sem (approved)"] = s2

# ─────────────────────────────────────────────
# BUTTON
# ─────────────────────────────────────────────
if st.button("🚀 Predict Risk"):

    if age == 0:
        st.warning("⚠️ Enter valid age")
    else:
        prob = model.predict_proba(df)[0][1]

        st.divider()

        st.markdown('<div class="result-box">', unsafe_allow_html=True)

        st.metric("Dropout Probability", f"{round(prob*100)}%")

        if prob > 0.7:
            st.error("🔴 HIGH RISK")
        elif prob > 0.4:
            st.warning("🟡 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")

        st.markdown('</div>', unsafe_allow_html=True)

        # Suggestions
        with st.expander("📌 Suggestions"):
            if fees == 0:
                st.warning("Clear pending fees immediately")

            if s2 < s1:
                st.info("Performance dropped — consider mentoring")

            if scholarship == 1:
                st.success("Scholarship reduces risk")