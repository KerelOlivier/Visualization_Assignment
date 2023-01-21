from dash import dcc, html
import plotly.graph_objects as go
import dash_daq as daq


class HorizontalBar(html.Div):
    def __init__(self, name, feature, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature = feature

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id),
            ],
        )

    def update(self, neighbourhood=None):

        # Get rid of upper margin
        self.fig = go.Figure(layout=go.Layout(margin={"t": 0}))

        filter = self.df.head(100)

        values = filter["host_listings_neighbourhood_count"]

        self.fig.add_trace(go.Bar(x=values, y=filter["host_name"], orientation="h"))
        # self.fig.update_xaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        # self.fig.update_yaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")

        # highlight points with selection other graph
        # if selected_data is None:
        #     selected_index = self.df.index  # show all
        # else:
        #     selected_index = [  # show only selected indices
        #         x.get('pointIndex', None)
        #         for x in selected_data['points']
        #     ]

        # update axis titles
        self.fig.update_layout(
            xaxis_title="Number",
            yaxis_title="Names",
            paper_bgcolor="#212121",
            plot_bgcolor="#212121",
        )

        return self.fig
