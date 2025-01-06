from report.models import ProduceReport, ProduceReportDetails, Item
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

# Create a Dash app
app = DjangoDash("UserReportApp")
fig = go.Figure(data=go.Scatter(x=[], y=[]))


# Fetch data
def fetch_user_data(item, user_id):
    user_reports = ProduceReport.objects.filter(user=user_id)
    report_ids = [report.report_id for report in user_reports]
    timestamps = [report.creation_time for report in user_reports]
    total_quantity = []
    for report_id in report_ids:
        detailed_reports = ProduceReportDetails.objects.filter(
            report_id=report_id, name=item
        )
        total_quantity.append(sum([x.quantity for x in detailed_reports]))
    print(timestamps, total_quantity)
    return timestamps, total_quantity


# Layout
try:
    options = list(Item.objects.all().values_list("name", flat=True))
except Exception as e:
    options = []
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="item-selector",
            options=options,
            placeholder="Select something",
        ),
        dcc.Graph(id="line-chart", figure=fig, style={"height": "100vh"}),
    ],
    style={"width": "80%", "margin": "auto", "height": "100vh"},
)


# Callbacks
@app.callback(Output("line-chart", "figure"), [Input("item-selector", "value")])
def update_graph(value, **kwargs):
    dates, quantities = fetch_user_data(value, kwargs["user"].id)
    print("after fetch", dates, quantities)
    fig = go.Figure(data=go.Scatter(x=dates, y=quantities))
    return fig
