import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from django.utils.timezone import now
from django.db.models import F, Sum, ExpressionWrapper, FloatField
from django.db.models.functions import TruncMonth

from productionReport.models import ProductionReportDetails
from core.kpiUtils import DAILY_NUTRIENT_REQUIREMENTS

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def load_kc3_production_data(living_lab):
    monthly_kg = (
        ProductionReportDetails.objects
        .filter(report_id__city=living_lab)
        .annotate(month=TruncMonth('report_id__production_date'))
        .annotate(
            quantity_kg=ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor'),
                output_field=FloatField(),
            )
        )
        .values('month')
        .annotate(total_kg=Sum('quantity_kg'))
        .order_by('month')
    )
    df = pd.DataFrame(list(monthly_kg))
    if df.empty:
        return df
    df['month'] = pd.to_datetime(df['month'])
    return df
 
 
def load_kc3_nutrient_data(living_lab):
    nutrient_fields = list(DAILY_NUTRIENT_REQUIREMENTS.keys())
    aggregations = {
        nutrient: Sum(
            ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor') * 10 * F(f'name__category__{nutrient}'),
                output_field=FloatField(),
            )
        )
        for nutrient in nutrient_fields
    }
    monthly = (
        ProductionReportDetails.objects
        .filter(report_id__city=living_lab)
        .annotate(month=TruncMonth('report_id__production_date'))
        .values('month')
        .annotate(**aggregations)
        .order_by('month')
    )
    df = pd.DataFrame(list(monthly))
    if df.empty:
        return df
    df['month'] = pd.to_datetime(df['month'])
    return df
 
 
def load_kc3_colour_data(living_lab):
    kg_by_color = (
        ProductionReportDetails.objects
        .filter(report_id__city=living_lab)
        .annotate(month=TruncMonth('report_id__production_date'))
        .annotate(
            quantity_kg=ExpressionWrapper(
                F('quantity') * F('name__kg_conversion_factor'),
                output_field=FloatField(),
            )
        )
        .values('month', 'name__category__color')
        .annotate(total_kg=Sum('quantity_kg'))
        .order_by('month', 'name__category__color')
    )
    df = pd.DataFrame(list(kg_by_color))
    if df.empty:
        return df
    df = df.rename(columns={'name__category__color': 'color'})
    df['month'] = pd.to_datetime(df['month'])
    return df
 
 
def _records(df):
    """DataFrame -> JSON-safe records for a dcc.Store (dates as ISO strings)."""
    if df.empty:
        return []
    return df.assign(month=df['month'].dt.strftime('%Y-%m-%d')).to_dict('records')
 
 
def _filter_period(df, selected_year, selected_month):
    """Shared year/month filtering. selected_month == 0 means "All months",
    which isn't wired up on the frontend yet (same TODO as the original app) —
    so for now it deliberately yields no rows, matching current behaviour."""
    if df.empty:
        return df
    df = df[pd.to_datetime(df['month']).dt.year == selected_year]
    if selected_month != 0:
        df = df[pd.to_datetime(df['month']).dt.month == selected_month]
    else:
        df = df.iloc[0:0]
    return df


def build_kc3_production_figure(records, view, selected_year):
    title = (
        f"Production in the Living Lab — {selected_year}"
        if view == 'll'
        else f"Production per Garden (drill-down) — {selected_year}"
    )
 
    fig = go.Figure()
    df = pd.DataFrame(records)
    if not df.empty:
        df['month'] = pd.to_datetime(df['month'])
        df = df[df['month'].dt.year == selected_year]
        if not df.empty:
            fig.add_trace(go.Scatter(
                x=df['month'], y=df['total_kg'], mode='lines+markers', name="Placeholder",
            ))
 
    fig.update_layout(
        title=title, paper_bgcolor='white', plot_bgcolor='white', font_color='black',
        legend=dict(bgcolor='white'), margin=dict(t=40, b=30, l=40, r=20), height=320,
        xaxis=dict(
            gridcolor='#e5e5e5', tickmode='array',
            tickvals=[pd.Timestamp(year=selected_year, month=m, day=1) for m in range(1, 13)],
            ticktext=MONTH_ABBR,
            range=[
                pd.Timestamp(year=selected_year, month=1, day=1),
                pd.Timestamp(year=selected_year, month=12, day=31),
            ],
        ),
        yaxis=dict(gridcolor='#e5e5e5', title='Quantity (kg)'),
    )
    return fig
 
 
def build_kc3_nutrients_figure(records, selected_year, selected_month, adult_days):
    nutrient_fields = list(DAILY_NUTRIENT_REQUIREMENTS.keys())
 
    df = pd.DataFrame(records)
    if not df.empty:
        df['month'] = pd.to_datetime(df['month'])
        df = df[df['month'].dt.year == selected_year]
        if selected_month != 0:
            df = df[df['month'].dt.month == selected_month]
 
    totals = {n: (df[n].sum() if not df.empty and n in df else 0) for n in nutrient_fields}
 
    nutrient_coverage = {
        nutrient: (totals[nutrient] or 0) / (daily_req * adult_days) * 100 if adult_days else 0
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
        shapes=[dict(
            type='line', x0=-0.5, x1=len(nutrient_coverage) - 0.5, y0=100, y1=100,
            line=dict(color='black', dash='dash'),
        )],
    )
    return fig
 
 
def build_kc3_colour_figure(records, selected_year, selected_month):
    df = _filter_period(pd.DataFrame(records), selected_year, selected_month)
 
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available for the selected period")
        return fig
 
    colour_map = {'Red': 'red', 'Yellow/Orange': '#ffae42', 'Green': 'green', 'White': 'lightgrey'}
    grouped = df.groupby('color', as_index=False)['total_kg'].sum()
 
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=grouped['color'],
        values=grouped['total_kg'],
        marker=dict(colors=grouped['color'].map(colour_map)),
        hole=0.4,
    ))
    fig.update_layout(
        paper_bgcolor='white', font_color='black', margin=dict(t=20, b=20, l=20, r=20),
        height=280, legend=dict(bgcolor='white'),
    )
    return fig
 
 
def build_kc3_people_figure(nutrient_records, view, selected_year, selected_month):
    """Returns (figure, adult_days) — adult_days also feeds the nutrients chart."""
    if view != 'll':  # TODO: garden drill-down view not implemented yet
        fig = go.Figure()
        fig.update_layout(title="No data available for the selected period")
        return fig, 0
 
    df = _filter_period(pd.DataFrame(nutrient_records), selected_year, selected_month)
 
    daily_kcal = DAILY_NUTRIENT_REQUIREMENTS['energy_kcal']
    total_calories = df['energy_kcal'].sum() if not df.empty and 'energy_kcal' in df else 0
    adult_days = total_calories / daily_kcal if daily_kcal else 0
 
    fig = go.Figure(go.Indicator(
        mode="number",
        value=round(adult_days, 1),
        number={"suffix": " days", "font": {"size": 60}, "valueformat": ".1f"},
        title={"text": f"🧑 1 Adult is fed for <br><sup>Based on {daily_kcal:g} kcal/day</sup>"},
    ))
    fig.update_layout(
        paper_bgcolor='white', plot_bgcolor='white', font_color='black', margin=dict(t=20, b=40, l=40, r=20),
        height=280, showlegend=True, legend=dict(bgcolor='white'),
        yaxis=dict(range=[0, 110], title='Calory equivalent', gridcolor='#e5e5e5'),
        xaxis=dict(gridcolor='#e5e5e5'),
    )
    return fig, adult_days

class KC3_NutritiousFoodProductionCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False, adult_days=1):

        production_df = load_kc3_production_data(living_lab)
        nutrient_df = load_kc3_nutrient_data(living_lab)
        colour_df = load_kc3_colour_data(living_lab)
        production_records = _records(production_df)
        nutrient_records = _records(nutrient_df)
        colour_records = _records(colour_df)
 
        default_view, default_year, default_month = 'll', now().year, 0
 
        production_fig = build_kc3_production_figure(production_records, default_view, default_year)
        colour_fig = build_kc3_colour_figure(colour_records, default_year, default_month)
        people_fig, adult_days = build_kc3_people_figure(
            nutrient_records, default_view, default_year, default_month
        )
        nutrients_fig = build_kc3_nutrients_figure(nutrient_records, default_year, default_month, adult_days)



        super().__init__(
            children=[
                html.Div([
                        html.P("View:", style={"color": "black", "margin-bottom": "4px"}),
                        dcc.RadioItems(
                            id={"type": "view-toggle", "index": id},
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
                            id={"type": "year-selector", "index": id},
                            options=[{'label': str(y), 'value': y} for y in range(2024, 2027)], #TODO make the end the current year
                            value=now().year,
                            clearable=False,
                            style={"margin-bottom": "15px", "max-width": "200px"},
                        ),
                        html.P("Month:", style={"color": "black", "margin-bottom": "4px"}),
                        dcc.Dropdown(
                            id={"type": "month-selector", "index": id},
                            options=#[{"label": "All", "value": 0}] + TODO Fix the full year option later
                            [
                                {"label": month, "value": i}
                                for i, month in enumerate(MONTH_NAMES, start=1)
                            ],
                            value=0,
                            clearable=False,
                            style={"margin-bottom": "15px", "max-width": "200px"},
                        ),
                    ]),

            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            html.H6(
                                "Number of days one adult gets the daily calory intake "
                                "met by garden production",
                                style={"color": "black"},
                            ),
                            dbc.Spinner(
                                dcc.Graph(id={"type": "people-graph", "index": id}, figure=people_fig),
                                size="lg", color="dark", delay_show=750,
                            ),
                        ]),
                        sm=12, md=6,
                    ),
                    dbc.Col(
                        html.Div([
                            html.H6("Colour coverage", style={"color": "black"}),
                            dbc.Spinner(
                                dcc.Graph(id={"type": "colour-graph", "index": id}, figure=colour_fig),
                                size="lg", color="dark", delay_show=750,
                            ),
                        ]),
                        sm=12, md=6,
                    ),
                ],
                className="dashboard-row",
            ),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6(
                            "Nutrients coverage (Reference: 30-year old female according to EFSA data)",
                            style={"color": "black"},
                        ),
                        dbc.Spinner(
                            dcc.Graph(id={"type": "nutrients-graph", "index": id}, figure=nutrients_fig),
                            size="lg", color="dark", delay_show=750,
                        ),
                    ]),
                    sm=12, md=12,
                ),
                className="dashboard-row",
            ),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H6("Production over time", style={"color": "black"}),
                        dbc.Spinner(
                            dcc.Graph(id={"type": "production-graph", "index": id}, figure=production_fig),
                            size="lg", color="dark", delay_show=750,
                        ),
                    ]),
                    sm=12, md=12,
                ),
                className="dashboard-row",
            ),
            dcc.Store(id={"type": "production-data", "index": id}, data=production_records),
            dcc.Store(id={"type": "nutrient-data", "index": id}, data=nutrient_records),
            dcc.Store(id={"type": "colour-data", "index": id}, data=colour_records),   # ← add this line
            dcc.Store(id={"type": "adult-days", "index": id}, data=adult_days),
        ]
        ,className="mb-3 figure-card"),