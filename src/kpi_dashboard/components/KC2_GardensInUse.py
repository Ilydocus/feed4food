import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now

from cultivationReport.models import CultivationReport

def current_year():
    return now().year

def load_total_gardens_in_use(living_lab, dummy=False):
    if dummy:
        return 9
    year = current_year()
    return set(
        CultivationReport.objects
        .filter(
            city=living_lab, 
            cultivation_date__year=year)
        .values_list("garden", flat=True)
        .distinct()
    )


class KC2_GardensInUseCard(dbc.Card):
    def __init__(self, title, id, living_lab, dummy=False):
        value = len(load_total_gardens_in_use(living_lab, dummy=dummy))

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0"),
                    ],
                    className="d-flex justify-content-between align-items-center p-3",
                ),
                html.Div(
                    [
                        html.H1(
                            value,
                            id={"type": "metric-value", "index": id},
                            className="mt-2",
                            style={"fontWeight": "700"},
                        ),
                        html.P(
                            "Gardens/Holdings in Use have a cultivation report for the current year",
                            id={"type": "metric-text", "index": id},
                            className="text-muted mt-1",
                        ),
                    ],
                    className="p-3 pt-0",
                ),
            ],
            className="mb-3 p-0",
        )
