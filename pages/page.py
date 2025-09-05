from dash import html, dcc

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


overview_layout = html.Div(
    children=[
        html.P(id="overview-starter"),
        dcc.Store(id="overiview-store"),
    ],
)


