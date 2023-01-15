from dash import dcc, html
import plotly.graph_objects as go
import geopandas as gpd
import plotly.express as px
import json
from shapely.geometry import Polygon
import pandas as pd
import geovoronoi as gv
import plotly.express as px


class NoiseMap(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
        self.df = pd.read_csv("data/noise.csv")
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
        self.fig = px.choropleth_mapbox(self.df, geojson=self.voronoi, locations='id', color='density',
                    color_continuous_scale="Viridis",
                    range_color=(0, 200),
                    mapbox_style="carto-darkmatter",
                    zoom=10, center = {"lat": 40.705990161916645, "lon": -73.97582996116756},
                    opacity=0.2,
                    hover_data=["area", "incident_cnt", "density"],
                    labels={'incident_cnt':'complaints', 'density':'complaints/km^2'}
                    )        

    def update(self):
        
        self.fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        self.fig.update_traces(marker_line_width=0)
        self.fig.update_xaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        self.fig.update_yaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        print("updating map")
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
        print(type(self.fig))
        return self.fig
