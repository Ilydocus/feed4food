import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from django.utils.timezone import now
from django.db.models import Sum

from eventReport.models import EventReport, EventPersonDetails
from demographicReport.models import DemographicReport

CITY_TRAINING_EXTENT_TARGETS = {
    'Strovolos': {'total': 1, 'other': 10},
    'Drama': {'total': 1, 'other': 10},
    'Bucharest': {'total': 1, 'other': 25},
}

DEFAULT_TRAINING_EXTENT_TOTAL_TARGET = 1  
DEFAULT_TRAINING_EXTENT_OTHER_TARGET = 10 #For all underrepresented groups

def get_training_target(city, group):
    city_targets = CITY_TRAINING_EXTENT_TARGETS.get(city, {})
    if group == 'Total population':
        return city_targets.get('total', DEFAULT_TRAINING_EXTENT_TOTAL_TARGET)
    return city_targets.get('other', DEFAULT_TRAINING_EXTENT_OTHER_TARGET)


def load_training_extent_data(living_lab):
    # Getting information about the date
    today = now()
    year = today.year

    # # Get the data from the reports
    # qs = EventReport.objects.filter(city=living_lab, event_date__year=year)

    # rows = [
    #     {
    #         "total_participants": r.total_participants,
    #     }
    #     for r in qs
    # ]

    # For the demographic, get the latest data for this year
    latest_report = DemographicReport.objects.filter(city=living_lab, data_date__year=year).order_by('-data_date', '-creation_time').prefetch_related('perunderrepresentedgroups__name').first()

    rows = []
    if latest_report is not None:
        rows.append({
            'group': 'Total population',
            'population': latest_report.total_population,
        })

        for g in latest_report.perunderrepresentedgroups.all():
            rows.append({
                'group': g.name.name if g.name else 'unknown',
                'population': g.population,
            })

    df = pd.DataFrame(rows, columns=['group', 'population'])

    # Now add data from the Event reports for the given year
    event_totals = EventReport.objects.filter(
        city=living_lab, event_date__year=year
    ).aggregate(
        total_invited=Sum('total_invited'),
        total_participants=Sum('total_participants'),
    )

    per_group = (
        EventPersonDetails.objects
        .filter(report_id__city=living_lab, report_id__event_date__year=year)
        .values('name__name')
        .annotate(
            number_invited=Sum('number_invited'),
            number_participants=Sum('number_participant'),
        )
    )
    per_group_map = {
        g['name__name']: (g['number_invited'], g['number_participants'])
        for g in per_group
    }

    # Merge the data from Events into the Demographic data
    def lookup_invited(group):
        if group == 'Total population':
            return event_totals['total_invited'] or 0
        return per_group_map.get(group, (0, 0))[0]

    def lookup_participants(group):
        if group == 'Total population':
            return event_totals['total_participants'] or 0
        return per_group_map.get(group, (0, 0))[1]

    if not df.empty:
        df['number_invited'] = df['group'].apply(lookup_invited)
        df['number_participants'] = df['group'].apply(lookup_participants)
    else:
        # No demographic report, but events may still exist — build rows from event data alone
        rows = [{
            'group': 'Total population',
            'population': None,
            'number_invited': event_totals['total_invited'] or 0,
            'number_participants': event_totals['total_participants'] or 0,
        }]
        for group_name, (inv, part) in per_group_map.items():
            rows.append({
                'group': group_name or 'unknown',
                'population': None,
                'number_invited': inv,
                'number_participants': part,
            })
        df = pd.DataFrame(rows)

    return df


def build_training_extent_figure(df, group, target):

    row = df[df['group'] == group]

    population = row['population'].iloc[0] if not row.empty else None
    participants = row['number_participants'].iloc[0] if not row.empty else None

    has_data = (
        population is not None
        and not pd.isna(population)
        and population != 0
        and participants is not None
        and not pd.isna(participants)
    )

    if not has_data:
        fig = go.Figure(go.Indicator(
            mode="number",
            value=None,
            number={'valueformat': "", 'suffix': ""},
            title={'text': f"{group}"},
        ))
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            annotations=[dict(
                text="N/A",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=36, color="grey"),
                xref="paper", yref="paper",
            )]
        )
        return fig

    pct = round(100 * participants / population, 1)
    status_color = "#1e7e34" if pct >= target else "#c82333"  # green if meets/exceeds target, red otherwise

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        domain={'x': [0, 1], 'y': [0.15, 1]},  # leaves bottom 15% of the figure free for the caption
        number={'suffix': "%",'font': {'color': status_color}},
        title={'text': f"{group}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, target], 'color': "#f8d7da"},    # red below target
                {'range': [target, 100], 'color': "#d4edda"},  # green above target
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.9,
                'value': target,
            }
        }
    ))

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=[dict(
            text=f"{participants}  participants / {population} (existing population) — target {target}%",
            x=0.5, y=0.05,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12, color="grey"),
        )]
    )
    return fig


class KC1P_ExtentCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        df = load_training_extent_data(living_lab=living_lab) 
        groups = df['group'].unique().tolist()
        default_group = 'Total population' if 'Total population' in groups else groups[0]

        city_targets = CITY_TRAINING_EXTENT_TARGETS.get(living_lab, {})
        default_target = get_training_target(living_lab, default_group)

        fig = build_training_extent_figure(df, default_group, default_target)

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.RadioItems(
                            id={"type": "group-toggle", "index": id},
                            options=[{"label": g, "value": g} for g in groups],
                            value=default_group,
                            inline=True,
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary btn-sm",
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "extent-graph", "index": id}, #Give a unique name for the callback
                        responsive=True,
                        style={"height": "100%"},
                        figure=fig,
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dcc.Store(id={"type": "extent-data", "index": id}, data=df.to_dict("records")),
                dcc.Store(id={"type": "extent-target", "index": id}, data=city_targets),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(dcc.Markdown(description, link_target="_blank")),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )
