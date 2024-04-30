import dash_bootstrap_components as dbc
import dash
from dash import html


def page_link_component(page_name, page_path, icon):
    return dbc.NavLink(
        [
            html.Div(
                [html.I(className=icon), html.Div(page_name, className="ms-2")],
                style={"display": "flex", "alignItems": "center"},
            )
        ],
        href=page_path,
        active="exact",
        className="d-xl-none",
    )


def navbar_component():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.Container(
                [
                    (
                        page_link_component(
                            page["name"], page["path"], "fa-solid fa-house"
                        )
                        if page["name"] == "Dashboard"
                        else (
                            page_link_component(
                                page["name"],
                                page["path"],
                                "fa-solid fa-magnifying-glass-chart",
                            )
                            if page["name"] == "Insights"
                            else page_link_component(
                                page["name"], page["path"], "fa-solid fa-table"
                            )
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            )
        ],
        brand="Superstore",
        brand_href="/",
        color="dark",
        dark=True,
        expand="xl",
    )

    return navbar
