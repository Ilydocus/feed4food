import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from django.utils.timezone import now
from django.db.models import Q, Count, Sum

from eventReport.models import EventParticipantDetails 

CITY_TRAINING_RELEVANCE_TARGETS = {
    'Strovolos': {'total': 7, 'other': 7},
    'Drama': {'total': 7, 'other': 7},
    'Bucharest': {'total': 7, 'other': 7},
}

DEFAULT_TRAINING_RELEVANCE_TOTAL_TARGET = 7  
DEFAULT_TRAINING_RELEVANCE_OTHER_TARGET = 7 #For all underrepresented groups

def get_training_relevance_target(city, group):
    city_targets = CITY_TRAINING_RELEVANCE_TARGETS.get(city, {})
    if group == 'Total population':
        return city_targets.get('total', DEFAULT_TRAINING_RELEVANCE_TOTAL_TARGET)
    return city_targets.get('other', DEFAULT_TRAINING_RELEVANCE_OTHER_TARGET)


def load_training_relevance_data(living_lab):
    # Getting information about the date
    today = now()
    year = today.year

    # Total - without group distinction
    base_qs = EventParticipantDetails.objects.filter(
        report_id__city=living_lab,
        report_id__event_date__year=year,
    )

    # Total - without group distinction
    total_count = base_qs.count()
    total_grade = base_qs.aggregate(total=Sum('event_grade'))['total'] or 0

    # Per-group counts
    per_group = (
        base_qs
        .values('group__name')
        .annotate(
            count=Count('participant_id'),
            total_grade=Sum('event_grade'),
        )
    )

    rows = [{
        'group': 'Total population',
        'count': total_count,
        'total_grade': total_grade,
    }]

    for g in per_group:
        rows.append({
            'group': g['group__name'] or 'Not part of an underrepresented group',
            'count': g['count'],
            'total_grade': g['total_grade'] or 0,
        })

    df = pd.DataFrame(rows, columns=['group', 'count', 'total_grade'])

    return df


def build_training_relevance_figure(df, group, target):

    #Outcome is calculated based on the number of participants from whom we have details
    row = df[df['group'] == group]

    count = row['count'].iloc[0] if not row.empty else None
    grade = row['total_grade'].iloc[0] if not row.empty else None
    
    has_data = (
        count is not None
        and not pd.isna(count)
        and count != 0,
        grade is not None
        and not pd.isna(grade)
        and grade != 0
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

    pct = round(grade / count, 1)
    status_color = "#1e7e34" if pct >= target else "#c82333"  # green if meets/exceeds target, red otherwise

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        domain={'x': [0, 1], 'y': [0.15, 1]},  # leaves bottom 15% of the figure free for the caption
        number={'suffix': "/10",'font': {'color': status_color}},
        title={'text': f"{group}"},
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, target], 'color': "#f8d7da"},    # red below target
                {'range': [target, 10], 'color': "#d4edda"},  # green above target
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
            text=f"Average grade given {round(grade/count,1)} by {count} participants with registered grade — target {target}/10",
            x=0.5, y=0.05,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=12, color="grey"),
        )]
    )
    return fig


class KC1P_RelevanceCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        df = load_training_relevance_data(living_lab=living_lab) 
        groups = df['group'].unique().tolist()
        default_group = 'Total population' if 'Total population' in groups else groups[0]

        city_targets = CITY_TRAINING_RELEVANCE_TARGETS.get(living_lab, {})
        default_target = get_training_relevance_target(living_lab, default_group)

        fig = build_training_relevance_figure(df, default_group, default_target)

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
                        id={"type": "relevance-graph", "index": id}, #Give a unique name for the callback
                        responsive=True,
                        style={"height": "100%"},
                        figure=fig,
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                dcc.Store(id={"type": "relevance-data", "index": id}, data=df.to_dict("records")),
                dcc.Store(id={"type": "relevance-target", "index": id}, data=city_targets),
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
