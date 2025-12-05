import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

import pandas as pd
import plotly.graph_objects as go
from django.db.models import Sum
from django.utils.timezone import now

from waterReport.models import WaterReportRainfall, WaterReportIrrigation


def current_year():
    return now().year


def load_totals_rainfall_current_year(dummy=False):
    if dummy:
        return 420.0
    year = current_year()
    total = (
        WaterReportRainfall.objects
        .filter(start_date__year=year)
        .aggregate(total=Sum("quantity"))
        .get("total") or 0
    )
    return float(total)


def load_totals_irrigation_current_year(dummy=False):
    if dummy:
        data = {
            "source": ["harvested", "tap", "other"],
            "quantity": [120, 260, 90],
        }
        return pd.DataFrame(data)
    year = current_year()
    qs = (
        WaterReportIrrigation.objects
        .filter(start_date__year=year)
        .values("source")
        .annotate(quantity=Sum("quantity"))
    )
    rows = [{"source": r["source"], "quantity": r["quantity"]} for r in qs]
    return pd.DataFrame(rows)


def build_two_bar_water_figure_current_year(dummy=False):
    rainfall_total = load_totals_rainfall_current_year(dummy=dummy)
    df_irr = load_totals_irrigation_current_year(dummy=dummy)

    irrigation_total = df_irr["quantity"].sum() if not df_irr.empty else 0
    target_quantity = irrigation_total * 0.15

    fig = go.Figure()

    for source in ["harvested", "tap", "other"]:
        qty = df_irr[df_irr["source"] == source]["quantity"].sum()
        fig.add_trace(
            go.Bar(
                y=["Irrigation Water Use"],
                x=[qty],
                name=f"Irrigation – {source}",
                orientation="h",
            )
        )

    fig.add_trace(
        go.Bar(
            y=["Rainwater Harvested"],
            x=[rainfall_total],
            name="Rainwater Harvested",
            orientation="h",
        )
    )

    fig.add_vline(
        x=target_quantity,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text="Target (15%)",
        annotation_position="top",
    )

    fig.update_layout(
        barmode="stack",
        xaxis_title="Total Water",
        yaxis_title="",
        legend_title="Water Type",
        height=300,
        margin=dict(l=40, r=20, t=20, b=30),
    )

    return fig


def irrigation_coverage_stat(dummy=False):
    rainfall = load_totals_rainfall_current_year(dummy=dummy)
    df_irr = load_totals_irrigation_current_year(dummy=dummy)
    irrigation_total = df_irr["quantity"].sum() if not df_irr.empty else 0

    if irrigation_total == 0:
        return html.Div("No irrigation water used this year.")

    pct = (rainfall / irrigation_total) * 100
    color = "green" if pct >= 15 else "red"

    return html.Div(
        [
            html.Div(
                f"{pct:.1f}%",
                className="fw-bold",
                style={"fontSize": "2.5rem", "color": color}
            ),
            html.Small(
                "of irrigation demand covered by harvested rainwater.",
                className="text-muted"
            ),
        ]
    )


class KA5_YearlyWaterCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        year = current_year()
        title_with_year = f"{title} (Jan {year} to Present)"

        fig = build_two_bar_water_figure_current_year(dummy=dummy)
        stat_ui = irrigation_coverage_stat(dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title_with_year, className="m-0"),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Row([
                    dbc.Col(
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
                        md=10,
                        sm=12
                    ),
                    dbc.Col(
                        html.Div(
                            stat_ui,
                            className="p-3"
                        ),
                        md=2,
                        sm=12
                    ),
                ], className="px-3"),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title_with_year)),
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
