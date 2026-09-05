from productionReport.models import ProductionReport, ProductionReportDetails, Product
from dash import dcc, html
from dash.dependencies import Input, Output, MATCH, State
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import pandas as pd

from django.db.models import ExpressionWrapper, FloatField, Sum, F
from django.db.models.functions import TruncMonth

from core.kpiUtils import DAILY_NUTRIENT_REQUIREMENTS

from .components.KA1_Costs import KA1_CostsCard, build_costs_figure
from .components.KA1_Funding import KA1_FundingCard
from .components.KA5_IrrigationWaterUse import KA5_WaterUseCard, build_wateruse_figure
from .components.KC2_GardensInUse import KC2_GardensInUseCard
from .components.KA5_RainwaterHarvested import KA5_RainwaterCard, build_rainwater_figure
from .components.KA5_YearlyWaterCard import KA5_YearlyWaterCard
from .components.KA1_BalanceCard import KA1_BalanceCard 
from .components.KA1_MonthlyBreakdownCard import KA1_MonthlyBreakdownCard, build_monthly_breakdown_figure
from .components.KC2_AreaChemicalCard import KC2_AreaChemicalCard
from .components.KA2_PlantChemicalCard import KA2_PlantChemicalCard
from .components.KC2_PlantsPerProductCard import KC2_PlantsPerProductCard, build_plants_cultivated_figure
from .components.KC2_ChemicalUsePerProductCard import KC2_ChemicalUsePerProductCard
from .components.KC2_SurfaceCultivatedPerProductCard import KC2_SurfaceCultivatedPerProductCard, build_surface_cultivation_figure
from .components.KA1_EventRevenueScatterCard import KA1_EventRevenueScatterCard
from .components.KA1_SalesRevenueLineCard import KA1_SalesRevenueLineCard, build_sales_figure
from .components.KA1_EventsAndOtherRevenuesBarCard import KA1_EventsAndOtherRevenuesBarCard
from .components.KC2_FertilizerActiveIngredientTable import KC2_FertilizerActiveIngredientTable
from .components.KA1_QuantitySold import KA1_QuantitySold, build_quantitysold_figure
from .components.KC2_FertilizerIntensityCard import KC2_FertilizerIntensityCard
from .components.KC2_PesticideSharePieCard import KC2_PesticideSharePieCard
from .components.KC1P_Extent import KC1P_ExtentCard, build_training_extent_figure, DEFAULT_TRAINING_EXTENT_OTHER_TARGET, DEFAULT_TRAINING_EXTENT_TOTAL_TARGET
from .components.KC1P_Attractivity import KC1P_AttractivityCard, build_training_attractivity_figure, DEFAULT_TRAINING_ATTRACTIVITY_OTHER_TARGET, DEFAULT_TRAINING_ATTRACTIVITY_TOTAL_TARGET
from .components.KC1P_Outcome import KC1P_OutcomeCard, build_training_outcome_figure, DEFAULT_TRAINING_OUTCOME_OTHER_TARGET, DEFAULT_TRAINING_OUTCOME_TOTAL_TARGET
from .components.KC1P_Relevance import KC1P_RelevanceCard, build_training_relevance_figure, DEFAULT_TRAINING_RELEVANCE_OTHER_TARGET, DEFAULT_TRAINING_RELEVANCE_TOTAL_TARGET
from .components.KC4_NativeCultivationCard import KC4_NativeCultivationCard
from .components.KC3_NutritiousFoodProduction import KC3_NutritiousFoodProductionCard, build_kc3_nutrients_figure, build_kc3_production_figure, build_kc3_colour_figure, build_kc3_people_figure

# ─────────────────────────────────────────────
# APP INITIALIZATION
# ─────────────────────────────────────────────
app = DjangoDash("KPIVisualisationApp", external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure()



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

try:
    item_options = list(Product.objects.all().values_list("name", flat=True))
except Exception as e:
    item_options = []
item_options2 = ['All varieties']

def make_gauge(value, target, title, max_val=None):
    """Return a Plotly gauge+number+delta figure."""
    if max_val is None:
        max_val = max(value, target) * 1.5 if max(value, target) > 0 else 20
    delta_val = value - target
    color = "green" if delta_val >= 0 else "red"
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=value,
        mode="gauge+number+delta",
        title={'text': title, 'font': {'color': 'black', 'size': 13}},
        delta={
            'reference': target,
            'valueformat': '.0f',
            'increasing': {'color': 'green'},
            'decreasing': {'color': 'red'},
        },
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': 'black'},
            'bar': {'color': '#1f77b4'},
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': target,
            },
        },
        number={'font': {'color': 'black'}},
    ))
    fig.update_layout(
        paper_bgcolor='white',
        font_color='black',
        margin=dict(t=60, b=20, l=20, r=20),
        height=220,
    )
    return fig

KC4_DATA = [
    ('Bucharest', 12, 20, 15),
    ('Strovolos',  8, 14, 10),
    ('Drama',     15, 25, 20),
]

# kc4_content = [
#     html.H5("KC4: Native Varieties Cultivation — Progress per Living Lab", style={"color": "black", "padding": "10px"}),
#     dbc.Row([
#         dbc.Col(
#             html.Div([
#                 html.H6(lab, style={"color": "black", "text-align": "center"}),
#                 dcc.Graph(
#                     id=f"kc4-gauge-{lab.lower()}",
#                     figure=make_gauge(
#                         value=native, target=target, title=f"Native varieties\n(target {target} / total {total})", max_val=total,
#                     ),
#                     config={'displayModeBar': False},
#                 ),
#                 html.P(
#                     f"{'✅ Target met' if native >= target else '❌ Below target'}  ({native}/{total} varieties are native)",
#                     style={"color": "green" if native >= target else "red", "text-align": "center", "font-weight": "bold"},
#                 ),
#             ]), sm=12, md=4,
#         )
#         for lab, native, total, target in KC4_DATA
#     ]),
# ]


# ─────────────────────────────────────────────
# MAIN APP LAYOUT
# ─────────────────────────────────────────────
app.layout = html.Div([
    dcc.Store(id='kc3-adult-days-store'),
    html.P("Living Lab:", style={"color": "white"}), 
    dcc.Dropdown(
        id="ll-selector",
        placeholder="Select a Living Lab",
        style={"margin-bottom": "15px"},
        options=[
            {'label': 'Bucharest', 'value': 'Bucharest'},
            {'label': 'Drama', 'value': 'Drama'},
            {'label': 'Strovolos', 'value': 'Strovolos'},
        ],
    ),
    html.P("KPI:", style={"color": "white"}), 
    dcc.Dropdown(
        id="kpi-selector",
        placeholder="Select a KPI to display",
        style={"margin-bottom": "15px"},
        options=[
            {'label': 'KA1: Economic Viability', 'value': 'ka1'},
            {'label': 'KC1-P: Effective training', 'value': 'kc1p'},
            {'label': 'KC2: Pesticide Use', 'value': 'kc2'},
            {'label': 'KC3: Nutritious food production', 'value': 'kc3'},                    
            {'label': 'KC4: Native varieties cultivation', 'value': 'kc4'},
            {'label': 'KC5: Water Use', 'value': 'kc5'},
            #{'label': 'Gardener', 'value': 'gard'},
        ],
    ),

    # Dashboard Containers
    html.Div(id="ka1-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc1p-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc2-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc3-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc4-dashboard", children=[], style={'display': 'none'}),
    html.Div(id="kc5-dashboard", children=[], style={'display': 'none'}),
    #html.Div(id="gard-dashboard", children=[], style={'display': 'none'}),

], style={"background-color":"#003399", "height": "100%", "padding": "10px"})


# ─────────────────────────────────────────────
# CALLBACKS: VISIBILITY & RENDERING
# ─────────────────────────────────────────────
@app.callback(
    [
        Output('ka1-dashboard', 'style'),
        Output('kc1p-dashboard', 'style'),
        Output('kc2-dashboard', 'style'),
        Output('kc3-dashboard', 'style'),
        Output('kc4-dashboard', 'style'),
        Output('kc5-dashboard', 'style'),
        #Output('gard-dashboard', 'style'),
    ],
    [Input('kpi-selector', 'value')]
)
def show_hide_dashboards(kpi_value):
    base_style = {'display': 'none', "background-color": "#003399", "padding": "10px"}
    visibility = {kpi: dict(base_style) for kpi in ['ka1','kc1p','kc2','kc3','kc4','kc5']}
    if kpi_value:
        visibility[kpi_value]['display'] = 'block'
    return (
        visibility['ka1'], visibility['kc1p'], visibility['kc2'], visibility['kc3'],
        visibility['kc4'], visibility['kc5']
    )


def create_kpi_layout(kpi_name, ll_value):
    if kpi_name == 'ka1':
        return html.Div([
            dbc.Row([dbc.Col(KA1_BalanceCard(id="balance-ka1", living_lab=ll_value, dummy=False), sm=12, md=12, className="mb-4")]),
            dbc.Row([dbc.Col(KA1_MonthlyBreakdownCard("Monthly Financial Breakdown", id="monthly-breakdown-ka1", living_lab=ll_value, dummy=False), sm=12, md=12)]),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Revenue and Sales")),
                    dbc.CardBody([
                        KA1_EventRevenueScatterCard("Revenue per Event", id="revenue-ka1", living_lab=ll_value, dummy=False),
                        KA1_SalesRevenueLineCard("Production Sales and Sales in Restaurant", id="prodsales-ka1", living_lab=ll_value, dummy=False)
                    ]),
                ]), sm=12, md=4),
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Cost and Revenue")),
                    dbc.CardBody([
                        KA1_CostsCard("Workforce Costs, Purchase Costs, and Other Costs", id="costs-ka1", living_lab=ll_value, dummy=False),
                        KA1_EventsAndOtherRevenuesBarCard("Revenues from Events vs. Other Revenues", id="revenueevents-ka1", living_lab=ll_value, dummy=False)
                    ]),
                ]), sm=12, md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H4("Product Sales")),
                        dbc.CardBody([KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-ka1", living_lab=ll_value, dummy=False)]),
                    ]),
                    dbc.Card([
                        dbc.CardHeader(html.H4("Funding")),
                        dbc.CardBody([KA1_FundingCard("Project Funding and Other Funding", id="funding-ka1", living_lab=ll_value, dummy=False)])
                    ], style={'marginTop': '20px'})
                ], sm=12, md=4)
            ]),
        ])

    elif kpi_name == 'kc1p':
        return html.Div([
            dbc.Row([
                dbc.Col(KC1P_ExtentCard(title="Extent of the training", id="extent-kc1p", living_lab=ll_value,dummy=False), 
                    sm=12, md=6),
                dbc.Col(KC1P_AttractivityCard(title="Attractivity of the training", id="attractivity-kc1p", living_lab=ll_value,dummy=False), 
                                    sm=12, md=6),                          
            ]),
            dbc.Row([
                 dbc.Col(KC1P_OutcomeCard(title="Outcome of the training", id="outcome-kc1p", living_lab=ll_value,dummy=False), #Check wether the title appears as I want to
                    sm=12, md=6),
                dbc.Col(KC1P_RelevanceCard(title="Relevance of the training", id="relevance-kc1p", living_lab=ll_value,dummy=False), #Check wether the title appears as I want to
                                    sm=12, md=6),                          
            ]),
        ])

    elif kpi_name == 'kc2':
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Cultivated Area")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KC2_AreaChemicalCard("Surface of Cultivated Area Treated with Chemical Fertilizers/Pesticides", id="metric-area-kc2", living_lab=ll_value, dummy=False), sm=6, md=6),
                            dbc.Col(KC2_FertilizerIntensityCard("Quantity of Chemical Fertilizer/Pesticides over Cultivated Area", id="metric-intensity-kc2", living_lab=ll_value, dummy=False), sm=6, md=6),
                        ]),
                        dbc.Row([dbc.Col(KC2_PesticideSharePieCard("Share of Gardens Treated with Chemical Fertilizers/Pesticides", id="metric-sharepie-kc2", living_lab=ll_value, dummy=False), sm=12, md=12)])
                    ]),
                ]), sm=12, md=6),
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Additional Information")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KC2_GardensInUseCard("Gardens/Holdings in Use", id="metric-InUse-kc2", living_lab=ll_value, dummy=False), sm=6, md=6),
                            dbc.Col(KC2_FertilizerActiveIngredientTable("Active Ingredient in Pesticide/Fertilizer Commercial Product", id="metric-ingredient-kc2", living_lab=ll_value, dummy=False), sm=6, md=6),
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
                                dbc.Col(KC2_ChemicalUsePerProductCard("Quantity of Chemical Fertilizer/Pesticide Used per Commercial Product", id="metric-chemicaluse-kc2", living_lab=ll_value, dummy=False), sm=4, md=4),
                                dbc.Col(KC2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated per Product", id="metric-surfaceActively-kc2", living_lab=ll_value, dummy=False), sm=4, md=4),
                                dbc.Col(KC2_PlantsPerProductCard("Plants Actively Cultivated per Product", id="graph3-kc2", living_lab=ll_value, dummy=False), sm=4, md=4),
                            ])
                        ])
                    ]), sm=12, style={'marginTop': '20px'}
                )
            ),
        ])

    elif kpi_name == 'kc3':
        return html.Div([
                    dbc.Row([
                        dbc.Col(KC3_NutritiousFoodProductionCard("Nutritious food production", id="metric-kc3", dummy=False, living_lab=ll_value)
                                , sm=12, md=12),
                            ]),
                        ]),

    elif kpi_name == 'kc4':
        #return html.Div(kc4_content, style={"background-color": "white", "padding": "20px", "border-radius": "8px"})
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Native varieties cultivation progress")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KC4_NativeCultivationCard("Progress", id="metric1-kc4", dummy=False, ll=ll_value), sm=6, md=6),
                        ]),
                    ]),
                ]), sm=6, md=6),      
            ]),
        ])

    elif kpi_name == 'kc5':
        return html.Div([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Water Reuse")),
                    dbc.CardBody([KA5_YearlyWaterCard("Irrigation Details", id="graph1-kc5", dummy=True)]),
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

    # elif kpi_name == 'gard':
    #     return html.Div([
    #         dbc.Row([dbc.Col(KA1_BalanceCard(id="balance-ka1", dummy=True), sm=12, md=12, className="mb-4")]),
    #         dbc.Row([dbc.Col(KA1_MonthlyBreakdownCard("Monthly Financial Breakdown", id="monthly-breakdown-ka1", dummy=True), sm=12, md=12)]),
    #         dbc.Row([
    #             dbc.Col(dbc.Card([
    #                 dbc.CardHeader(html.H4("Sales Overview")),
    #                 dbc.CardBody([
    #                     dbc.Row([
    #                         dbc.Col(KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-gard", dummy=True), sm=12, md=6),
    #                         dbc.Col(KA1_SalesRevenueLineCard("Production Sales", id="sales-gard", dummy=True), sm=12, md=6),
    #                     ])
    #                 ]),
    #             ]), sm=12, md=8),
    #             dbc.Col(dbc.Card([
    #                 dbc.CardHeader(html.H4("Treated Areas")),
    #                 dbc.CardBody([
    #                     KA2_AreaChemicalCard("Surface Treated with Chemicals", id="areatreat-gard", dummy=True),
    #                     KA2_PlantChemicalCard("Plants Treated with Chemicals", id="planttreat-gard", dummy=True),
    #                 ]),
    #             ]), sm=12, md=4),
    #         ], className="mb-4"),

    #         dbc.Row([
    #             dbc.Col(dbc.Card([
    #                 dbc.CardHeader(html.H4("Cultivation & Chemicals")),
    #                 dbc.CardBody([
    #                     dbc.Row([
    #                         dbc.Col(KA2_ChemicalUsePerProductCard("Chemical Use per Product", id="chemical-gard", dummy=True), sm=12, md=4),
    #                         dbc.Col(KA2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated", id="surface-gard", dummy=True), sm=12, md=4),
    #                         dbc.Col(KA2_PlantsPerProductCard("Plants Actively Cultivated", id="plants-gard", dummy=True), sm=12, md=4),
    #                     ])
    #                 ]),
    #             ]), sm=12, md=12),
    #         ], className="mb-4"),

    #         dbc.Row([
    #             dbc.Col(dbc.Card([
    #                 dbc.CardHeader(html.H4("Water & Irrigation")),
    #                 dbc.CardBody([
    #                     dbc.Row([
    #                         dbc.Col(KA5_RainwaterCard("Rainwater Harvested", id="rain-gard", dummy=True), sm=12, md=6),
    #                         dbc.Col(KA5_WaterUseCard("Water Use per Source", id="wateruse-gard", dummy=True), sm=12, md=6),
    #                     ]),
    #                     KA5_YearlyWaterCard("Irrigation Frequency", id="freq-gard", dummy=True),
    #                 ]),
    #             ]), sm=12, md=12),
    #         ]),
    #     ])

    return html.Div([])


@app.callback(
    [
        Output('ka1-dashboard', 'children'),
        Output('kc1p-dashboard', 'children'),
        Output('kc2-dashboard', 'children'),
        Output('kc3-dashboard', 'children'),
        Output('kc4-dashboard', 'children'),
        Output('kc5-dashboard', 'children'),
        #Output('gard-dashboard', 'children'),
    ],
    [Input('kpi-selector', 'value'), Input('ll-selector', 'value')]
)
def update_kpi_layout(kpi_value, ll_value):
    return (
        create_kpi_layout('ka1',ll_value) if kpi_value == 'ka1' else html.Div([]),
        create_kpi_layout('kc1p',ll_value) if kpi_value == 'kc1p' else html.Div([]),
        create_kpi_layout('kc2',ll_value) if kpi_value == 'kc2' else html.Div([]),
        create_kpi_layout('kc3',ll_value) if kpi_value == 'kc3' else html.Div([]),
        create_kpi_layout('kc4',ll_value) if kpi_value == 'kc4' else html.Div([]),
        create_kpi_layout('kc5',ll_value) if kpi_value == 'kc5' else html.Div([]),
        #create_kpi_layout('gard') if kpi_value == 'gard' else html.Div([]),
    )

# ─────────────────────────────────────────────
# KC4? CALLBACKS
# ─────────────────────────────────────────────


@app.callback(
    Output({"type": "metric-value", "index": "species-count"}, "children"),
    Input("kpi-selector", "value"),
)
def display_species_count(kpi_value, **kwargs):
    try:
        return Product.objects.count()
    except Exception:
        return 0

@app.callback(
    Output({"type": "metric-value", "index": "native-count"}, "children"),
    Input("kpi-selector", "value"),
)
def display_native_count(kpi_value, **kwargs):
    try:
        return Product.objects.filter(locale=True).count()
    except Exception:
        return 0


# ─────────────────────────────────────────────
# Other CALLBACKS
# ─────────────────────────────────────────────

@app.callback(
    Output({"type": "graph", "index": MATCH}, "figure"),
    Input({"type": "month-dropdown", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def update_monthly_breakdown_graph(month_key, living_lab):
    return build_monthly_breakdown_figure(month_key=month_key, living_lab=living_lab, dummy=False)

@app.callback(
    Output({"type": "quantitysold-graph", "index": MATCH}, "figure"),
    Input({"type": "quantitysold-graph-mode", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def callback_update_KA1_QuantitySold(mode, living_lab):
    return build_quantitysold_figure(living_lab=living_lab, mode=mode, dummy=False)

@app.callback(
    Output({"type": "costscard-graph", "index": MATCH}, "figure"),
    Input({"type": "costscard-graph-mode", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def update_costs_card_chart(mode, living_lab):
    return build_costs_figure(mode=mode, living_lab=living_lab, dummy=False)

@app.callback(
    Output({"type": "salesrevenue-graph", "index": MATCH}, "figure"),
    Input({"type": "salesrevenue-graph-mode", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def update_sales_revenue_chart(mode, living_lab):
    return build_sales_figure(living_lab=living_lab, mode=mode, dummy=False)

@app.callback(
    Output({"type": "surfacecultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "surfacecultivated-graph-mode", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def callback_update_surfacecultivated_chart(chart_type, living_lab):
    return build_surface_cultivation_figure(chart_type=chart_type, living_lab=living_lab, dummy=False)

@app.callback(
    Output({"type": "plantscultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "plantscultivated-graph-mode", "index": MATCH}, "value"),
    Input('ll-selector', 'value'),
)
def callback_update_plantscultivated_chart(chart_type, living_lab):
    return build_plants_cultivated_figure(chart_type=chart_type, living_lab=living_lab, dummy=False)

@app.callback(
    Output({"type": "rainwater-graph", "index": MATCH}, "figure"),
    Input({"type": "rainwater-graph-mode", "index": MATCH}, "value"),
)
def callback_update_rainwater_chart(chart_type):
    return build_rainwater_figure(chart_type=chart_type, dummy=False)

@app.callback(
    Output({"type": "wateruse-graph", "index": MATCH}, "figure"),
    Input({"type": "wateruse-graph-mode", "index": MATCH}, "value"),
)
def callback_update_wateruse_chart(chart_type):
    return build_wateruse_figure(chart_type=chart_type, dummy=False)

@app.callback(
    Output({"type": "extent-graph", "index": MATCH}, "figure"),
    Input({"type": "group-toggle", "index": MATCH}, "value"),
    State({"type": "extent-data", "index": MATCH}, "data"),
    State({"type": "extent-target", "index": MATCH}, "data"),
)
def update_extent_graph(selected_group, stored_data, city_targets):
    df = pd.DataFrame(stored_data)
    city_targets = city_targets or {}

    if selected_group == 'Total population':
        target = city_targets.get('total', DEFAULT_TRAINING_EXTENT_TOTAL_TARGET)
    else:
        target = city_targets.get('other', DEFAULT_TRAINING_EXTENT_OTHER_TARGET)

    return build_training_extent_figure(df, selected_group, target)

@app.callback(
    Output({"type": "attractivity-graph", "index": MATCH}, "figure"),
    Input({"type": "group-toggle", "index": MATCH}, "value"),
    State({"type": "attractivity-data", "index": MATCH}, "data"),
    State({"type": "attractivity-target", "index": MATCH}, "data"),
)
def update_attractivity_graph(selected_group, stored_data, city_targets):
    df = pd.DataFrame(stored_data)
    city_targets = city_targets or {}

    if selected_group == 'Total population':
        target = city_targets.get('total', DEFAULT_TRAINING_ATTRACTIVITY_TOTAL_TARGET)
    else:
        target = city_targets.get('other', DEFAULT_TRAINING_ATTRACTIVITY_OTHER_TARGET)

    return build_training_attractivity_figure(df, selected_group, target)

@app.callback(
    Output({"type": "outcome-graph", "index": MATCH}, "figure"),
    Input({"type": "group-toggle", "index": MATCH}, "value"),
    State({"type": "outcome-data", "index": MATCH}, "data"),
    State({"type": "outcome-target", "index": MATCH}, "data"),
)
def update_outcome_graph(selected_group, stored_data, city_targets):
    df = pd.DataFrame(stored_data)
    city_targets = city_targets or {}

    if selected_group == 'Total population':
        target = city_targets.get('total', DEFAULT_TRAINING_OUTCOME_TOTAL_TARGET)
    else:
        target = city_targets.get('other', DEFAULT_TRAINING_OUTCOME_OTHER_TARGET)

    return build_training_outcome_figure(df, selected_group, target)

@app.callback(
    Output({"type": "relevance-graph", "index": MATCH}, "figure"),
    Input({"type": "group-toggle", "index": MATCH}, "value"),
    State({"type": "relevance-data", "index": MATCH}, "data"),
    State({"type": "relevance-target", "index": MATCH}, "data"),
)
def update_relevance_graph(selected_group, stored_data, city_targets):
    df = pd.DataFrame(stored_data)
    city_targets = city_targets or {}

    if selected_group == 'Total population':
        target = city_targets.get('total', DEFAULT_TRAINING_RELEVANCE_TOTAL_TARGET)
    else:
        target = city_targets.get('other', DEFAULT_TRAINING_RELEVANCE_OTHER_TARGET)

    return build_training_relevance_figure(df, selected_group, target)

@app.callback(
    Output({"type": "production-graph", "index": MATCH}, "figure"),
    Input({"type": "view-toggle", "index": MATCH}, "value"),
    Input({"type": "year-selector", "index": MATCH}, "value"),
    State({"type": "production-data", "index": MATCH}, "data"),
)
def update_kc3_production(view, selected_year, production_records):
    return build_kc3_production_figure(production_records, view, selected_year)
 
@app.callback(
    Output({"type": "nutrients-graph", "index": MATCH}, "figure"),
    Input({"type": "year-selector", "index": MATCH}, "value"),
    Input({"type": "month-selector", "index": MATCH}, "value"),
    Input({"type": "adult-days", "index": MATCH}, "data"),
    State({"type": "nutrient-data", "index": MATCH}, "data"),
)
def update_kc3_nutrients(selected_year, selected_month, adult_days, nutrient_records):
    return build_kc3_nutrients_figure(nutrient_records, selected_year, selected_month, adult_days)

@app.callback(
    Output({"type": "colour-graph", "index": MATCH}, "figure"),
    Input({"type": "year-selector", "index": MATCH}, "value"),
    Input({"type": "month-selector", "index": MATCH}, "value"),
    State({"type": "colour-data", "index": MATCH}, "data"),
)
def update_kc3_colour(selected_year, selected_month, colour_records):
    return build_kc3_colour_figure(colour_records, selected_year, selected_month)
 
@app.callback(
    Output({"type": "people-graph", "index": MATCH}, "figure"),
    Output({"type": "adult-days", "index": MATCH}, "data"),
    Input({"type": "view-toggle", "index": MATCH}, "value"),
    Input({"type": "year-selector", "index": MATCH}, "value"),
    Input({"type": "month-selector", "index": MATCH}, "value"),
     State({"type": "nutrient-data", "index": MATCH}, "data"),
)
def update_kc3_people(view, selected_year, selected_month, nutrient_records):
    return build_kc3_people_figure(nutrient_records, view, selected_year, selected_month)
 