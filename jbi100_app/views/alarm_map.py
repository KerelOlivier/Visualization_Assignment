from dash import dcc, html
import plotly.graph_objects as go
import time
import jbi100_app.views.colors as clrs

class Map(html.Div):
    def __init__(self, name, df):

        # set the initial variables
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.zoom = 1
        self.nbh = None
        self.colours = [clrs.marker_2, clrs.marker_3]
        self.mode = 0

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6("Fire alarms"),
                dcc.Graph(id=self.html_id)
            ],
        )
        


    def update(self, mode=None, loc_change=False, colours=[clrs.marker_2, clrs.marker_3], neighbourhood=None):
        """
        Updates the scattermap for fire alarms and co monitors

        :param mode: the mode of the map (fire or co)
        :param loc_change: whether the neighbourhood parameter should be taken into account
        :param colours: the colours to use for the markers
        :param neighbourhood: the neighbourhood we want to look at (None if all of NYC)
        """
        colours=[clrs.marker_2, clrs.marker_3]
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
                    (self.df.neighbourhood_group == self.nbh ) |
                    (self.df.neighbourhood == self.nbh)
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

        # get correct colours
        marker_colours = dict(zip([True,False], colours))

        if self.mode == 'fire':
            # fire alarm node         
            filter["colour"] = filter["has_fire_alarm"].replace(to_replace=marker_colours)
            hover_txt = filter.has_fire_alarm.astype(str)
        elif self.mode == 'co':
            # co monitor mode
            filter["colour"] = filter["has_co_monitor"].replace(to_replace=marker_colours)
            hover_txt = filter.has_co_monitor.astype(str)

        # now create the scattermap
        self.fig.add_trace(go.Scattermapbox(
                            lat=filter.latitude,
                            lon=filter.longitude,
                            marker_color=filter.colour,
                            marker_allowoverlap=False,
                            hoverinfo="text",
                            hovertext=hover_txt,

        ))

        # set the layout correctly with zoom and center
        self.fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

        self.fig.update_layout(mapbox = {
            "center": center,
            "zoom": zoom
        })

        self.fig.update_traces(mode='markers', marker_size=10)
        self.fig.update_layout(mapbox_style="carto-darkmatter")


        return self.fig
