import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now
from django.db.models import Q, Sum

from productionReport.models import ProductionReportDetails
from inputReport.models import InputReportDetails


def current_year():
    return now().year

def load_chemical_fertilizer_area(living_lab, dummy=False, year=None):
    if dummy:
        return 450 if year == current_year() else 360
    total = (
        InputReportDetails.objects
        .filter(
            Q(name_input__input_type="Pesticide") | Q(name_input__input_type="Fertilizer", name_input__input_category="Synthetic"),
            report_id__city=living_lab,
            report_id__application_date__year=year,
        )
        .aggregate(total=Sum("area"))
        ["total"]
    )
    return total or 0


def load_chemical_fertilizer_quantity(living_lab, dummy=False, year=None):
    if dummy:
        return 900 if year == current_year() else 760
    total = (
            InputReportDetails.objects
            .filter(
                Q(name_input__input_type="Pesticide") | Q(name_input__input_type="Fertilizer", name_input__input_category="Synthetic"),
                report_id__city=living_lab,
                report_id__application_date__year=year,
            )
            .aggregate(total=Sum("quantity"))
            ["total"]
        )
    return total or 0


def trend_arrow(curr, prev):
    if curr > prev:
        return "▲", "red"
    if curr < prev:
        return "▼", "green"
    return "►", "gray"


class KC2_FertilizerIntensityCard(dbc.Card):
    def __init__(self, title, id, living_lab, description=None, dummy=False):
        year = current_year()
        last_year = year - 1

        quantity = load_chemical_fertilizer_quantity(living_lab, dummy=dummy, year=year)
        area = load_chemical_fertilizer_area(living_lab, dummy=dummy, year=year)
        intensity = (quantity / area) if area else 0

        prev_quantity = load_chemical_fertilizer_quantity(living_lab, dummy=dummy, year=last_year)
        prev_area = load_chemical_fertilizer_area(living_lab, dummy=dummy, year=last_year)
        prev_intensity = (prev_quantity / prev_area) if prev_area else 0

        arrow, arrow_color = trend_arrow(intensity, prev_intensity)

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
                            [
                                html.Span(
                                    f"{intensity:.2f} kg/m²",
                                    style={"fontSize": "44px", "fontWeight": "700"},
                                ),
                                html.Span(
                                    f" {arrow}",
                                    style={
                                        "fontSize": "32px",
                                        "fontWeight": "900",
                                        "color": arrow_color,
                                        "marginLeft": "8px",
                                    },
                                ),
                            ],
                            className="mt-2 d-flex align-items-end",
                        ),

                        html.Div(
                            f"{quantity:.0f} kg fertilizer over {area:.0f} m²",
                            className="text-muted mt-1",
                        ),

                        html.Div(
                            "Compared to last year",
                            className="text-muted mt-1",
                        ),

                        html.Div(
                            "Note: treating the same surface twice counts twice",
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
