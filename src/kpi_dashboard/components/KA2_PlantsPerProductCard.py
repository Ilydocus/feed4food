import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from productionReport.models import ProductionReportDetails


def load_plants_cultivated_data():
    qs = (
        ProductionReportDetails.objects
        .select_related("report_id", "name")
        .filter(name__cultivation_type="plants")
    )

    rows = []
    for r in qs:
        if not r.report_id.production_date:
            continue

        rows.append({
            "date": r.report_id.production_date,
            "product": r.name.name,
            "quantity": r.quantity,
        })

    if not rows:
        return pd.DataFrame(columns=["date", "product", "quantity"])

    df = pd.DataFrame(rows)
    return df


def build_plants_line_figure():
    df = load_plants_cultivated_data()

    if df.empty:
        return px.area(title="No data available")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()

    fig = px.area(
        df,
        x="month_year",
        y="quantity",
        color="product",
        line_group="product",
        markers=True,
        labels={
            "month_year": "Month-Year",
            "quantity": "Number of Plants",
            "product": "Product",
        },
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text="Product",
        xaxis=dict(
            tickformat="%b %Y",
            title="Month-Year",
        ),
    )

    return fig


class KA2_PlantsPerProductCard(dbc.Card):
    def __init__(self, title, id, description=None):
        fig = build_plants_line_figure()

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
