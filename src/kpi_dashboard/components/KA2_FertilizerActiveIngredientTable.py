import dash_bootstrap_components as dbc
from dash import html
from productionReport.models import Product
from inputReport.models import Input, InputReportDetails  

class KA2_FertilizerActiveIngredientTable(dbc.Card):
    def __init__(self, title, id, dummy=False):
        rows = self.build_rows(dummy)

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

    def build_rows(self, dummy):
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

        qs = InputReportDetails.objects.select_related("name_input").all()

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
