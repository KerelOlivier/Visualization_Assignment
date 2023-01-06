from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.histogram import Histogram

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State

import pathlib
import os
import pandas as pd

if __name__ == "__main__":
    # Create data
    df = px.data.iris()
    APP_PATH = str(pathlib.Path(__file__).parent.resolve())

    df2 = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "airbnb_open_data_full_clean.csv")))

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", "sepal_length", "sepal_width", df)
    scatterplot2 = Scatterplot("Scatterplot 2", "petal_length", "petal_width", df)
    scatterplot3 = Scatterplot("Scatterplot 3", "petal_length", "petal_width", df)
    scatterplot4 = Scatterplot("Scatterplot 4", "petal_length", "petal_width", df)

    histogram = Histogram("Histogram", "host_listings_neighbourhood_count", df2)

    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="header",
                children=[
                    html.H4(id="header_title", children="Airbnb in New York"),
                ],
            ),

            # graphs
            html.Div(
                id="graph-grid",
                className="nine columns",
                children=[scatterplot1,
                    html.Div( id="settings", className="three columns", children=make_menu_layout()),
                        scatterplot2, histogram, scatterplot3, scatterplot4],
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
            Output(histogram.html_id, "figure")
        ],
        [
            Input("select_neigh", "value"), 
            Input("zip_code_text", "value")
        ],
        [
            State("header_title", "children"),
            State(histogram.html_id, "figure")
        ],
    )
    def update_neighbourhoods(select_name, zip_code_text, header_state, histogram_current):
        if zip_code_text is not None:
            if (not zip_code_text.isdigit()) or (len(zip_code_text) != 5):
                return (
                    header_state,
                    "The value entered is not a valid zip code.",
                    zip_code_text,
                    histogram_current
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
                        histogram_current
                    )
                else:
                    neighbourhood = df_filter[["neighbourhood"]].iloc[0][0]
                    return "Airbnb in New York: " + neighbourhood, None, "", histogram.update(neighbourhood)
        elif select_name != "All":
            return "Airbnb in New York: " + select_name, None, None, histogram.update(select_name) 
        else:
            return "Airbnb in New York", None, None, histogram.update()

    app.run_server(debug=False, dev_tools_ui=False)
