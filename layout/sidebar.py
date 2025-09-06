import pandas as pd
import dash_bootstrap_components as dbc
from layout.css import SIDEBAR_STYLE
from dash import html, dcc, callback, Input, Output

img_path = "assets/us-logo.png"

sidebar = html.Div(
    [
        html.Img(src=img_path, style={"width": "70%"}),
        html.P(id="app-starter"),
        dcc.Store(id="sidebar-store"),
        # html.H4("Pages:"),
        # html.Hr(),
        # dbc.Nav(
        #     [
        #         dbc.NavLink("Overview", href="/", active="exact"),
        #         dbc.NavLink("Station", href="/station", active="exact"),
        #         dbc.NavLink("Trip", href="/trip", active="exact"),
        #         dbc.NavLink("Bike", href="/bike", active="exact"),
        #     ],
        #     vertical=True,
        #     pills=True,
        # ),
        html.H4("Universial filters:"),
        html.Hr(),
        html.Div(id="universial-sidebar-filters"),
        html.H4("Tab filters:"),
        html.Hr(),
        html.Div(id="tab-sidebar-filters")
    ],
    style=SIDEBAR_STYLE,
)


@callback(
    Output("sidebar-store", "data"),
    Input("app-starter", "children")
)
def app_startup(empty):
    """
    On app startup read all the asset CSV files
    """
    # Trips
    df_trips = pd.read_csv("assets/trips.csv").sort_values(by=["started_at"])
    trip_records = df_trips.to_dict("records")
    # Stations
    df_stations = pd.read_csv("assets/madrid-stations.csv")
    station_records = df_stations.to_dict("records")
    # Zones
    df_zones = pd.read_csv("assets/madrid-statistic-zones-clusters.csv")
    zone_records = df_zones.to_dict("records")
    return trip_records, station_records, zone_records
