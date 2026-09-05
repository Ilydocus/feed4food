from collections import defaultdict

import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
from django.utils.timezone import now
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from cultivationReport.models import CultivationReportDetails, CultivationReport

def load_latest_area_per_product_by_garden_month(living_lab):

        # 1. Find all distinct (garden, month) combinations with reports in this city
    combos = (
        CultivationReport.objects
        .filter(city=living_lab, garden__isnull=False, cultivation_date__isnull=False)
        .annotate(month_start=TruncMonth("cultivation_date"))
        .values_list("garden_id", "month_start")
        .distinct()
    )

    # 2. For each (garden, month) combo, find the latest report and record its month
    report_id_to_month = {}
    for garden_id, month_start in combos:
        latest_report = (
            CultivationReport.objects
            .filter(
                city=living_lab,
                garden_id=garden_id,
                cultivation_date__year=month_start.year,
                cultivation_date__month=month_start.month,
            )
            .order_by("-cultivation_date", "-creation_time")
            .first()
        )
        if latest_report:
            report_id_to_month[latest_report.report_id] = month_start

    if not report_id_to_month:
        return {}

    # 3. Get area per product per report, then bucket into the right month
    qs = (
        CultivationReportDetails.objects
        .filter(report_id__in=report_id_to_month.keys(),
                name__cultivation_type="m²",) #Only include for this graphs the products cultivated with a surface
        .values("report_id", "name__name")
        .annotate(total_area=Sum("area_cultivated"))
    )

    results = defaultdict(lambda: defaultdict(float))
    for row in qs:
        month_start = report_id_to_month[row["report_id"]]
        product = row["name__name"]
        results[month_start][product] += row["total_area"] or 0

    return {month: dict(products) for month, products in results.items()}

def load_surface_cultivation_data(living_lab, dummy=False):
    if dummy:
        data = [
            {"date": "2025-01-01", "product": "Lettuce", "surface": 120},
            {"date": "2025-02-01", "product": "Lettuce", "surface": 150},
            {"date": "2025-03-01", "product": "Lettuce", "surface": 160},
            {"date": "2025-04-01", "product": "Lettuce", "surface": 180},
            {"date": "2025-05-01", "product": "Lettuce", "surface": 200},
            {"date": "2025-01-01", "product": "Spinach", "surface": 80},
            {"date": "2025-02-01", "product": "Spinach", "surface": 95},
            {"date": "2025-03-01", "product": "Spinach", "surface": 110},
            {"date": "2025-04-01", "product": "Spinach", "surface": 130},
            {"date": "2025-05-01", "product": "Spinach", "surface": 140},
        ]
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
        return df

    monthly_data = load_latest_area_per_product_by_garden_month(living_lab)

    if not monthly_data:
        return pd.DataFrame(columns=["date", "product", "surface", "month_year"])

    rows = []
    for month_start, products in monthly_data.items():
        for product, surface in products.items():
            rows.append({
                "date": month_start,
                "product": product,
                "surface": surface,
            })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


def build_surface_cultivation_figure(living_lab, chart_type="area", dummy=False):
    df = load_surface_cultivation_data(living_lab, dummy=dummy)
    if df.empty:
        return px.area(title="No data available")

    if chart_type == "stacked":
        fig = px.bar(
            df,
            x="month_year",
            y="surface",
            color="product",
            barmode="stack",
            labels={
                "month_year": "Month-Year",
                "surface": "Surface (m²)",
                "product": "Product",
            }
        )
    else:
        fig = px.area(
            df,
            x="month_year",
            y="surface",
            color="product",
            line_group="product",
            markers=True,
            labels={
                "month_year": "Month-Year",
                "surface": "Surface (m²)",
                "product": "Product",
            }
        )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(tickformat="%b %Y", title="Month-Year"),
    )
    return fig


class KC2_SurfaceCultivatedPerProductCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        fig = build_surface_cultivation_figure(chart_type="area", living_lab=living_lab, dummy=dummy)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "surfacecultivated-graph-mode", "index": id},
                            options=[
                                {"label": "Area Chart", "value": "area"},
                                {"label": "Stacked Bar", "value": "stacked"},
                            ],
                            value="area",
                            clearable=False,
                            style={"width": "200px"},
                        )
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.CardBody(
                    [
                        dbc.Spinner(
                            dcc.Graph(
                                id={"type": "surfacecultivated-graph", "index": id},
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
                        dbc.ModalBody(dcc.Markdown(description or "", link_target="_blank")),
                    ],
                    id={"type": "surfacecultivated-graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
