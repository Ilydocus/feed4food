import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now

from productionReport.models import ProductionReportDetails
from inputReport.models import InputReportDetails


def current_year():
    return now().year


def load_surface_gardens(dummy=False):
    if dummy:
        return [1, 2, 3]
    return (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="plants")
        .values_list("report_id__garden", flat=True)
        .distinct()
    )


def load_total_plants(dummy=False):
    if dummy:
        return 15
    qs = (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="plants")
        .values_list("name", flat=True)
        .distinct()
    )
    return len(qs)


def load_treated_plants(dummy=False):
    if dummy:
        return 6
    year = current_year()
    surface_gardens = load_surface_gardens()
    treated_gardens = (
        InputReportDetails.objects
        .filter(
            report_id__application_date__year=year,
            name_input__input_category__in=["Chemical Fertilizer", "Pesticide"],
            report_id__garden__in=surface_gardens,
        )
        .values_list("report_id__garden", flat=True)
        .distinct()
    )
    qs = (
        ProductionReportDetails.objects
        .filter(
            report_id__garden__in=treated_gardens,
            name__cultivation_type="plants",
        )
        .values_list("name", flat=True)
        .distinct()
    )
    return len(qs)


class KA2_PlantChemicalCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        treated = load_treated_plants(dummy=dummy)
        total = load_total_plants(dummy=dummy)

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
                        html.Div(
                            f"{treated}",
                            style={"fontSize": "44px", "fontWeight": "700"},
                            className="mt-2",
                        ),
                        html.Div(
                            f"out of {total} plants",
                            className="text-muted mt-1",
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
