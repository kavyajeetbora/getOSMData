from ipyleaflet import Map, DrawControl, GeoJSON, WidgetControl, basemaps
from ipywidgets import HTML
import shapely
import osmnx as ox
import json

class RoadMap(Map):
    def __init__(self, center):
        super().__init__(center = center, zoom=10, scroll_wheel_zoom=True)
        self.dc = DrawControl()
        self.dc.on_draw(self.handle_draw)
        self.add_control(self.dc)

    def update_html(self, feature, **kwargs):

        html1 = HTML('''
            Hover over a road
        ''')
        html1.layout.margin = "0px 20px 20px 0px"
        control1 = WidgetControl(widget=html1, position='bottomright')
        m.controls = tuple(list(m.controls)[:-1]) ## Remove the last control before adding new control to the map
        self.add_control(control = control1)

        html1.value = '''
            <p>Street Type: {}</p>
            <p>Length: {:.2f}</p>
        '''.format(feature['properties']['highway'], feature['properties']['length'])

    def handle_draw(self, target, action, geo_json):
        geometry = geo_json['geometry']
        if geometry['type'] == "Polygon":
            print("Valid Geometry")
            area = shapely.geometry.Polygon(geometry['coordinates'][0])

            try:
                network = ox.graph.graph_from_polygon(area)
                # ox.plot_graph(network)

                nodes, roads = ox.graph_to_gdfs(network)
                roads = roads.reset_index()

                if roads.shape[0]>0:

                    roads_json = json.loads(roads.to_json(drop_id=True))
                    geojson_layer = GeoJSON(data = roads_json, name='Roads', hover_style={'fillColor': 'red', 'fillOpacity': 0.5})
                    geojson_layer.on_hover(self.update_html)
                    self.add_layer(layer = geojson_layer)
                else:
                    print("Area too small or no roads founds within the specified area")

            except Exception as e:
                print(e)
        else:
            print("The application doesnot work with point/line features")


if __name__ == "__main__":
    m = RoadMap(center=(28.7, 77.1))
    