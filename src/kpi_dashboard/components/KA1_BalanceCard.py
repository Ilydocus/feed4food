import dash
import dash_bootstrap_components as dbc
from dash import html

from django.db.models import Sum, F
from django.utils.timezone import now

from financialReport.models import FinancialReport
from salesReport.models import SalesReportDetails
# If you have EventReport later, you can plug it in here.


# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def current_year():
    return now().year


# -------------------------------------------------
# DATA LOADERS
# -------------------------------------------------

def load_financial_totals_current_year():
    year = current_year()

    qs = FinancialReport.objects.filter(year=year)

    totals = qs.aggregate(
        exp_workforce=Sum("exp_workforce"),
        exp_purchase=Sum("exp_purchase"),
        exp_others=Sum("exp_others"),

        fun_feed4food=Sum("fun_feed4food"),
        fun_others=Sum("fun_others"),

        rev_restaurant=Sum("rev_restaurant"),
        rev_others=Sum("rev_others"),
    )

    # Convert None to 0
    return {k: float(v or 0) for k, v in totals.items()}


def load_sales_revenue_current_year():
    year = current_year()

    qs = SalesReportDetails.objects.filter(sale_date__year=year)
    # product sales = quantity * price
    total_sales = qs.aggregate(total=Sum(F("quantity") * F("price")))["total"] or 0
    return float(total_sales)


# -------------------------------------------------
# COMPUTATION
# -------------------------------------------------

def compute_revenue_expense_balance():
    fin = load_financial_totals_current_year()
    sales_revenue = load_sales_revenue_current_year()

    # --- Revenues ---
    total_revenue = (
        sales_revenue +
        fin["rev_restaurant"] +
        fin["rev_others"] +
        fin["fun_feed4food"] +
        fin["fun_others"]
    )

    # --- Expenses ---
    total_expenses = (
        fin["exp_workforce"] +
        fin["exp_purchase"] +
        fin["exp_others"]
    )

    net_balance = total_revenue - total_expenses

    return total_revenue, total_expenses, net_balance


# -------------------------------------------------
# DASH CARD
# -------------------------------------------------

class KA1_BalanceCard(dbc.Card):
    def __init__(self, id):
        year = current_year()

        total_revenue, total_expenses, net_balance = compute_revenue_expense_balance()

        super().__init__(
            children=[
                dbc.CardHeader(html.H4(f"Balance ({year})")),

                dbc.CardBody(
                    dbc.Row(
                        [
                            # --- Total Revenue ---
                            dbc.Col(
                                html.Div([
                                    html.H6("Total Revenue", className="text-muted"),
                                    html.H4(f"{total_revenue:,.2f}")
                                ]),
                                md=4, sm=12,
                            ),

                            # --- Total Expenses ---
                            dbc.Col(
                                html.Div([
                                    html.H6("Total Expenses", className="text-muted"),
                                    html.H4(f"{total_expenses:,.2f}")
                                ]),
                                md=4, sm=12,
                            ),

                            # --- Net Balance ---
                            dbc.Col(
                                html.Div([
                                    html.H6("Net Balance", className="text-muted"),
                                    html.H4(
                                        f"{net_balance:,.2f}",
                                        style={
                                            "color": "green" if net_balance >= 0 else "red"
                                        }
                                    )
                                ]),
                                md=4, sm=12,
                            ),
                        ],
                        className="text-center",  # aligns all text nicely
                    )
                ),
            ],
            className="mb-3"
        )
