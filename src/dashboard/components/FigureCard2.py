import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go


class FigureCard2(dbc.Card):
    def __init__(self, title, id, description=None):
        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                        dbc.Button(
                            html.Span(
                                "help",
                                className="material-symbols-outlined d-flex",
                            ),
                            id={"type": "graph-info-btn", "index": id},
                            n_clicks=0,
                            color="light",
                        ),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dbc.Card(
        dbc.CardBody(nutrient_indicators),
        className="shadow-sm",
        style={"height": "100%"},
    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
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

# # Sample data
# food_item = {
#     "name": "Salmon",
#     "nutrients": {
#         "Iron": True,
#         "B12": True,
#         "Vitamin D": True,
#         "Calcium": False
#     }
# }

#List of nutrients
all_nutrients = {
        "Iron": True,
        "Calcium": False,
        "Vitamin B12": True,
        "Vitamin D": True       
}

# Create indicators programmatically
nutrient_indicators = []
for nutrient, present in all_nutrients.items():
    color = "success" if present else "danger"
    
    indicator = dbc.Row([
        dbc.Col(
            html.Div(className="rounded-circle bg-" + color, 
                    style={"width": "20px", "height": "20px"}),
            width="auto"
        ),
        dbc.Col(nutrient, width="auto")
    ], className="mb-2 align-items-center")
    
    nutrient_indicators.append(indicator)

# app.layout = dbc.Container([
#     html.H3(f"Nutrient Profile: {food_item['name']}", className="my-4"),
#     dbc.Card(
#         dbc.CardBody(nutrient_indicators),
#         className="shadow-sm"
#     )
# ])