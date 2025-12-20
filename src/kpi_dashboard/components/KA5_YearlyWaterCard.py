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


def build_two_bar_water_figures_current_year(dummy=False):
    rainfall_total = load_totals_rainfall_current_year(dummy=dummy)
    df_irr = load_totals_irrigation_current_year(dummy=dummy)

    irrigation_total = df_irr["quantity"].sum() if not df_irr.empty else 0
    target_quantity = irrigation_total * 0.15

    x_max = max(rainfall_total, irrigation_total) * 1.1

    fig_in = go.Figure()
    fig_in.add_trace(
        go.Bar(
            y=["Rainwater Harvested"],
            x=[rainfall_total],
            name="Rainwater Harvested",
            orientation="h",
        )
    )
    fig_in.update_layout(
        xaxis_title="Total Water",
        xaxis=dict(range=[0, x_max]),
        yaxis_title="",
        height=120,
        bargap=0.5,
        margin=dict(l=40, r=20, t=20, b=25),
        showlegend=True,
    )

    fig_out = go.Figure()
    for source in ["harvested", "tap", "other"]:
        qty = df_irr[df_irr["source"] == source]["quantity"].sum()
        fig_out.add_trace(
            go.Bar(
                y=["Irrigation Water Use"],
                x=[qty],
                name=f"Irrigation – {source}",
                orientation="h",
            )
        )

    fig_out.add_vline(
        x=target_quantity,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text="Target (15%)",
        annotation_position="top right",
        annotation_font=dict(size=12),
    )

    fig_out.update_layout(
        barmode="stack",
        xaxis_title="Total Water",
        xaxis=dict(range=[0, x_max]),
        yaxis_title="",
        height=120,
        bargap=0.5,
        margin=dict(l=40, r=20, t=30, b=25),
        showlegend=True,
    )

    return fig_in, fig_out


def irrigation_coverage_stat(dummy=False):
    rainfall = load_totals_rainfall_current_year(dummy=dummy)
    df_irr = load_totals_irrigation_current_year(dummy=dummy)

    harvested_irr = (
        df_irr[df_irr["source"] == "harvested"]["quantity"].sum()
        if not df_irr.empty else 0
    )

    if rainfall == 0:
        return html.Div("No rainwater harvested this year.")

    pct = (harvested_irr / rainfall) * 100
    color = "green" if pct >= 15 else "red"

    return html.Div(
        [
            html.Div(
                f"{pct:.1f}%",
                className="fw-bold",
                style={"fontSize": "2.5rem", "color": color, "textAlign": "center"},
            ),
            html.Small(
                "of harvested rainwater used for irrigation.",
                className="text-muted",
            ),
        ],
        style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
    )


class KA5_YearlyWaterCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        year = current_year()
        title_with_year = f"{title} (Jan {year} to Present)"

        fig_in, fig_out = build_two_bar_water_figures_current_year(dummy=dummy)
        stat_ui = irrigation_coverage_stat(dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [html.H5(title_with_year, className="m-0")],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Row(
                    [
                        # Graphs column
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id={"type": "graph-in", "index": id},
                                    figure=fig_in,
                                    responsive=True,
                                    style={"height": "120px"},
                                ),
                                dcc.Graph(
                                    id={"type": "graph-out", "index": id},
                                    figure=fig_out,
                                    responsive=True,
                                    style={"height": "120px"},
                                ),
                            ],
                            md=10,
                        ),
                        # Percentage stat column
                        dbc.Col(
                            html.Div(stat_ui, className="p-3 d-flex align-items-center justify-content-center"),
                            md=2,
                        ),
                    ],
                    className="px-3",
                ),
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
