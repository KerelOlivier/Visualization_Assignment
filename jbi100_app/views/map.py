from dash import dcc, html
import plotly.graph_objects as go


class Map(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
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

        if neighbourhood is not None:
            filter = self.df[(self.df.neighbourhood_group == neighbourhood) | (self.df.neighbourhood == neighbourhood)]
        else:
            filter = self.df

        marker_colours = dict(zip([True,False], colours))
        if mode == 0:
            # fire alarm node         
            filter["colour"] = filter["has_fire_alarm"].replace(to_replace=marker_colours)
        elif mode == 1:
            # co monitor mode
            filter["colour"] = filter["has_co_monitor"].replace(to_replace=marker_colours)
        #elif mode == 2:
            # noise complaints mode
        

        self.fig.add_trace(go.Scattermapbox(
                            lat=filter.latitude,
                            lon=filter.longitude,
                            marker_color=filter.colour,
                            hovertext=filter.id
        ))

        self.fig.update_layout(mapbox_style="open-street-map")
        self.fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

        self.fig.update_traces(mode='markers', marker_size=10)

        return self.fig
