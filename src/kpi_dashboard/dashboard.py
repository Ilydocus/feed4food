from dash import dcc, html
from dash.dependencies import Input, Output, MATCH
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

# from .components.KA1_PriceProduct import KA1_PriceProduct
from .components.KA1_Costs import KA1_CostsCard, build_costs_figure
from .components.KA1_Funding import KA1_FundingCard
from .components.KA5_IrrigationWaterUse import KA5_WaterUseCard, build_wateruse_figure
from .components.KA2_MetricCard_2 import KA2_MetricCard
from .components.KA5_RainwaterHarvested import KA5_RainwaterCard, build_rainwater_figure
from .components.KA5_YearlyWaterCard import KA5_YearlyWaterCard
from .components.KA1_BalanceCard import KA1_BalanceCard 
from .components.KA1_MonthlyBreakdownCard import KA1_MonthlyBreakdownCard
from .components.KA2_MetricCard import KA2_AreaChemicalCard
from .components.KA2_PlantChemicalCard import KA2_PlantChemicalCard
from .components.KA2_PlantsPerProductCard import KA2_PlantsPerProductCard, build_plants_cultivated_figure
from .components.KA2_ChemicalUsePerProductCard import KA2_ChemicalUsePerProductCard
from .components.KA2_SurfaceCultivatedPerProductCard import KA2_SurfaceCultivatedPerProductCard, build_surface_cultivation_figure
from .components.KA1_EventRevenueScatterCard import KA1_EventRevenueScatterCard
from .components.KA1_SalesRevenueLineCard import KA1_SalesRevenueLineCard, build_sales_figure
from .components.KA1_EventsAndOtherRevenuesBarCard import KA1_EventsAndOtherRevenuesBarCard
from .components.KA1_MonthlyBreakdownCard import build_monthly_breakdown_figure
from .components.KA2_FertilizerActiveIngredientTable import KA2_FertilizerActiveIngredientTable
from .components.KA1_QuantitySold import KA1_QuantitySold, build_quantitysold_figure

app = DjangoDash("KPIVisualisationApp", external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure()

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
            {'label': 'Gardener', 'value': 'gard'},
        ],
    ),

    html.Div(id="ka1-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc1p-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc2-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc3-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc4-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc5-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="gard-dashboard", children=[], style={'display': 'none'}),
], style={"background-color":"#003399", "height": "100%"})


@app.callback(
    [
        Output('ka1-dashboard', 'style'),
        Output('kc1p-dashboard', 'style'),
        Output('kc2-dashboard', 'style'),
        Output('kc3-dashboard', 'style'),
        Output('kc4-dashboard', 'style'),
        Output('kc5-dashboard', 'style'),
        Output('gard-dashboard', 'style'),
    ],
    [Input('kpi-selector', 'value')]
)
def show_hide_dashboards(kpi_value):
    visibility = {kpi: {'display': 'none'} for kpi in ['ka1','kc1p','kc2','kc3','kc4','kc5','gard']}
    if kpi_value:
        visibility[kpi_value] = {'display': 'block'}
    return (
        visibility['ka1'], visibility['kc1p'], visibility['kc2'], visibility['kc3'],
        visibility['kc4'], visibility['kc5'], visibility['gard']
    )


def create_kpi_layout(kpi_name):
    if kpi_name == 'ka1':
        return html.Div([
            dbc.Row([
                dbc.Col(KA1_BalanceCard(id="balance-ka1", dummy=True), sm=12, md=12, className="mb-4")
            ]),
            dbc.Row([
                dbc.Col(KA1_MonthlyBreakdownCard("Monthly Financial Breakdown", id="monthly-breakdown-ka1", dummy=True), sm=12, md=12)
            ]),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Revenue and Sales")),
                    dbc.CardBody([
                        KA1_EventRevenueScatterCard("Revenue per Event", id="revenue-ka1", dummy=True),
                        KA1_SalesRevenueLineCard("Production Sales and Sales in Restaurant", id="prodsales-ka1", dummy=True)
                    ]),
                ]), sm=12, md=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Cost and Revenue")),
                    dbc.CardBody([
                        KA1_CostsCard("Workforce Costs, Purchase Costs, and Other Costs", id="costs-ka1", dummy=True),
                        KA1_EventsAndOtherRevenuesBarCard("Revenues from Events vs. Other Revenues", id="revenueevents-ka1", dummy=True)
                    ]),
                ]), sm=12, md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Product Sales")),
                        dbc.CardBody([
                            KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-ka1", dummy=True),
                        ]),
                    ]),
                    dbc.Card([
                        dbc.CardHeader(html.H4("Funding")),
                        dbc.CardBody([
                            KA1_FundingCard("Project Funding and Other Funding", id="funding-ka1", dummy=True)
                        ]),
                    ], style={'marginTop': '20px'})
                ], sm=12, md=4)
            ]),
        ])

    elif kpi_name == 'kc1p':
        return html.Div([
            dbc.Row(dbc.Col([KA5_FigureCard("KC3 Balance", id="balance-kc3")], sm=12, md=12)),
        ])

    elif kpi_name == 'kc2':
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Cultivated Area")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KA2_AreaChemicalCard("Surface of Cultivated Area Treated with Chemical Fertilizers/Pesticides", id="metric1-kc2", dummy=True), sm=6, md=6),
                            dbc.Col(KA2_PlantChemicalCard("Number of Plants in Cultivated Area Treated with Chemical Fertilizers/Pesticides", id="metric-2-kc2", dummy=True), sm=6, md=6)
                        ])
                    ]),
                ]), sm=12, md=6),
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Additional Information")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KA2_MetricCard("Gardens/Holdings in Use", id="metric3-kc2", dummy=True), sm=6, md=6),
                            dbc.Col(KA2_FertilizerActiveIngredientTable("Active Ingredient in Pesticide/Fertilizer Commercial Product", id="metric4-trend-kc2", dummy=True), sm=6, md=6)
                        ])
                    ]),
                ]), sm=12, md=6),
            ]),
            dbc.Row(
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(html.H4("Usage Overview")),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col(KA2_ChemicalUsePerProductCard("Quantity of Chemical Fertilizer/Pesticide Used per Product", id="graph1-kc2", dummy=True), sm=4, md=4),
                                dbc.Col(KA2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated per Product", id="graph2-kc2", dummy=True), sm=4, md=4),
                                dbc.Col(KA2_PlantsPerProductCard("Plants Actively Cultivated per Product", id="graph3-kc2", dummy=True), sm=4, md=4),
                            ])
                        ])
                    ]), sm=12, style={'marginTop': '20px'}
                )
            ),
        ])

    elif kpi_name == 'kc3':
        return html.Div([
            dbc.Row(dbc.Col([KA5_FigureCard("KC3 Balance", id="balance-kc3")], sm=12, md=12)),
        ])

    elif kpi_name == 'kc4':
        return html.Div([
            dbc.Row(dbc.Col([KA5_FigureCard("KC4 Balance", id="balance-kc4")], sm=12, md=12)),
        ])

    elif kpi_name == 'kc5':
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Irrigation Details")),
                    dbc.CardBody([KA5_YearlyWaterCard("Irrigation Frequency", id="graph1-kc5", dummy=True)]),
                ]), sm=12, md=12),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Rainwater Harvested")),
                    dbc.CardBody([KA5_RainwaterCard("Rainwater Harvested", id="graph2-kc5", dummy=True)]),
                ]), sm=12, md=6),
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Irrigation Water Use per Source")),
                    dbc.CardBody([KA5_WaterUseCard("Irrigation Water Use per Source", id="graph3-kc5", dummy=True)]),
                ]), sm=12, md=6),
            ])
        ])

    elif kpi_name == 'gard':
        return html.Div([

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Sales Overview")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-gard", dummy=True),
                                sm=12, md=6
                            ),
                            dbc.Col(
                                KA1_SalesRevenueLineCard("Production Sales", id="sales-gard", dummy=True),
                                sm=12, md=6
                            ),
                        ])
                    ]),
                ]), sm=12, md=8),

                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Treated Areas")),
                    dbc.CardBody([
                        KA2_AreaChemicalCard("Surface Treated with Chemicals", id="areatreat-gard", dummy=True),
                        KA2_PlantChemicalCard("Plants Treated with Chemicals", id="planttreat-gard", dummy=True),
                    ]),
                ]), sm=12, md=4),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Cultivation & Chemicals")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                KA2_ChemicalUsePerProductCard("Chemical Use per Product", id="chemical-gard", dummy=True),
                                sm=12, md=4
                            ),
                            dbc.Col(
                                KA2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated", id="surface-gard", dummy=True),
                                sm=12, md=4
                            ),
                            dbc.Col(
                                KA2_PlantsPerProductCard("Plants Actively Cultivated", id="plants-gard", dummy=True),
                                sm=12, md=4
                            ),
                        ])
                    ]),
                ]), sm=12, md=12),
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Water & Irrigation")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                KA5_RainwaterCard("Rainwater Harvested", id="rain-gard", dummy=True),
                                sm=12, md=6
                            ),
                            dbc.Col(
                                KA5_WaterUseCard("Water Use per Source", id="wateruse-gard", dummy=True),
                                sm=12, md=6
                            ),
                        ]),
                        KA5_YearlyWaterCard("Irrigation Frequency", id="freq-gard", dummy=True),
                    ]),
                ]), sm=12, md=12),
            ]),
        ])


    return html.Div([])


@app.callback(
    [
        Output('ka1-dashboard', 'children'),
        Output('kc1p-dashboard', 'children'),
        Output('kc2-dashboard', 'children'),
        Output('kc3-dashboard', 'children'),
        Output('kc4-dashboard', 'children'),
        Output('kc5-dashboard', 'children'),
        Output('gard-dashboard', 'children'),
    ],
    [Input('kpi-selector', 'value')]
)
def update_kpi_layout(kpi_value):
    return (
        create_kpi_layout('ka1') if kpi_value == 'ka1' else html.Div([]),
        create_kpi_layout('kc1p') if kpi_value == 'kc1p' else html.Div([]),
        create_kpi_layout('kc2') if kpi_value == 'kc2' else html.Div([]),
        create_kpi_layout('kc3') if kpi_value == 'kc3' else html.Div([]),
        create_kpi_layout('kc4') if kpi_value == 'kc4' else html.Div([]),
        create_kpi_layout('kc5') if kpi_value == 'kc5' else html.Div([]),
        create_kpi_layout('gard') if kpi_value == 'gard' else html.Div([]),
    )


@app.callback(
    Output({"type": "graph", "index": MATCH}, "figure"),
    Input({"type": "month-dropdown", "index": MATCH}, "value"),
)
def update_monthly_breakdown_graph(month_key):
    return build_monthly_breakdown_figure(month_key, dummy=True)

@app.callback(
    Output({"type": "quantitysold-graph", "index": MATCH}, "figure"),
    Input({"type": "quantitysold-graph-mode", "index": MATCH}, "value"),
)
def callback_update_KA1_QuantitySold(mode):
    return build_quantitysold_figure(mode=mode, dummy=True)

@app.callback(
    Output({"type": "costscard-graph", "index": MATCH}, "figure"),
    Input({"type": "costscard-graph-mode", "index": MATCH}, "value"),
)
def update_costs_card_chart(mode):
    return build_costs_figure(mode=mode, dummy=True)

@app.callback(
    Output({"type": "salesrevenue-graph", "index": MATCH}, "figure"),
    Input({"type": "salesrevenue-graph-mode", "index": MATCH}, "value"),
)
def update_sales_revenue_chart(mode):
    return build_sales_figure(mode=mode, dummy=True)

@app.callback(
    Output({"type": "surfacecultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "surfacecultivated-graph-mode", "index": MATCH}, "value"),
)
def callback_update_surfacecultivated_chart(chart_type):
    return build_surface_cultivation_figure(chart_type=chart_type, dummy=True)

@app.callback(
    Output({"type": "plantscultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "plantscultivated-graph-mode", "index": MATCH}, "value"),
)
def callback_update_plantscultivated_chart(chart_type):
    return build_plants_cultivated_figure(chart_type=chart_type, dummy=True)

@app.callback(
    Output({"type": "rainwater-graph", "index": MATCH}, "figure"),
    Input({"type": "rainwater-graph-mode", "index": MATCH}, "value"),
)
def callback_update_rainwater_chart(chart_type):
    return build_rainwater_figure(chart_type=chart_type, dummy=True)

@app.callback(
    Output({"type": "wateruse-graph", "index": MATCH}, "figure"),
    Input({"type": "wateruse-graph-mode", "index": MATCH}, "value"),
)
def callback_update_wateruse_chart(chart_type):
    return build_wateruse_figure(chart_type=chart_type, dummy=True)
