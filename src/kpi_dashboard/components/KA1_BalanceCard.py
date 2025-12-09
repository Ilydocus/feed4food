import dash
import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now
from financialReport.models import FinancialReport
from salesReport.models import SalesReportDetails
from django.db.models import Sum, F
import calendar


def build_dummy_balance_data():
    total_revenue = 25000
    total_expenses = 18000
    net_balance = total_revenue - total_expenses
    return total_revenue, total_expenses, net_balance


def dummy_trend():
    return "+5%", "▲", "green"


class KA1_BalanceCard(dbc.Card):
    def __init__(self, id, dummy=False):
        today = now()
        year = today.year
        month = today.month
        month_name = calendar.month_name[month]
        compare_year = year - 1

        if dummy:
            total_revenue, total_expenses, net_balance = build_dummy_balance_data()
            year = 2025  # keep dummy consistent
        else:
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
            fin = {k: float(v or 0) for k, v in totals.items()}

            sales_qs = SalesReportDetails.objects.filter(sale_date__year=year)
            sales_revenue = float(sales_qs.aggregate(total=Sum(F("quantity") * F("price")))["total"] or 0)

            total_revenue = (
                sales_revenue
                + fin["rev_restaurant"]
                + fin["rev_others"]
                + fin["fun_feed4food"]
                + fin["fun_others"]
            )
            total_expenses = (
                fin["exp_workforce"]
                + fin["exp_purchase"]
                + fin["exp_others"]
            )
            net_balance = total_revenue - total_expenses

        # Dummy YoY trends
        rev_pct, rev_arrow, rev_color = dummy_trend()
        exp_pct, exp_arrow, exp_color = dummy_trend()
        bal_pct, bal_arrow, bal_color = dummy_trend()

        comparison_text = f"Trend compared to {month_name} {compare_year}"

        super().__init__(
            children=[
                dbc.CardHeader(html.H4(f"Balance for {year} (Jan to Present Month)")),
                dbc.CardBody(
                    dbc.Row(
                        [
                            # Revenue
                            dbc.Col(
                                html.Div([
                                    html.H6("Total Revenue", className="text-muted"),
                                    html.H4([
                                        f"{total_revenue:,.2f} ",
                                        html.Span(
                                            f"{rev_arrow} {rev_pct}",
                                            style={"fontSize": "0.9rem", "color": rev_color}
                                        )
                                    ]),
                                    html.Div(
                                        comparison_text,
                                        className="text-muted",
                                        style={"fontSize": "0.8rem"}
                                    )
                                ]),
                                md=4, sm=12,
                            ),

                            # Expenses
                            dbc.Col(
                                html.Div([
                                    html.H6("Total Expenses", className="text-muted"),
                                    html.H4([
                                        f"{total_expenses:,.2f} ",
                                        html.Span(
                                            f"{exp_arrow} {exp_pct}",
                                            style={"fontSize": "0.9rem", "color": exp_color}
                                        )
                                    ]),
                                    html.Div(
                                        comparison_text,
                                        className="text-muted",
                                        style={"fontSize": "0.8rem"}
                                    )
                                ]),
                                md=4, sm=12,
                            ),

                            # Net Balance
                            dbc.Col(
                                html.Div([
                                    html.H6("Net Balance", className="text-muted"),
                                    html.H4([
                                        f"{net_balance:,.2f} ",
                                        html.Span(
                                            f"{bal_arrow} {bal_pct}",
                                            style={"fontSize": "0.9rem", "color": bal_color}
                                        )
                                    ],
                                    style={"color": "green" if net_balance >= 0 else "red"}),
                                    html.Div(
                                        comparison_text,
                                        className="text-muted",
                                        style={"fontSize": "0.8rem"}
                                    )
                                ]),
                                md=4, sm=12,
                            ),
                        ],
                        className="text-center",
                    )
                ),
            ],
            className="mb-3"
        )
