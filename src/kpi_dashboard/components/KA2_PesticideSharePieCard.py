import dash_bootstrap_components as dbc
from dash import html, dcc
from django.utils.timezone import now

from productionReport.models import ProductionReport
from inputReport.models import InputReportDetails


def current_year():
    return now().year


def load_total_gardens_in_use(dummy=False):
    if dummy:
        return {"Garden A", "Garden B", "Garden C", "Garden D"}
    year = current_year()
    return set(
        ProductionReport.objects
        .filter(production_date__year=year)
        .values_list("garden", flat=True)
        .distinct()
    )


def load_gardens_using_pesticides(dummy=False):
    if dummy:
        return {"Garden A", "Garden C"}
    year = current_year()
    return set(
        InputReportDetails.objects
        .filter(
            report_id__application_date__year=year,
            name_input__input_category="Pesticide",
        )
        .values_list("report_id__garden", flat=True)
        .distinct()
    )


class KA2_PesticideSharePieCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        total_gardens = load_total_gardens_in_use(dummy=dummy)
        pesticide_gardens = load_gardens_using_pesticides(dummy=dummy)

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
