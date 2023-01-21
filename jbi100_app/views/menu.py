from dash import dcc, html
from ..config import color_list1, color_list2
import pandas as pd
import pathlib
import os

# Load data
APP_PATH = str(pathlib.Path(__file__).parent.parent.parent.resolve())

df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "neighbourhoods.csv")))
neighbourhood_list = (
    ["All"]
    + sorted(df.neighbourhood_group.unique().tolist())
    + sorted(df.neighbourhood.unique().tolist())
)


def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Settings"),
            html.Div(
                id="intro"
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Br(),
            html.Label("Enter your zip code to find your neighbourhood:"),
            dcc.Input(
                id="zip_code_text",
                type="text",
                placeholder="i.e. 10460",
            ),
            html.Div(id="error", style={"color": "red"}),
            html.Br(),
            html.Label("Select a neighbourhood group or neighbourhood:"),
            dcc.Dropdown(
                id="select_neigh",
                options=[{"label": i, "value": i} for i in neighbourhood_list],
                value=neighbourhood_list[0],
            ),
            html.Label("Select a view of the map:"),
            dcc.RadioItems(
                id="map_view",
                options=[
                    {'label': 'Fire alarms', 'value': 'fire'},
                    {'label': 'CO monitors', 'value': 'co'},                    
                    {'label': 'Noise complaints', 'value': 'noise'},
                ],
                value='fire'

            ),
            html.Label("Colourblind mode:"),
            dcc.RadioItems(
                id="cb_mode",
                options=[
                    {'label': 'disable', 'value': 'default'}, 
                    {'label': 'enabled', 'value': 'cb_mode'},
                ],
                value='default'

            ),
        ],
        style={"textAlign": "float-left"},
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
