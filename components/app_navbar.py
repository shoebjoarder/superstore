import dash_bootstrap_components as dbc
import dash
from dash import html


def navbar_component():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.Container(
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
                            className="d-lg-none",
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
                                        style={
                                            "display": "flex",
                                            "align-items": "center",
                                        },
                                    )
                                ],
                                href=page["path"],
                                active="exact",
                                className="d-lg-none",
                            )
                            if page["name"] == "Insights"
                            else dbc.NavLink(
                                [
                                    html.Div(
                                        [
                                            html.I(className="bi bi-table"),
                                            html.Div(page["name"], className="ms-2"),
                                        ],
                                        style={
                                            "display": "flex",
                                            "align-items": "center",
                                        },
                                    )
                                ],
                                href=page["path"],
                                active="exact",
                                className="d-lg-none",
                            )
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            )
        ],
        brand="Superstore",
        brand_href="#",
        color="dark",
        dark=True,
        expand="lg",
    )

    return navbar
