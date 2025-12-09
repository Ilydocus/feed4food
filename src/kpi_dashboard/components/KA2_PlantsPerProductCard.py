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


def build_plants_cultivated_figure(chart_type="line", dummy=False):
    if dummy:
        dummy_data = [
            {"month_year": "2025-01", "product": "Tomato",    "quantity": 120},
            {"month_year": "2025-01", "product": "Cucumber",  "quantity":  80},
            {"month_year": "2025-02", "product": "Tomato",    "quantity": 140},
            {"month_year": "2025-02", "product": "Cucumber",  "quantity":  90},
            {"month_year": "2025-03", "product": "Tomato",    "quantity": 135},
            {"month_year": "2025-03", "product": "Cucumber",  "quantity": 100},
            {"month_year": "2025-04", "product": "Tomato",    "quantity": 150},
            {"month_year": "2025-04", "product": "Cucumber",  "quantity": 110},
            {"month_year": "2025-05", "product": "Tomato",    "quantity": 155},
            {"month_year": "2025-05", "product": "Cucumber",  "quantity": 115},
        ]
        df = pd.DataFrame(dummy_data)
        df["month_year"] = pd.to_datetime(df["month_year"])

    else:
        df = load_plants_cultivated_data()
        if df.empty:
            return px.line(title="No data available")

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Δ Chart Type
    if chart_type == "stacked":
        fig = px.bar(
            df,
            x="month_year",
            y="quantity",
            color="product",
            barmode="stack",
            labels={
                "month_year": "Month-Year",
                "quantity": "Number of Plants",
                "product": "Product",
            },
        )
    else:
        fig = px.line(
            df,
            x="month_year",
            y="quantity",
            color="product",
            markers=True,
            labels={
                "month_year": "Month-Year",
                "quantity": "Number of Plants",
                "product": "Product",
            },
        )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        legend_title_text="Product",
        xaxis=dict(
            tickformat="%b %Y",
            title="Month-Year",
        ),
    )

    return fig


class KA2_PlantsPerProductCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_plants_cultivated_figure("line", dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "plantscultivated-graph-mode", "index": id},
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Stacked Bar", "value": "stacked"},
                            ],
                            value="line",
                            clearable=False,
                            style={"width": "200px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),

                dbc.CardBody(
                    [
                        dbc.Spinner(
                            dcc.Graph(
                                id={"type": "plantscultivated-graph", "index": id},
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
                    id={"type": "plantscultivated-graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
