import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from salesReport.models import SalesReportDetails


def build_figure():
    qs = SalesReportDetails.objects.all()

    if not qs.exists():
        return go.Figure()

    data = [{
        "product": r.product.name,
        "quantity": r.quantity,
        "month": f"{r.sale_date.month}-{r.sale_date.year}",
    } for r in qs]

    df = pd.DataFrame(data)

    return px.bar(
        df,
        x="month",
        y="quantity",
        color="product",
        labels={
            "month": "Month-Year",
            "quantity": "Quantity Sold",
            "product": "Product",
        },
        barmode="stack",
    )


class KA1_QuantitySold(dbc.Card):
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
