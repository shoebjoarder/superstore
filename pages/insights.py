import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from dash import dcc, html

dash.register_page(__name__, name="Insights", path="/graph-page")


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Insights"),
                        # dcc.Graph(id="graph-graph", figure=profit_fig),
                    ]
                ),
            ],
            className="mt-4 mb-3",
        ),
    ]
)
