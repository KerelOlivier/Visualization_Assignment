from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State

import pathlib
import os
import pandas as pd

if __name__ == "__main__":
    # Create data
    df = px.data.iris()

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", "sepal_length", "sepal_width", df)
    scatterplot2 = Scatterplot("Scatterplot 2", "petal_length", "petal_width", df)

    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="header",
                children=[
                    html.H4(id="header_title", children="Airbnb in New York"),
                ],
            ),
            # Left column
            html.Div(
                id="left-column", className="three columns", children=make_menu_layout()
            ),
            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[scatterplot1, scatterplot2],
            ),
        ],
    )

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"),
        [
            Input("select-color-scatter-1", "value"),
            Input(scatterplot2.html_id, "selectedData"),
        ],
    )
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"),
        [
            Input("select-color-scatter-2", "value"),
            Input(scatterplot1.html_id, "selectedData"),
        ],
    )
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)

    # Update title based on drop down
    @app.callback(
        [
            Output("header_title", "children"),
            Output("error", "children"),
            Output("zip_code_text", "value"),
        ],
        [Input("select_neigh", "value"), Input("zip_code_text", "value")],
        [State("header_title", "children")],
    )
    def update_neighbourhoods(select_name, zip_code_text, header_state):
        if zip_code_text is not None:
            if (not zip_code_text.isdigit()) or (len(zip_code_text) != 5):
                return (
                    header_state,
                    "The value entered is not a valid zip code.",
                    zip_code_text,
                )
            else:
                # Load data
                APP_PATH = str(pathlib.Path(__file__).parent.resolve())
                df = pd.read_csv(
                    os.path.join(APP_PATH, os.path.join("data", "neighbourhoods.csv")),
                    dtype=str,
                )

                # Get first neighbourhood with zipcode
                df_filter = df[df.zipcode == zip_code_text]
                if df_filter.empty:
                    return (
                        header_state,
                        "The value entered does not correspond to a New York neighbourhood.",
                        zip_code_text,
                    )
                else:
                    neighbourhood = df_filter[["neighbourhood"]].iloc[0][0]
                    return "Airbnb in New York: " + neighbourhood, None, ""
        elif select_name != "All":
            return "Airbnb in New York: " + select_name, None, None
        else:
            return "Airbnb in New York", None, None

    # # Update error based on zip code
    # @app.callback(
    #     Output("error", "children"),
    #     Input("zip_code_text", "value"),
    # )
    # def check_zip_code_error(value):
    #     if value is not None:
    #         if (not value.isdigit()) or (len(value) != 5):
    #             return "The value entered is not a valid zip code."
    #         else:
    #             #Load data
    #             APP_PATH = str(pathlib.Path(__file__).parent.resolve())
    #             df = pd.read_csv(
    #                 os.path.join(APP_PATH, os.path.join("data", "neighbourhoods.csv")), dtype=str
    #             )

    #             # Get first neighbourhood with zipcode
    #             df_filter = df[df.zipcode == value]
    #             if df_filter.empty:
    #                 return "The value entered does not correspond to a New York neighbourhood."
    #             else:
    #                 neighbourhood = df_filter[['neighbourhood']].iloc[0][0]
    #                 return None

    # Update title based on zip code
    # @app.callback(
    #     Output("header_title", "children"),
    #     Input("zip_code_text", "value"),
    # )
    # def update_zip_code_title(value):
    #     if value is not None:
    #         if (value.isdigit()) and (len(value) == 5):
    #             #Load data
    #             APP_PATH = str(pathlib.Path(__file__).parent.resolve())
    #         df = pd.read_csv(
    #             os.path.join(APP_PATH, os.path.join("data", "neighbourhoods.csv")), dtype=str
    #         )

    #         # Get first neighbourhood with zipcode
    #         df_filter = df[df.zipcode == value]
    #         if not df_filter.empty:
    #             neighbourhood = df_filter[['neighbourhood']].iloc[0][0]
    #             return "Airbnb in New York: " + neighbourhood

    app.run_server(debug=False, dev_tools_ui=False)
