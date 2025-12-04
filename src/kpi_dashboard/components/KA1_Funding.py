import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from financialReport.models import FinancialReport


def load_funding_data():
    qs = FinancialReport.objects.all()

    rows = [
        {
            "month": r.month,
            "year": r.year,
            "fun_feed4food": r.fun_feed4food,
            "fun_others": r.fun_others,
        }
        for r in qs
    ]

    if not rows:
        return pd.DataFrame(columns=["month", "year", "fun_feed4food", "fun_others"])

    df = pd.DataFrame(rows)

    # proper datetime
    df["month_year"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-01")

    return df


def build_figure(dummy=False):
    if dummy:
        data = [
            {"month_year": "1-2025", "Project Funding": 500,  "Other Funding": 80},
            {"month_year": "2-2025", "Project Funding": 600,  "Other Funding": 90},
            {"month_year": "3-2025", "Project Funding": 700,  "Other Funding": 85},
            {"month_year": "4-2025", "Project Funding": 650,  "Other Funding": 100},
            {"month_year": "5-2025", "Project Funding": 720,  "Other Funding": 110},
        ]
        df = pd.DataFrame(data)

        # FIX: convert dummy x-axis to datetime to avoid duplicates
        df["month_year"] = pd.to_datetime(df["month_year"], format="%m-%Y")

    else:
        df = load_funding_data()
        if df.empty:
            return go.Figure()

        df = df.rename(
            columns={
                "fun_feed4food": "Project Funding",
                "fun_others": "Other Funding",
            }
        )

    fig = px.bar(
        df,
        x="month_year",
        y=["Project Funding", "Other Funding"],
        barmode="group",
        height=400,
    )

    fig.update_layout(
        xaxis=dict(tickformat="%b %Y")
    )

    return fig


class KA1_FundingCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_figure(dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "graph", "index": id},
                        responsive=True,
                        style={"height": "100%"},
                        figure=fig,
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(
                            dcc.Markdown(description, link_target="_blank")
                        ),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
