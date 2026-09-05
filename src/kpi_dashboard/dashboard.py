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
from .components.KA2_PlantsPerProductCard import KA2_PlantsPerProductCard, build_plants_cultivated_figure
from .components.KA2_ChemicalUsePerProductCard import KA2_ChemicalUsePerProductCard
from .components.KA2_SurfaceCultivatedPerProductCard import KA2_SurfaceCultivatedPerProductCard, build_surface_cultivation_figure
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

kc3_content = [
    #html.H5("KC3: Nutritious Food Production", style={"color": "black", "padding": "10px"}),
    html.Div([
        html.P("View:", style={"color": "black", "margin-bottom": "4px"}),
        # dcc.RadioItems(
        #     id="kc3-view-toggle",
        #     options=[
        #         {'label': '  Living Lab level',  'value': 'll'},
        #         {'label': '  Garden drill-down',  'value': 'garden'},
        #     ],
        #     value='ll', #default
        #     inline=True,
        #     style={"color": "black", "margin-bottom": "10px"},
        #     inputStyle={"margin-right": "6px", "margin-left": "14px"},
        # ),
        dcc.RadioItems(
            id="kc3-view-toggle",
            options=[
                {
                    'label': '  Living Lab level',
                    'value': 'll'
                },
                {
                    'label': html.Span(
                        '  Garden drill-down',
                        title='Coming soon',  # this is the tooltip
                        style={'color': 'gray', 'cursor': 'not-allowed'}
                    ),
                    'value': 'garden',
                    'disabled': True
                },
            ],
            value='ll',
            inline=True,
            style={"color": "black", "margin-bottom": "10px"},
            inputStyle={"margin-right": "6px", "margin-left": "14px"},
        )
    ]),
    html.Div([
        html.P("Year:", style={"color": "black", "margin-bottom": "4px"}),
        dcc.Dropdown(
            id="kc3-year-selector",
            options=[{'label': str(y), 'value': y} for y in range(2024, 2027)], #TODO make the end the current year
            value=2025,
            clearable=False,
            style={"margin-bottom": "15px", "max-width": "200px"},
        ),
        html.P("Month:", style={"color": "black", "margin-bottom": "4px"}),
        dcc.Dropdown(
            id="kc3-month-selector",
            options=#[{"label": "All", "value": 0}] + TODO Fix the full year option later
            [
                {"label": month, "value": i}
                for i, month in enumerate([
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ], start=1)
            ],
            value=0,
            clearable=False,
            style={"margin-bottom": "15px", "max-width": "200px"},
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Number of days one adult gets the daily calory intake met by garden production", style={"color": "black"}),
                dcc.Graph(id="kc3-people-visualizer"),
            ]), sm=12, md=6,
        ),
        
        dbc.Col(
            html.Div([
                html.H6("Colour coverage", style={"color": "black"}),
                dcc.Graph(id="kc3-colour-chart"),
            ]), sm=12, md=6,
        ),
    ], className="dashboard-row"),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Nutrients coverage (Reference: 30-year old female according to EFSA data)", style={"color": "black"}),
                dcc.Graph(id="kc3-nutrients-chart"),
            ]), sm=12, md=12,
        ),
        
    ], className="dashboard-row"),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Production over time", style={"color": "black"}),
                dcc.Graph(id="kc3-production-line"),
            ]), sm=12, md=12,
        ),
    ], className="dashboard-row"),
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
                                dbc.Col(KA2_ChemicalUsePerProductCard("Quantity of Chemical Fertilizer/Pesticide Used per Commercial Product", id="graph1-kc2", dummy=True), sm=4, md=4),
                                dbc.Col(KA2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated per Product", id="graph2-kc2", dummy=True), sm=4, md=4),
                                dbc.Col(KA2_PlantsPerProductCard("Plants Actively Cultivated per Product", id="graph3-kc2", dummy=True), sm=4, md=4),
                            ])
                        ])
                    ]), sm=12, style={'marginTop': '20px'}
                )
            ),
        ])

    elif kpi_name == 'kc3':
        return html.Div(kc3_content, style={"background-color": "white", "padding": "20px", "border-radius": "8px"})

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
# KC3 CALLBACKS
# ─────────────────────────────────────────────
@app.callback(
    Output('kc3-production-line', 'figure'),
    Input('kc3-view-toggle', 'value'),
    Input('kc3-year-selector', 'value'),
    Input('ll-selector', 'value'),
)
def update_kc3_production(view, selected_year,ll):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # import random
    # random.seed(int(year))

    if view == 'll':
        # series = {
        #     'Amsterdam': [random.randint(80, 200) for _ in months],
        #     'Bucharest': [random.randint(60, 180) for _ in months],
        #     'Drama':     [random.randint(50, 160) for _ in months],
        # }
        title = f"Production in the Living Lab — {selected_year}"
    else:
        # series = {
        #     'Garden A (AMS)': [random.randint(20, 80)  for _ in months],
        #     'Garden B (AMS)': [random.randint(15, 70)  for _ in months],
        #     'Garden C (BCH)': [random.randint(10, 60)  for _ in months],
        #     'Garden D (DRM)': [random.randint(12, 65)  for _ in months],
        # }
        title = f"Production per Garden (drill-down) — {selected_year}"

    # Import data from the database
    monthly_kg = (
        ProductionReportDetails.objects
        .filter(report_id__city=ll)
        .annotate(month=TruncMonth('report_id__production_date'))
        .annotate(
            quantity_kg=ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor'),
                output_field=FloatField()
            )
        )
        .values('month')
        .annotate(total_kg=Sum('quantity_kg'))
        .order_by('month')
    )

    # df = pd.DataFrame(monthly_kg)
    # series = df.set_index('month')['total_kg']
    df = pd.DataFrame(list(monthly_kg))
    series = df.set_index(pd.to_datetime(df['month']))['total_kg']

    fig = go.Figure()
    #for date, values in series.items():
    fig.add_trace(go.Scatter(x=series.index, y=series.values, mode='lines+markers', name="Placeholder"))

    fig.update_layout(
        title=title, paper_bgcolor='white', plot_bgcolor='white', font_color='black',
        legend=dict(bgcolor='white'), margin=dict(t=40, b=30, l=40, r=20), height=320,
        xaxis=dict(gridcolor='#e5e5e5',tickmode='array', tickvals=[pd.Timestamp(year=selected_year, month=m, day=1) for m in range(1, 13)],
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            range=[
                pd.Timestamp(year=selected_year, month=1, day=1),
                pd.Timestamp(year=selected_year, month=12, day=31)
            ]), 
        yaxis=dict(gridcolor='#e5e5e5', title='Quantity (kg)'),
    )
    return fig

@app.callback(
    Output('kc3-nutrients-chart', 'figure'),
    Input('kc3-year-selector', 'value'),
    Input('kc3-month-selector', 'value'),
    Input('ll-selector', 'value'),
    Input("kc3-adult-days-store", "data")
)
def update_kc3_nutrients(selected_year,selected_month,ll, adult_days):
    # nutrients = ['Calories', 'Protein', 'Vitamin C', 'Iron', 'Calcium', 'Fibre']
    # coverage  = [45, 30, 80, 25, 15, 60] 

    nutrient_fields = [f for f in DAILY_NUTRIENT_REQUIREMENTS.keys()]

    # Build aggregation dict dynamically for all nutrients
    aggregations = {
        nutrient: Sum(
            ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor') * 10 * F(f'name__category__{nutrient}'),
                output_field=FloatField()
            )
        )
        for nutrient in nutrient_fields
    }

    qs = ProductionReportDetails.objects.filter(
        report_id__city=ll,
        report_id__production_date__year=selected_year,
    )
    if selected_month != 0:
        qs = qs.filter(report_id__production_date__month=selected_month)

    nutrient_totals = qs.aggregate(**aggregations)

    nutrient_coverage = {
        nutrient: (nutrient_totals[nutrient] or 0) / (daily_req * adult_days) * 100
        for nutrient, daily_req in DAILY_NUTRIENT_REQUIREMENTS.items()
        if daily_req > 0
    }

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(nutrient_coverage.keys()),
        y=list(nutrient_coverage.values()),
        marker_color=[
            'green' if v >= 100 else 'orange' if v >= 50 else 'red'
            for v in nutrient_coverage.values()
        ],
    ))

    fig.update_layout(
        yaxis_title="Coverage (%)",
        yaxis=dict(ticksuffix="%"),
        shapes=[  # reference line at 100%
            dict(
                type='line',
                x0=-0.5, x1=len(nutrient_coverage) - 0.5,
                y0=100, y1=100,
                line=dict(color='black', dash='dash')
            )
        ]
    )

    # fig = go.Figure(go.Bar(
    #     x=nutrients, y=coverage, marker_color=['green' if v >= 50 else 'orange' for v in coverage],
    #     text=[f"{v}%" for v in coverage], textposition='outside',
    # ))
    # fig.update_layout(
    #     paper_bgcolor='white', plot_bgcolor='white', font_color='black', margin=dict(t=20, b=30, l=40, r=20),
    #     height=280, yaxis=dict(range=[0, 110], title='% coverage', gridcolor='#e5e5e5'),
    #     xaxis=dict(gridcolor='#e5e5e5'), showlegend=False,
    # )
    return fig

@app.callback(
    Output('kc3-colour-chart', 'figure'),
    Input('kc3-year-selector', 'value'),
    Input('kc3-month-selector', 'value'),
    Input('ll-selector', 'value'),
)
def update_kc3_colour(selected_year, selected_month, ll):

    #Get the data
    queryset = ProductionReportDetails.objects.filter(
        report_id__city=ll,
        report_id__production_date__year=selected_year,
        report_id__production_date__month=selected_month,
    )

    kg_by_color = (
        queryset
        .annotate(month=TruncMonth('report_id__production_date'))
        .annotate(
            quantity_kg=ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor'),
                output_field=FloatField()
            )
        )
        .values('month', 'name__category__color')
        .annotate(total_kg=Sum('quantity_kg'))
        .order_by('month', 'name__category__color')
    )

    # Compute total kg
    df = pd.DataFrame(list(kg_by_color))

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available for the selected period",
        )
        return fig

    df = df.rename(columns={"name__category__color": "color"})
    df['month'] = pd.to_datetime(df['month'])

    total_kg = df['total_kg'].sum()


    # colours = ['Red', 'Orange', 'Yellow', 'Green', 'Purple', 'White']
    # values  = [15, 10, 12, 35, 8, 20]  
    colour_map = {'Red': 'red', 'Yellow/Orange': '#ffae42', 'Green': 'green', 'White': 'lightgrey'}
    # fig = go.Figure(go.Pie(labels=colours, values=values, marker_colors=[colour_map[c] for c in colours], hole=0.4))
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df['color'],
        values=df['total_kg'],
        marker=dict(colors=df['color'].map(colour_map)), 
        hole=0.4 
    ))

    fig.update_layout(paper_bgcolor='white', font_color='black', margin=dict(t=20, b=20, l=20, r=20), height=280, legend=dict(bgcolor='white'))
    return fig

@app.callback(
    Output('kc3-people-visualizer', 'figure'),
    Output("kc3-adult-days-store", "data"),
    Input('kc3-view-toggle', 'value'),
    Input('kc3-year-selector', 'value'),
    Input('kc3-month-selector', 'value'),
    Input('ll-selector', 'value'),
)
def update_kc3_people(view, selected_year, selected_month, ll):
    
    if view != 'll': #TODO Fix the other view later
        fig = go.Figure()
        fig.update_layout(
            title="No data available for the selected period",
        )
        return fig
    
    # Get the data
    calorie_qs = (
        ProductionReportDetails.objects
        .filter(
            report_id__city=ll,
            report_id__production_date__year=selected_year,
            report_id__production_date__month=selected_month,
        )
        .annotate(
            quantity_kg=ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor'),
                output_field=FloatField()
            )
        )
        .aggregate(
            total_calories=Sum(ExpressionWrapper(
                F('quantity_kg') * 10 * F('name__category__energy_kcal'),
                # *10 converts kg to 100g units (1kg = 10 * 100g)
                output_field=FloatField()
            ))
        )
    )

    total_calories = calorie_qs['total_calories'] or 0
    adult_days = total_calories / DAILY_NUTRIENT_REQUIREMENTS['energy_kcal']

    # fig = go.Figure()
    # for entity, pct in zip(entities, pct_met):
    #     fig.add_trace(go.Scatter(
    #         x=[entity], y=[pct], mode='markers+text',
    #         marker=dict(size=pct, color='green' if pct >= 50 else 'orange', opacity=0.7, line=dict(width=2, color='black')),
    #         text=[f"{pct}%"], textposition='middle center', textfont=dict(color='black', size=13), name=entity,
    #     ))
    fig = go.Figure(go.Indicator(
        mode="number",
        value=round(adult_days, 1),
        number={"suffix": " days", "font": {"size": 60}, "valueformat": ".1f"},
        title={"text": "🧑 1 Adult is fed for <br><sup>Based on 2072 kcal/day</sup>"},
    ))
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white', font_color='black', margin=dict(t=20, b=40, l=40, r=20),
        height=280, showlegend=True, legend=dict(bgcolor='white'), yaxis=dict(range=[0, 110], title='Calory equivalent', gridcolor='#e5e5e5'), xaxis=dict(gridcolor='#e5e5e5'),
    )
    return fig, adult_days

# @app.callback(
#     Output('kc3-people-visualizer', 'figure'),
#     Input('kc3-view-toggle', 'value'),
#     Input('kc3-year-selector', 'value'),
# )
# def update_kc3_people(view, year):
#     import random
#     random.seed(42)
#     if view == 'll':
#         entities = ['Amsterdam', 'Bucharest', 'Drama']
#         pct_met  = [62, 41, 55]
#     else:
#         entities = ['Garden A', 'Garden B', 'Garden C', 'Garden D']
#         pct_met  = [70, 35, 58, 48]

#     fig = go.Figure()
#     for entity, pct in zip(entities, pct_met):
#         fig.add_trace(go.Scatter(
#             x=[entity], y=[pct], mode='markers+text',
#             marker=dict(size=pct, color='green' if pct >= 50 else 'orange', opacity=0.7, line=dict(width=2, color='black')),
#             text=[f"{pct}%"], textposition='middle center', textfont=dict(color='black', size=13), name=entity,
#         ))
#     fig.update_layout(
#         paper_bgcolor='white', plot_bgcolor='white', font_color='black', margin=dict(t=20, b=40, l=40, r=20),
#         height=280, showlegend=True, legend=dict(bgcolor='white'), yaxis=dict(range=[0, 110], title='% daily nutrient needs met', gridcolor='#e5e5e5'), xaxis=dict(gridcolor='#e5e5e5'),
#     )
#     return fig

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
)
def callback_update_surfacecultivated_chart(chart_type):
    return build_surface_cultivation_figure(chart_type=chart_type, dummy=False)

@app.callback(
    Output({"type": "plantscultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "plantscultivated-graph-mode", "index": MATCH}, "value"),
)
def callback_update_plantscultivated_chart(chart_type):
    return build_plants_cultivated_figure(chart_type=chart_type, dummy=False)

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