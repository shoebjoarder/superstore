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
    )


def sidebar_component():
    sidebar = dbc.Nav(
        [
            (
                page_link_component(page["name"], page["path"], "fa-solid fa-house")
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
        ],
        vertical=True,
        pills=True,
        className="mt-4 d-none d-xl-block",
    )

    return sidebar
