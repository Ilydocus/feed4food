import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from salesReport.models import SalesReportDetails


def build_figure(mode="bar", dummy=False):
    if dummy:
        data = [
            {"product": "Tomatoes", "quantity": 40, "price": 2.5, "month": "1-2025"},
            {"product": "Lettuce",  "quantity": 25, "price": 1.8, "month": "1-2025"},
            {"product": "Carrots",  "quantity": 30, "price": 1.2, "month": "1-2025"},
            {"product": "Tomatoes", "quantity": 55, "price": 2.5, "month": "2-2025"},
            {"product": "Lettuce",  "quantity": 29, "price": 1.8, "month": "2-2025"},
            {"product": "Carrots",  "quantity": 34, "price": 1.2, "month": "2-2025"},
            {"product": "Tomatoes", "quantity": 48, "price": 2.5, "month": "3-2025"},
            {"product": "Lettuce",  "quantity": 32, "price": 1.8, "month": "3-2025"},
            {"product": "Carrots",  "quantity": 37, "price": 1.2, "month": "3-2025"},
            {"product": "Tomatoes", "quantity": 62, "price": 2.5, "month": "4-2025"},
            {"product": "Lettuce",  "quantity": 28, "price": 1.8, "month": "4-2025"},
            {"product": "Carrots",  "quantity": 41, "price": 1.2, "month": "4-2025"},
            {"product": "Tomatoes", "quantity": 58, "price": 2.5, "month": "5-2025"},
            {"product": "Lettuce",  "quantity": 31, "price": 1.8, "month": "5-2025"},
            {"product": "Carrots",  "quantity": 38, "price": 1.2, "month": "5-2025"},
        ]
        df = pd.DataFrame(data)
    else:
        qs = SalesReportDetails.objects.select_related("product").all()
        if not qs.exists():
            return go.Figure()

        data = [{
            "product": r.product.name,
            "quantity": r.quantity,
            "price": r.price,
            "revenue": r.quantity * r.price,
            "month": f"{r.sale_date.month}-{r.sale_date.year}",
        } for r in qs]

        df = pd.DataFrame(data)

    if dummy:
        df["revenue"] = df["quantity"] * df["price"]

    df["month_year"] = pd.to_datetime(df["month"], format="%m-%Y", errors="coerce")
    df = df.dropna(subset=["month_year"])

    if mode == "bar":
        fig = px.bar(
            df,
            x="month_year",
            y="revenue",
            color="product",
            barmode="stack",
            labels={"month_year": "Month-Year", "revenue": "Revenue", "product": "Product"},
        )
    else:
        fig = px.area(
            df,
            x="month_year",
            y="revenue",
            color="product",
            labels={"month_year": "Month-Year", "revenue": "Revenue", "product": "Product"},
        )

    # Stable graph height
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(tickformat="%b %Y"),
    )

    return fig


class KA1_QuantitySold(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_figure(dummy=dummy)

        super().__init__(
            children=[
                # Header
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "quantitysold-graph-mode", "index": id},
                            options=[
                                {"label": "Stacked Bar", "value": "bar"},
                                {"label": "Stacked Line", "value": "line"},
                            ],
                            value="bar",
                            clearable=False,
                            style={"width": "180px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),

                # Body with fixed height
                dbc.CardBody(
                    [
                        dbc.Spinner(
                            dcc.Graph(
                                id={"type": "quantitysold-graph", "index": id},
                                responsive=True,
                                style={"height": "320px", "width": "100%"},
                                figure=fig,
                            ),
                            size="lg",
                            color="dark",
                            delay_show=750,
                        ),
                    ],
                    style={"height": "350px", "padding": "0.5rem"},
                ),

                # Modal
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(dcc.Markdown(description, link_target="_blank")),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
