import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict

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
                name__cultivation_type="plants",) #Only include for this graphs the products cultivated with a surface
        .values("report_id", "name__name")
        .annotate(total_area=Sum("area_cultivated"))
    )

    results = defaultdict(lambda: defaultdict(float))
    for row in qs:
        month_start = report_id_to_month[row["report_id"]]
        product = row["name__name"]
        results[month_start][product] += row["total_area"] or 0

    return {month: dict(products) for month, products in results.items()}

def load_plants_cultivation_data(living_lab):

    monthly_data = load_latest_area_per_product_by_garden_month(living_lab)

    if not monthly_data:
        return pd.DataFrame(columns=["date", "product", "plants", "month_year"])

    rows = []
    for month_start, products in monthly_data.items():
        for product, plants in products.items():
            rows.append({
                "date": month_start,
                "product": product,
                "plants": plants,
            })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    return df


def build_plants_cultivated_figure(living_lab, chart_type="line", dummy=False):
    if dummy:
        dummy_data = [
            {"month_year": "2025-01", "product": "Tomato",    "plants": 120},
            {"month_year": "2025-01", "product": "Cucumber",  "plants":  80},
            {"month_year": "2025-02", "product": "Tomato",    "plants": 140},
            {"month_year": "2025-02", "product": "Cucumber",  "plants":  90},
            {"month_year": "2025-03", "product": "Tomato",    "plants": 135},
            {"month_year": "2025-03", "product": "Cucumber",  "plants": 100},
            {"month_year": "2025-04", "product": "Tomato",    "plants": 150},
            {"month_year": "2025-04", "product": "Cucumber",  "plants": 110},
            {"month_year": "2025-05", "product": "Tomato",    "plants": 155},
            {"month_year": "2025-05", "product": "Cucumber",  "plants": 115},
        ]
        df = pd.DataFrame(dummy_data)
        df["month_year"] = pd.to_datetime(df["month_year"])

    else:
        df = load_plants_cultivation_data(living_lab)
        if df.empty:
            return px.line(title="No data available")

    # Chart Type
    if chart_type == "stacked":
        fig = px.bar(
            df,
            x="month_year",
            y="plants",
            color="product",
            barmode="stack",
            labels={
                "month_year": "Month-Year",
                "plants": "Number of Plants",
                "product": "Product",
            },
        )
    else:
        fig = px.line(
            df,
            x="month_year",
            y="plants",
            color="product",
            markers=True,
            labels={
                "month_year": "Month-Year",
                "plants": "Number of Plants",
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


class KC2_PlantsPerProductCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        fig = build_plants_cultivated_figure(living_lab=living_lab, chart_type="line", dummy=dummy)

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
