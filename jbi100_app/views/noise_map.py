from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gpd
import plotly.express as px
import json
from shapely.geometry import Polygon
import pandas as pd
import geovoronoi as gv
import plotly.express as px
import jbi100_app.views.colors as clrs


class NoiseMap(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = pd.read_csv("data/noise.csv")
        self.nbh = None
        self.bnb_df = df
        self.bnb_loc_df = self.bnb_df[["name", "longitude", "latitude"]]
        with open('data/voronoi.geojson' , 'r') as file:
            self.voronoi = json.load(file)
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id),
            ],
        )

    def update(self, loc_change=False, neighbourhood=None):
        
        # Set the neighbourhood if changed
        if loc_change:
            self.nbh = neighbourhood

        # Filter data corresponding to the neighbourhood 
        if self.nbh is not None:
            filter = self.bnb_df[
                    (self.bnb_df.neighbourhood_group == self.nbh ) |
                    (self.bnb_df.neighbourhood == self.nbh)
                    ]
        else:
            filter = self.bnb_df

        # Determine the data geographical center
        center_lat = filter["latitude"].mean()
        center_lon = filter["longitude"].mean()

        center = {"lat":center_lat, "lon":center_lon}

        groups = {
            "Brooklyn",
            "Manhattan",
            "Bronx",
            "Staten Island",
            "Queens"
        } 

        # Determine the zoom level
        zoom = 9
        if self.nbh is None:
            zoom = 9
        else:
            if self.nbh in groups:
                zoom = 11
            else:
                zoom = 14

        # Creat the choropleth layer
        self.fig = px.choropleth_mapbox(self.df, geojson=self.voronoi, locations='id', color='density',
                    color_continuous_scale=clrs.colour_gradient,
                    range_color=(0, 200),
                    mapbox_style="carto-darkmatter",
                    zoom=zoom, center = center,
                    opacity=0.5,
                    hover_data={"area":False, "incident_cnt":True, "density":False, "id":False},
                    labels={'incident_cnt':'complaints'}
                    )

        self.fig.update_traces(marker_line_width=0)

        # create the scatter layer
        self.scatter = px.scatter_mapbox(filter,
                                        lat="latitude",lon="longitude",
                                        hover_name="name",
                                        color_discrete_sequence=[clrs.marker_4],
                                        hover_data={'latitude':False, 
                                                    'longitude':False},
                                        mapbox_style="carto-darkmatter")

        self.fig.add_trace(self.scatter.data[0])   

        #update the layout
        self.fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select',
            paper_bgcolor=clrs.card_colour,
            plot_bgcolor=clrs.card_colour,
            coloraxis_colorbar=dict(
                title="Complaint density",
                titlefont=dict(color=clrs.txt_colour),
                ticks="outside",
                tickcolor=clrs.txt_colour,
                tickfont=dict(color=clrs.txt_colour)
            ))
        return self.fig
