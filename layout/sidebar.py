import pandas as pd
from datetime import datetime
from layout.css import SIDEBAR_STYLE
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

import logging
logger = logging.getLogger(__name__)

img_path = "assets/us-logo.png"

sidebar = html.Div(
    [
        html.Img(src=img_path, style={"width": "70%"}),
        html.P(id="app-starter"),
        # Store all data
        dcc.Store(id="full-data-store"),
        #FIXME
        dcc.Store("filtered-data-store"),
        # Data after beeing filtered by filter
        dcc.Store("filtered-trip-store"),
        dcc.Store("filtered-station-store"),
        dcc.Store("filtered-zone-store"),
        # Trip filter
        html.H3("Trip filters:"),
        html.Hr(),
        # Date range picker
        html.H5("Date range:"),
        dcc.DatePickerRange(
            id='date-range-filter',
            display_format='MMM Do, YY',
            min_date_allowed=None,
            max_date_allowed=None,
            start_date=None,
            end_date=None,
            calendar_orientation='vertical',
        ),
        html.H5("Trip state:"),
        dcc.Checklist(id="trip-state-checklist"),
        # Station Filters
        html.H3("Station filters"),
        html.Hr(),
        html.H5("Charging station:"),
        dcc.Checklist(id="chargning-station-checklist"),
        html.H5("Station state:"),
        dcc.Checklist(id="station-state-checklist"),
        html.H5("Station type:"),
        dcc.Checklist(id="station-type-checklist"),
    ],
    style=SIDEBAR_STYLE,
)


@callback(
    Output("full-data-store", "data"),
    Input("app-starter", "children"),
    State("full-data-store", "data")
)
def app_startup(empty, previous_data):
    """
    On app startup read all the asset CSV files
    """
    if previous_data:
        raise PreventUpdate
    logger.critical(f"Loading all data from csv, current value is {previous_data}")
    # Trips
    df_trips = pd.read_csv("assets/trips.csv").sort_values(by=["started_at"]).dropna()
    trip_records = df_trips.to_dict("records")
    # Stations
    df_stations = pd.read_csv("assets/madrid-stations.csv").dropna()
    df_stations["is_charging_station"] = df_stations["is_charging_station"].astype(str)
    station_records = df_stations.to_dict("records")

    # Zones
    df_zones = pd.read_csv("assets/madrid-statistic-zones-clusters.csv").dropna()
    zone_records = df_zones.to_dict("records")
    return trip_records, station_records, zone_records


@callback(
    [
        # Date range
        Output("date-range-filter", "min_date_allowed"),
        Output("date-range-filter", "max_date_allowed"),
        Output("date-range-filter", "start_date"),
        Output("date-range-filter", "end_date"),
        # Checklists
        ## Trip state
        Output("trip-state-checklist", "options"),
        Output("trip-state-checklist", "value"),
        ## Chargning stations
        Output("chargning-station-checklist", "options"),
        Output("chargning-station-checklist", "value"),
        ## Station state
        Output("station-state-checklist", "options"),
        Output("station-state-checklist", "value"),
        ## Station type
        Output("station-type-checklist", "options"),
        Output("station-type-checklist", "value"),
    ],
    [
        Input("full-data-store", "data")
    ],
)
def initalize_filters(data):
    """
    Get trip data, and find min and max. Set this as a limit for the
    calendar and set it as inital dates.
    """
    logger.critical("Loading fitler values")
    trip_records, station_records, zone_records = data
    trip_df = pd.DataFrame.from_records(trip_records)
    station_df = pd.DataFrame.from_records(station_records)
    # Get datetime info
    trip_df["started_at"] = pd.to_datetime(trip_df["started_at"])
    trip_df["ended_at"] = pd.to_datetime(trip_df["ended_at"])
    min_start = trip_df["started_at"].min().date()
    max_end = trip_df["ended_at"].max().date()
    # Get trip state parameters
    trip_states = list(trip_df["state"].unique())
    trip_options = [{"label": state, "value": state} for state in trip_states]
    # Get charging station parameters
    is_charging_station = list(station_df["is_charging_station"].unique())
    charging_stations_options = [{"label": is_charging_station, "value": is_charging_station} for is_charging_station in is_charging_station]
    # Get station state parameters
    station_states = list(station_df["state"].unique())
    station_state_options = [{"label": state, "value": state} for state in station_states]
    # Get station type parameters
    station_types = list(station_df["station_type"].unique())
    station_type_options = [{"label": type, "value": type} for type in station_types]
    return min_start, max_end, min_start, max_end, trip_options, trip_states, charging_stations_options, is_charging_station, station_state_options, station_states, station_type_options, station_types


@callback(
    [
        Output("filtered-trip-store", "data"),
        Output("filtered-station-store", "data"),
        Output("filtered-zone-store", "data")
    ],
    [
        Input("full-data-store", "data"),
        # Date filter
        Input("date-range-filter", "start_date"),
        Input("date-range-filter", "end_date"),
        # Checklist filter
        Input("trip-state-checklist", "value"),
        Input("chargning-station-checklist", "value"),
        Input("station-state-checklist", "value"),
        Input("station-type-checklist", "value"),
    ],

)
def apply_sidebar_filter(data, min_date, max_date, selected_trip_states, is_chargning_station, selected_station_states, selected_station_types):
    trip_records, station_records, zone_records = data
    # Date only applies to trip data
    min_date = datetime.strptime(min_date, "%Y-%m-%d").date()
    max_date = datetime.strptime(max_date, "%Y-%m-%d").date()
    filtered_trips = []
    # Filter trips
    for trip_record in trip_records:
        # Extract datetime string
        started_at = trip_record["started_at"]
        ended_at = trip_record["ended_at"]
        if started_at and ended_at:
            # Convert to datetime object
            start_date = datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S%z").date()
            end_date = datetime.strptime(ended_at, "%Y-%m-%d %H:%M:%S%z").date()
        else:
            # If missing, print record and skip
            from pprint import pprint
            pprint(trip_record)
            continue
        satsfires_date = start_date >= min_date and end_date <= max_date
        satisfies_states = trip_record["state"] in selected_trip_states
        if satsfires_date and satisfies_states:
            # Check for filtration condition
            filtered_trips.append(trip_record)
    return filtered_trips, station_records, zone_records

