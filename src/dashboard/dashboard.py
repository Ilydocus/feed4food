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
from .components.FigureCard3 import FigureCard3
from .components.FigureCard4 import FigureCard4
from .components.FigureCard5 import FigureCard5
from .components.FigureCard6 import FigureCard6
from .components.KA1 import ExpensesRevenues

# Trying to fix the graph height problem
#dash.page_container = html.Div([dcc.Location(id='_pages_location', refresh='callback-nav'), html.Div(id='_pages_content', disable_n_clicks=True, style={"height": "100%"}), dcc.Store(id='_pages_store'), html.Div(id='_pages_dummy', disable_n_clicks=True)], style={"height": "100%"}, id="parent_page_content")

# Create a Dash app
app = DjangoDash("KPIDisplayApp",external_stylesheets=[dbc.themes.BOOTSTRAP])
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

# app.layout = dbc.Container(
#     [
#         html.P("KPI:", style={"color": "white"}),
#         dcc.Dropdown(
#             id="kpi-selector",
#             #options=['KF1: Production per product', 'KF2: Sales per product', 'KF3: Workforce'],
#             #options=kpi_options,
#             placeholder="Select a KPI to display",
#             style={"margin-bottom": "15px"},
#             options=[
#                     {'label': 'KS3: Local and nutritious food production', 'value': 'on'},
#                     {'label': 'KF2: Sales per product', 'value': 'off'},
#                     {'label': 'KF3: Workforce', 'value': 'off2'}
#                 ],
#         ),
#         # Create Div to place a conditionally visible element inside
#         # html.Div([
#             html.P("Plant variety:", style={"color": "white"}, id="product-text"),
#         # ], style= {"color": "white",'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
#         # ),
#         html.Div([
#             dcc.Dropdown(
#                 id="item-selector",

#                 placeholder="Select a product",
#                 style={"margin-bottom": "15px"},
#             ),
#         ], style= {'display': 'block',"margin-bottom": "15px"} # <-- This is the line that will be changed by the dropdown callback
#         ),
#         html.Div([
#             #dcc.Graph(id="line-chart", figure=fig),
#             dcc.Graph(id="kpi-chart", figure=fig, className="h-90"
#             ),
#         ], style= {'display': 'block'} # <-- This is the line that will be changed by the dropdown callback
#         )
#     ],
#     fluid=True, style={"background-color":"#003399", "height": "100%" }
# )

app.layout = html.Div([html.P("KPI:", style={"color": "white"}), 
dcc.Dropdown(
            id="kpi-selector",
            #options=['KF1: Production per product', 'KF2: Sales per product', 'KF3: Workforce'],
            #options=kpi_options,
            placeholder="Select a KPI to display",
            style={"margin-bottom": "15px"},
            options=[
                    {'label': 'KS3: Local and nutritious food production', 'value': 'ks3'},
                    {'label': 'KA1: Economic viability', 'value': 'ka1'},
                    #{'label': 'KC1: Efficient trainuWorkforce', 'value': 'off2'}
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
                    #dbc.Col(MetricCard("TV Shows", id="tv-count"), width=4),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        FigureCard(
                            "Target progress: Cultivated species",
                            id="target-all-species",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=7,
                    ),
                    dbc.Col(
                        FigureCard2(
                            "Nutrients coverage",
                            id="nutrients-covered",
                            #description=figure_descriptions.get("title-counts"),
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
                    FigureCard3(
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
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             FigureCard(
            #                 "Catalog Diversity",
            #                 id="diversity",
            #                 #description=figure_descriptions.get("diversity"),
            #             ),
            #             sm=12,
            #             md=6,
            #         ),
            #         dbc.Col(
            #             FigureCard(
            #                 "Top Countries",
            #                 id="top-country",
            #                 #description=figure_descriptions.get("top-country"),
            #             ),
            #             sm=12,
            #             md=6,
            #         ),
            #     ],
            #     className="dashboard-row",
            # ),
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             FigureCard(
            #                 "2 Week Catalog Change",
            #                 id="growth",
            #                 #description=figure_descriptions.get("growth"),
            #             ),
            #             sm=12,
            #             md=12,
            #         ),
            #     ],
            #     className="dashboard-row",
            # ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="ks3-dashboard"),
#### KA1 KPI dashboard
html.Div([
    dbc.Row(
    dbc.Col(
        [
            # dbc.Row(
            #     [
            #         dbc.Col(MetricCard("Latest balance", id="species-count"), width=6),
            #         dbc.Col(MetricCard2("Native species", id="native-count"), width=6),
                    
            #     ]
            # ),
            dbc.Row(
                [
                    dbc.Col(
                        ExpensesRevenues(
                            "Expenses and revenues in the LL Amsterdam",
                            id="expenses-revenues",
                            #description=figure_descriptions.get("summary"),
                        ),
                        sm=12,
                        md=12,
                    ),
                    # dbc.Col(
                    #     FigureCard2(
                    #         "Nutrients coverage",
                    #         id="nutrients-covered",
                    #         #description=figure_descriptions.get("title-counts"),
                    #     ),
                    #     sm=12,
                    #     md=5,
                    # ),
                ],
                className="dashboard-row",
            ),
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
                    # dbc.Col(
                    #     FigureCard2(
                    #         "Nutrients coverage",
                    #         id="nutrients-covered",
                    #         #description=figure_descriptions.get("title-counts"),
                    #     ),
                    #     sm=12,
                    #     md=5,
                    # ),
                ],
                className="dashboard-row",
            ),
        ],
    ),
    id="dashboard",
)
], style= {'display': 'block',"background-color":"#003399",}, # <-- This is the line that will be changed by the dropdown callback
id="ka1-dashboard")

],style={"background-color":"#003399", "height": "100%" })

    # Callbacks
# @app.callback(Output("kpi-chart", "figure"), [Input("item-selector", "value")])
# def update_graph(value, **kwargs):
#     dates, quantities = fetch_user_data(value, kwargs["user"].id)
#     df = pd.DataFrame({
#     "Day": dates,
#     "Quantity": quantities
# })
#     #fig = go.Figure(data=go.Scatter(x=dates, y=quantities))
#     #fig = px.bar(df, x="Day", y="Quantity")
#     fig = go.Figure(go.Indicator(
#     domain = {'x': [0, 1], 'y': [0, 1]},
#     value = 9,
#     mode = "gauge+number+delta",
#     title = {'text': "All varieties"},
#     delta = {'reference': 8},
#     gauge = {'axis': {'range': [None, 20]},
#              #'steps' : [
#              #    {'range': [0, 250], 'color': "lightgray"},
#              #    {'range': [250, 400], 'color': "gray"}],
#              'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 15}}))
#     #fig.update_layout(yaxis=dict(range=[min(quantities), max(quantities)]))
#     return fig

# @app.callback(
#     Output("item-selector", "options"),
#     Input("kpi-selector", "value"),
# )
# def chained_callback_product(kpi_selector):
#     return (
#         item_options2 if kpi_selector == "on" else []
#     )

#     # dff = copy.deepcopy(options)

#     # if kpi_selector is not None:
#     #     res=["test","test2"]
#     #     #dff = dff.query("State == @state")
#     # else:
#     #     res=[]
    
#     # return res

# @app.callback(
#    Output(component_id='product-text', component_property='style'),
#    Input(component_id='kpi-selector', component_property='value'))

# def show_hide_element(visibility_state):
#     if visibility_state == 'on':
#         return {"color": "white",'display': 'block'}
#     if visibility_state == 'off':
#         return {'display': 'none'}
#     if visibility_state is None:
#         return {'display': 'none'}
#     else:
#         return {'display': 'none'}


# Metric card callbacks
# @app.callback(
#     Output({"type": "metric-value", "index": "species-count"}, "children"),
# )
# def display_species_count():
#     print(len(item_options))
#     return {len(item_options)}#data_connector.get_platform_count(filters)

#Showing the dashboard part only when KPI is selected
@app.callback(
   Output(component_id='ks3-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'ks3':
        return {'display': 'block'}
    #if visibility_state == 'off':
    #    return {'display': 'none'}
    #if visibility_state is None:
        #return {'display': 'none'}
    else:
        return {'display': 'none'}

@app.callback(
   Output(component_id='ka1-dashboard', component_property='style'),
   [Input(component_id='kpi-selector', component_property='value')])
def show_hide_element2(visibility_state):
    if visibility_state == 'ka1':
        return {'display': 'block'}
    #if visibility_state == 'off':
    #    return {'display': 'none'}
    #if visibility_state is None:
        #return {'display': 'none'}
    else:
        return {'display': 'none'}

@app.callback(
    Output({"type": "metric-value", "index": "species-count"}, "children"),
    [Input("kpi-selector", "value")]  # Add this input
)
def display_species_count(kpi_value, **kwargs):
    try:
        # Count unique Items in the database
        ##TODO:update to have the ones for which at least one report exists
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
        # Count items with the locale flag in the database
        ##TODO:update to have the ones for which at least one report exists
        species_count = Product.objects.filter(locale=True).count()
        return species_count
    except Exception as e:
        return 0

# @app.callback(
#    Output(component_id='kpi-chart', component_property='style'),
#    Input(component_id='kpi-selector', component_property='value'),
#    Input(component_id='item-selector', component_property='value'))

# def show_hide_element3(visibility_state, item_selected):
#     if visibility_state == 'on' and item_selected is not None:
#         return {'display': 'block'}
#     if visibility_state == 'off':
#         return {'display': 'none'}
#     if visibility_state is None:
#         return {'display': 'none'}
#     else:
#         return {'display': 'none'}




