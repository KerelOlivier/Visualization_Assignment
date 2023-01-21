from dash import dcc, html
import jbi100_app.views.colors as clrs


class RQ3(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.xf = feature_x
        self.yf = feature_y
        self.x = self.df[self.xf]
        self.y = self.df[self.yf]
        self.x_mean = self.x.mean()
        self.y_mean = self.y.mean()
        self.x_diff = self.x - self.x_mean
        self.y_diff = self.y - self.y_mean
        self.b = (self.x_diff * self.y_diff).sum() / (self.x_diff**2).sum()
        self.a = self.y_mean - self.b * self.x_mean

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[html.H6(name), dcc.Graph(id=self.html_id)],
        )

    def update(self, neighbourhood=None):

        # Choose size
        size = 10

        # get the relevant data
        if neighbourhood is not None:
            if not self.df[self.df.neighbourhood == neighbourhood].empty:
                variable = "neighbourhood"
                filter = self.df[self.df.neighbourhood != neighbourhood]
                filter1 = self.df[self.df.neighbourhood == neighbourhood]
            else:
                size = 20
                variable = "neighbourhood_group"
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
                filter = data[data.neighbourhood_group != neighbourhood]
                filter1 = data[data.neighbourhood_group == neighbourhood]
        else:
            variable = "neighbourhood"
            filter = self.df

        self.fig = dict(
            data=[
                dict(
                    x=filter[self.xf],
                    y=filter[self.yf],
                    text=filter[variable],
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
                        color=clrs.marker_1,
                        line=dict(width=0.5, color="white"),
                    ),
                )
            ],
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
                    gridcolor="#424242",
                    color="#f1f1f1",
                ),
                # title=dict(
                #    text="Number of <br> Airbnbs vs Hotels <br> per neighbourhood",
                #    x=0.5,
                # ),
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
        if variable == "neighbourhood":
            self.fig["data"].append(
                dict(
                    x=[self.x.min(), self.x.max()],
                    y=[
                        self.a + self.b * self.x.min(),
                        self.a + self.b * self.x.max(),
                    ],
                    mode="lines",
                    line=dict(color="rgb(200, 200, 200)", width=0.5),
                    showlegend=False,
                    hoverinfo="none",
                )
            )
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
                    line=dict(color="rgb(200, 200, 200)", width=0.5),
                    showlegend=False,
                    hoverinfo="none",
                )
            )
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
                        color="green",
                        line=dict(width=0.5, color="white"),
                    ),
                )
            )
        return self.fig
