import streamlit as st
import datetime

# State Variables (using Streamlit's session state)
if 'district_court' not in st.session_state:
    st.session_state.district_court = ""
if 'debtor_creditor' not in st.session_state:
    st.session_state.debtor_creditor = "Debtor"
if 'judgment_amount' not in st.session_state:
    st.session_state.judgment_amount = 0.0
if 'judgment_date' not in st.session_state:
    st.session_state.judgment_date = None
if 'interest_rate' not in st.session_state:
    st.session_state.interest_rate = 0.06
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""

def calculate_va_judgment_interest(judgment_amount, judgment_date, interest_rate=0.06):
    if not isinstance(judgment_date, datetime.date):
        return {"error": "Invalid date format."}
    today = datetime.date.today()
    days_elapsed = (today - judgment_date).days
    accrued_interest = judgment_amount * (interest_rate / 365) * days_elapsed
    total_amount_owed = judgment_amount + accrued_interest
    return {
        "judgment_amount": judgment_amount,
        "judgment_date": judgment_date,
        "interest_rate": interest_rate,
        "days_elapsed": days_elapsed,
        "accrued_interest": accrued_interest,
        "total_amount_owed": total_amount_owed,
    }

def calculate_interest():
    st.session_state.error_message = ""
    if not isinstance(st.session_state.judgment_date, datetime.date):
        st.session_state.error_message = "Invalid date format."
        st.session_state.results = {}
        return
    if st.session_state.judgment_amount <= 0:
        st.session_state.error_message = "Judgment amount must be greater than zero."
        st.session_state.results = {}
        return
    if st.session_state.interest_rate < 0:
        st.session_state.error_message = "Interest rate must be a non-negative number."
        st.session_state.results = {}
        return
    st.session_state.results = calculate_va_judgment_interest(
        st.session_state.judgment_amount,
        st.session_state.judgment_date,
        st.session_state.interest_rate,
    )

def display_results():
    results = st.session_state.results
    district_court = st.session_state.district_court
    debtor_creditor = st.session_state.debtor_creditor

    if "error" in results:
        st.error(f"**Error:** {results['error']}")
    elif results:
        st.markdown(f"""
## Virginia District Court Judgment Interest Calculation

* **District Court:** {district_court}
* **{debtor_creditor}:** (Information provided by user)
* **Judgment Amount:** ${results['judgment_amount']:.2f}
* **Judgment Date:** {results['judgment_date']}
* **Interest Rate:** {results['interest_rate'] * 100:.2f}%
* **Days Elapsed:** {results['days_elapsed']}
* **Accrued Interest:** ${results['accrued_interest']:.2f}
* **Total Amount Owed:** ${results['total_amount_owed']:.2f}
""")

# Streamlit UI
st.title("Virginia District Court Judgment Interest Calculator")

col1, col2 = st.columns(2)
with col1:
    st.text_input("District Court", key="district_court")
with col2:
    st.selectbox("Debtor/Creditor", ["Debtor", "Creditor"], key="debtor_creditor")

col3, col4 = st.columns(2)
with col3:
    st.number_input("Judgment Amount", key="judgment_amount", value=0.0)
with col4:
    st.date_input("Judgment Date", key="judgment_date")

col5, col6 = st.columns(2)
with col5:
    st.number_input("Interest Rate (%)", key="interest_rate", value=0.06, format="%.2f")

if st.button("Calculate"):
    calculate_interest()

if st.session_state.error_message:
    st.error(st.session_state.error_message)

st.markdown("<br>", unsafe_allow_html=True) # add a line break.
display_results()