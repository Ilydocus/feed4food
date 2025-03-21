import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go


class FigureCard5(dbc.Card):
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

months = ['November','December','January','February']

fig = go.Figure()
fig.add_trace(go.Bar(x=months, y=[-200,-400, -600, -320],
                #base=[-500,-600,-700],
                marker_color='crimson',
                name='expenses'))
fig.add_trace(go.Bar(x=months, y=[300,1500, 200, 750],
                #base=0,
                marker_color='green',
                name='revenues'
                ))

fig.update_layout(barmode='relative')