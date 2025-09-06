import pandas as pd
from datetime import datetime
from layout.css import SIDEBAR_STYLE
from dash import html, dcc, callback, Input, Output

img_path = "assets/us-logo.png"

sidebar = html.Div(
    [
        html.Img(src=img_path, style={"width": "70%"}),
        html.P(id="app-starter"),
        dcc.Store(id="full-data-store"),
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
        html.H5("State"),
        dcc.Checklist(id="state-checklist"),
        # Data after beeing filtered by universial filter
        dcc.Store("filtered-by-universial-data"),
        html.H3("Tab filters:"),
        html.Hr(),
        # To be updated by tab
        html.Div(id="tab-sidebar-filters"),
        dcc.Store("fully-filtered-datax")
    ],
    style=SIDEBAR_STYLE,
)


@callback(
    Output("full-data-store", "data"),
    Input("app-starter", "children")
)
def app_startup(empty):
    """
    On app startup read all the asset CSV files
    """
    # Trips
    df_trips = pd.read_csv("assets/trips.csv").sort_values(by=["started_at"]).dropna()
    trip_records = df_trips.to_dict("records")
    # Stations
    df_stations = pd.read_csv("assets/madrid-stations.csv").dropna()
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
        # Checklist
        Output("state-checklist", "options"),
        Output("state-checklist", "value"),
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
    trip_records, station_records, zone_records = data
    trip_df = pd.DataFrame.from_records(trip_records)
    # Get dateime
    trip_df["started_at"] = pd.to_datetime(trip_df["started_at"])
    trip_df["ended_at"] = pd.to_datetime(trip_df["ended_at"])
    min_start = trip_df["started_at"].min()
    max_end = trip_df["ended_at"].max()
    # Get state possibilites
    states = list(trip_df["state"].unique())
    options = [{"label": state, "value": state} for state in states]
    return min_start, max_end, min_start, max_end, options, states

@callback(
    [
        Output("filtered-by-universial-data", "data"),
    ],
    [
        Input("full-data-store", "data"),
        Input("date-range-filter", "start_date"),
        Input("date-range-filter", "end_date"),

    ],

)
def apply_universial_filter(data, min_date, max_date):
    from pprint import pprint
    # Date only applies to trip data
    trip_records, station_records, zone_records = data
    min_date = datetime.strptime(min_date, "%Y-%m-%dT%H:%M:%S%z").date()
    max_date = datetime.strptime(max_date, "%Y-%m-%dT%H:%M:%S%z").date()
    filtered_trips = []
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
            pprint(trip_record)
            continue
        if start_date > min_date and end_date < max_date:
            # Check for filtration condition
            filtered_trips.append(trip_record)
    pprint(filtered_trips)
    return filtered_trips, station_records, zone_records
