import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from dash.dash_table import DataTable
from salesReport.models import SalesReportDetails
from django.utils.timezone import now


def load_sales_data(living_lab):
    # Only show for one year
    today = now()
    year = today.year
    qs = SalesReportDetails.objects.select_related("product").filter(report_id__city=living_lab, sale_date__year=year)
    rows = [
        {"product": r.product.name, "price": r.price}
        for r in qs
    ]
    if not rows:
        return pd.DataFrame(columns=["product", "price"])
    return pd.DataFrame(rows)


class KA1_PriceProduct(dbc.Card):
    def __init__(self, title, id, living_lab description=None):
        df = load_sales_data(living_lab) 

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
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
                                data=df.to_dict("records"),
                                style_table={"height": "400px", "overflowY": "auto"},
                                style_cell={"textAlign": "center"},
                            )
                        ],
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
