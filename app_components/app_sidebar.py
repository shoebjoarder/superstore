import dash_bootstrap_components as dbc
import dash
from dash import html


def sidebar_component():
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
                                        className="fa-solid fa-magnifying-glass-chart"
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
        className="mt-4 d-none d-xl-block",
    )

    return sidebar
