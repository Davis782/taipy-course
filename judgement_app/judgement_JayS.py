from taipy.gui import Gui, Markdown
import taipy.gui.builder as tgb
import datetime
import traceback

# State Variables
district_court = ""
debtor_creditor = "Debtor"
judgment_amount = 0.0
judgment_date = None
interest_rate = 0.06
results = {}
error_message = ""

def calculate_va_judgment_interest(judgment_amount, judgment_date, interest_rate=0.06):
    """Calculates the accrued interest and total amount owed on a Virginia District Court judgment."""
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
    """Handles the calculation and result display."""
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
    # ... (display_results function code) ...
    pass #Add pass, to prevent indentation error.

with tgb.Page() as main_page:
    # ... (main_page code) ...
    pass #Add pass, to prevent indentation error.

pages = {"/": main_page} #Define the pages variable outside of the function.

Gui(pages=pages).run(title="VA Judgment Calculator", dark_mode=False, debug=True, port=5000)