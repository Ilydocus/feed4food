import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from productionReport.models import Product, ProductionReport, ProductionReportDetails


class KA5_FigureCard(dbc.Card):
    def __init__(self, title, id, description=None):
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
                        figure=fig
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
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


data = [{
    "name": product.name or "Unknown", 
    "unit": product.unit or 0
} for product in Product.objects.all()]

df = pd.DataFrame(data)

if not df.empty:
    fig = px.line(df, x='name', y='unit', markers=True)
else:
    fig = go.Figure()  

# print("PRODUCTION REPORT:")
# print("----------------------------------")
# print(ProductionReport.objects.all())
# print(Product.objects.all())
# print(ProductionReportDetails.objects.all())

# df = pd.DataFrame({
#     "months": ["November", "December", "January", "February"],
#     "balance": [100, 1100, -400, 430]
# })

# fig = px.line(df, x='months', y='balance', markers=True)
