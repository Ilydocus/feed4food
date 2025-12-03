import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from inputReport.models import InputReportDetails


def load_chemical_quantity_data():
    qs = (
        InputReportDetails.objects
        .select_related("report_id", "name_product", "name_input")
        .filter(
            name_input__input_category="Synthetic"
        )
        .values(
            "report_id__application_date",
            "name_product__name",
            "quantity",
        )
    )

    if not qs:
        return pd.DataFrame(columns=["date", "product", "quantity"])

    df = pd.DataFrame(qs)
    df = df.rename(columns={
        "report_id__application_date": "date",
        "name_product__name": "product"
    })

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()

    return df


def build_chemical_bar_figure():
    df = load_chemical_quantity_data()

    if df.empty:
        return px.bar(title="No data available")

    fig = px.bar(
        df,
        x="month_year",
        y="quantity",
        color="product",
        barmode="stack",
        labels={
            "month_year": "Month-Year",
            "quantity": "Quantity Used",
            "product": "Product",
        }
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(tickformat="%b %Y", title="Month-Year")
    )

    return fig


class KA2_ChemicalUsePerProductCard(dbc.Card):
    def __init__(self, title, id, description=None):
        fig = build_chemical_bar_figure()

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span(
                                "help",
                                className="material-symbols-outlined d-flex"
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
                        figure=fig,
                        responsive=True,
                        style={"height": "100%"},
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(
                            dcc.Markdown(description or "", link_target="_blank")
                        ),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
