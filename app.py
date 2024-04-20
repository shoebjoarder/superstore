import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime, timedelta
from pages import home_page, table_page, graph_page

# Load the data
url = "https://raw.githubusercontent.com/shoebjoarder/superstore/main/Sample%20-%20Superstore%20-%20CSV.csv"
df = pd.read_csv(url)


# Initialize the app
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)


# App layout
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# Callback for URL routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home_page(df)
    elif pathname == "/table-page":
        return table_page(df)
    elif pathname == "/graph-page":
        return graph_page()
    else:
        return "404 Page Not Found"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
