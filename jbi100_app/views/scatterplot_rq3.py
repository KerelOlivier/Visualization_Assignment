from dash import dcc, html
import jbi100_app.views.colors as clrs


class RQ3(html.Div):
    """
    Class for creating a scatterplot for Research Question 3
    """
    def __init__(self, name, feature_x, feature_y, df):
        """
        @param name: Title of the plot
        @param feature_x: Name of the feature on the x-axis
        @param feature_y: Name of the feature on the y-axis
        @param df: Dataframe
        """
        
        # set the initial variables
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.xf = feature_x
        self.yf = feature_y
        self.x = self.df[self.xf]
        self.y = self.df[self.yf]
        self.x_mean = self.x.mean()
        self.y_mean = self.y.mean()
        
        # set variables for regression line
        self.x_diff = self.x - self.x_mean
        self.y_diff = self.y - self.y_mean
        # b is the slope of the regression line
        self.b = (self.x_diff * self.y_diff).sum() / (self.x_diff**2).sum()
        # a is the intercept of the regression line
        self.a = self.y_mean - self.b * self.x_mean

        # equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def update(self, neighbourhood=None):
        """
        Updates the encoding for the scatterplot.
        There is a distinction between neighbourhood and neighbourhood group.
        
        @param neighbourhood: Name of the neighbourhood to be highlighted
        """

        # initialize marker's size
        size = 10

        # get the relevant data when a neighbourhood is chosen
        if neighbourhood is not None:
            if not self.df[self.df.neighbourhood == neighbourhood].empty:
                variable = "neighbourhood"
                # store data for all the other neighbourhoods
                filter = self.df[self.df.neighbourhood != neighbourhood]
                # store data where the neighbourhood is selected
                filter1 = self.df[self.df.neighbourhood == neighbourhood]
            else:
                size = 20
                # set the variable "neighbourhood_group"
                variable = "neighbourhood_group"
                # counting sums of airbnb and hotels per neighbourhood group
                data = (
                    self.df.groupby("neighbourhood_group")
                    .agg(
                        {
                            "airbnb_counts_per_neighbourhood": "sum",
                            "hotel_counts_per_neighbourhood": "sum",
                        }
                    )
                    .reset_index()
                )
                # store data for all the other neighbourhood groups
                filter = data[data.neighbourhood_group != neighbourhood]
                # store data where the neighbourhood group is selected
                filter1 = data[data.neighbourhood_group == neighbourhood]
        else:
            # by default set variable as neighbourhood
            variable = "neighbourhood"
            filter = self.df

        # set the figure
        self.fig = dict(
            data=[
                dict(
                    x=filter[self.xf],
                    y=filter[self.yf],
                    text=filter[variable],
                    # hovering information
                    hovertext=[
                        f"<b>{n}</b><br><b># Airbnbs:</b> {a}<br><b># hotels:</b> {h}<extra></extra>"
                        for n, a, h in zip(
                            filter[variable], filter[self.xf], filter[self.yf]
                        )
                    ],
                    hovertemplate="%{hovertext}",
                    mode="markers",
                    marker=dict(
                        size=size,
                        color=clrs.marker_off,
                        line=dict(width=1, color="white"),
                    ),
                )
            ],
            # axes settings and general layout
            layout=dict(
                xaxis=dict(
                    title="Number of Airbnbs",
                    fixedrange=True,
                    gridcolor=clrs.line_colour,
                    color=clrs.txt_colour,
                ),
                yaxis=dict(
                    title="Number of hotels",
                    fixedrange=True,
                    gridcolor=clrs.line_colour,
                    color=clrs.txt_colour,
                ),
                hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
                margin=dict(l=100, b=40, t=100, r=100),
                hovermode="closest",
                showlegend=False,
                autosize=True,
                yaxis_zeroline=False,
                xaxis_zeroline=False,
                dragmode="select",
                paper_bgcolor=clrs.card_colour,
                plot_bgcolor=clrs.card_colour,
                titlefont=dict(color=clrs.txt_colour, size=20, family="Arial"),
            ),
        )
        # add the regression line for neighbourhood
        if variable == "neighbourhood":
            # if the variable is neighbourhood, use the precalculated slope and intercept
            self.fig["data"].append(
                dict(
                    x=[self.x.min(), self.x.max()],
                    y=[
                        self.a + self.b * self.x.min(),
                        self.a + self.b * self.x.max(),
                    ],
                    mode="lines",
                    line=dict(color="white", width=1),
                    showlegend=False,
                    hoverinfo="none",
                )
            )
        # recalculate the slope and intercept for neighbourhood groups
        else:
            x_diff = (
                data.airbnb_counts_per_neighbourhood
                - data.airbnb_counts_per_neighbourhood.mean()
            )
            y_diff = (
                data.hotel_counts_per_neighbourhood
                - data.hotel_counts_per_neighbourhood.mean()
            )
            b = (x_diff * y_diff).sum() / (x_diff**2).sum()
            a = (
                data.hotel_counts_per_neighbourhood.mean()
                - b * data.airbnb_counts_per_neighbourhood.mean()
            )
            self.fig["data"].append(
                dict(
                    x=[
                        data.airbnb_counts_per_neighbourhood.min(),
                        data.airbnb_counts_per_neighbourhood.max(),
                    ],
                    y=[
                        a + b * data.airbnb_counts_per_neighbourhood.min(),
                        a + b * data.airbnb_counts_per_neighbourhood.max(),
                    ],
                    mode="lines",
                    line=dict(color="white", width=1),
                    showlegend=False,
                    hoverinfo="none",
                )
            )

        # set green highlighted markers for selected neighbourhood group
        if neighbourhood is not None:
            self.fig["data"].append(
                dict(
                    x=filter1[self.xf],
                    y=filter1[self.yf],
                    text=filter1[variable],
                    hovertext=[
                        f"<b>{n}</b><br><b># Airbnbs:</b> {a}<br><b># hotels:</b> {h}<extra></extra>"
                        for n, a, h in zip(
                            filter1[variable], filter1[self.xf], filter1[self.yf]
                        )
                    ],
                    hovertemplate="%{hovertext}",
                    mode="markers",
                    marker=dict(
                        size=size,
                        color=clrs.marker_3,
                        line=dict(width=1, color="white"),
                    ),
                )
            )
        return self.fig
