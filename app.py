from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.histogram import Histogram
from jbi100_app.views.horizontal_bar import HorizontalBar
from jbi100_app.views.word_cloud import WordsCloud
from jbi100_app.views.map_group import MapGroup
import jbi100_app.views.colors as clrs

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


def update_colors(theme="default"):
    if theme == "cb_mode":
        clrs.bg_colour = "#121212"
        clrs.card_colour = "#212121"
        clrs.txt_colour = "#f1f1f1"
        clrs.line_colour = "#424242"

        clrs.marker_1 = "#FEC601"   # Yellow
        clrs.marker_2 = "#3DA5D9"   # Light blue
        clrs.marker_3 = "#EA7317"   # Orange
        clrs.marker_4 = "#73BFB8"   # Teal
        clrs.marker_5 = "#2364AA"   # Dark blue
        clrs.marker_off = "#a8a8a8" # Grey

        clrs.colour_gradient = "Ice_r"
        clrs.wc_colour_func = clrs.my_tf_color_func_cb

    else: #default colors
        clrs.bg_colour = "#121212"
        clrs.card_colour = "#212121"
        clrs.txt_colour = "#f1f1f1"
        clrs.line_colour = "#424242"

        clrs.marker_1 = "#FFD449"   # Yellow
        clrs.marker_2 = "#A8D5E2"   # Light blue
        clrs.marker_3 = "#F9A620"   # Orange
        clrs.marker_4 = "#A8D5E2"   # Dark green
        clrs.marker_5 = "#548C2F"   # Green
        clrs.marker_off = "#a8a8a8" # Grey

        clrs.colour_gradient = "Greens"
        clrs.wc_colour_func = clrs.my_tf_color_func

if __name__ == "__main__":
    title = "Visualizing the NYC Airbnb debate"

    #current neighbourhood
    current_neighbourhood = None
    # To make sure it's initialized
    print("current neighbourhood", current_neighbourhood)
    # Update title based on drop down


    # Create data
    df = px.data.iris()
    APP_PATH = str(pathlib.Path(__file__).parent.resolve())
    df2 = pd.read_csv(
        os.path.join(APP_PATH, os.path.join("data", "airbnb_open_data_full_clean.csv"))
    )
    # for scatterplot_rq3.py
    df_rq3 = pd.read_csv(
        os.path.join(APP_PATH, os.path.join("data", "hotel_final_grouped.csv"))
    )

    mode = 0

    # Instantiate custom views
    wordcloud = WordsCloud("wordcloud", "Advertising of AirBnbs in selected area", df2)
    mapgroup = MapGroup(df2)
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
                    html.H4(id="header_title", children=title),
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
        """
        Updates the current map we are looking at
        """
        if map_view == 'fire':
            map_new = "Fire alarms"
        elif map_view == 'co':
            map_new = "Carbon monoxide monitors"
        else:
            map_new = 'Noise complaints density and Airbnb locations'
        return map_new

    def update_wc(neighbourhood):
        """
        Updates the word cloud by creating one,
        turning it into an image, and decoding it,
        since wordcloud doesn't work with Dash
        """
        img = BytesIO()
        wordcloud.update(neighbourhood).save(img, format="PNG")
        return "data:image/png;base64,{}".format(
            base64.b64encode(img.getvalue()).decode()
        )




    @app.callback(
        [
            Output("header_title", "children"),
            Output("error", "children"),
            Output("zip_code_text", "value"),
            Output("select_neigh", "value"),
            Output(histogram.html_id, "figure"),
            Output(horizontal_bar.html_id, "figure"),
            Output(wordcloud.html_id, "src"),
            Output(mapgroup.html_id, "figure"),
            Output(rq3.html_id, "figure"),
            Output("map_title", "children"),
            Output("switch_table", "className")
        ],
        [
            Input("select_neigh", "value"),
            Input("zip_code_text", "value"),
            Input("local_switch", "on"),
            Input("map_view", "value"),
            Input("cb_mode", "value"),
            Input("histogram", "clickData")
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
        cb_mode,
        histo_click,
        header_state,
        histogram_current,
        hb_current,
        wordcloud_current,
        scatterplot_current,
        title_current,
    ):
        # determine if there is a predetermined neighbourhood
        # We can't use a variable because dash is stateless and maintains
        # Sessions using cookies, which we can't easily access and process
        if select_name != None:
            current_neighbourhood = select_name
        elif zip_code_text != None and zip_code_text != "" and zip_code_text.isdigit() and len(zip_code_text) == 5:
            # Load data
            APP_PATH = str(pathlib.Path(__file__).parent.resolve())
            df = pd.read_csv(
                os.path.join(APP_PATH, os.path.join("data", "neighbourhoods.csv")),
                dtype=str,
            )
            df_filter = df[df.zipcode == zip_code_text]
            if(len(df_filter) == 0):
                current_neighbourhood = None
            else:
                current_neighbourhood = df_filter[["neighbourhood"]].iloc[0][0]
        else:
            current_neighbourhood = None
        


        map_title_new = update_map_view(map_view, title_current)

        # Refresh the page when a different colour scheme is selected
        if dash.callback_context.triggered_id == "cb_mode":
            update_colors(cb_mode)
            map_title_new = update_map_view(map_view, title_current)
            return (
                title,
                None,
                zip_code_text,
                select_name,
                histogram.update(current_neighbourhood, local_switch),
                horizontal_bar.update(neighbourhood=current_neighbourhood),
                update_wc(current_neighbourhood),
                mapgroup.update(map_mode=map_view, neighbourhood=current_neighbourhood),
                rq3.update(None),
                map_title_new,
                ""
            )

        # Update the h_barchart when a property count is selected in the histogram
        if dash.callback_context.triggered_id == "histogram":
            prop_cnt = histo_click['points'][0]['x']
            return (
                header_state,
                None,
                zip_code_text,
                select_name,
                histogram_current,
                horizontal_bar.update(current_neighbourhood, prop_cnt),
                wordcloud_current,
                mapgroup.fig,
                rq3.fig,
                map_title_new,
                ""                   
            )

        # Toggle between the different map views 
        if dash.callback_context.triggered_id == "map_view":
            map_title_new = update_map_view(map_view, title_current)
            return (
                header_state,
                None,
                zip_code_text,
                select_name,
                histogram_current,
                hb_current,
                wordcloud_current,
                mapgroup.update(map_view, neighbourhood=current_neighbourhood, loc_change=True),
                rq3.fig,
                map_title_new,
                ""
            )

        # focus on selected neighbourhood based on zipcode
        if zip_code_text != None and zip_code_text != "":
            # Check for validity of the zip code and find the neighbourhood if valid
            if (not zip_code_text.isdigit()) or (len(zip_code_text) != 5):
                return (
                    header_state,
                    "The value entered is not a valid zip code.",
                    zip_code_text,
                    select_name,
                    histogram_current,
                    hb_current,
                    wordcloud_current,
                    mapgroup.fig,
                    rq3.fig,
                    map_title_new,
                    ""
                    
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
                        "",
                        select_name,
                        histogram_current,
                        hb_current,
                        wordcloud_current,
                        mapgroup.fig,                        
                        rq3.fig,
                        map_title_new,
                        ""
                    )
                else:
                    current_neighbourhood = df_filter[["neighbourhood"]].iloc[0][0]
                    return (
                        f"{title}: {current_neighbourhood}",
                        None,
                        zip_code_text,
                        current_neighbourhood,
                        histogram.update(current_neighbourhood, local_switch),
                        horizontal_bar.update(current_neighbourhood),  
                        update_wc(current_neighbourhood),                    
                        mapgroup.update(map_mode=map_view, loc_change=True, neighbourhood=current_neighbourhood),
                        rq3.update(current_neighbourhood),
                        map_title_new,
                        ""
                    )
        # Load data for selected neighbourhood 
        elif select_name != "All":
            current_neighbourhood = select_name
            return (
                f"{title}: {select_name}",
                None,
                None,
                select_name,
                histogram.update(current_neighbourhood, local_switch),
                horizontal_bar.update(current_neighbourhood),
                update_wc(current_neighbourhood),                
                mapgroup.update(map_mode=map_view, loc_change=True, neighbourhood=current_neighbourhood),
                rq3.update(current_neighbourhood),
                map_title_new,
                ""
            )
        # Base case: load visualizations for all neighbourhoods
        else:
            map_title_new = update_map_view(map_view, title_current)
            return (
                title,
                None,
                None,
                select_name,
                histogram.update(None, local_switch),
                horizontal_bar.update(None),
                update_wc(None),
                mapgroup.update(map_mode=map_view, loc_change=True),
                rq3.update(None),
                map_title_new,
                "disabled"
            )

    app.run_server(debug=False, dev_tools_ui=False)
