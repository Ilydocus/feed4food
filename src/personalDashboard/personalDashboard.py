from productionReport.models import ProductionReport, ProductionReportDetails, Product
from dash import dcc, html, callback
from dash.dependencies import Input, Output, MATCH, State
import plotly.graph_objs as go
import plotly.express as px
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import pandas as pd

# The personal display is using the same visualization as the KPI display but with different data
#from kpi_dashboard.components.KA1_Costs import KA1_CostsCard, build_costs_figure
#from kpi_dashboard.components.KA1_Funding import KA1_FundingCard
from kpi_dashboard.components.KC5_IrrigationWaterUse import KC5_WaterUseCard, build_wateruse_figure
from kpi_dashboard.components.KC5_RainwaterHarvested import KC5_RainwaterCard, build_rainwater_figure
from kpi_dashboard.components.KC5_YearlyWaterCard import KC5_YearlyWaterCard
from kpi_dashboard.components.KA1_BalanceCard import KA1_BalanceCard 
from kpi_dashboard.components.KA1_MonthlyBreakdownCard import KA1_MonthlyBreakdownCard, build_monthly_breakdown_figure
#from kpi_dashboard.components.KC2_PlantChemicalCard import KC2_PlantChemicalCard
from kpi_dashboard.components.KC2_PlantsPerProductCard import KC2_PlantsPerProductCard, build_plants_cultivated_figure
from kpi_dashboard.components.KC2_ChemicalUsePerProductCard import KC2_ChemicalUsePerProductCard
from kpi_dashboard.components.KC2_SurfaceCultivatedPerProductCard import KC2_SurfaceCultivatedPerProductCard, build_surface_cultivation_figure
#from kpi_dashboard.components.KA1_EventRevenueScatterCard import KA1_EventRevenueScatterCard
from kpi_dashboard.components.KA1_SalesRevenueLineCard import KA1_SalesRevenueLineCard, build_sales_figure
#from kpi_dashboard.components.KA1_EventsAndOtherRevenuesBarCard import KA1_EventsAndOtherRevenuesBarCard
from kpi_dashboard.components.KA1_QuantitySold import KA1_QuantitySold, build_quantitysold_figure
from kpi_dashboard.components.KC2_AreaChemicalCard import KC2_AreaChemicalCard
from kpi_dashboard.components.KC3_NutritiousFoodProduction import KC3_NutritiousFoodProductionCard, build_kc3_people_figure, build_kc3_colour_figure, build_kc3_production_figure, build_kc3_nutrients_figure

# ─────────────────────────────────────────────
# APP INITIALIZATION
# ─────────────────────────────────────────────
app = DjangoDash("PersonalDisplayApp", external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

fig = go.Figure()

# ─────────────────────────────────────────────
# ALL POSSIBLE CARDS
# ─────────────────────────────────────────────
items = [
    {"id": "balance", "title": "Balance"},
    {"id": "breakdown", "title": "Monthly breakdown"},
    {"id": "sales", "title": "Sales overview"},
    {"id": "treated", "title": "Treated areas"},
    {"id": "cultivation", "title": "Cultivation & Chemicals"},
    {"id": "water", "title": "Water & Irrigation"},
    {"id": "nutritious", "title": "Nutritious food production"},
]

def make_balance_card(user=None):
    return dbc.Row([dbc.Col(KA1_BalanceCard(id="balance-ka1", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=12, className="mb-4")])

def make_breakdown_card(user=None):
    return dbc.Row([dbc.Col(KA1_MonthlyBreakdownCard("Monthly Financial Breakdown", id="monthly-breakdown-ka1", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=12)])


def make_sales_card(user=None):
    return dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Sales Overview")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KA1_QuantitySold("Quantity Sold per Product", id="quantitysold-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=6),
                            dbc.Col(KA1_SalesRevenueLineCard("Production Sales", id="sales-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=6),
                        ])
                    ]),
                ]), sm=12, md=8),
            ], className="mb-4")

def make_treated_card(user=None):
    return dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Treated Areas")),
                    dbc.CardBody([
                        KC2_AreaChemicalCard("Surface Treated with Chemicals", id="areatreat-gard", living_lab="", user=user, dummy=False, personalDashboard=True),
                        #KC2_PlantChemicalCard("Plants Treated with Chemicals", id="planttreat-gard", living_lab="", user=user, dummy=False, personalDashboard=True), #TODO Need to think about the logic here
                    ]),
                ]), sm=12, md=4),
            ], className="mb-4")


def make_cultivation_card(user=None):
    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Cultivation & Chemicals")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(KC2_ChemicalUsePerProductCard("Chemical Use per Product", id="chemical-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=4),
                    dbc.Col(KC2_SurfaceCultivatedPerProductCard("Surface Actively Cultivated", id="surface-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=4),
                    dbc.Col(KC2_PlantsPerProductCard("Plants Actively Cultivated", id="plants-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=4),
                ])
            ]),
        ]), sm=12, md=12),
    ], className="mb-4")

def make_water_card(user=None):
    return dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Water & Irrigation")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KC5_RainwaterCard("Rainwater Harvested", id="rain-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=6),
                            dbc.Col(KC5_WaterUseCard("Water Use per Source", id="wateruse-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=6),
                        ]),
                        KC5_YearlyWaterCard("Irrigation Frequency", id="freq-gard", living_lab="", user=user, dummy=False, personalDashboard=True),
                    ]),
                ]), sm=12, md=12),
            ])

def make_nutrition_card(user=None):
    return dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader(html.H4("Nutritious Food Production")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(KC3_NutritiousFoodProductionCard("", id="nutrition-gard", living_lab="", user=user, dummy=False, personalDashboard=True), sm=12, md=12),
                        ]),
                    ]),
                ]), sm=12, md=12),
            ])

# Map id -> card builder function
CARD_MAP = {
    "balance": make_balance_card,
    "breakdown": make_breakdown_card,
    "sales": make_sales_card,
    "treated": make_treated_card,
    "cultivation": make_cultivation_card,
    "water": make_water_card,
    "nutritious": make_nutrition_card,
}

# ─────────────────────────────────────────────
# MAIN APP LAYOUT
# ─────────────────────────────────────────────
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Select visualization"),
                dbc.Checklist(
                    options=[{"label": item["title"], "value": item["id"]} for item in items],
                    value=[item["id"] for item in items],
                    id="card-checklist",
                    inline=True,
                )
            ])
        ], className="mb-3 p-3", style={"background": "#f8f9fa"}),

        #Placeholder so that user variable is available when building the cards
        html.Div([
            html.Div(id=f"wrapper-{item['id']}")
            for item in items
        ], id="cards-container"),

        # Invisible trigger that fires once when the page loads - to get a callback where user can be fetched
        dcc.Interval(id="load-trigger", n_intervals=0, max_intervals=1, interval=1),

    ], fluid=True)

], style={"background-color":"#003399", "height": "100%", "padding": "10px"})


# ─────────────────────────────────────────────
# CALLBACKS: VISIBILITY & RENDERING
# ─────────────────────────────────────────────

@app.callback(
    [Output(f"wrapper-{item['id']}", "style") for item in items],
    Input("card-checklist", "value"),
)
def toggle_cards(selected_ids):
    return [
        {"display": "block"} if item["id"] in selected_ids else {"display": "none"}
        for item in items
    ]

# Create cards with access to user
@app.expanded_callback(
    [Output(f"wrapper-{item['id']}", "children") for item in items],
    [Input("load-trigger", "n_intervals")],
)
def populate_cards(n_intervals, **kwargs):
    request = kwargs.get("request")
    user = request.user if request else None

    return [CARD_MAP[item["id"]](user=user) for item in items]

# ─────────────────────────────────────────────
# CALLBACKS FOR UPDATING CARDS
# ─────────────────────────────────────────────

@app.expanded_callback(
    Output({"type": "graph", "index": MATCH}, "figure"),
    Input({"type": "month-dropdown", "index": MATCH}, "value"),
)
def update_monthly_breakdown_graph(month_key, **kwargs):
    request = kwargs.get("request")
    user = request.user if request else None

    return build_monthly_breakdown_figure(month_key=month_key, living_lab="", user=user, dummy=True, personalDashboard=True)

@app.expanded_callback(
    Output({"type": "quantitysold-graph", "index": MATCH}, "figure"),
    Input({"type": "quantitysold-graph-mode", "index": MATCH}, "value"),
)
def callback_update_KA1_QuantitySold(mode,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None
    
    return build_quantitysold_figure(mode=mode, living_lab="", dummy=False, user=user, personalDashboard=True)

# @app.callback(
#     Output({"type": "costscard-graph", "index": MATCH}, "figure"),
#     Input({"type": "costscard-graph-mode", "index": MATCH}, "value"),
# )
# def update_costs_card_chart(mode):
#     return build_costs_figure(mode=mode, dummy=True)

@app.expanded_callback(
    Output({"type": "salesrevenue-graph", "index": MATCH}, "figure"),
    Input({"type": "salesrevenue-graph-mode", "index": MATCH}, "value"),
)
def update_sales_revenue_chart(mode,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None
    
    return build_sales_figure(mode=mode, living_lab="", dummy=False, user=user, personalDashboard=True)

@app.expanded_callback(
    Output({"type": "surfacecultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "surfacecultivated-graph-mode", "index": MATCH}, "value"),
)
def callback_update_surfacecultivated_chart(chart_type,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None
    
    return build_surface_cultivation_figure(chart_type=chart_type, living_lab="", dummy=False, user=user, personalDashboard=True)

@app.expanded_callback(
    Output({"type": "plantscultivated-graph", "index": MATCH}, "figure"),
    Input({"type": "plantscultivated-graph-mode", "index": MATCH}, "value"),
)
def callback_update_plantscultivated_chart(chart_type,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None
    
    return build_plants_cultivated_figure(chart_type=chart_type, living_lab="", dummy=False, user=user, personalDashboard=True)

@app.expanded_callback(
    Output({"type": "rainwater-graph", "index": MATCH}, "figure"),
    Input({"type": "rainwater-graph-mode", "index": MATCH}, "value"),
)
def callback_update_rainwater_chart(chart_type,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None

    return build_rainwater_figure(chart_type=chart_type, living_lab="", dummy=False, user=user, personalDashboard=True)

@app.expanded_callback(
    Output({"type": "wateruse-graph", "index": MATCH}, "figure"),
    Input({"type": "wateruse-graph-mode", "index": MATCH}, "value"),
)
def callback_update_wateruse_chart(chart_type,**kwargs):
    request = kwargs.get("request")
    user = request.user if request else None

    return build_wateruse_figure(chart_type=chart_type, living_lab="", dummy=False, user=user, personalDashboard=True)

# @app.callback(
#     Output({"type": "extent-graph", "index": MATCH}, "figure"),
#     Input({"type": "group-toggle", "index": MATCH}, "value"),
#     State({"type": "extent-data", "index": MATCH}, "data"),
#     State({"type": "extent-target", "index": MATCH}, "data"),
# )
# def update_extent_graph(selected_group, stored_data, city_targets):
#     df = pd.DataFrame(stored_data)
#     city_targets = city_targets or {}

#     if selected_group == 'Total population':
#         target = city_targets.get('total', DEFAULT_TRAINING_EXTENT_TOTAL_TARGET)
#     else:
#         target = city_targets.get('other', DEFAULT_TRAINING_EXTENT_OTHER_TARGET)

#     return build_training_extent_figure(df, selected_group, target)

# @app.callback(
#     Output({"type": "attractivity-graph", "index": MATCH}, "figure"),
#     Input({"type": "group-toggle", "index": MATCH}, "value"),
#     State({"type": "attractivity-data", "index": MATCH}, "data"),
#     State({"type": "attractivity-target", "index": MATCH}, "data"),
# )
# def update_attractivity_graph(selected_group, stored_data, city_targets):
#     df = pd.DataFrame(stored_data)
#     city_targets = city_targets or {}

#     if selected_group == 'Total population':
#         target = city_targets.get('total', DEFAULT_TRAINING_ATTRACTIVITY_TOTAL_TARGET)
#     else:
#         target = city_targets.get('other', DEFAULT_TRAINING_ATTRACTIVITY_OTHER_TARGET)

#     return build_training_attractivity_figure(df, selected_group, target)

# @app.callback(
#     Output({"type": "outcome-graph", "index": MATCH}, "figure"),
#     Input({"type": "group-toggle", "index": MATCH}, "value"),
#     State({"type": "outcome-data", "index": MATCH}, "data"),
#     State({"type": "outcome-target", "index": MATCH}, "data"),
# )
# def update_outcome_graph(selected_group, stored_data, city_targets):
#     df = pd.DataFrame(stored_data)
#     city_targets = city_targets or {}

#     if selected_group == 'Total population':
#         target = city_targets.get('total', DEFAULT_TRAINING_OUTCOME_TOTAL_TARGET)
#     else:
#         target = city_targets.get('other', DEFAULT_TRAINING_OUTCOME_OTHER_TARGET)

#     return build_training_outcome_figure(df, selected_group, target)

# @app.callback(
#     Output({"type": "relevance-graph", "index": MATCH}, "figure"),
#     Input({"type": "group-toggle", "index": MATCH}, "value"),
#     State({"type": "relevance-data", "index": MATCH}, "data"),
#     State({"type": "relevance-target", "index": MATCH}, "data"),
# )
# def update_relevance_graph(selected_group, stored_data, city_targets):
#     df = pd.DataFrame(stored_data)
#     city_targets = city_targets or {}

#     if selected_group == 'Total population':
#         target = city_targets.get('total', DEFAULT_TRAINING_RELEVANCE_TOTAL_TARGET)
#     else:
#         target = city_targets.get('other', DEFAULT_TRAINING_RELEVANCE_OTHER_TARGET)

#     return build_training_relevance_figure(df, selected_group, target)

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
 