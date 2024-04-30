import dash_bootstrap_components as dbc
from dash import html


# TODO: Not implemented
def page_not_found():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1("404. Page not found.", className="text-center"),
                            html.P(
                                "The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.",
                                className="text-center",
                            ),
                            html.A(
                                "Go back to homepage",
                                href="/",
                                className="btn btn-primary",
                            ),
                        ],
                        className="d-flex flex-column justify-content-center align-items-center",
                    )
                ],
                style={"height": "100vh"},
                className="d-flex justify-content-center align-items-center",
            )
        ],
        fluid=True,
    )
