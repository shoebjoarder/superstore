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
                            className="d-xl-none",
                        )
                        if page["name"] == "Dashboard"
                        else (
                            dbc.NavLink(
                                [
                                    html.Div(
                                        [
                                            html.I(
                                                className="fa-solid fa-magnifying-glass-chart"
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
                                className="d-xl-none",
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
                                className="d-xl-none",
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
        expand="xl",
    )

    return navbar
