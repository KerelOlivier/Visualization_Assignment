from jbi100_app.views.noise_map import NoiseMap
from jbi100_app.views.alarm_map import Map
from dash import dcc, html
import dash_daq as daq


class MapGroup(html.Div):
  def __init__(self, alarm_df) -> None:
    
    self.scatter = Map("alarm map", alarm_df)
    self.noise = NoiseMap("noise map")
    self.html_id = self.scatter.html_id
    super().__init__(
            className="graph_card",
            children=[
                html.H6("Fire alarms", id="map_title"),
                dcc.Graph(id=self.html_id),
            ],
        )

  def update(self, map_mode='scatter', alarm_mode=None, loc_change=False, colours=["blue", "red"], neighbourhood=None):
    if map_mode == 'scatter':
      self.html_id = self.scatter.html_id      
      self.fig = self.scatter.update(mode=alarm_mode, loc_change=loc_change, colours=colours, neighbourhood=neighbourhood)
    else:
      self.html_id = self.noise.html_id
      self.fig = self.noise.update()
    return self.fig