import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px

from salesReport.models import SalesReportDetails
from financialReport.models import FinancialReport
from django.utils.timezone import now
from core import reportUtils


def load_sales_data(living_lab, dummy=False):
    # Note: for some reason the dummy mode does not work anymore, remove it for now
    # if dummy:
    #     rows = [
    #         {"date": pd.to_datetime("2025-01-05"), "source": "Production Sales", "value": 300},
    #         {"date": pd.to_datetime("2025-01-18"), "source": "Production Sales", "value": 450},
    #         {"date": pd.to_datetime("2025-02-02"), "source": "Production Sales", "value": 520},
    #         {"date": pd.to_datetime("2025-03-01"), "source": "Production Sales", "value": 600},
    #         {"date": pd.to_datetime("2025-03-15"), "source": "Production Sales", "value": 480},
    #         {"date": pd.to_datetime("2025-04-05"), "source": "Production Sales", "value": 550},
    #         {"date": pd.to_datetime("2025-04-20"), "source": "Production Sales", "value": 620},
    #         {"date": pd.to_datetime("2025-05-02"), "source": "Production Sales", "value": 530},
    #         {"date": pd.to_datetime("2025-05-15"), "source": "Production Sales", "value": 700},
    #         {"date": pd.to_datetime("2025-01-01"), "source": "Restaurant Sales", "value": 800},
    #         {"date": pd.to_datetime("2025-02-01"), "source": "Restaurant Sales", "value": 950},
    #         {"date": pd.to_datetime("2025-03-01"), "source": "Restaurant Sales", "value": 1050},
    #         {"date": pd.to_datetime("2025-04-01"), "source": "Restaurant Sales", "value": 1100},
    #         {"date": pd.to_datetime("2025-05-01"), "source": "Restaurant Sales", "value": 1200},
    #     ]

    #     df = pd.DataFrame(rows)
    #     df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()
    #     df["month_year"] = pd.to_datetime(df["month_year"])
    #     return df

    # Getting information about the date
    today = now()
    year = today.year

    rows = []

    qs = SalesReportDetails.objects.select_related("report_id").filter(report_id__city=living_lab, sale_date__year=year)

    for r in qs:
        if not r.sale_date:
            continue
        rows.append({
            "date": r.sale_date,
            "source": "Production Sales",
            "value": r.quantity * r.price,
        })

    qs_fin = FinancialReport.objects.filter(city=living_lab, year=year)

    for f in qs_fin:
        if f.start_date:
            month_start = pd.to_datetime(f.start_date)
        else:
            # By default take the first day of the month
            month_num = list(reportUtils.Months.values).index(f.month) + 1 
            month_start = pd.Timestamp(year=f.year, month=month_num, day=1)
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

    print("Final", df, flush=True)

    return df


def build_sales_figure(living_lab, mode="line", dummy=False):
    df = load_sales_data(living_lab, dummy=dummy)

    if df.empty:
        return px.line(title="No data available")

    df_agg = (
        df.groupby(["month_year", "source"], as_index=False)
          .agg({"value": "sum"})
          .sort_values("month_year")
    )

    if mode == "line":
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
    else:
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
        xaxis=dict(type="date", tickformat="%b %Y", title="Month-Year"),
    )

    return fig


class KA1_SalesRevenueLineCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        fig = build_sales_figure(living_lab, dummy=dummy) 

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dcc.Dropdown(
                            id={"type": "salesrevenue-graph-mode", "index": id},
                            options=[
                                {"label": "Line Chart", "value": "line"},
                                {"label": "Stacked Bar Chart", "value": "bar"},
                            ],
                            value="line",
                            clearable=False,
                            style={"width": "180px"},
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "salesrevenue-graph", "index": id},
                        figure=fig,
                        responsive=True,
                        style={"height": "350px"},
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
