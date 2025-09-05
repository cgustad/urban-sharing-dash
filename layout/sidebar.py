import dash_bootstrap_components as dbc
from layout.css import SIDEBAR_STYLE
from dash import html, dcc

img_path = "assets/us-logo.png"

sidebar = html.Div(
    [
        html.Img(src=img_path, style={"width": "70%"}),
        dcc.Store(id="sidebar-store"),
        html.H4("Pages:"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Station", href="/station", active="exact"),
                dbc.NavLink("Trip", href="/trip", active="exact"),
                dbc.NavLink("Bike", href="/bike", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.H4("Filters:"),
        html.Hr(),
        html.Div(id="sidebar-filters"),
    ],
    style=SIDEBAR_STYLE,
)
