import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now

from productionReport.models import ProductionReportDetails
from inputReport.models import InputReportDetails


def current_year():
    return now().year


def load_surface_area_current_year(dummy=False):
    if dummy:
        return [1, 2, 3]
    return (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="m²")
        .values_list("report_id__garden", flat=True)
        .distinct()
    )


def load_total_surface_area(dummy=False):
    if dummy:
        return 1200
    qs = (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="m²")
        .values_list("quantity", flat=True)
    )
    return sum(qs) if qs else 0


def load_chemical_treated_area(dummy=False):
    if dummy:
        return 450
    year = current_year()
    surface_gardens = load_surface_area_current_year()
    qs = (
        InputReportDetails.objects
        .filter(
            report_id__application_date__year=year,
            name_input__input_category__in=["Chemical Fertilizer", "Pesticide"],
            report_id__garden__in=surface_gardens,
        )
        .values_list("area", flat=True)
    )
    return sum(qs) if qs else 0


def load_last_year_treated_area(dummy=False):
    if dummy:
        return 380  # placeholder
    year = current_year() - 1
    surface_gardens = load_surface_area_current_year()
    qs = (
        InputReportDetails.objects
        .filter(
            report_id__application_date__year=year,
            name_input__input_category__in=["Chemical Fertilizer", "Pesticide"],
            report_id__garden__in=surface_gardens,
        )
        .values_list("area", flat=True)
    )
    return sum(qs) if qs else 0


def trend_arrow(curr, prev):
    if curr > prev:
        return "▲", "green"
    if curr < prev:
        return "▼", "red"
    return "►", "gray"


class KA2_AreaChemicalCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        treated = load_chemical_treated_area(dummy=dummy)
        total = load_total_surface_area(dummy=dummy)
        last_year = load_last_year_treated_area(dummy=dummy)

        percentage = (treated / total * 100) if total else 0

        arrow, arrow_color = trend_arrow(treated, last_year)

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
                                    f"{treated:.0f} m²",
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
                            className="mt-2 d-flex align-items-center",
                        ),

                        html.Div(
                            f"{percentage:.1f}% of total surface area {total:.0f} m²",
                            className="text-muted mt-1",
                        ),

                        html.Div(
                            f"Compared to same period last year",
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
