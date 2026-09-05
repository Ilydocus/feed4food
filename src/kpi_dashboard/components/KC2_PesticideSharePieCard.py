import dash_bootstrap_components as dbc
from dash import html, dcc
from django.utils.timezone import now
from django.db.models import Q

from cultivationReport.models import CultivationReport
from inputReport.models import InputReportDetails


def current_year():
    return now().year


def load_total_gardens_in_use(living_lab, dummy=False):
    if dummy:
        return {"Garden A", "Garden B", "Garden C", "Garden D"}
    year = current_year()
    return set(
        CultivationReport.objects
        .filter(
            city=living_lab, 
            cultivation_date__year=year)
        .values_list("garden", flat=True)
        .distinct()
    )


def load_gardens_using_pesticides(living_lab, dummy=False):
    if dummy:
        return {"Garden A", "Garden C"}
    year = current_year()
    return set(
        InputReportDetails.objects
        .filter(
            Q(name_input__input_type="Pesticide") | Q(name_input__input_type="Fertilizer", name_input__input_category="Synthetic"),
            report_id__city =living_lab,
            report_id__application_date__year=year,  
        )
        .values_list("report_id__garden", flat=True)
        .distinct()
    )


class KC2_PesticideSharePieCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        total_gardens = load_total_gardens_in_use(living_lab, dummy=dummy)
        pesticide_gardens = load_gardens_using_pesticides(living_lab, dummy=dummy)

        using_pesticides = len(pesticide_gardens & total_gardens)
        not_using = len(total_gardens) - using_pesticides

        figure = {
            "data": [
                {
                    "type": "pie",
                    "labels": [
                        "Gardens using pesticides",
                        "Gardens not using pesticides",
                    ],
                    "values": [using_pesticides, not_using],
                    "hole": 0.5,
                }
            ],
            "layout": {
                "margin": {"t": 20, "b": 20, "l": 20, "r": 20},
                "legend": {"orientation": "h", "y": -0.1},
            },
        }

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
                        dcc.Graph(
                            figure=figure,
                            config={"displayModeBar": False},
                            style={"height": "260px"},
                        ),

                        html.Div(
                            f"{using_pesticides} out of {len(total_gardens)} gardens use pesticides",
                            className="text-muted text-center mt-1",
                        ),
                    ],
                    className="p-3 pt-0",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(description or ""),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 p-0",
        )
