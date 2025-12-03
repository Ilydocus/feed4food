import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from waterReport.models import WaterReportRainfall


def load_rainfall_data():
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


def build_figure():
    df = load_rainfall_data()

    if df.empty:
        return go.Figure()

    return px.bar(
        df,
        x="month",
        y="quantity",
        labels={
            "month": "Month-Year",
            "quantity": "Rainwater Harvested Quantity",
        },
    )


class KA5_RainwaterCard(dbc.Card):
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
