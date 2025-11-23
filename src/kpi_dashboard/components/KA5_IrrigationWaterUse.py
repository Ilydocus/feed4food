import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from waterReport.models import WaterReport, WaterReportIrrigation, WaterReportRainfall

class KA5_FigureCard(dbc.Card):
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
                    dcc.Graph(
                        id={"type": "graph", "index": id},
                        responsive=True,
                        style={"height": "100%"},
                        figure=fig
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


# Assuming your data is already correct from the database, so let's group it properly

data = [{
    "month": f"{report.start_date.month}-{report.start_date.year}", 
    "source": report.source,
    "quantity": report.quantity
} for report in WaterReportIrrigation.objects.all()]

df = pd.DataFrame(data)

if not df.empty:
    # Create a stacked bar chart using Plotly Express
    fig = px.bar(
        df,
        x="month", 
        y="quantity", 
        color="source",  # This will create the stack based on source
        labels={"month": "Month-Year", "quantity": "Water Use Quantity", "source": "Source"},
        barmode="stack"  # This enables stacking of bars
    )
else:
    fig = go.Figure()  # Empty figure if no data
 
