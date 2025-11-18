from productionReport.models import ProductionReport, ProductionReportDetails, Product
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

from .components.MetricCard import MetricCard
from .components.MetricCard2 import MetricCard2
from .components.FigureCard import FigureCard
from .components.FigureCard2 import FigureCard2
from .components.FigureCard4 import FigureCard4
from .components.FigureCard5 import FigureCard5
from .components.FigureCard6 import FigureCard6
from .components.KA1 import ExpensesRevenues


# Create a Dash app
app = DjangoDash("KPIVisualisationApp",external_stylesheets=[dbc.themes.BOOTSTRAP])
#fig = go.Figure(data=go.Scatter(x=[], y=[]))
fig = go.Figure()



# Fetch data
def fetch_user_data(item, user_id):
    user_reports = ProductionReport.objects.filter(user=user_id)
    report_ids = [report.report_id for report in user_reports]
    timestamps = [report.creation_time for report in user_reports]
    date_produced = [report.start_date for report in user_reports]
    total_quantity = []
    for report_id in report_ids:
        detailed_reports = ProductionReportDetails.objects.filter(
            report_id=report_id, name=item
        )
        total_quantity.append(sum([x.quantity for x in detailed_reports]))
    return date_produced, total_quantity




# Layout
try:
    item_options = list(Product.objects.all().values_list("name", flat=True))
except Exception as e:
    item_options = []
item_options2=['All varieties']


app.layout = html.Div([html.P("KPI:", style={"color": "white"}), 
dcc.Dropdown(
            id="kpi-selector",
            placeholder="Select a KPI to display",
            style={"margin-bottom": "15px"},
            options=[
                    {'label': 'KA1', 'value': 'ka1'},
                    {'label': 'KC1-P', 'value': 'kc1p'},
                    {'label': 'KC2', 'value': 'kc2'},
                    {'label': 'KC3', 'value': 'kc3'},                    
                    {'label': 'KC4', 'value': 'kc4'},
                    {'label': 'KC5', 'value': 'kc5'},
                ],
        ),
#### KS3 KPI dashboard
html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(MetricCard("Cultivated species", id="species-count"), width=6),
                    dbc.Col(MetricCard2("Native species", id="native-count"), width=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard(
                            "Target progress: Cultivated species",
                            id="target-all-species",
                        ),
                        sm=12,
                        md=7,
                    ),
                    dbc.Col(
                        FigureCard2(
                            "Nutrients coverage",
                            id="nutrients-covered",
                        ),
                        sm=12,
                        md=5,
                    ),
                ],
                className="dashboard-row",
            ),
            dbc.Row(
                [
                dbc.Col(
                    FigureCard4(
                        "Target progress: Native species",
                        id="target-native",
                        #description=figure_descriptions.get("quality"),
                    ),
                    width=6,
                ),
                dbc.Col(
                    FigureCard4(
                        "Color coverage",
                        id="colors-covered",
                        #description=figure_descriptions.get("quality"),
                    ),
                    width=6,
                ),
                ],className="dashboard-row",
            ),
            
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="ka1-dashboard"),
#### KA1 KPI dashboard
html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard6(
                            "Balance",
                            id="balance",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="kc1p-dashboard"),


html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard6(
                            "Balance",
                            id="balance",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="kc2-dashboard"),

html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard6(
                            "Balance",
                            id="balance",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="kc3-dashboard"),

html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard6(
                            "Balance",
                            id="balance",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="kc4-dashboard"),

html.Div([
    dbc.Row(
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard6(
                            "Balance",
                            id="balance",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="kc5-dashboard")

],style={"background-color":"#003399", "height": "100%" })



#Showing the dashboard part only when KPI is selected
@app.callback(
   Output(component_id='ka1-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'ka1':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
   Output(component_id='kc1p-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'kc1p':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
   Output(component_id='kc2-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'kc2':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
   Output(component_id='kc3-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'kc3':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    

@app.callback(
   Output(component_id='kc4-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'kc4':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
   Output(component_id='kc5-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'kc5':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output({"type": "metric-value", "index": "species-count"}, "children"),
    [Input("kpi-selector", "value")]  # Add this input
)
def display_species_count(kpi_value, **kwargs):
    try:
        species_count = Product.objects.count()
        return species_count
    except Exception as e:
        return 0

@app.callback(
    Output({"type": "metric-value", "index": "native-count"}, "children"),
    [Input("kpi-selector", "value")]  # Add this input
)
def display_native_count(kpi_value, **kwargs):
    try:
        species_count = Product.objects.filter(locale=True).count()
        return species_count
    except Exception as e:
        return 0



