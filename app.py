from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.views.histogram import Histogram
from jbi100_app.views.horizontal_bar import HorizontalBar
from jbi100_app.views.word_cloud import WordsCloud
from jbi100_app.views.map_group import MapGroup

import dash
from jbi100_app.views.scatterplot_rq3 import RQ3
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output, State
from io import BytesIO
import base64
import pathlib
import os
import pandas as pd

if __name__ == "__main__":
    # Create data
    df = px.data.iris()
    APP_PATH = str(pathlib.Path(__file__).parent.resolve())
    df2 = pd.read_csv(
        os.path.join(APP_PATH, os.path.join("data", "airbnb_open_data_full_clean.csv"))
    )
    # rq3. might replace
    df_rq3 = pd.read_csv(
        os.path.join(APP_PATH, os.path.join("data", "hotel_final_grouped.csv"))
    )


    mode = 0

    # Instantiate custom views
    wordcloud = WordsCloud("wordcloud", "Advertising of AirBnbs in selected area", df2)
    mapgroup = MapGroup(df2)
    # can change it later
    rq3 = RQ3(
        "Number of Airbnbs vs Hotels per neighbourhood",
        "airbnb_counts_per_neighbourhood",
        "hotel_counts_per_neighbourhood",
        df_rq3,
    )

    histogram = Histogram(
        "Distribution of number of Airbnbs owned by individual owners in selected area",
        "host_listings_neighbourhood_count",
        df2,
    )

    menu =  html.Div(
                        id="settings",
                        className="three columns",
                        children=make_menu_layout(),
                    )

    horizontal_bar = HorizontalBar(
        "Number of properties per owner",
        "host_listings_neighbourhood_count",
        df2,
    )

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
                children=[
                    rq3,
                    html.Div(
                        id="settings",
                        className="three columns",
                        children=make_menu_layout(),
                    ),
                    histogram,
                    wordcloud,
                    mapgroup,
                    horizontal_bar,
                ],
            ),
        ],
    )

    def update_map_view(map_view, map_title):
        print("map: ", map_view)
        if map_view == 'fire':
            map_new = "Fire alarms"
        elif map_view == 'co':
            map_new = "Carbon monoxide monitors"
        # elif map_view == 2:
        else:
            map_new = 'noise complaints density and airbnb locations '
        return map_new

    def update_wc(neighbourhood):
        img = BytesIO()
        wordcloud.update(neighbourhood).save(img, format="PNG")
        return "data:image/png;base64,{}".format(
            base64.b64encode(img.getvalue()).decode()
        )



    # Update title based on drop down
    @app.callback(
        [
            Output("header_title", "children"),
            Output("error", "children"),
            Output("zip_code_text", "value"),
            Output(histogram.html_id, "figure"),
            Output(horizontal_bar.html_id, "figure"),
            Output(wordcloud.html_id, "src"),
            Output(mapgroup.html_id, "figure"),
            Output(rq3.html_id, "figure"),
            Output("map_title", "children"),
        ],
        [
            Input("select_neigh", "value"),
            Input("zip_code_text", "value"),
            Input("local_switch", "on"),
            Input("map_view", "value"),
        ],
        [
            State("header_title", "children"),
            State(histogram.html_id, "figure"),
            State(horizontal_bar.html_id, "figure"),
            State(wordcloud.html_id, "src"),
            State("map_title", "children"),
            State(rq3.html_id, "figure"),
        ],
    )


    def update_neighbourhoods(
        select_name,
        zip_code_text,
        local_switch,
        map_view,
        header_state,
        histogram_current,
        hb_current,
        wordcloud_current,
        scatterplot_current,
        title_current,
    ):
        if dash.callback_context.triggered_id == "map_view":
            map_title_new = update_map_view(map_view, title_current)
            return (
                header_state,
                None,
                zip_code_text,
                histogram_current,
                hb_current,
                wordcloud_current,
                mapgroup.update(map_view),
                scatterplot_current,
                map_title_new
            )
        if zip_code_text is not None:
            if (not zip_code_text.isdigit()) or (len(zip_code_text) != 5):
                return (
                    header_state,
                    "The value entered is not a valid zip code.",
                    zip_code_text,
                    histogram_current,
                    hb_current,
                    wordcloud_current,
                    mapgroup.fig,
                    scatterplot_current,
                    title_current
                    
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
                        histogram_current,
                        hb_current,
                        wordcloud_current,
                        mapgroup.fig,                        
                        scatterplot_current,
                        title_current
                    )
                else:
                    neighbourhood = df_filter[["neighbourhood"]].iloc[0][0]
                    return (
                        "Airbnb in New York: " + neighbourhood,
                        None,
                        "",
                        histogram.update(neighbourhood, local_switch),
                        horizontal_bar.update(neighbourhood),  
                        update_wc(neighbourhood),                    
                        mapgroup.update(loc_change=True, neighbourhood=neighbourhood),
                        rq3.update(neighbourhood),
                        title_current
                    )
        elif select_name != "All":
            return (
                "Airbnb in New York: " + select_name,
                None,
                None,
                histogram.update(select_name, local_switch),
                horizontal_bar.update(select_name),
                update_wc(select_name),                
                mapgroup.update(loc_change=True, neighbourhood=select_name),
                rq3.update(select_name),
                title_current
            )
        else:
            map_title_new = update_map_view(map_view, title_current)
            return (
                "Airbnb in New York",
                None,
                None,
                histogram.update(None, local_switch),
                horizontal_bar.update(None),
                update_wc(None),
                mapgroup.update(loc_change=True),
                rq3.update(None),
                map_title_new
            )

    app.run_server(debug=False, dev_tools_ui=False)
