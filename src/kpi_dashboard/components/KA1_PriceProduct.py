import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from dash.dash_table import DataTable
from salesReport.models import SalesReportDetails  # Assuming you're using Django models for SalesReportDetails

class KA1_PriceProduct(dbc.Card):
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
                    html.Div(
                        id={"type": "table", "index": id},
                        children=[
                            DataTable(
                                id={"type": "sales-table", "index": id},
                                columns=[
                                    {"name": "Product", "id": "product"},
                                    {"name": "Price", "id": "price"},
                                ],
                                data=df.to_dict('records'),  # Data passed to the table
                                style_table={'height': '400px', 'overflowY': 'auto'},  # Optional styling
                                style_cell={'textAlign': 'center'},  # Optional styling
                            )
                        ]
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


# Fetch data for SalesReportDetails (replace with your actual query)
data = [{
    "product": report.product.name,
    "price": report.price,
} for report in SalesReportDetails.objects.all()]

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

if df.empty:
    # Display an empty DataFrame message or similar if no data is available
    df = pd.DataFrame(columns=["product", "price"])
