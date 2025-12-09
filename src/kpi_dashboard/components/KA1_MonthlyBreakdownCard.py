import datetime
from django.db.models import Sum, F
import pandas as pd

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from financialReport.models import FinancialReport
from salesReport.models import SalesReportDetails



def build_dummy_monthly_breakdown_figure(month_key):
    # Accept "01" or "02"
    if month_key == "01":
        rows = [
            ["Revenue from Selling Product", "Product Sales", 12000],
            ["Revenues from Off-Farm Activities", "Sales in Restaurant", 4000],
            ["Revenues from Off-Farm Activities", "Revenue from Events", 1500],
            ["Revenues from Off-Farm Activities", "Other Revenues", 2000],
            ["Funding Received", "Project Funding", 3000],
            ["Funding Received", "Other Funding", 1000],
            ["Expenses", "Workforce Costs", -5000],
            ["Expenses", "Purchase Costs", -4000],
            ["Expenses", "Other Costs", -2000],
        ]
        month_name = "Jan"
        year = 2025
    else:  # "02"
        rows = [
            ["Revenue from Selling Product", "Product Sales", 9000],
            ["Revenues from Off-Farm Activities", "Sales in Restaurant", 3500],
            ["Revenues from Off-Farm Activities", "Revenue from Events", 1000],
            ["Revenues from Off-Farm Activities", "Other Revenues", 1500],
            ["Funding Received", "Project Funding", 2500],
            ["Funding Received", "Other Funding", 800],
            ["Expenses", "Workforce Costs", -5200],
            ["Expenses", "Purchase Costs", -3800],
            ["Expenses", "Other Costs", -1500],
        ]
        month_name = "Feb"
        year = 2025

    df = pd.DataFrame(rows, columns=["Category", "Subcategory", "Value"])
    totals = df.groupby("Category", sort=False)["Value"].sum().to_dict()
    df["Total"] = df["Category"].map(totals)

    fig = px.bar(
        df,
        x="Value",
        y="Category",
        color="Subcategory",
        orientation="h",
        barmode="stack",
        title=f"For {month_name} {year}",
    )
    for category, total_value in totals.items():
        total_text = f"Total: {total_value:,.2f}"
        fig.add_annotation(
            x=total_value,
            y=category,
            text=total_text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="black"),
            xshift=8,
        )
    fig.update_layout(height=430, margin=dict(l=40, r=20, t=60, b=40), legend_title="")
    return fig



def build_monthly_breakdown_figure(month_key="01", dummy=False):
    """
    month_key: string "01".."12"
    dummy: if True, return dummy figure for the month_key
    """
    if dummy:
        return build_dummy_monthly_breakdown_figure(month_key)

    # Convert month_key to int month
    try:
        month = int(month_key)
    except Exception:
        month = datetime.date.today().month

    year = datetime.date.today().year

    # original aggregations (you had these)
    fr = FinancialReport.objects.filter(month=str(month), year=year).aggregate(
        workforce=Sum("exp_workforce"),
        purchase=Sum("exp_purchase"),
        other_exp=Sum("exp_others"),
        project_fund=Sum("fun_feed4food"),
        other_fund=Sum("fun_others"),
        restaurant=Sum("rev_restaurant"),
        other_revenues=Sum("rev_others"),
    )

    def nz(v):
        return v or 0

    workforce = nz(fr.get("workforce"))
    purchase = nz(fr.get("purchase"))
    other_costs = nz(fr.get("other_exp"))
    project_funding = nz(fr.get("project_fund"))
    other_funding = nz(fr.get("other_fund"))
    restaurant_sales = nz(fr.get("restaurant"))
    other_revenues = nz(fr.get("other_revenues"))

    try:
        from eventReport.models import EventReport
        events_total = EventReport.objects.filter(
            event_date__year=year,
            event_date__month=month,
        ).aggregate(t=Sum("event_revenues"))
        events_revenue = nz(events_total.get("t"))
    except Exception:
        events_revenue = 0

    product_sales_total = (
        SalesReportDetails.objects.filter(
            sale_date__year=year,
            sale_date__month=month,
        )
        .annotate(value=F("quantity") * F("price"))
        .aggregate(total=Sum("value"))
    )
    product_sales = nz(product_sales_total.get("total"))

    rows = []
    rows.append(["Revenue from Selling Product", "Product Sales", product_sales])
    off_farm = {
        "Sales in Restaurant": restaurant_sales,
        "Revenue from Events": events_revenue,
        "Other Revenues": other_revenues,
    }
    for k, v in off_farm.items():
        rows.append(["Revenues from Off-Farm Activities", k, v])
    funding = {
        "Project Funding": project_funding,
        "Other Funding": other_funding,
    }
    for k, v in funding.items():
        rows.append(["Funding Received", k, v])
    expenses = {
        "Workforce Costs": workforce * -1,
        "Purchase Costs": purchase * -1,
        "Other Costs": other_costs * -1,
    }
    for k, v in expenses.items():
        rows.append(["Expenses", k, v])

    df = pd.DataFrame(rows, columns=["Category", "Subcategory", "Value"])
    totals = df.groupby("Category", sort=False)["Value"].sum().to_dict()
    df["Total"] = df["Category"].map(totals)

    month_name = datetime.date(2000, month, 1).strftime("%B")

    fig = px.bar(
        df,
        x="Value",
        y="Category",
        color="Subcategory",
        orientation="h",
        barmode="stack",
        title=f"For {month_name} {year}",
    )
    for category, total_value in totals.items():
        total_text = f"Total: {total_value:,.2f}"
        fig.add_annotation(
            x=total_value,
            y=category,
            text=total_text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="black"),
            xshift=8,
        )
    fig.update_layout(height=430, margin=dict(l=40, r=20, t=60, b=40), legend_title="")
    return fig


class KA1_MonthlyBreakdownCard(dbc.Card):
    def __init__(self, title, id, dummy=False):
        if dummy:
            default_month = "01"
        else:
            default_month = datetime.date.today().strftime("%m")

        fig = build_monthly_breakdown_figure(default_month, dummy=dummy)

        super().__init__(
            [
                dbc.CardHeader(html.H4(title, className="card-title")),

                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            id={"type": "month-dropdown", "index": id},
                            options=[
                                {"label": "January", "value": "01"},
                                {"label": "February", "value": "02"},
                                # add more months if you want
                            ],
                            value=default_month,
                            clearable=False,
                            style={"marginBottom": "12px", "width": "200px"},
                        ),

                        dcc.Graph(
                            id={"type": "graph", "index": id},
                            figure=fig,
                            responsive=True,
                            config={"displayModeBar": False},
                            style={"height": "430px"}
                        ),
                    ]
                ),
            ],
            className="mb-3",
        )
