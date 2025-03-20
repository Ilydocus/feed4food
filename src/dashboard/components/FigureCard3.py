import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go


class FigureCard3(dbc.Card):
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

fig = go.Figure(go.Indicator(
    mode = "number+gauge+delta", value = 2,
    domain = {'x': [0.1, 1], 'y': [0, 1]},
    title = {'text' :"<b>Native species</b>"},
    delta = {'reference': 1},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 10]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75,
            'value': 5},
        #'steps': [
         #   {'range': [0, 150], 'color': "lightgray"},
         #   {'range': [150, 250], 'color': "gray"}]
         }))
