from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

trip_layout = html.Div(
    children=[
        html.P(id="trip-starter"),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3("Histogram")
                    ],
                ),
                dbc.CardBody(
                    [
                        html.H5("Station:"),
                        dcc.Dropdown(
                            id="trip-stations-dropdown",
                            options=[],
                            value=None,
                        ),
                        dcc.Graph(id="trip-histogram"),
                        dash_table.DataTable(id="station-trips")
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    [
        Output("trip-stations-dropdown", "options"),
        Output("trip-stations-dropdown", "value"),
    ],
    [
        Input("filtered-data-store", "data"),
    ]

)
def get_stations(filtered_data):
    """
    Populate stations dropdown.
    """
    trip_records, station_records, zone_records = filtered_data
    trip_df = pd.DataFrame.from_records(trip_records)
    start_station_ids = list(trip_df["start_station_id"].unique())
    options = []
    for station_id in start_station_ids:
        for station_record in station_records:
            if station_record["meta_station_id"] == station_id:
                station_name = station_record["name"]
                option = {"label": station_name, "value": station_id}
                options.append(option)
                break
    value = next(iter(options)).get("value")
    return options, value


@callback(
    [
        Output("trip-histogram", "figure"),
        Output("station-trips", "data"),
        Output("station-trips", "columns"),
    ],
    [
        Input("filtered-data-store", "data"),
        Input("trip-stations-dropdown", "value"),
    ],
)
def create_station_histogram(filtered_data, station_id):
    trip_records, station_records, zone_records = filtered_data
    trip_df = pd.DataFrame.from_records(trip_records)
    station_trip_df = trip_df[trip_df["start_station_id"] == station_id]
    drop_columns = ["Unnamed: 0", "system_id", "vehicle_type_id", "start_latitude", "start_longitude", "end_latitude", "end_longitude"]
    columns = [{"name": i, "id": i} for i in station_trip_df.columns if i not in drop_columns]
    fig = px.histogram(station_trip_df, x="started_at")
    return fig, station_trip_df.to_dict("records"), columns
