from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
#from pages.model_graph.page import model_layout
from pages.dataframes.page import dataframes_layout
#from pages.overview.page import overview_layout
from layout.sidebar import sidebar
from layout.css import CONTENT_STYLE

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# Define content
content = html.Div(id="page-content", style=CONTENT_STYLE)
# Set layout
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        dcc.Tabs(id="app-tabs",
                 value="tab-1-overview",
                 children=[
                     dcc.Tab(label="Overview", value="tab-1-overview"),
                     dcc.Tab(label="Station", value="tab-2-station"),
                     dcc.Tab(label="Bike", value="tab-3-bike"),
                     dcc.Tab(label="DataFrames", value="tab-4-dataframes"),
                 ],
                 style=CONTENT_STYLE,
                 ),
        html.Div(id="tab-content",
                 style=CONTENT_STYLE
                 ),
    ]
)


# Update content based on sidebar selection
@app.callback(
    Output("tab-content", "children"),
    [
        Input("app-tabs", "value")
    ],
)
def render_tab_content(tab):
    under_construction_img = html.Img(src="assets/under-construction.svg", style={"width": "80%"})
    incomplete_tab = under_construction_img
    match tab:
        case "tab-1-overview":
            return incomplete_tab
        case "tab-2-station":
            return incomplete_tab
        case "tab-3-bike":
            return incomplete_tab
        case "tab-4-dataframes":
            return dataframes_layout
        case _:
            return html.Div("ERROR Unknown tab selected!")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
