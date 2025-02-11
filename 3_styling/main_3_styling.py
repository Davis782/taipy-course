from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd

# Load data
data = pd.read_csv("data.csv")

# Prepare chart data
chart_data = (
    data.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Define start and end dates
start_date = pd.to_datetime("2015-01-01").tz_localize('UTC')  # Localize to UTC
end_date = pd.to_datetime("2018-12-31").tz_localize('UTC')    # Localize to UTC

# Prepare categories and subcategories
categories = list(data["Category"].unique())
selected_category = "Furniture"
selected_subcategory = "Bookcases"
subcategories = list(
    data[data["Category"] == selected_category]["Sub-Category"].unique()
)

# Define layout for the chart
layout = {"yaxis": {"title": "Revenue (USD)"}, "title": "Sales by State"}

# Function to change category


def change_category(state):
    state.subcategories = list(
        data[data["Category"] == state.selected_category]["Sub-Category"].unique()
    )
    state.selected_subcategory = state.subcategories[0]

# Function to apply changes based on filters


def apply_changes(state):
    state.data = data[
        (
            pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
            .dt.tz_localize('UTC')  # Localize to UTC
            >= state.start_date
        )
        & (
            pd.to_datetime(data["Order Date"], format="%d/%m/%Y")
            .dt.tz_localize('UTC')  # Localize to UTC
            <= state.end_date
        )
    ]
    state.data = state.data[state.data["Category"] == state.selected_category]
    state.data = state.data[state.data["Sub-Category"]
                            == state.selected_subcategory]
    state.chart_data = (
        state.data.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    state.layout = {
        "yaxis": {"title": "Revenue (USD)"},
        "title": f"Sales by State for {state.selected_category} - {state.selected_subcategory}",
    }


# Build the GUI layout
with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("# Sales by **State**", mode="md")
        with tgb.part(class_name="card"):
            with tgb.layout(columns="1 2 1"):
                with tgb.part():
                    tgb.text("Filter **From**", mode="md")
                    tgb.date("{start_date}")
                    tgb.text("To")
                    tgb.date("{end_date}")
                with tgb.part():
                    tgb.text("Filter Product **Category**", mode="md")
                    tgb.selector(
                        value="{selected_category}",
                        lov=categories,
                        on_change=change_category,
                        dropdown=True,
                    )
                    tgb.text("Filter Product **Subcategory**", mode="md")
                    tgb.selector(
                        value="{selected_subcategory}",
                        lov="{subcategories}",
                        dropdown=True,
                    )
                with tgb.part(class_name="text-center"):
                    tgb.button(
                        "Apply",
                        class_name="plain apply_button",
                        on_action=apply_changes,
                    )
        tgb.html("br")
        tgb.chart(
            data="{chart_data}",
            x="State",
            y="Sales",
            type="bar",
            layout="{layout}",
        )
        tgb.html("br")
        tgb.table(data="{data}")

# Run the GUI
Gui(page=page).run(title="Sales", dark_mode=False, debug=True, port=5052)
