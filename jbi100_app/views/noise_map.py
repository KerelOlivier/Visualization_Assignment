from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gpd
import plotly.express as px
import json
from shapely.geometry import Polygon
import pandas as pd
import geovoronoi as gv


class NoiseMap(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        self.df = pd.read_csv("data/noise_complaints_clean.csv")
        self.voronoi = self.calc_voronoi()
        print("test")
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    def calc_voronoi(self):
        long_min = self.df['longitude'].min()-0.025
        long_max = self.df['longitude'].max()+0.025
        lat_min = self.df['latitude'].min()-0.025
        lat_max = self.df['latitude'].max()+0.025

        points = [
        (long_min, lat_max),
        (long_max, lat_max),
        (long_max, lat_min),
        (long_min, lat_min),
            ]
        shape = Polygon(points)
        coords = self.df[['longitude', 'latitude']].to_numpy()
        region_polys, region_pts = gv.voronoi_regions_from_coords(coords, shape)


    def update(self):




        print("Hello world")

        self.fig =  px.choropleth_mapbox()

        # x_values = self.df[self.feature_x]
        # y_values = self.df[self.feature_y]
        # self.fig.add_trace(go.Scatter(
        #     x=x_values, 
        #     y=y_values,
        #     mode='markers',
        #     marker_color='rgb(200,200,200)'
        # ))
        # self.fig.update_traces(mode='markers', marker_size=10)
        # self.fig.update_layout(
        #     yaxis_zeroline=False,
        #     xaxis_zeroline=False,
        #     dragmode='select',
        #     paper_bgcolor="#212121",
        #     plot_bgcolor="#212121",
        # )
        # self.fig.update_xaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        # self.fig.update_yaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        # # highlight points with selection other graph
        # if selected_data is None:
        #     selected_index = self.df.index  # show all
        # else:
        #     selected_index = [  # show only selected indices
        #         x.get('pointIndex', None)
        #         for x in selected_data['points']
        #     ]

        # self.fig.data[0].update(
        #     selectedpoints=selected_index,

        #     # color of selected points
        #     selected=dict(marker=dict(color=selected_color)),

        #     # color of unselected pts
        #     unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        # )

        # # update axis titles
        # self.fig.update_layout(
        #     xaxis_title=self.feature_x,
        #     yaxis_title=self.feature_y,
        # )

        return self.fig
