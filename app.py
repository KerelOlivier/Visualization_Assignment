from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.histogram import Histogram

import plotly.express as px
import plotly.graph_objects as go

from dash import html
from dash.dependencies import Input, Output
from dash import dcc

from wordcloud import WordCloud 

# tmp data
import geopandas as gpd

import pathlib
import os
import pandas as pd

if __name__ == '__main__':

    # Create data
    df = px.data.iris()
    long_df = px.data.medals_long()
    geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    # Create the plots
    scatter = px.scatter(df, x='sepal_length', y='sepal_width')

    vbarchart = px.bar(long_df, x="nation", y="count", color="medal", title="Long-Form Input")

    hbarchart = px.bar(long_df, x="count", y="nation", color='medal', orientation='h')

    scattermap = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y, # center latitude
                        lon=geo_df.geometry.x, # center longitude
                        hover_name="name",
                        zoom=1,)
    scattermap.update_layout(mapbox_style="open-street-map") # Needed to avoid paying for mapbox
    scattermap.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    wc = WordCloud().generate("aaaaa bbbbb ccccc")
    wcfig = go.Figure().add_trace(go.Image(z=wc))
    wcfig.update_layout(
        height=400,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"t": 0, "b": 0, "l": 0, "r": 0},
    )

    #Create the layout
    app.layout = html.Div(
        id="container",
        children=[
            html.Section(
                className = "card",
                children=[dcc.Graph(figure=scatter)]
            ),
            html.Section(
                className = "card",
                
            ),
            html.Section(
                className = "card",
                children=[dcc.Graph(figure=vbarchart)]
            ),
            html.Section(
                className = "card",
                children=[dcc.Graph(figure=wcfig,config={"displayModeBar": False})]
            ),
            html.Section(
                className = "card",
                children=[dcc.Graph(figure=scattermap)]
            ),
            html.Section(
                className = "card a6",
                children=[dcc.Graph(figure=hbarchart)]
            )
        ]
    )



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
