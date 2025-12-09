import dash_bootstrap_components as dbc
from dash import html


class KA2_MetricCard(dbc.Card):
    def __init__(self, title, id, dummy=False):
        value = "9" if dummy else "-"

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
                        html.H1(
                            value,
                            id={"type": "metric-value", "index": id},
                            className="mt-2",
                            style={"fontWeight": "700"},
                        ),
                        html.P(
                            title,
                            id={"type": "metric-text", "index": id},
                            className="text-muted mt-1",
                        ),
                    ],
                    className="p-3 pt-0",
                ),
            ],
            className="mb-3 p-0",
        )
