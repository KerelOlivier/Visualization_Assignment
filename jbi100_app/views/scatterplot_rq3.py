from dash import dcc, html

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
        self.b = (self.x_diff * self.y_diff).sum() / (self.x_diff ** 2).sum()
        self.a = self.y_mean - self.b * self.x_mean
        
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )
        
    def update(self, hoverData):
        self.fig = dict(
            data=[
                dict(
                    x=self.x,
                    y=self.y,
                    text=self.df["neighbourhood_group"],
                    hovertext=[
                        f"<b>{n}</b><br><b># Airbnbs:</b> {a}<br><b># hotels:</b> {h}<extra></extra>"
                        for n, a, h in zip(
                            self.df["neighbourhood_group"], self.x, self.y
                        )
                    ],
                    hovertemplate="%{hovertext}",
                    mode="markers",
                    marker=dict(
                        size=15,
                        color=["rgb(200, 200, 200)"] * len(self.df),
                        line=dict(width=0.5, color="white"),
                    ),
                )
            ],
            layout=dict(
                xaxis=dict(
                    title="Number of Airbnbs",
                    fixedrange=True,
                    gridcolor="#424242",
                    color="#f1f1f1",
                ),
                yaxis=dict(
                    title="Number of hotels",
                    fixedrange=True,
                    gridcolor="#424242",
                    color="#f1f1f1",
                ),
                title=dict(
                    text="Number of <br> Airbnbs vs Hotels <br> Per neighbourhood group",
                    x=0.5,
                ),
                hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
                margin=dict(l=100, b=40, t=100, r=100),
                hovermode="closest",
                showlegend=False,
                autosize=True,
                yaxis_zeroline=False,
                xaxis_zeroline=False,
                dragmode="select",
                paper_bgcolor="#212121",
                plot_bgcolor="#212121",
                titlefont=dict(color="#f1f1f1", size=20, family="Arial"),
            ),
        )
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
        
        if hoverData is not None:
            selected_point = hoverData["points"][0]["pointNumber"]
            colors = [
                "rgb(87, 245, 66)"
                if i == selected_point
                else "rgb(100, 100, 100)"
                for i in range(len(self.df))
            ]
            self.fig["data"][0]["marker"]["color"] = colors
        return self.fig
