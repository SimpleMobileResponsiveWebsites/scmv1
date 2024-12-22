import streamlit as st
import pandas as pd

# Title and description of the app
st.title("Risk Assessment: Identifying and Mitigating Risks")
st.write("""
    This application helps you identify, assess, and mitigate risks in your project, business, or process.
    You can list the risks, evaluate their likelihood and impact, and come up with mitigation strategies.
""")

# Function to load the risks data (if any)
def load_risks():
    # This could be a file read in practice, here it's a placeholder for simplicity.
    return pd.DataFrame(columns=["Risk", "Likelihood", "Impact", "Mitigation Strategy", "Status"])

# Session state for storing the risks data
if "risks" not in st.session_state:
    st.session_state.risks = load_risks()

# Risk identification section
st.header("Step 1: Identify Risks")
risk_name = st.text_input("Enter a Risk Description:")

if st.button("Add Risk") and risk_name:
    new_risk = {
        "Risk": risk_name,
        "Likelihood": None,
        "Impact": None,
        "Mitigation Strategy": None,
        "Status": "Not Mitigated"
    }
    st.session_state.risks = st.session_state.risks.append(new_risk, ignore_index=True)
    st.success(f"Risk '{risk_name}' added!")

# Display the current risks
st.write("### Current Risks List")
st.dataframe(st.session_state.risks)

# Risk evaluation section
st.header("Step 2: Evaluate Risk Likelihood and Impact")
risk_to_evaluate = st.selectbox("Select a risk to evaluate", st.session_state.risks["Risk"])

# Likelihood and Impact Sliders
if risk_to_evaluate:
    likelihood = st.slider("Likelihood (1-5)", 1, 5, 3)
    impact = st.slider("Impact (1-5)", 1, 5, 3)
    
    if st.button(f"Evaluate Risk '{risk_to_evaluate}'"):
        risk_index = st.session_state.risks[st.session_state.risks["Risk"] == risk_to_evaluate].index[0]
        st.session_state.risks.at[risk_index, "Likelihood"] = likelihood
        st.session_state.risks.at[risk_index, "Impact"] = impact
        st.success(f"Risk '{risk_to_evaluate}' evaluated with Likelihood: {likelihood} and Impact: {impact}")

# Mitigation strategies section
st.header("Step 3: Mitigate Risks")
risk_to_mitigate = st.selectbox("Select a risk to mitigate", st.session_state.risks["Risk"])

if risk_to_mitigate:
    mitigation = st.text_area("Enter Mitigation Strategy")
    if st.button(f"Add Mitigation Strategy for '{risk_to_mitigate}'"):
        risk_index = st.session_state.risks[st.session_state.risks["Risk"] == risk_to_mitigate].index[0]
        st.session_state.risks.at[risk_index, "Mitigation Strategy"] = mitigation
        st.session_state.risks.at[risk_index, "Status"] = "Mitigated"
        st.success(f"Mitigation strategy for '{risk_to_mitigate}' added!")

# Display the risks with evaluations and mitigation
st.write("### Risk Assessment Overview")
st.dataframe(st.session_state.risks)

# Option to reset or clear the risk data
if st.button("Clear All Risks"):
    st.session_state.risks = load_risks()
    st.success("All risks have been cleared.")
