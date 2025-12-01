import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from financialReport.models import FinancialReport


def load_costs_data():
    qs = FinancialReport.objects.all()

    rows = [
        {
            "month": r.month,
            "year": r.year,
            "exp_workforce": r.exp_workforce,
            "exp_purchase": r.exp_purchase,
            "exp_others": r.exp_others,
        }
        for r in qs
    ]

    if not rows:
        return pd.DataFrame(columns=["month", "year", "exp_workforce", "exp_purchase", "exp_others"])

    df = pd.DataFrame(rows)
    df["month_year"] = df["month"].astype(str) + "-" + df["year"].astype(str)
    return df


def build_figure():
    df = load_costs_data()

    if df.empty:
        return go.Figure()

    return px.line(
        df,
        x="month_year",
        y=["exp_workforce", "exp_purchase", "exp_others"],
        labels={
            "month_year": "Month-Year",
            "value": "Cost",
        },
        markers=True,
    )


class KA1_CostsCard(dbc.Card):
    def __init__(self, title, id, description=None):
        fig = build_figure()

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span(
                                "help",
                                className="material-symbols-outlined d-flex",
                            ),
                            id={"type": "graph-info-btn", "index": id},
                            n_clicks=0,
                            color="light",
                        ),
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
