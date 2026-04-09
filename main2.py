import streamlit as st
import time

# Import ALL Logic Engines
from logic_engine import check_ceiling_limit
from logic_engine_mv import calculate_compensation
from logic_engine_dv import DomesticViolenceLogicEngine  # <--- NEW

# Import ALL Parsers
from llm_parser import parse_query, parse_mv_query, parse_dv_query  # <--- NEW

st.set_page_config(page_title="ALMA: Multi-Domain Legal AI", page_icon="⚖️", layout="wide")

import base64

# ================= BACKGROUND =================
def set_bg():
    with open("hero.png", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# ================= CLEAN UI CSS =================
st.markdown("""
<style>

/* ===== TITLE ===== */
h1 {
    color: #ffffff !important;
    font-weight: 700;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
}

/* ===== SUBTITLE ===== */
h3 {
    color: #e6f7ff !important;
    font-weight: 500;
}

/* ===== INFO BOX (FIXED 🔥) ===== */
div[data-testid="stAlert"] {
    background: rgba(140, 82, 255, 0.15) !important;
    color: #ffffff !important;
    border-left: 4px solid #8c52ff !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px);
    padding: 12px;
}

/* TEXT INSIDE INFO BOX */
div[data-testid="stAlert"] p {
    color: #ffffff !important;
    font-weight: 500;
}

/* ===== INPUT BOX ===== */
textarea {
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 8px !important;
    color: black !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    background-color: #007bff;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: 500;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
}

/* ===== REMOVE EXTRA BLOCK BACKGROUNDS ===== */
.block-container {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: SELECT DOMAIN ---
with st.sidebar:
    st.header("⚙️ Select Legal Domain")
    domain = st.radio(
        "Choose the Act to verify:",
        ("West Bengal Land Reforms Act", "Motor Vehicles Act", "Domestic Violence Act") # <--- UPDATED
    )
    st.markdown("---")
    st.markdown("Powered by **Neuro-Symbolic Architecture**")

st.title("⚖️ ALMA: Neuro-Symbolic Legal Verifier")

# ==========================================================
# MODULE 1: LAND REFORMS ACT
# ==========================================================
if domain == "West Bengal Land Reforms Act":
    st.markdown("### 🌱 Land Ceiling Verification")
    st.info("Input: Family Size, Current Holding, New Transaction (Buy/Sell/Inherit).")
    
    user_query = st.text_area("Enter your scenario:", "I have a family of 4 and own 15 acres of irrigated land. I want to sell 2 acres.", height=100)

    if st.button("🚀 Process Land Transaction"):
        with st.spinner("🧠 ALMA is extracting tokens..."):
            extracted = parse_query(user_query)
            if "error" in extracted:
                st.error("AI Parsing Error.")
                st.stop()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Family Size", extracted.get('family_size', 1))
        c2.metric("Current Acres", extracted.get('current_holding_acres', 0.0))
        c3.metric("Transaction", extracted.get('intent', 'buy').upper())
        c4.metric("New Acres", extracted.get('new_amount_acres', 0.0))
        
        st.divider()
        with st.spinner("⚖️ Applying Section 14M/14U/14Y..."):
            time.sleep(0.5)
            is_legal, message = check_ceiling_limit(
                family_size=int(extracted.get('family_size', 1)),
                current_acres=float(extracted.get('current_holding_acres', 0.0)),
                current_type=extracted.get('current_land_type', 'non-irrigated'),
                new_acres=float(extracted.get('new_amount_acres', 0.0)),
                new_type=extracted.get('new_land_type', 'non-irrigated'),
                intent=extracted.get('intent', 'buy')
            )
            if is_legal: st.success(message)
            else: st.error(message)

# ==========================================================
# MODULE 2: MOTOR VEHICLES ACT
# ==========================================================
elif domain == "Motor Vehicles Act":
    st.markdown("### 🚗 Complete MACT Compensation Engine")
    st.info("Input: Age, Income, Status, Dependents, Employment Type, Medical Bills, and Accident Details (Death/Injury, Hit-and-Run, etc.).")
    
    default_prompt = "A 45-year-old unemployed housewife survived an accident with 30% permanent disability. She spent 15 days in the hospital."
    user_query = st.text_area("Enter accident claim details:", default_prompt, height=100)

    if st.button("🚀 Calculate Statutory Compensation"):
        with st.spinner("🧠 ALMA is extracting tokens..."):
            extracted = parse_mv_query(user_query)
            if "error" in extracted:
                st.error(f"AI Parsing Error: {extracted.get('error')}")
                st.stop()
                
        st.markdown("#### Extracted Demographics & Details")
        
        # ROW 1: Basic Demographics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Age", extracted.get('age', 0))
        c2.metric("Monthly Income", f"₹{extracted.get('monthly_income', 0.0):,.0f}")
        c3.metric("Dependents", extracted.get('dependents', 0))
        c4.metric("Status", str(extracted.get('marital_status', 'Unknown')).title())
        
        # ROW 2: Accident & Claim Specifics
        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Claim Type", str(extracted.get('claim_type', 'fault')).upper())
        c6.metric("Outcome", str(extracted.get('outcome', 'death')).title())
        c7.metric("Disability %", f"{extracted.get('disability_percent', 0.0)}%")
        c8.metric("Medical Bills", f"₹{extracted.get('medical_bills', 0.0):,.0f}")
        
        st.divider()
        with st.spinner("⚖️ Applying MACT Legal Framework (Sec 161/164/166)..."):
            time.sleep(0.5)
            # Passing ALL new variables to the logic engine
            success, message = calculate_compensation(
                age=int(extracted.get('age', 0)),
                monthly_income=float(extracted.get('monthly_income', 0.0)),
                dependents=int(extracted.get('dependents', 0)),
                marital_status=extracted.get('marital_status', 'single'),
                employment_type=extracted.get('employment_type', 'self-employed'),
                medical_bills=float(extracted.get('medical_bills', 0.0)),
                claim_type=extracted.get('claim_type', 'fault'),
                outcome=extracted.get('outcome', 'injury'), 
                disability_percent=float(extracted.get('disability_percent', 0.0)),
                hospital_days=int(extracted.get('hospital_days', 0))
            )
            
            if success: 
                st.success(message)
            else: 
                st.error(message)
            
# ==========================================================
# MODULE 3: DOMESTIC VIOLENCE ACT
# ==========================================================
elif domain == "Domestic Violence Act":
    st.markdown("### 🏠 PWDVA Relief Engine")
    st.info("Calculates statutory claims based on standard of living and reported incidents.")
    
    user_query = st.text_area("Describe the situation:", height=100)

    if st.button("🚀 Analyze Relief Eligibility"):
        with st.spinner("Extracting Legal Triggers..."):
            extracted = parse_dv_query(user_query)
        
        dv_engine = DomesticViolenceLogicEngine(extracted)
        money_report = dv_engine.calculate_monetary_relief()
        orders = dv_engine.evaluate_reliefs()
        
        # Display Math Results
        money_report = dv_engine.calculate_monetary_relief()

        # Display Results
        st.subheader("📊 Compensation Breakdown")
        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Support", f"₹{money_report['monthly']:,.0f}")
        col2.metric("One-time Payout", f"₹{money_report['one_time']:,.0f}") # This now includes Salary + Medical
        col3.metric("Total First Month", f"₹{money_report['total_initial']:,.0f}") # This will correctly show ₹60,000
        
        # Display Reasoning (Transparent AI)
        with st.expander("📝 Detailed Calculation Logic & Statutory Reasons", expanded=True):
            for reason in money_report['reasons']:
                st.write(f"✅ {reason}")

        st.divider()
        st.subheader("⚖️ Recommended Legal Reliefs")
        
        for o in orders:
            with st.expander(f"Section {o['section']}: {o['relief']}"):
                st.write(o['desc'])