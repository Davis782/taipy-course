from taipy.gui import Gui, Markdown
import taipy.gui.builder as tgb
import datetime

# State Variables
district_court = ""
debtor_creditor = "Debtor"
judgment_amount = 0.0
judgment_date = None
interest_rate = 0.06
results = {}
error_message = ""

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

def calculate_interest(state):
    global results, error_message
    error_message = ""
    if not isinstance(state.judgment_date, datetime.date):
        error_message = "Invalid date format."
        results = {}
        return
    if state.judgment_amount <= 0:
        error_message = "Judgment amount must be greater than zero."
        results = {}
        return
    if state.interest_rate < 0:
        error_message = "Interest rate must be a non-negative number."
        results = {}
        return
    results = calculate_va_judgment_interest(state.judgment_amount, state.judgment_date, state.interest_rate)

def display_results(results, district_court, debtor_creditor):
    if "error" in results:
        return Markdown(f"**Error:** {results['error']}")
    else:
        return Markdown(f"""
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

with tgb.Page() as main_page:
    tgb.text("## Virginia District Court Judgment Interest Calculator")
    with tgb.layout(columns="1 1"):
        tgb.input(label="District Court", value="{district_court}")
        tgb.selector(label="Debtor/Creditor", value="{debtor_creditor}", lov=["Debtor", "Creditor"])
    with tgb.layout(columns="1 1"):
        tgb.input(label="Judgment Amount", value="{judgment_amount}", type="number")
        tgb.date(label="Judgment Date", value="{judgment_date}")
    with tgb.layout(columns="1 1"):
        tgb.input(label="Interest Rate (%)", value="{interest_rate}", type="number", format="%.2f")
    tgb.button("Calculate", on_action=calculate_interest)
    tgb.text("{error_message}", class_name="error", visible="{error_message != ''}")
    tgb.html("<br>")
    tgb.html("{display_results(results, district_court, debtor_creditor)}")

pages = {"/": main_page}

Gui(pages=pages).run(title="VA Judgment Calculator", dark_mode=False, debug=True, port=5000)
