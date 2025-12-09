import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from waterReport.models import WaterReportRainfall


def load_rainfall_data(dummy=False):
    if dummy:
        data = [
            {"month": "Jan-2025", "quantity": 120},
            {"month": "Feb-2025", "quantity": 95},
            {"month": "Mar-2025", "quantity": 150},
            {"month": "Apr-2025", "quantity": 130},
            {"month": "May-2025", "quantity": 160},
        ]
        return pd.DataFrame(data)

    qs = WaterReportRainfall.objects.all()

    rows = [
        {
            "month": f"{r.start_date.month}-{r.start_date.year}",
            "quantity": r.quantity,
        }
        for r in qs
    ]

    if not rows:
        return pd.DataFrame(columns=["month", "quantity"])

    return pd.DataFrame(rows)


def build_rainwater_figure(chart_type="bar", dummy=False):
    df = load_rainfall_data(dummy=dummy)

    if df.empty:
        return go.Figure()

    if chart_type == "line":
        fig = px.line(
            df,
            x="month",
            y="quantity",
            markers=True,
            labels={
                "month": "Month-Year",
                "quantity": "Rainwater Harvested Quantity",
            },
        )
    else:
        fig = px.bar(
            df,
            x="month",
            y="quantity",
            labels={
                "month": "Month-Year",
                "quantity": "Rainwater Harvested Quantity",
            },
        )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
    )

    return fig


class KA5_RainwaterCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_rainwater_figure("bar", dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "rainwater-graph-mode", "index": id},
                            options=[
                                {"label": "Bar Chart", "value": "bar"},
                                {"label": "Line Chart", "value": "line"},
                            ],
                            value="bar",
                            clearable=False,
                            style={"width": "200px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),

                dbc.CardBody(
                    [
                        dbc.Spinner(
                            dcc.Graph(
                                id={"type": "rainwater-graph", "index": id},
                                figure=fig,
                                responsive=True,
                                style={"height": "350px", "width": "100%"},
                            ),
                            size="lg",
                            color="dark",
                            delay_show=750,
                        ),
                    ],
                    style={"height": "380px", "padding": "0.5rem"},
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(
                            dcc.Markdown(description or "", link_target="_blank")
                        ),
                    ],
                    id={"type": "rainwater-graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
