from dash import dcc, html
import plotly.graph_objects as go
import dash_daq as daq
import jbi100_app.views.colors as clrs

class Histogram(html.Div):
    def __init__(self, name, feature, df):
        self.html_id = "histogram"
        self.df = df
        self.feature = feature

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                html.Tr(
                    id="switch_table",
                    children=
                    [
                        html.Td("Count of local properties owned by local owners"),
                        html.Td(
                            daq.BooleanSwitch(
                                id="local_switch", on=False, color=clrs.marker_1
                            )
                        ),
                        html.Td("Count of all properties owned by local owners"),
                    ]
                ),
                dcc.Graph(id=self.html_id),
            ],
        )

    def update(self, neighbourhood=None, local_switch=""):

        # Get rid of upper margin
        self.fig = go.Figure(layout=go.Layout(margin={"t": 0}))

        # Filter to relevant neighbourhood if selected
        if neighbourhood is not None:

            # Check if we are showing properties in local area or all NYC
            local_switch = "{}".format(local_switch)
            if local_switch == "True":
                if not self.df[self.df.neighbourhood == neighbourhood].empty:
                    host_ids = self.df[
                        self.df.neighbourhood == neighbourhood
                    ].host_id.unique()
                else:
                    host_ids = self.df[
                        self.df.neighbourhood_group == neighbourhood
                    ].host_id.unique()
                filter = self.df[self.df.host_id.isin(host_ids)]
                filter = filter.groupby("host_id")["id"].count().reset_index()
                filter.rename(columns={"id": self.feature}, inplace=True)

            else:
                filter = self.df[
                    (self.df.neighbourhood_group == neighbourhood)
                    | (self.df.neighbourhood == neighbourhood)
                ]
        else:
            filter = self.df

        filter = filter[["host_id", self.feature]].drop_duplicates()

        values = filter[self.feature]

        # Histogram of number of properties owned by local Airbnb hosts
        self.fig.add_trace(
            go.Histogram(
                histfunc="count",
                x=values,
                marker_color=clrs.marker_1,
                hovertemplate="%{y} Airbnb owner(s) own(s) %{x} properties in the selected area.<extra></extra>",
            ),
            
        )
        self.fig.update_xaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)
        self.fig.update_yaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)

        # update axis titles
        self.fig.update_layout(
            xaxis_title="Number of Airbnb properties owned in selected area",
            yaxis_title="Number of Airbnb owners",
            paper_bgcolor=clrs.card_colour,
            plot_bgcolor=clrs.card_colour,
        )

        # If no Airbnb hosts own more than 10 Airbnbs then still fix range so not too small
        if filter[self.feature].max() < 10:
            self.fig.update_layout(xaxis_range=[0, 10])

        return self.fig
