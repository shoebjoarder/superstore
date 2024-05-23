import dash_bootstrap_components as dbc
import dash
from dash import dcc, html
from datetime import date


def graph_dropdown(title: str, type: str, size: int) -> dbc.Col:
    title_hypen = title.lower().replace(" ", "-")
    return dbc.Col(
        [
            dbc.Label(title),
            dbc.Select(
                options=[],
                id=f"dropdown-{type}-{title_hypen}",
            ),
        ],
        xs=size,
    )


def create_layout() -> dbc.Container:
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4("Insights"),
                            dbc.Label(
                                ["Get in-depth insights using the interactive charts."]
                            ),
                        ]
                    ),
                ],
                className="mt-4 mb-3",
            ),
            dbc.Row(
                [
                    dbc.Label("Filter by date"),
                    dcc.DatePickerRange(
                        id="insights-date-range",
                        # TODO: FIX required to help choose date easily
                        min_date_allowed=date(
                            1995,
                            8,
                            5,
                        ),
                        max_date_allowed=date.today(),
                        initial_visible_month=date.today(),
                        clearable=True,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    graph_dropdown("Select data", "timeline", 6),
                    graph_dropdown("Select interval", "timeline", 6),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [dcc.Loading([dcc.Graph(id="insights-timeline-graph")], type="circle")],
                className="mb-5",
            ),
            dbc.Row(
                [
                    graph_dropdown("Y-axis", "scatter", 4),
                    graph_dropdown("X-axis", "scatter", 4),
                    graph_dropdown("Select data", "scatter", 4),
                ]
            ),
            dbc.Row(
                [
                    dcc.Loading(
                        [dcc.Graph(id="insights-scatterplot-graph")], type="circle"
                    )
                ],
                class_name="mb-5",
            ),
        ]
    )


layout = create_layout()

dash.register_page(__name__, name="Insights", path="/graph-page")
