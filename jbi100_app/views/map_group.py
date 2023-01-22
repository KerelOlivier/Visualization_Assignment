from jbi100_app.views.noise_map import NoiseMap
from jbi100_app.views.alarm_map import Map
import jbi100_app.views.colors as clrs

from dash import dcc, html
import dash_daq as daq


class MapGroup(html.Div):
  def __init__(self, df) -> None:
    
    self.scatter = Map("alarm map", df)
    self.noise = NoiseMap("noise map", df)
    self.html_id = self.scatter.html_id
    super().__init__(
            className="graph_card",
            children=[
                html.H6("Fire alarms", id="map_title"),
                dcc.Graph(id=self.html_id),
            ],
        )

  def update(self, map_mode='fire', alarm_mode=None, loc_change=False, colours=[clrs.marker_2, clrs.marker_4], neighbourhood=None):
    # Determine which map to display
    if map_mode == 'fire' or map_mode == 'co':
      self.html_id = self.scatter.html_id      
      self.fig = self.scatter.update(mode=map_mode, loc_change=loc_change, colours=colours, neighbourhood=neighbourhood)
    else:
      self.html_id = self.noise.html_id
      self.fig = self.noise.update(loc_change=loc_change, neighbourhood=neighbourhood)
    return self.fig