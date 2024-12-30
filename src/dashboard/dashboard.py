from daily_reports.models import ProduceReport, ProduceReportDetails, Items
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

# Create a Dash app
app = DjangoDash('UserReportApp')
fig = go.Figure(data=go.Scatter(x=[], y=[]))


# Fetch data
def fetch_user_data(item, user_id):
    user_reports = ProduceReport.objects.filter(user=user_id)
    report_ids = [report.id for report in user_reports]
    timestamps = [report.timestamp for report in user_reports]
    total_quantity = []
    for report_id in report_ids:
        detailed_reports = ProduceReportDetails.objects.filter(report_id=report_id, item_id=item)
        total_quantity.append(sum([x.quantity for x in detailed_reports]))
    return timestamps, total_quantity

# Layout
app.layout = html.Div([
    dcc.Dropdown(id='item-selector',
                  options=list(Items.objects.all().values_list('name', flat=True)), 
                  value='Apples',
                  placeholder='Select something'
                  ),
    dcc.Graph(id='line-chart', figure=fig, style={'height': '100vh'})],
    style={'width': '80%', 'margin': 'auto', 'height': '100vh'}
)

# Callbacks
@app.callback(
    Output('line-chart', 'figure'),
    [Input('item-selector', 'value')]
)
def update_graph(value, **kwargs):
    dates, quantities = fetch_user_data(value, kwargs['user'].id)
    fig = go.Figure(data=go.Scatter(x=dates, y=quantities))
    return fig