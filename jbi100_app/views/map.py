from dash import dcc, html
import plotly.graph_objects as go
import time


class Map(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.zoom = 1
        self.nbh = None
        self.colours = ["blue", "red"]
        self.mode = 0
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name, id="map_title"),
                dcc.Graph(id=self.html_id)
            ],
        )
        
        

    def update(self, mode, colours=["blue", "red"], neighbourhood=None):

        self.fig = go.Figure()

        print("step 1:", time.perf_counter())
        if neighbourhood is not None:
            filter = self.df[(self.df.neighbourhood_group == neighbourhood) | (self.df.neighbourhood == neighbourhood)]
            self.nbh = neighbourhood
        elif self.nbh is not None:
            filter = self.df[(self.df.neighbourhood_group == self.nbh) | (self.df.neighbourhood == self.nbh)]
        else:
            filter = self.df

        print("step 2:", time.perf_counter())

        marker_colours = dict(zip([True,False], colours))
        if mode is not None:
            self.mode = mode

        if self.mode == 0:
            # fire alarm node         
            filter["colour"] = filter["has_fire_alarm"].replace(to_replace=marker_colours)
        elif self.mode == 1:
            # co monitor mode
            filter["colour"] = filter["has_co_monitor"].replace(to_replace=marker_colours)
        #elif self.mode == 2:
            # noise complaints mode
        print("step 3:", time.perf_counter())


        self.fig.add_trace(go.Scattermapbox(
                            lat=filter.latitude,
                            lon=filter.longitude,
                            marker_color=filter.colour,
                            hovertext=filter.id,

        ))

        print("step 4:", time.perf_counter())

        self.fig.update_layout(mapbox_style="open-street-map")
        self.fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

        self.fig.update_traces(mode='markers', marker_size=10)
        print("step 5:", time.perf_counter())


        return self.fig

    def aggregate_data():
        print()