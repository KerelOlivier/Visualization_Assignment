import pandas as pd
import geovoronoi as gv
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys
import matplotlib.pyplot as pt
from shapely.geometry import MultiPolygon, Polygon, Point
from shapely.ops import unary_union
from  shapely.wkt import loads
import matplotlib.pyplot as plt
import geopandas as gpd

df = pd.read_csv("data/noise.csv").drop(columns='geometry')
gdf = gpd.read_file("data/voronoi.geojson")
gdf = gdf.to_crs({'proj':'cea'})
gdf['area'] = gdf.area/10**6
areas = pd.DataFrame(gdf[['id', 'area']]).astype({'id': 'int64'})
res = pd.merge(df, areas, on='id')
res['density'] = res['incident_cnt']/res['area']
print(res)
print(res['density'].median())
res.to_csv("data/noise.csv")
exit()

# read cleaned data
df = pd.read_csv("data/noise.csv")
df = df.set_index('id')

#create new york shape boundary
dfn = gpd.read_file('data/nyc_neighbourhoods.geojson')
ps = list(dfn['geometry'])
shape = gpd.GeoSeries(unary_union(ps))[0]

#create voronoi
coords = df[['longitude', 'latitude']].to_numpy()
region_polys, region_pts = gv.voronoi_regions_from_coords(coords, shape)

series = gpd.GeoSeries(region_polys)
gdf = gpd.GeoDataFrame(geometry=series)
print(gdf)
print(type(region_pts), type)
s = pd.DataFrame.from_dict(region_pts, orient='index')
# mapping = gpd.GeoDataFrame()
# print(gdf)
# print(mapping)
mapping = gpd.GeoDataFrame(s)
gdf = gdf.join(mapping)
gdf = gdf.rename(columns={0: 'id'})
gdf = gdf.set_index('id')
print(gdf)
print(df.head())


series.plot()
plt.show()
print(gdf)
with open('data/voronoi.geojson' , 'w') as file:
    file.write(gdf.to_json())
# gdf.to_file("data/voronoi.geojson", driver="GeoJSON")  



exit()

# read data
df = pd.read_csv("data/noise_complaints_residential_070622_070922.csv")

# remove NaN
df = df.dropna()

# group by incident adress and sum incidents
locations = df[['incident_address','longitude','latitude']].groupby(['incident_address']).mean()
incident_cnt= df[['incident_address','longitude','latitude']].groupby(['incident_address']).count()
incident_cnt['incident_cnt']  = incident_cnt['longitude']
incident_cnt = incident_cnt.drop(columns=['longitude','latitude'] )
df = locations.join(incident_cnt)
print("[0]:", len(df))

#aggregate points that are close together
coords = df.groupby([df.longitude.round(3), df.latitude.round(3)])[['longitude', 'latitude']].transform('mean')
incident_cnt = df.groupby([df.longitude.round(3), df.latitude.round(3)])['incident_cnt'].transform('sum')
df = coords.join(incident_cnt)
df = df.groupby([df.longitude.round(3), df.latitude.round(3)]).first()
print("[1]:", len(df))

# Fix the id
df["id"] = list(range(len(df))) 
df = df.set_index('id')
print("[2]:", len(df))

#Add geom1etry column
df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
print("[3]:", len(df))

#create new york shape boundary
dfn = gpd.read_file('data/nyc_neighbourhoods.geojson')
ps = list(dfn['geometry'])
shape = gpd.GeoSeries(unary_union(ps))[0]
print("[4]:", len(df))

# Remove all points outside the shape
df['within'] = df['geometry'].map(lambda x: x.within(shape))
print(df)
df = df.loc[df['within'] == True]
print("[5]:", len(df))


df.to_csv("data/noise.csv")

exit()


df = pd.read_csv("data/noise_complaints_residential_070622_070922.csv")

df = df.dropna()
locations = df[['incident_address','longitude','latitude']].groupby(['incident_address']).mean()
counts = df[['incident_address','longitude','latitude']].groupby(['incident_address']).count()
counts['incident_count'] = counts['latitude']
counts = counts.drop(columns=['longitude','latitude'] )
# counts.drop('latitude')
res = locations.join(counts)
# print(locations)
# print(counts)
# print(res)
# print(res.sort_values('incident_count'))
# print(res['latitude'].min())
# print(res['latitude'].max())
# print(res['longitude'].min())
# print(res['longitude'].max())


# Create shape polygon using box
long_min = res['longitude'].min()-0.025
long_max = res['longitude'].max()+0.025
lat_min = res['latitude'].min()-0.025
lat_max = res['latitude'].max()+0.025
points = [
    (long_min, lat_max),
    (long_max, lat_max),
    (long_max, lat_min),
    (long_min, lat_min),
]

shape = Polygon(points)

# Create shape polygon using neighbourhoods
df = gpd.read_file('data/nyc_neighbourhoods.geojson')
ps = list(df['geometry'])
boundary = gpd.GeoSeries(unary_union(ps))
# boundary.plot(color='red')
# plt.show()
# boundary = boundary.simplify(0.0025)
# boundary.plot(color='red')
# plt.show()
# print(type(boundary[0]))

# Remove points outside shape
points = gpd.GeoDataFrame(res, geometry=gpd.points_from_xy(res.longitude, res.latitude))[['geometry']]
print("before:", len(points))
points['witihin'] = points['geometry'].map(lambda x: x.within(boundary))
print(points)
# points = points[points.geometry.within(boundary)]
print("after:", len(points))

# print(f'#QgsGeometry.fromPolygon([[QgsPoint({long_min}, {lat_max}), QgsPoint({long_max}, {lat_max}), QgsPoint({long_max}, {lat_min}), QgsPoint({long_min}, {lat_min})]])')
# print(shape)
coords = res[['longitude', 'latitude']].to_numpy()
print(len(coords))
coords2 = res[['longitude', 'latitude']].groupby([(res.longitude/2).round(3), (res.latitude/2).round(3)]).transform('mean').to_numpy()
print(len(coords2))
region_polys, region_pts = gv.voronoi_regions_from_coords(coords2, boundary[0])


# Convert voronoi to geojson
print(region_polys)
series = gpd.GeoSeries(region_polys)
print(gpd.GeoDataFrame(geometry=series))
series.plot()
plt.show()
# fig, ax = subplot_for_map()
# plot_voronoi_polys(ax, region_polys=region_polys)
# plt.show()




# shape = MultiPolygon(polygons = ps)



#QgsGeometry.fromPolygon([[QgsPoint(x1,y1),QgsPoint(x2,y2), QgsPoint(x3,y3)]])
# boundary = QgsGeometry.fromPolygonXY([[QgsPointXY(-74.27589258036565, 40.93666770708578), QgsPointXY(-73.67576734196948, 40.93666770708578), QgsPointXY(-73.67576734196948, 40.47531261674751), QgsPointXY(-74.27589258036565, 40.47531261674751)]])
# layer = QgsVectorLayer('Polygon', 'poly' , "memory")
# poly = QgsFeature()
# poly.setGeometry(boundary)
# pr = layer.dataProvider() 
# pr.addFeatures([poly])
# (True, [<qgis._core.QgsFeature object at 0x7f52441e9870>])
# QgsProject.instance().addMapLayer(layer)
# <QgsVectorLayer: 'poly' (memory)>