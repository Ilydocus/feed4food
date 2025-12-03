import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now

from productionReport.models import ProductionReportDetails
from inputReport.models import InputReportDetails


def current_year():
    return now().year


def load_surface_area_current_year():
    """All gardens with products cultivated in m²."""
    return (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="m²")
        .values_list("report_id__garden", flat=True)
        .distinct()
    )


def load_total_surface_area():
    """Total surface area (m²) cultivated in the selected gardens."""
    qs = (
        ProductionReportDetails.objects
        .filter(name__cultivation_type="m²")
        .values_list("quantity", flat=True)
    )
    return sum(qs) if qs else 0


def load_chemical_treated_area():
    """Surface area treated with chemical fertilizers/pesticides."""
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


class KA2_AreaChemicalCard(dbc.Card):
    def __init__(self, title, id, description=None):
        treated = load_chemical_treated_area()
        total = load_total_surface_area()

        super().__init__(
            children=[
                # Header
                html.Div(
                    [
                        html.H5(title, className="m-0"),
                    ],
                    className="d-flex justify-content-between align-items-center p-3",
                ),

                # KPI display
                html.Div(
                    [
                        html.Div(
                            f"{treated:.0f} m²",
                            style={"fontSize": "44px", "fontWeight": "700"},
                            className="mt-2",
                        ),
                        html.Div(
                            f"out of {total:.0f} m² total",
                            className="text-muted mt-1",
                        ),
                    ],
                    className="p-3 pt-0",
                ),

                # Modal
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
