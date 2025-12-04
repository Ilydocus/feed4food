import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from salesReport.models import SalesReportDetails
from financialReport.models import FinancialReport


def load_sales_data(dummy=False):
    if dummy:
        rows = [
            {
                "date": pd.to_datetime("2025-01-05"),
                "source": "Production Sales",
                "value": 300,
            },
            {
                "date": pd.to_datetime("2025-01-18"),
                "source": "Production Sales",
                "value": 450,
            },
            {
                "date": pd.to_datetime("2025-02-02"),
                "source": "Production Sales",
                "value": 520,
            },
            {
                "date": pd.to_datetime("2025-01-01"),
                "source": "Restaurant Sales",
                "value": 800,
            },
            {
                "date": pd.to_datetime("2025-02-01"),
                "source": "Restaurant Sales",
                "value": 950,
            },
        ]
        df = pd.DataFrame(rows)
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
        df["month_year"] = pd.to_datetime(df["month_year"])
        return df

    rows = []

    qs = SalesReportDetails.objects.select_related("report_id", "product")

    for r in qs:
        if not r.sale_date:
            continue
        rows.append({
            "date": r.sale_date,
            "source": "Production Sales",
            "value": r.quantity * r.price,
        })

    qs_fin = FinancialReport.objects.all()

    for f in qs_fin:
        if not f.start_date:
            continue
        month_start = pd.to_datetime(f.start_date)
        rows.append({
            "date": month_start,
            "source": "Restaurant Sales",
            "value": f.rev_restaurant,
        })

    if not rows:
        return pd.DataFrame(columns=["date", "source", "value"])

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["month_year"] = pd.to_datetime(df["month_year"])

    return df


def build_sales_figure(dummy=False):
    df = load_sales_data(dummy=dummy)

    if df.empty:
        return px.line(title="No data available")

    df_agg = (
        df.groupby(["month_year", "source"], as_index=False)
          .agg({"value": "sum"})
          .sort_values("month_year")
    )

    fig = px.line(
        df_agg,
        x="month_year",
        y="value",
        color="source",
        markers=True,
        labels={
            "month_year": "Month-Year",
            "value": "Revenue",
            "source": "Source",
        }
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            type="date",
            tickformat="%b %Y",
            title="Month-Year",
        ),
    )

    return fig


class KA1_SalesRevenueLineCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_sales_figure(dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span("help", className="material-symbols-outlined d-flex"),
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
