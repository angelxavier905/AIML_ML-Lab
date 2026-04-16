import streamlit as st
import pandas as pd
import numpy as np
import pickle

# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
model = pickle.load(open("model.pkl", "rb"))

# ─────────────────────────────────────────────
# FEATURE LIST (IMPORTANT)
# ─────────────────────────────────────────────
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
# TITLE
# ─────────────────────────────────────────────
st.title("🎓 Student Dropout Risk Predictor")
st.write("Enter student details:")

# ─────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────
age = st.number_input("Age", 15, 50)

scholarship = st.selectbox("Do you have a scholarship?", ["Yes", "No"])
debtor = st.selectbox("Do you have unpaid fees or loans?", ["Yes", "No"])
fees = st.selectbox("Are your tuition fees up to date?", ["Yes", "No"])

s1 = st.slider("Semester 1 subjects passed (0–6)", 0, 6)
s2 = st.slider("Semester 2 subjects passed (0–6)", 0, 6)

# Convert inputs
scholarship = 1 if scholarship == "Yes" else 0
debtor = 1 if debtor == "Yes" else 0
fees = 1 if fees == "Yes" else 0

# ─────────────────────────────────────────────
# CREATE INPUT DATA
# ─────────────────────────────────────────────
data = {col: 0 for col in features}
df = pd.DataFrame([data])

# Fill important features
df["Age at enrollment"] = age
df["Scholarship holder"] = scholarship
df["Debtor"] = debtor
df["Tuition fees up to date"] = fees
df["Curricular units 1st sem (approved)"] = s1
df["Curricular units 2nd sem (approved)"] = s2

# ─────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────
if st.button("Predict Risk"):

    prob = model.predict_proba(df)[0][1]
    pred = model.predict(df)[0]

    st.subheader("📊 Result")
    st.write(f"Dropout Probability: {round(prob, 2)}")

    if prob >= 0.7:
        st.error("🔴 HIGH RISK")
    elif prob >= 0.4:
        st.warning("🟡 MEDIUM RISK")
    else:
        st.success("🟢 LOW RISK")

    # ───────────────── REASON LOGIC ─────────────────
    if s1 < 3 and s2 < 3:
        reason = "Very low academic performance"
        suggestion = "Focus on improving academics with tutoring and mentoring"

    elif s1 < 3:
        reason = "Low performance in Semester 1"
        suggestion = "Improve Semester 1 subjects with better study planning"

    elif s2 < 3:
        reason = "Low performance in Semester 2"
        suggestion = "Focus on Semester 2 subjects and attend extra classes"

    elif debtor == 1 and fees == 0:
        reason = "Serious financial issues (debt + unpaid fees)"
        suggestion = "Clear dues and apply for financial aid immediately"

    elif debtor == 1:
        reason = "Outstanding financial debt"
        suggestion = "Plan to clear debt and seek financial support"

    elif fees == 0:
        reason = "Tuition fees not paid"
        suggestion = "Pay pending fees or apply for assistance"

    elif scholarship == 0:
        reason = "No financial support (scholarship)"
        suggestion = "Apply for scholarships or financial aid"

    else:
        reason = "No major risk factors detected"
        suggestion = "Continue maintaining performance"

    # ───────────────── OUTPUT ─────────────────
    st.write("### 🔍 Key Reason")
    st.write(reason)

    st.write("### 💡 Suggested Action")
    st.write(suggestion)