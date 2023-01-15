from dash import dcc, html
import plotly.graph_objects as go
import time


class Map(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.zoom = 1
        self.nbh = "Astoria"
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
        
        
    

    def update(self, mode, loc_change=False, colours=["blue", "red"], neighbourhood=None):

        self.fig = go.Figure()

        # we are now changing the location to use
        if loc_change:
            self.nbh = neighbourhood

        # set the mode if we are changing that
        if mode is not None:
            self.mode = mode

        # check what data to use
        if self.nbh is not None:
             filter = self.df[
                    (self.df.neighbourhood_group == self.nbh)
                    | (self.df.neighbourhood == self.nbh)
                    ]
        else:
            filter = self.df

        groups = {
            "Brooklyn",
            "Manhattan",
            "Bronx",
            "Staten Island",
            "Queens"
        }

        # we also need to know the zoom level and center
        if self.nbh is None:
            zoom = 9
        else:
            if self.nbh in groups:
                zoom = 11
            else:
                zoom = 14
        
        center_lat = filter["latitude"].mean()
        center_lon = filter["longitude"].mean()

        center = {"lat":center_lat, "lon":center_lon}

        #print("step 2:", time.perf_counter()

        # get correct colours
        marker_colours = dict(zip([True,False], colours))

        if self.mode == 0:
            # fire alarm node         
            filter["colour"] = filter["has_fire_alarm"].replace(to_replace=marker_colours)
        elif self.mode == 1:
            # co monitor mode
            filter["colour"] = filter["has_co_monitor"].replace(to_replace=marker_colours)
        #elif self.mode == 2:
            # noise complaints mode

        #print("step 3:", time.perf_counter())


        # now create the scattermap (this is the slowest thing)
        self.fig.add_trace(go.Scattermapbox(
                            lat=filter.latitude,
                            lon=filter.longitude,
                            marker_color=filter.colour,
                            hovertext=filter.id,

        ))

        #print("step 4:", time.perf_counter())

        # set the layout correctly with zoom and center
        self.fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

        self.fig.update_layout(mapbox = {
            "center": center,
            "zoom": zoom
        })

        self.fig.update_traces(mode='markers', marker_size=10)
        #print("step 5:", time.perf_counter())
        self.fig.update_layout(mapbox_style="open-street-map")


        return self.fig

    def aggregate_data():
        print()