import dash_bootstrap_components as dbc
import dash
from dash import dcc, html


MONTHS = 12


def create_graph(graph_id: str) -> dbc.Col:
    return dbc.Col(
        [dcc.Loading([dcc.Graph(id=graph_id)], type="circle")],
        class_name="mb-3",
        xs=12,
        lg=6,
    )


def create_card(card_title: str) -> dbc.Col:
    card_title_hypen = card_title.lower().replace(" ", "-")
    return dbc.Col(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P(card_title, className="card-title"),
                                        style={"flex": "1"},
                                    ),
                                    dbc.Col(
                                        html.I(
                                            className="fa-regular fa-circle-question",
                                            id=f"tooltip-target-{card_title_hypen}",
                                        ),
                                        style={"flex": "0", "cursor": "pointer"},
                                    ),
                                    dbc.Tooltip(
                                        f"This represents the {card_title.lower()} in the past {MONTHS} months.",
                                        target=f"tooltip-target-{card_title_hypen}",
                                    ),
                                ],
                            ),
                            dbc.Row(
                                [
                                    dcc.Loading(
                                        [
                                            html.H4(
                                                id=card_title_hypen,
                                                className="card-text",
                                            ),
                                        ],
                                        type="circle",
                                    )
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ],
        className="mb-3",
        xs=12,
        md=6,
    )


def create_link_card(title: str, description: str, label: str, link: str) -> dbc.Col:
    return dbc.Col(
        [
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5(
                                title,
                                className="card-title",
                            ),
                            html.P(
                                description,
                                className="card-text",
                            ),
                            dbc.Button(
                                [
                                    label,
                                    html.I(className="fa-solid fa-arrow-right"),
                                ],
                                color="primary",
                                href=link,
                            ),
                        ]
                    )
                ]
            )
        ],
        className="mb-3",
        xs=12,
        md=6,
    )


def create_layout() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Superstore Dashboard"),
                            html.P(
                                "An overview of the most recent data of the Superstore."
                            ),
                        ]
                    ),
                ],
                className="mt-4",
            ),
            dbc.Row(
                [create_card("Accumulated Sales"), create_card("Profit Ratio")],
            ),
            dbc.Row(
                [
                    create_graph("dashboard-sales-graph"),
                    create_graph("dashboard-profit-graph"),
                ]
            ),
            dbc.Row(
                [
                    create_link_card(
                        "Superstore Data Table",
                        "Preview and manipulate the Superstore data table.",
                        "To data table ",
                        "/table-page",
                    ),
                    create_link_card(
                        "Superstore Insights",
                        "Get insights into the data using interactive charts.",
                        "To insights ",
                        "/graph-page",
                    ),
                ]
            ),
        ]
    )


layout = create_layout()

dash.register_page(__name__, name="Dashboard", path="/")
