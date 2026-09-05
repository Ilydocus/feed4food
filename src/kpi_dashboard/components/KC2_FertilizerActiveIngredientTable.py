import dash_bootstrap_components as dbc
from dash import html
from django.utils.timezone import now
from django.db.models import Q

from inputReport.models import Input, InputReportDetails  

def current_year():
    return now().year

class KC2_FertilizerActiveIngredientTable(dbc.Card):
    def __init__(self, title, id, living_lab, dummy=False):
        rows = self.build_rows(living_lab, dummy)

        table = dbc.Table(
            [
                html.Thead(
                    html.Tr([
                        html.Th("Fertilizer"),
                        html.Th("Active Ingredient"),
                    ])
                ),
                html.Tbody(rows),
            ],
            bordered=True,
            striped=True,
            hover=True,
            className="m-0",
        )

        super().__init__(
            children=[
                html.Div(
                    [html.H5(title, className="m-0")],
                    className="d-flex justify-content-between align-items-center p-3",
                ),
                html.Div(table, className="p-3 pt-0"),
            ],
            className="mb-3 p-0",
        )

    def build_rows(self, living_lab, dummy):
        if dummy:
            dummy_data = [
                {"name": "NitroX", "active": "Nitrogen / Phosphorus / Potassium"},
                {"name": "FertiPlus",         "active": "Nitrogen"},
                {"name": "ChemGrow",  "active": "Organic Matter"},
            ]
            return [
                html.Tr([html.Td(d["name"]), html.Td(d["active"])])
                for d in dummy_data
            ]

        year = current_year()

        qs = InputReportDetails.objects.select_related("name_input").filter(
                    Q(name_input__input_type="Pesticide") | Q(name_input__input_type="Fertilizer", name_input__input_category="Synthetic"),
                    report_id__city =living_lab,
                    report_id__application_date__year=year,  
                )

        if not qs.exists():
            return [html.Tr([html.Td("—"), html.Td("—")])]

        # Avoid duplicates
        ferts = {}
        for r in qs:
            if r.name_input:
                ferts[r.name_input.name] = r.name_input.active_ingredient

        return [
            html.Tr([html.Td(name), html.Td(active)])
            for name, active in ferts.items()
        ]
