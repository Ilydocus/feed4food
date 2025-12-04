import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from salesReport.models import SalesReportDetails


def build_figure(dummy=False):
    if dummy:
        data = [
            {"product": "Tomatoes", "quantity": 40, "month": "1-2025"},
            {"product": "Lettuce",  "quantity": 25, "month": "1-2025"},
            {"product": "Carrots",  "quantity": 30, "month": "1-2025"},

            {"product": "Tomatoes", "quantity": 55, "month": "2-2025"},
            {"product": "Lettuce",  "quantity": 29, "month": "2-2025"},
            {"product": "Carrots",  "quantity": 34, "month": "2-2025"},

            {"product": "Tomatoes", "quantity": 48, "month": "3-2025"},
            {"product": "Lettuce",  "quantity": 32, "month": "3-2025"},
            {"product": "Carrots",  "quantity": 37, "month": "3-2025"},

            {"product": "Tomatoes", "quantity": 62, "month": "4-2025"},
            {"product": "Lettuce",  "quantity": 28, "month": "4-2025"},
            {"product": "Carrots",  "quantity": 41, "month": "4-2025"},

            {"product": "Tomatoes", "quantity": 58, "month": "5-2025"},
            {"product": "Lettuce",  "quantity": 31, "month": "5-2025"},
            {"product": "Carrots",  "quantity": 38, "month": "5-2025"},
        ]
        df = pd.DataFrame(data)

    else:
        qs = SalesReportDetails.objects.all()
        if not qs.exists():
            return go.Figure()

        data = [{
            "product": r.product.name,
            "quantity": r.quantity,
            "month": f"{r.sale_date.month}-{r.sale_date.year}",
        } for r in qs]

        df = pd.DataFrame(data)

    df["month_year"] = pd.to_datetime(df["month"], format="%m-%Y", errors="coerce")
    df = df.dropna(subset=["month_year"])

    fig = px.bar(
        df,
        x="month_year",
        y="quantity",
        color="product",
        labels={
            "month_year": "Month-Year",
            "quantity": "Quantity Sold",
            "product": "Product",
        },
        barmode="stack",
    )

    fig.update_layout(
        xaxis=dict(tickformat="%b %Y")
    )

    return fig


class KA1_QuantitySold(dbc.Card):
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
