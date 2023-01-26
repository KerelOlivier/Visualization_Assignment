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

    def update(self, neighbourhood=None, prop_cnt = -1):

        # Get rid of upper margin
        self.fig = go.Figure(layout=go.Layout(margin={"t": 0}))

        # Number of properties owned by landlord in all NY
        total = self.df.groupby("host_id")["id"].count().reset_index()
        total.rename(columns={"id": "total_number"}, inplace=True)      

        # If specific neighbourhood selected then filter to this
        if neighbourhood is not None:
            if not self.df[self.df.neighbourhood == neighbourhood].empty:
                filter = self.df[self.df.neighbourhood == neighbourhood]
            else:
                filter = self.df[self.df.neighbourhood_group == neighbourhood]

            filter = filter.groupby("host_id")["id"].count().reset_index()
            filter.rename(columns={"id": "local_number"}, inplace=True)

            filter = filter.merge(total, on="host_id", how="left")

            # If certain count is selected in other chart then filter to this
            if prop_cnt > 0:
                filter = filter[filter['total_number'] == prop_cnt]

            # Get number of properties in rest of city
            filter["diff_number"] = filter["total_number"] - filter["local_number"]

            filter.sort_values("total_number", inplace=True, ascending=False)

            # create a trace for the properties in the currently selected area
            self.fig.add_trace(
                go.Bar(
                    y=filter["host_id"],
                    x=filter["local_number"],
                    name="local",
                    orientation="h",
                    customdata=filter["total_number"],
                    hovertemplate="%{y} owns %{x} properties in the local area, and %{customdata} in total in NY.<extra></extra>",
                    marker=dict(color=clrs.marker_1),
                )
            )

            # create a trace for the properties in different areas
            diff_areas = filter[filter.diff_number > 0]
            self.fig.add_trace(
                go.Bar(
                    y=diff_areas["host_id"],
                    x=diff_areas["diff_number"],
                    name="other areas",
                    orientation="h",
                    customdata=diff_areas[["local_number", "total_number"]],
                    hovertemplate="%{y} owns %{customdata[0]} properties in the local area, and %{customdata[1]} in total in NY.<extra></extra>",
                    marker=dict(color=clrs.marker_5),
                )
            )

            self.fig.update_layout(barmode="stack")
            #Update legend font color
            self.fig.update_layout(legend=dict(font=dict(color=clrs.txt_colour)))

        else:
            
            # Plot all Airbnb hosts if no neighbourhood selected
            filter = total

            # If certain count is selected in other chart then filter to this
            if prop_cnt > 0:
                filter = filter[filter['total_number'] == prop_cnt]

            filter.sort_values("total_number", inplace=True, ascending=False)

            values = filter["total_number"]

            self.fig.add_trace(
                go.Bar(
                    x=values,
                    y=filter["host_id"],
                    orientation="h",
                    hovertemplate="%{y} owns %{x} properties in total in NY.<extra></extra>",
                    marker=dict(color=clrs.marker_1),
                )
            )

        length = len(filter)

        # Show all Airbnb host IDs
        self.fig.update_yaxes(tickmode="linear")

        # update axis titles
        self.fig.update_layout(
            xaxis_title="Number of properties",
            yaxis_title="Airbnb owners",
            paper_bgcolor=clrs.card_colour,
            plot_bgcolor=clrs.card_colour,
            yaxis=dict(autorange="reversed"),
            bargap=0.7,
            height=max(500, length*30),
        )
        
        self.fig.update_xaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)
        self.fig.update_yaxes(fixedrange=True, gridcolor=clrs.line_colour, color=clrs.txt_colour)

        return self.fig



