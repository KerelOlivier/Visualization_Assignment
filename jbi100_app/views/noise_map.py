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

        if loc_change:
            self.nbh = neighbourhood

        if self.nbh is not None:
            filter = self.bnb_df[
                    (self.bnb_df.neighbourhood_group == self.nbh ) |
                    (self.bnb_df.neighbourhood == self.nbh)
                    ]
        else:
            filter = self.bnb_df

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

        zoom = 9
        # we also need to know the zoom level and center
        if loc_change:
            if self.nbh is None:
                zoom = 9
            else:
                if self.nbh in groups:
                    zoom = 11
                else:
                    zoom = 14

        self.fig = px.choropleth_mapbox(self.df, geojson=self.voronoi, locations='id', color='density',
                    color_continuous_scale=clrs.colour_gradient,
                    range_color=(0, 200),
                    mapbox_style="carto-darkmatter",
                    zoom=zoom, center = center,
                    opacity=0.5,
                    hover_data=["area", "incident_cnt", "density"],
                    labels={'incident_cnt':'complaints', 'density':'complaints/km^2'}
                    )

        self.fig.update_traces(marker_line_width=0)
        self.scatter = px.scatter_mapbox(filter,
                                        lat="latitude",lon="longitude",
                                        hover_name="name",
                                        color_discrete_sequence=[clrs.marker_4],
                                        hover_data={'latitude':False, 
                                                    'longitude':False},
                                        opacity=0.5,
                                        mapbox_style="carto-darkmatter")

        self.fig.add_trace(self.scatter.data[0])   


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
        print(type(self.fig))
        return self.fig
