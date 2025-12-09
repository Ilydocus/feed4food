import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from waterReport.models import WaterReportIrrigation


def load_water_data(dummy=False):
    if dummy:
        data = [
            {"month": "Jan-2025", "source": "Rainwater", "quantity": 500},
            {"month": "Feb-2025", "source": "Rainwater", "quantity": 450},
            {"month": "Mar-2025", "source": "Rainwater", "quantity": 600},
            {"month": "Apr-2025", "source": "Rainwater", "quantity": 550},
            {"month": "May-2025", "source": "Rainwater", "quantity": 620},

            {"month": "Jan-2025", "source": "Well", "quantity": 300},
            {"month": "Feb-2025", "source": "Well", "quantity": 320},
            {"month": "Mar-2025", "source": "Well", "quantity": 280},
            {"month": "Apr-2025", "source": "Well", "quantity": 310},
            {"month": "May-2025", "source": "Well", "quantity": 330},
        ]
        return pd.DataFrame(data)

    qs = WaterReportIrrigation.objects.select_related().all()

    rows = [
        {
            "month": f"{r.start_date.month}-{r.start_date.year}",
            "source": r.source,
            "quantity": r.quantity,
        }
        for r in qs
    ]

    if not rows:
        return pd.DataFrame(columns=["month", "source", "quantity"])

    return pd.DataFrame(rows)


def build_wateruse_figure(chart_type="stackedbar", dummy=False):
    df = load_water_data(dummy=dummy)

    if df.empty:
        return go.Figure()

    if chart_type == "stackedline":
        fig = px.line(
            df,
            x="month",
            y="quantity",
            color="source",
            markers=True,
            labels={
                "month": "Month-Year",
                "quantity": "Water Use Quantity",
                "source": "Source",
            },
        )
    else:
        fig = px.bar(
            df,
            x="month",
            y="quantity",
            color="source",
            barmode="stack",
            labels={
                "month": "Month-Year",
                "quantity": "Water Use Quantity",
                "source": "Source",
            },
        )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
    )

    return fig


class KA5_WaterUseCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_wateruse_figure("stackedbar", dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0"),
                        dcc.Dropdown(
                            id={"type": "wateruse-graph-mode", "index": id},
                            options=[
                                {"label": "Stacked Bar", "value": "stackedbar"},
                                {"label": "Stacked Line", "value": "stackedline"},
                            ],
                            value="stackedbar",
                            clearable=False,
                            style={"width": "200px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-items-center p-3",
                ),

                dbc.CardBody(
                    [
                        dbc.Spinner(
                            dcc.Graph(
                                id={"type": "wateruse-graph", "index": id},
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
                    id={"type": "wateruse-graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
