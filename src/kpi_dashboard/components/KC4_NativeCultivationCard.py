import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

#from inputReport.models import InputReportDetails


def load_native_cultivation_data():
    #TODO get the data - with a way to distinguish between LL passed as an argument? Or maybe it automagically works
    # qs = (
    #     InputReportDetails.objects
    #     .select_related("report_id", "name_product", "name_input")
    #     .filter(
    #         name_input__input_category="Synthetic"
    #     )
    #     .values(
    #         "report_id__application_date",
    #         "name_product__name",
    #         "quantity",
    #     )
    # )

    # if not qs:
    #     return pd.DataFrame(columns=["date", "product", "quantity"])

    # df = pd.DataFrame(qs)
    # df = df.rename(columns={
    #     "report_id__application_date": "date",
    #     "name_product__name": "product"
    # })

    # df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # df = df.dropna(subset=["date"])
    # df["month_year"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # return df
    return


def build_native_progress_figure(dummy=False):
    if dummy:
        dummy_data = [ #lab, native, total, target
            ('Bucharest', 12, 20, 15),
    ('Strovolos',  8, 14, 10),
    ('Drama',     15, 25, 20),
        ]

        df = pd.DataFrame(dummy_data, columns=["LL", "native", "total", "target"])

    else:
        df = load_native_cultivation_data()

        if df.empty:
            return px.bar(title="No data available")

    value = df["native"][1]
    target = df["target"][1]
    max_val=df["total"][1]
    total=df["total"][1]

    if max_val is None:
        max_val = max(value, target) * 1.5 if max(value, target) > 0 else 20 #?
    #delta_val = value - target
    #color = "green" if delta_val >= 0 else "red"
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=value,
        mode="gauge+number+delta",
        title={'text': f"Native varieties\n(target {target} / total {total})", 'font': {'color': 'black', 'size': 13}},
        delta={
            'reference': target,
            'valueformat': '.0f',
            'increasing': {'color': 'green', 'symbol': ''},
            'decreasing': {'color': 'red', 'symbol': ''},
        },
        gauge={
            'axis': {'range': [0, max_val], 'tickcolor': 'black'},
            'bar': {'color': '#1f77b4'},
            'threshold': {
                'line': {'color': 'red', 'width': 4},
                'thickness': 0.75,
                'value': target,
            },
        },
        number={'font': {'color': 'black'}},
    ))
    fig.update_layout(
        paper_bgcolor='white',
        font_color='black',
        margin=dict(t=0, b=0, l=20, r=20),
        height=50,
    )

    return fig


class KC4_NativeCultivationCard(dbc.Card):
    def __init__(self, title, id, description=None, dummy=False):
        fig = build_native_progress_figure(dummy=dummy)

        #For the text under, could probably done in a nicer way
        if dummy:
            dummy_data = [ #lab, native, total, target
                ('Bucharest', 12, 20, 15),
                ('Strovolos',  8, 14, 10),
                ('Drama',     15, 25, 20),
            ]

            df = pd.DataFrame(dummy_data, columns=["LL", "native", "total", "target"])
        else:
            df = load_native_cultivation_data()

        if df.empty:
            return px.bar(title="No data available")

        value = df["native"][1]
        target = df["target"][1]
        total=df["total"][1]

        super().__init__(
            children=[
                html.Div(
                    [
                        html.H5(title, className="m-0 align-center"),
                    ],
                    className="d-flex justify-content-between align-center p-3",
                ),
                dbc.Spinner(
                    dcc.Graph(
                        id={"type": "graph", "index": id},
                        figure=fig,
                        responsive=True,
                        style={"height": "100%"},
                    ),
                    size="lg",
                    color="dark",
                    delay_show=750,
                ),
                html.P(
                    f"{'✅ Target met' if value >= target else '❌ Below target'}  ({value}/{total} varieties are native)",
                    style={"color": "green" if value >= target else "red", "text-align": "center", "font-weight": "bold"},
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(html.H4(title)),
                        dbc.ModalBody(
                            dcc.Markdown(description or "", link_target="_blank")
                        ),
                    ],
                    id={"type": "graph-modal", "index": id},
                    is_open=False,
                    size="md",
                ),
            ],
            className="mb-3 figure-card",
        )



# html.H5("KC4: Native Varieties Cultivation — Progress per Living Lab", style={"color": "black", "padding": "10px"}),
#     dbc.Row([
#         dbc.Col(
#             html.Div([
#                 html.H6(lab, style={"color": "black", "text-align": "center"}),
#                 dcc.Graph(
#                     id=f"kc4-gauge-{lab.lower()}",
#                     figure=make_gauge(
#                         value=native, target=target, title=f"Native varieties\n(target {target} / total {total})", max_val=total,
#                     ),
#                     config={'displayModeBar': False},
#                 ),
#                 html.P(
#                     f"{'✅ Target met' if native >= target else '❌ Below target'}  ({native}/{total} varieties are native)",
#                     style={"color": "green" if native >= target else "red", "text-align": "center", "font-weight": "bold"},
#                 ),
#             ]), sm=12, md=4,
#         )
#         for lab, native, total, target in KC4_DATA
#     ]),
