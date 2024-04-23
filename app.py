import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from callbacks import get_data_table_filters_callbacks, get_data_table_entry_callbacks

# Load the data
url = "https://raw.githubusercontent.com/shoebjoarder/superstore/main/Sample%20-%20Superstore%20-%20CSV.csv"
df = pd.read_csv(url)
df = df.drop("Row ID", axis=1)
dff = df.copy(deep=True)

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    use_pages=True,
)

sidebar = dbc.Nav(
    [
        (
            dbc.NavLink(
                [
                    html.Div(
                        [
                            html.I(className="bi bi-house-door-fill"),
                            html.Div(page["name"], className="ms-2"),
                        ],
                        style={"display": "flex", "align-items": "center"},
                    )
                ],
                href=page["path"],
                active="exact",
            )
            if page["name"] == "Dashboard"
            else (
                dbc.NavLink(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="bi bi-bar-chart-fill"
                                ),  # Data Insights icon
                                html.Div(page["name"], className="ms-2"),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        )
                    ],
                    href=page["path"],
                    active="exact",
                )
                if page["name"] == "Insights"
                else dbc.NavLink(
                    [
                        html.Div(
                            [
                                html.I(className="bi bi-table"),
                                html.Div(page["name"], className="ms-2"),
                            ],
                            style={"display": "flex", "align-items": "center"},
                        )
                    ],
                    href=page["path"],
                    active="exact",
                )
            )
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="mt-4",
)

# sidebar = dbc.Nav(
#     [
#         dbc.NavLink(
#             [html.Div(page["name"], className="ms-2")],
#             href=page["path"],
#             active="exact",
#         )
#         for page in dash.page_registry.values()
#     ],
#     vertical=True,
#     pills=True,
#     className="mt-4",
# )

navbar = dbc.NavbarSimple(
    brand="Superstore",
    brand_href="#",
    color="dark",
    dark=True,
)

app.layout = dbc.Container(
    [
        dbc.Row([navbar]),
        dbc.Row(
            [
                dbc.Col([sidebar], xs=4, md=2),
                dbc.Col([dash.page_container], xs=8, md=10),
            ]
        ),
    ],
    fluid=True,
)

# Callbacks
get_data_table_filters_callbacks(app)
get_data_table_entry_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
