from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Card style, perhaps make this global
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Trip dataframe
df = pd.read_csv("assets/trips.csv")

overview_layout = html.Div(
    children=[
        html.P(id="overview-starter"),
        dcc.Store(id="overiview-store"),
                dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Datafame", className="card-title"),
                    ]
                ),
                dbc.CardBody(
                    [
                        #                        html.Pre(id="overview-file-list", style=styles["pre"])
                        dash_table.DataTable(df.to_dict("records"), [{"name": i, "id": i} for i in df.columns])

                    ]
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H2("Metadata Overview", className="card-title"),
                    ]
                ),
                dbc.CardBody(
                    [
                        dcc.Graph(figure= None, id="models-block")
                        #html.Pre(id="overview-file-list", style=styles["pre"])
                    ]
                )
            ]
        ),
    ],
)
