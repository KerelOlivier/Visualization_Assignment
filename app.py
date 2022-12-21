from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

import plotly.express as px
import plotly.graph_objects as go

from dash import html
from dash.dependencies import Input, Output
from dash import dcc

from wordcloud import WordCloud 

# tmp data
import geopandas as gpd


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



    app.run_server(debug=False, dev_tools_ui=False)