import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from productionReport.models import ProductionReportDetails


def load_surface_cultivation_data(dummy=False):
    if dummy:
        data = [
            {"date": "2025-01-01", "product": "Lettuce", "quantity": 120},
            {"date": "2025-02-01", "product": "Lettuce", "quantity": 150},
            {"date": "2025-03-01", "product": "Lettuce", "quantity": 160},
            {"date": "2025-04-01", "product": "Lettuce", "quantity": 180},
            {"date": "2025-05-01", "product": "Lettuce", "quantity": 200},

            {"date": "2025-01-01", "product": "Spinach", "quantity": 80},
            {"date": "2025-02-01", "product": "Spinach", "quantity": 95},
            {"date": "2025-03-01", "product": "Spinach", "quantity": 110},
            {"date": "2025-04-01", "product": "Spinach", "quantity": 130},
            {"date": "2025-05-01", "product": "Spinach", "quantity": 140},
        ]
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
        return df

    # normal DB mode
    qs = (
        ProductionReportDetails.objects
        .select_related("report_id", "name")
        .filter(name__cultivation_type="m²")
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
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()

    return df


def build_surface_line_figure(dummy=False):
    df = load_surface_cultivation_data(dummy=dummy)

    if df.empty:
        return px.area(title="No data available")

    fig = px.area(
        df,
        x="month_year",
        y="quantity",
        color="product",
        line_group="product",
        markers=True,
        labels={
            "month_year": "Month-Year",
            "quantity": "Surface (m²)",
            "product": "Product",
        }
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(tickformat="%b %Y", title="Month-Year"),
    )

    return fig


class KA2_SurfaceCultivatedPerProductCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_surface_line_figure(dummy=dummy)

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
                        dbc.ModalBody(dcc.Markdown(description or "", link_target="_blank")),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
