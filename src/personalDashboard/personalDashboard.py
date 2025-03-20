from report.models import ProduceReport, ProduceReportDetails, Item
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

# Trying to fix the graph height problem
#dash.page_container = html.Div([dcc.Location(id='_pages_location', refresh='callback-nav'), html.Div(id='_pages_content', disable_n_clicks=True, style={"height": "100%"}), dcc.Store(id='_pages_store'), html.Div(id='_pages_dummy', disable_n_clicks=True)], style={"height": "100%"}, id="parent_page_content")

# Create a Dash app
app = DjangoDash("PersonalDisplayApp",external_stylesheets=[dbc.themes.BOOTSTRAP])
#fig = go.Figure(data=go.Scatter(x=[], y=[]))
fig = go.Figure()

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


# Fetch data
def fetch_user_data(item, user_id):
    user_reports = ProduceReport.objects.filter(user=user_id)
    report_ids = [report.report_id for report in user_reports]
    timestamps = [report.creation_time for report in user_reports]
    date_produced = [report.start_date for report in user_reports]
    total_quantity = []
    for report_id in report_ids:
        detailed_reports = ProduceReportDetails.objects.filter(
            report_id=report_id, name=item
        )
        total_quantity.append(sum([x.quantity for x in detailed_reports]))
    return date_produced, total_quantity




# Layout
try:
    item_options = list(Item.objects.all().values_list("name", flat=True))
except Exception as e:
    item_options = []
# app.layout = html.Div(
#     [  dcc.Dropdown(
#             id="kpi-selector",
#             options=kpi_options,
#             placeholder="Select a KPI to display",
#             style={"margin-bottom": "15px"},
#         ),
#         dcc.Dropdown(
#             id="item-selector",
#             options=options,
#             placeholder="Select a product",
#             style={"margin-bottom": "15px"},
#         ),
#         #dcc.Graph(id="line-chart", figure=fig),
#         dcc.Graph(id="kpi-chart", figure=fig, className="h-100"
#         ),
#     ],
#     #  style={"width": "90%", "margin": "auto","height": "100vh",}, 
#     style={"height": "100%"}
# )

app.layout = dbc.Container(
    [
        html.P("Select data:", style={"color": "white"}),
        dcc.Dropdown(
            id="data-selector",
            #options=['KF1: Production per product', 'KF2: Sales per product', 'KF3: Workforce'],
            #options=kpi_options,
            placeholder="Select data to display",
            style={"margin-bottom": "15px"},
            options=[
                    {'label': 'Production per product', 'value': 'on'},
                    {'label': 'Sales per product', 'value': 'off'},
                    {'label': 'Workforce costs', 'value': 'off2'}
                ],
        ),
        # Create Div to place a conditionally visible element inside
        # html.Div([
            html.P("Product:", style={"color": "white"}, id="product-text"),
        # ], style= {"color": "white",'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
        # ),
        html.Div([
            dcc.Dropdown(
                id="item-selector",
                placeholder="Select a product",
                style={"margin-bottom": "15px"},
                options=item_options
            ),
        ], style= {'display': 'block',"margin-bottom": "15px"} # <-- This is the line that will be changed by the dropdown callback
        ),
        html.Div([
            #dcc.Graph(id="line-chart", figure=fig),
            dcc.Graph(id="data-chart", figure=fig, className="h-90"
            ),
        ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
        )
    ],
    fluid=True, style={"background-color":"#003399", "height": "100%" }
)

    # Callbacks
@app.callback(Output("data-chart", "figure"), [Input("item-selector", "value")])
def update_graph(value, **kwargs):
    dates, quantities = fetch_user_data(value, kwargs["user"].id)
    df = pd.DataFrame({
    "Day": dates,
    "Quantity": quantities
})
    #fig = go.Figure(data=go.Scatter(x=dates, y=quantities))
    fig = px.bar(df, x="Day", y="Quantity")
    #fig.update_layout(yaxis=dict(range=[min(quantities), max(quantities)]))
    return fig

@app.callback(
    Output("item-selector", "options"),
    Input("data-selector", "value"),
)
def chained_callback_product(kpi_selector):
    return (
        item_options if data-selector == "on" else []
    )

    # dff = copy.deepcopy(options)

    # if kpi_selector is not None:
    #     res=["test","test2"]
    #     #dff = dff.query("State == @state")
    # else:
    #     res=[]
    
    # return res

@app.callback(
   Output(component_id='product-text', component_property='style'),
   Input(component_id='data-selector', component_property='value'))

def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {"color": "white",'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}
    if visibility_state is None:
        return {'display': 'none'}
    else:
        return {'display': 'none'}

@app.callback(
   Output(component_id='item-selector', component_property='style'),
   [Input(component_id='data-selector', component_property='value')])

def show_hide_element2(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}
    if visibility_state is None:
        return {'display': 'none'}
    else:
        return {'display': 'none'}

@app.callback(
   Output(component_id='data-chart', component_property='style'),
   Input(component_id='data-selector', component_property='value'),
   Input(component_id='item-selector', component_property='value'))

def show_hide_element3(visibility_state, item_selected):
    if visibility_state == 'on' and item_selected is not None:
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}
    if visibility_state is None:
        return {'display': 'none'}
    else:
        return {'display': 'none'}




