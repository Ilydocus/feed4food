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
    df = df.groupby("month_year", as_index=False).sum()

    df["month_dt"] = pd.to_datetime(df["month_year"], format="%m-%Y", errors="coerce")
    df = df.sort_values("month_dt")

    return df


def build_costs_figure(mode="line", dummy=False):
    if dummy:
        data = [
            {"month_year": "1-2025", "exp_workforce": 1200, "exp_purchase": 800, "exp_others": 300},
            {"month_year": "2-2025", "exp_workforce": 1350, "exp_purchase": 900, "exp_others": 320},
            {"month_year": "3-2025", "exp_workforce": 1280, "exp_purchase": 1100, "exp_others": 280},
            {"month_year": "4-2025", "exp_workforce": 1400, "exp_purchase": 1000, "exp_others": 310},
            {"month_year": "5-2025", "exp_workforce": 1500, "exp_purchase": 1200, "exp_others": 350},
        ]
        df = pd.DataFrame(data)
        df["month_dt"] = pd.to_datetime(df["month_year"], format="%m-%Y", errors="coerce")

    else:
        df = load_costs_data()
        if df.empty:
            return go.Figure()

    if mode == "line":
        fig = px.line(
            df,
            x="month_dt",
            y=["exp_workforce", "exp_purchase", "exp_others"],
            labels={"month_dt": "Month-Year", "value": "Cost"},
            markers=True,
        )
    else:  # stacked bar
        df_melt = df.melt(id_vars=["month_dt"], value_vars=["exp_workforce", "exp_purchase", "exp_others"],
                          var_name="type", value_name="cost")
        fig = px.bar(
            df_melt,
            x="month_dt",
            y="cost",
            color="type",
            barmode="stack",
            labels={"month_dt": "Month-Year", "cost": "Cost"},
        )

    fig.update_layout(
        xaxis=dict(tickformat="%b %Y"),
        height=320,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return fig


class KA1_CostsCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_costs_figure(dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "costscard-graph-mode", "index": id},
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Stacked Bar Chart", "value": "bar"},
                            ],
                            value="line",
                            clearable=False,
                            style={"width": "180px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "costscard-graph", "index": id},
                        responsive=True,
                        style={"height": "320px"},
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
