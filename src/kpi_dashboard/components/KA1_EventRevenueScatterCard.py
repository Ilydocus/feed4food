import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from eventReport.models import EventReport


def load_event_revenue_data(dummy=False):
    if dummy:
        rows = [
            {
                "date": pd.to_datetime("2025-01-15"),
                "event_name": "Winter Gala",
                "revenue": 1200,
            },
            {
                "date": pd.to_datetime("2025-01-28"),
                "event_name": "Food Festival",
                "revenue": 900,
            },
            {
                "date": pd.to_datetime("2025-02-10"),
                "event_name": "Charity Run",
                "revenue": 1500,
            },
        ]
        df = pd.DataFrame(rows)
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
        return df

    qs = EventReport.objects.all()

    rows = []
    for r in qs:
        if not r.event_date:
            continue
        rows.append({
            "date": r.event_date,
            "event_name": r.event_name,
            "revenue": r.event_revenues,
        })

    if not rows:
        return pd.DataFrame(columns=["date", "event_name", "revenue"])

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


def build_event_revenue_figure(dummy=False):
    df = load_event_revenue_data(dummy=dummy)

    if df.empty:
        return px.scatter(title="No data available")

    month_order = sorted(df["month_year"].unique())

    fig = px.scatter(
        df,
        x="month_year",
        y="revenue",
        color="event_name",
        hover_name="event_name",
        labels={
            "month_year": "Month-Year",
            "revenue": "Revenue (€)",
            "event_name": "Event",
        }
    )

    tickvals = month_order
    ticktext = [pd.to_datetime(d).strftime("%b %Y") for d in month_order]
    fig.update_xaxes(tickmode="array", tickvals=tickvals, ticktext=ticktext)

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


class KA1_EventRevenueScatterCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_event_revenue_figure(dummy=dummy)

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
