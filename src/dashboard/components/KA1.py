import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go

from salesReport.models import SalesReport, SalesReportDetails
from core import reportUtils

import pandas as pd
from datetime import datetime


class ExpensesRevenues(dbc.Card):
    def __init__(self, title, id, description=None):
        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span(
                                "help",
                                className="material-symbols-outlined d-flex",
                            ),
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
                        responsive=True,
                        style={"height": "100%"},
                        #figure=fig #TODO fix
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(dcc.Markdown(description, link_target="_blank")),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )

def fetch_city_data_sales(city_name):
    if (SalesReport.objects.exists()):
        city_reports = SalesReport.objects.filter(city=city_name)
        report_ids = [report.report_id for report in city_reports]
        #currency = [report.currency for report in city_reports]

        #Get the dates of the sales
        # all_sale_dates = []
        revenue_per_date = {}
        for report_id in report_ids:
            detailed_reports = SalesReportDetails.objects.filter(
                report_id=report_id
            )
            for x in detailed_reports:
                revenue_per_date[x.sale_date] = 0.0 #Default revenue
        #     all_sale_dates.append([x.sale_date for x in detailed_reports])
        # for date in all_sale_dates:
        #     revenue_per_date[date] = 0.0 #Default revenue
        #Get the total revenues per date (and item)
        #total_revenue_per_date = []
        for date in list(revenue_per_date.keys()):
            for report_id in report_ids:
                detailed_reports = SalesReportDetails.objects.filter(
                    report_id=report_id, sale_date=date
                )
                for x in detailed_reports:
                    revenue_per_date[date]+= x.quantity*x.price 
        return list(revenue_per_date.keys()), list(revenue_per_date.values())
    else:
        return [],[]

#months = ['November','December','January','February']

#Extract financial data
#dates, revenues = fetch_city_data_revenues("Amsterdam") #TODO to fix

#Extract sales revenues
#TODO fix the below function - and then bring back the visualization again, issue to make it work when tables are empty
#dates, sales = fetch_city_data_sales(reportUtils.PartnerCities.Amsterdam) #TODO: Make it possible to switch between different LLs

#Extract event revenues
#TODO

#Create a dataframe with all this data, split by revenues and expenses

# df = pd.DataFrame({
#     "Dates": dates,
#     "Sales": sales
# })
# df['Dates'] = pd.to_datetime(df['Dates'])
# #Sum sales per month
# sales_byMonth=(df.groupby(pd.Grouper(key="Dates", freq='ME')).sum()).reset_index()
# #Add the month name
# sales_byMonth['Month']=sales_byMonth['Dates'].dt.strftime('%B')



# fig = go.Figure()
# fig.add_trace(go.Bar(x=sales_byMonth['Month'], y=sales_byMonth['Sales'],
#                 #base=[-500,-600,-700],
#                 marker_color='crimson',
#                 name='expenses'))
# fig.add_trace(go.Bar(x=sales_byMonth['Month'], y=sales_byMonth['Sales'],
#                 #base=0,
#                 marker_color='green',
#                 name='revenues'
#                 ))

# fig.update_layout(barmode='relative')