from dash import dcc, html
import plotly.graph_objects as go
import dash_daq as daq
import jbi100_app.views.colors as clrs


class HorizontalBar(html.Div):
    def __init__(self, name, feature, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.df["host_id"] = self.df["host_id"].apply(str)
        self.feature = feature

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                html.Div(
                    dcc.Graph(id=self.html_id),
                    style={"overflowY": "scroll", "height": 500},
                ),
            ],
        )

    def update(self, neighbourhood=None):

        # Get rid of upper margin
        self.fig = go.Figure(layout=go.Layout(margin={"t": 0}))

        # Number of properties owned by landlord
        total = self.df.groupby("host_id")["id"].count().reset_index()
        total.rename(columns={"id": "total_number"}, inplace=True)
        filter = total.head(20)

        if neighbourhood is not None:
            if not self.df[self.df.neighbourhood == neighbourhood].empty:
                filter = self.df[self.df.neighbourhood == neighbourhood]
            else:
                filter = self.df[self.df.neighbourhood_group == neighbourhood]

            filter = filter.groupby("host_id")["id"].count().reset_index()
            filter.rename(columns={"id": "local_number"}, inplace=True)

            filter = filter.merge(total, on="host_id", how="left")

            filter["diff_number"] = filter["total_number"] - filter["local_number"]

            filter.sort_values("total_number", inplace=True, ascending=False)

            self.fig.add_trace(
                go.Bar(
                    y=filter["host_id"],
                    x=filter["local_number"],
                    name="local",
                    orientation="h",
                    customdata=filter["total_number"],
                    hovertemplate="%{y} owns %{x} properties in the local area, and %{customdata} in total in NY.<extra></extra>",
                )
            )
            filter = filter[filter.diff_number > 0]
            self.fig.add_trace(
                go.Bar(
                    y=filter["host_id"],
                    x=filter["diff_number"],
                    name="other areas",
                    orientation="h",
                    customdata=filter[["local_number", "total_number"]],
                    hovertemplate="%{y} owns %{customdata[0]} properties in the local area, and %{customdata[1]} in total in NY.<extra></extra>",
                )
            )

            self.fig.update_layout(barmode="stack")

        else:
            filter = total

            filter.sort_values("total_number", inplace=True, ascending=False)

            values = filter["total_number"]

            self.fig.add_trace(
                go.Bar(
                    x=values,
                    y=filter["host_id"],
                    orientation="h",
                    hovertemplate="%{y} owns %{x} properties in total in NY.<extra></extra>",
                )
            )

        length = len(filter)

        self.fig.update_yaxes(tickmode="linear")

        # update axis titles
        self.fig.update_layout(
            xaxis_title="Number of properties",
            yaxis_title="Airbnb owners",
            paper_bgcolor=clrs.card_colour,
            plot_bgcolor=clrs.card_colour,
            yaxis=dict(autorange="reversed"),
            bargap=0.8,
            height=max(500, length * 30),
        )

        self.fig.update_xaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)
        self.fig.update_yaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)
        self.fig.update_traces(marker_color=clrs.marker_5)

        return self.fig
