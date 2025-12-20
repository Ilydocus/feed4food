import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from eventReport.models import EventReport
from financialReport.models import FinancialReport


def load_event_other_revenues_data():
    rows = []

    qs_events = EventReport.objects.all()

    for e in qs_events:
        if not e.event_date:
            continue
        rows.append({
            "date": pd.to_datetime(e.event_date),
            "source": "Event Revenues",
            "value": e.event_revenues,
        })

    qs_fin = FinancialReport.objects.all()

    for f in qs_fin:
        if not f.start_date:
            continue
        month_start = pd.to_datetime(f.start_date)
        rows.append({
            "date": month_start,
            "source": "Other Revenues",
            "value": f.rev_others,
        })

    if not rows:
        return pd.DataFrame(columns=["date", "source", "value"])

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["month_year"] = pd.to_datetime(df["month_year"])

    return df


def build_events_other_bar_figure(dummy=False):
    if dummy:
        dummy_data = [
            {"month_year": "2025-01", "source": "Event Revenues",  "value": 1200},
            {"month_year": "2025-01", "source": "Other Revenues",  "value":  600},

            {"month_year": "2025-02", "source": "Event Revenues",  "value": 1500},
            {"month_year": "2025-02", "source": "Other Revenues",  "value":  750},

            {"month_year": "2025-03", "source": "Event Revenues",  "value": 1100},
            {"month_year": "2025-03", "source": "Other Revenues",  "value":  700},

            {"month_year": "2025-04", "source": "Event Revenues",  "value": 1600},
            {"month_year": "2025-04", "source": "Other Revenues",  "value":  820},

            {"month_year": "2025-05", "source": "Event Revenues",  "value": 1700},
            {"month_year": "2025-05", "source": "Other Revenues",  "value":  900},
        ]

        df = pd.DataFrame(dummy_data)
        df["month_year"] = pd.to_datetime(df["month_year"])

    else:
        df = load_event_other_revenues_data()

        if df.empty:
            return px.bar(title="No data available")

        df["month_year"] = pd.to_datetime(df["month_year"])

    df_agg = (
        df.groupby(["month_year", "source"], as_index=False)
          .agg({"value": "sum"})
          .sort_values("month_year")
    )

    fig = px.bar(
        df_agg,
        x="month_year",
        y="value",
        color="source",
        barmode="stack",
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


class KA1_EventsAndOtherRevenuesBarCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_events_other_bar_figure(dummy=dummy)

        super().__init__(
            children=[
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
