from productionReport.models import ProductionReport, ProductionReportDetails, Product
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

# Import custom FigureCard components
from .components.KA1_QuantitySold import KA1_QuantitySold
from .components.KA1_PriceProduct import KA1_PriceProduct
from .components.KA1_Costs import KA1_CostsCard
from .components.KA1_Funding import KA1_FundingCard
from .components.KA5_IrrigationWaterUse import KA5_FigureCard
from .components.KA2_MetricCard_2 import KA2_MetricCard
from .components.KA5_RainwaterHarvested import KA5_RainwaterCard
from .components.KA5_YearlyWaterCard import KA5_YearlyWaterCard
from .components.KA1_BalanceCard import KA1_BalanceCard 
from .components.KA1_MonthlyBreakdownCard import KA1_MonthlyBreakdownCard
from .components.KA2_MetricCard import KA2_AreaChemicalCard
from .components.KA2_PlantChemicalCard import KA2_PlantChemicalCard
from .components.KA2_PlantsPerProductCard import KA2_PlantsPerProductCard
from .components.KA2_ChemicalUsePerProductCard import KA2_ChemicalUsePerProductCard
from .components.KA2_SurfaceCultivatedPerProductCard import KA2_SurfaceCultivatedPerProductCard
from .components.KA1_EventRevenueScatterCard import KA1_EventRevenueScatterCard
from .components.KA1_SalesRevenueLineCard import KA1_SalesRevenueLineCard
from .components.KA1_EventsAndOtherRevenuesBarCard import KA1_EventsAndOtherRevenuesBarCard
# Create a Dash app
app = DjangoDash("KPIVisualisationApp", external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize empty figure
fig = go.Figure()


# Layout
app.layout = html.Div([
    html.P("KPI:", style={"color": "white"}), 
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

    # Dashboard content placeholders
    html.Div(id="ka1-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc1p-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc2-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc3-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc4-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc5-dashboard", children=[], style={'display': 'none'}),
], style={"background-color":"#003399", "height": "100%"})

# Callback for showing the right KPI dashboard
@app.callback(
    [
        Output('ka1-dashboard', 'style'),
        Output('kc1p-dashboard', 'style'),
        Output('kc2-dashboard', 'style'),
        Output('kc3-dashboard', 'style'),
        Output('kc4-dashboard', 'style'),
        Output('kc5-dashboard', 'style')
    ],
    [Input('kpi-selector', 'value')]
)
def show_hide_dashboards(kpi_value):
    # Default: hide all dashboards
    visibility = {kpi: {'display': 'none'} for kpi in ['ka1', 'kc1p', 'kc2', 'kc3', 'kc4', 'kc5']}
    
    if kpi_value:
        visibility[kpi_value] = {'display': 'block'}  # Show selected dashboard
    
    return visibility['ka1'], visibility['kc1p'], visibility['kc2'], visibility['kc3'], visibility['kc4'], visibility['kc5']

# Helper function to generate the layout for each KPI
def create_kpi_layout(kpi_name):
    if kpi_name == 'ka1':
        return html.Div([

            dbc.Row([
                dbc.Col(
                    KA1_BalanceCard(id="balance-ka1", dummy = True),
                    sm=12, md=12,
                    className="mb-4"
                )
            ]),
            dbc.Row([
                dbc.Col(
                    KA1_MonthlyBreakdownCard(
                        "Monthly Financial Breakdown",
                        id="monthly-breakdown-ka1", dummy = True
                    ),
                    sm=12, md=12
                )
            ]),


            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Revenue and Sales", className="card-title")),
                                dbc.CardBody([
                                    KA1_EventRevenueScatterCard("Revenue per Event", id="revenue-ka1", dummy = True),
                                    KA1_SalesRevenueLineCard("Production Sales and Sales in Restaurant", id="prodsales-ka1", dummy = True)
                                ]),
                            ],
                        ),
                        sm=12, md=4
                    ),

                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Cost and Revenue", className="card-title")),
                                dbc.CardBody([
                                    KA1_CostsCard("Workforce Costs, Purchase Costs, and Other Costs", id="costs-ka1", dummy = True),
                                    KA1_EventsAndOtherRevenuesBarCard("Revenues from Events vs. Other Revenues", id="revenueevents-ka1", dummy = True)
                                ]),
                            ],
                        ),
                        sm=12, md=4
                    ),

                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4("Product Sales", className="card-title")),
                                    dbc.CardBody([
                                        KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-ka1", dummy = True),
                                        # KA1_PriceProduct("Price per Product", id="priceprod-ka1")
                                    ]),
                                ],
                            ),

                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4("Funding", className="card-title")),
                                    dbc.CardBody([
                                        KA1_FundingCard("Project Funding and Other Funding", id="funding-ka1", dummy = True)
                                    ]),
                                ],
                                style={'marginTop': '20px'}
                            ),
                        ],
                        sm=12, md=4
                    )
                ]
            ),
        ])



    elif kpi_name == 'kc1p':
        return html.Div([
            dbc.Row(
                dbc.Col([KA5_FigureCard("KC3 Balance", id="balance-kc3")], sm=12, md=12)
            ),
        ])

    elif kpi_name == 'kc2':
        return html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Cultivated Area", className="card-title")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(KA2_AreaChemicalCard("Surface of Cultivated Area Treated with Chemical Fertilizers/Pesticides", id="metric1-kc2", dummy = True), sm=6, md=6),
                                dbc.Col(KA2_PlantChemicalCard("Number of Plants in Cultivated Area Treated with Chemical Fertilizers/Pesticides", id="metric-2-kc2", dummy = True), sm=6, md=6)
                            ])
                        ]),
                    ]), sm=12, md=6
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Additional Information", className="card-title")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(KA2_MetricCard("Gardens/Holdings in Use", id="metric3-kc2", dummy = True), sm=6, md=6),
                                dbc.Col(KA2_MetricCard("Active Ingredient in Pesticide/Fertilizer Commercial Product", id="metric4-trend-kc2", dummy = True), sm=6, md=6)
                            ])
                        ]),
                    ]), sm=12, md=6
                ),
            ]),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Usage Overview", className="card-title")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(KA2_ChemicalUsePerProductCard("Quantity of Chemical Fertilizer/Pesticide Used per Product", id="graph1-kc2", dummy = True), sm=4, md=4),
                                dbc.Col(KA2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated per Product", id="graph2-kc2", dummy = True), sm=4, md=4),
                                dbc.Col(KA2_PlantsPerProductCard("Plants Actively Cultivated per Product", id="graph3-kc2", dummy = True), sm=4, md=4),
                            ])
                        ])
                    ]), sm=12, style={'marginTop': '20px'}  # Adding space between rows
                )
            ),
        ])


    elif kpi_name == 'kc3':
        return html.Div([
            dbc.Row(
                dbc.Col([KA5_FigureCard("KC3 Balance", id="balance-kc3")], sm=12, md=12)
            ),
        ])
    elif kpi_name == 'kc4':
        return html.Div([
            dbc.Row(
                dbc.Col([KA5_FigureCard("KC4 Balance", id="balance-kc4")], sm=12, md=12)
            ),
        ])
    elif kpi_name == 'kc5':
        return html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Irrigation Details", className="card-title")),
                        dbc.CardBody([
                            KA5_YearlyWaterCard("Irrigation Frequency", id="graph1-kc5", dummy = True)
                        ]),
                    ]),
                    sm=12, md=12
                ),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Rainwater Harvested", className="card-title")),
                        dbc.CardBody([
                            KA5_RainwaterCard("Rainwater Harvested", id="graph2-kc5", dummy = True)
                        ]),
                    ]),
                    sm=12, md=6
                ),

                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Irrigation Water Use per Source", className="card-title")),
                        dbc.CardBody([
                            KA5_FigureCard("Irrigation Water Use per Source", id="graph3-kc5", dummy = True)
                        ]),
                    ]),
                    sm=12, md=6
                ),
            ])
        ])

    else:
        return html.Div([])  # Return an empty div if no valid KPI

# Callback to dynamically update the layout for each KPI
@app.callback(
    [
        Output('ka1-dashboard', 'children'),
        Output('kc1p-dashboard', 'children'),
        Output('kc2-dashboard', 'children'),
        Output('kc3-dashboard', 'children'),
        Output('kc4-dashboard', 'children'),
        Output('kc5-dashboard', 'children')
    ],
    [Input('kpi-selector', 'value')]
)
def update_kpi_layout(kpi_value):
    # Generate and return layout for the selected KPI
    return (
        create_kpi_layout('ka1') if kpi_value == 'ka1' else html.Div([]),
        create_kpi_layout('kc1p') if kpi_value == 'kc1p' else html.Div([]),
        create_kpi_layout('kc2') if kpi_value == 'kc2' else html.Div([]),
        create_kpi_layout('kc3') if kpi_value == 'kc3' else html.Div([]),
        create_kpi_layout('kc4') if kpi_value == 'kc4' else html.Div([]),
        create_kpi_layout('kc5') if kpi_value == 'kc5' else html.Div([])
    )

