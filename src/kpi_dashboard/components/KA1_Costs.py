import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from financialReport.models import FinancialReport  # Assuming you're using Django models for FinancialReport

class KA1_CostsCard(dbc.Card):
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


# Fetch data for FinancialReport (replace with your actual query)
data = [{
    "month": report.month,
    "year": report.year,
    "exp_workforce": report.exp_workforce,
    "exp_purchase": report.exp_purchase,
    "exp_others": report.exp_others,
} for report in FinancialReport.objects.all()]

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Combine month and year into a single column 'month_year' in the format 'MM-YYYY'
df['month_year'] = df['month'].astype(str) + '-' + df['year'].astype(str)

if not df.empty:
    # Create a line chart with multiple lines for different costs using Plotly Express
    fig = px.line(
        df,
        x="month_year",  # X-axis is the month-year
        y=["exp_workforce", "exp_purchase", "exp_others"],  # Multiple y-values for different costs
        labels={
            "month_year": "Month-Year", 
            "value": "Cost",  # Default label for y-axis when plotting multiple lines
        },
        markers=True  # Show markers for each data point
    )
else:
    fig = go.Figure()  # Empty figure if no data
