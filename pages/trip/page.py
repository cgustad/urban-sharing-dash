from dash import html, dcc, callback, Input, Output
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
                        dcc.Dropdown(),
                        # dcc.Dropdown(
                        #     id="trip-stations-dropdown",
                        #     options=None,
                        #     value=None
                        # ),
                        dcc.Graph(id="trip-histogram"),
                    ],
                ),
            ],
        ),
    ],
)


@callback(
    Output("trip-histogram", "figure"),
    [
        Input("trip-starter", "childrenp"),
        Input("full-data-store", "data"),
    ]

)
def trip_histogram(empty, records_from_csv):
    trip_records, station_records, zone_records = records_from_csv
    trip_df = pd.DataFrame.from_records(trip_records)
    from pprint import pprint
    pprint(trip_df.columns)
    start_station_ids = list(trip_df["start_station_id"].unique())
    fig = px.histogram(trip_df, x="started_at")
    return fig
