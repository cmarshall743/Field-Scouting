import dash_table
import time
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import geocoder
from dash.dependencies import Input, Output, State
from utils import database
import dash
import plotly.graph_objects as go
from modules import scouting_map


app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

cursor = database.cnxn.cursor()

def layout_function():
    query = "SELECT * FROM [scouting_data]"
    df = pd.read_sql(query, database.cnxn)
    return html.Div([
        html.H1("Kings River Farming Field Scouting Beta 0.1.2"),
        dbc.Button("New Entry", id="open", color="info"),
        dbc.Button("Refresh", id="refresh", color="info"),
        dbc.Modal(
        [
         dbc.ModalHeader("New Entry"),
         dbc.ModalBody(
                html.Form(
                [
                    dbc.Label("Issue ID"),
                    dcc.Dropdown(
                        id="issue_dropdown",
                        placeholder="Select One",
                        options=[
                            {"label": "CRS", "value": "CRS"},
                            {"label": "Citricola Scale", "value": "Citricola Scale"},
                            {"label": "Snail Damage", "value": "Snail Damage"},
                            {"label": "Thrip", "value": "Thrip"},
                            {"label": "Cotney Cushin Scale", "value": "Cotney Cushin Scale"},
                            {"label": "Katydid", "value": "Katydid"},
                        ],
                    ),
                    dbc.Label(
                     "If necessary, please include a few more details"
                    ),
                    html.Br(),
                    dbc.Input(type="string",
                              id="description_input",
                              placeholder="Enter Description Here",
                              name="description"
                              ),
                    html.Br(),
                    dbc.Label(
                     "Click the button below to import your current location or paste coordinates from google maps"),
                    html.Br(),
                    dbc.Button(
                        "Get Location",
                        color="success",
                        id="get_location",
                        className="mr-1"
                        ),
                    dbc.Input(
                        id="location_manual",
                        placeholder="paste location here"
                    ),
                ],
                    style={"padding-top": "20px",
                           "height": "500px"},
                    id="entry_form",
                    action="/entry",
                    method="GET",
                    target="frame",
                ),

            ),

            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Close",
                        color="danger",
                        id="close",
                        className="mr-1",
                    ),
                    dbc.Button(
                        "Save",
                        color="primary",
                        id="save",
                        className="mr-1",
                    ),
                ],
            ),
        ],
            id="modal",
            style={"width": "50%"},
        ),

        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
        ),
        html.Div(id="temp"),
        html.Div(id="temp2"),
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                      style={'background': '#00FC87', 'padding-bottom': '2px', 'padding-left': '2px', 'height': '100vh'}
                      )
        ],
        )
    ]
    )


app.layout = layout_function


@app.callback(Output("graph", "figure"),
              Input("refresh", "n_clicks"),
              )
def update_map(clicked):
    return scouting_map.fig



@app.callback(
    Output(component_id="temp", component_property="children"),
    Input(component_id="save", component_property="n_clicks"),
    State("issue_dropdown", "value"),
    State("description_input", "value"),
    State("location_manual", "value"),
)
def get_description(clicked, issue, description, location):
    if clicked:
        print("clicked")
        print("issue " + issue + "description " + description + "location " + location)
        g = geocoder.ip("me")
        print(g.lat)
        print(g.lng)
        insert_record = """INSERT INTO scouting_data (Issue_Code, Description, Location, Latitude, Longitude
        ) VALUES (?,?,?,?,?)"""
        cursor.execute(insert_record, issue, description, location, g.lat, g.lng)
        database.cnxn.commit()
        time.sleep(.5)
        print("done sleeping")
        return issue, description, location


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)


