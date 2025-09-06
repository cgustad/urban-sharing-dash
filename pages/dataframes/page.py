from dash import html, dcc, dash_table, callback, Input, Output
import dash_bootstrap_components as dbc
from layout.css import CONTENT_STYLE

dataframes_layout = html.Div(
    children=[
        html.P(id="dataframes-starter"),
        dcc.Store(id="dataframes-store"),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Trips", className="card-title"),
                    ]
                ),
                dbc.CardBody(
                    [
                        dash_table.DataTable(id="trips-data-table",
                                             data=None),
                    ]
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Stations", className="card-title"),
                    ]
                ),
                dbc.CardBody(
                    [
                        dash_table.DataTable(id="stations-data-table",
                                             data=None),
                    ]
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Zones", className="card-title"),
                    ]
                ),
                dbc.CardBody(
                    [
                        dash_table.DataTable(id="zones-data-table",
                                             data=None),
                    ]
                )
            ]
        ),

    ],
)


@callback(
    [
        # Trips
        Output("trips-data-table", "data"),
        Output("trips-data-table", "columns"),
        # Stations
        Output("stations-data-table", "data"),
        Output("stations-data-table", "columns"),
        # Zones
        Output("zones-data-table", "data"),
        Output("zones-data-table", "columns"),
    ],
    [
        Input("dataframes-starter", "children"),
        Input("sidebar-store", "data"),
    ],
)
def load_table(empty, records_from_csv):
    """
    Gets starter from content, and dataframe records form sidebar storage element.
    We extract the column names and the data
    """
    trip_records, station_records, zone_records = records_from_csv
    # Trips
    trip_columns_list = list(trip_records[0].keys())
    trip_columns = [{"name": i, "id": i} for i in trip_columns_list]
    # Stations
    station_columns_list = list(station_records[0].keys())
    station_columns = [{"name": i, "id": i} for i in station_columns_list]
    # Zones
    zone_columns_list = list(zone_records[0].keys())
    zone_columns = [{"name": i, "id": i} for i in zone_columns_list]
    return trip_records, trip_columns, station_records, station_columns, zone_records, zone_columns
