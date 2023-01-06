from dash import dcc, html
import plotly.graph_objects as go


class Histogram(html.Div):
    def __init__(self, name, feature, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature = feature

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, neighbourhood=None):
        self.fig = go.Figure()

        if neighbourhood is not None:
            filter = self.df[(self.df.neighbourhood_group == neighbourhood) | (self.df.neighbourhood == neighbourhood)]
        else:
            filter = self.df

        filter = filter[['host_id', self.feature]].drop_duplicates()

        values = filter[self.feature]

        self.fig.add_trace(go.Histogram(
            histfunc="count",
            x=values
        ))
        self.fig.update_xaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")
        self.fig.update_yaxes(fixedrange=True, gridcolor="#424242", color="#f1f1f1")

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
            xaxis_title=self.feature,
            yaxis_title='Count',
            paper_bgcolor="#212121",
            plot_bgcolor="#212121",
        )

        return self.fig
