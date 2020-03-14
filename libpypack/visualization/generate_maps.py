from mordecai import Geoparser
from geopandas.tools import sjoin
from shapely.geometry import Point, Polygon

import geopandas
import pandas as pd
import libpypack.examples.states_21basic as state_file
import matplotlib.pyplot as plt

def create_new_df(tweet_df, column_name='locs'):
    loc_name = []
    lats = []
    lons = []

    for loc in tweet_df[column_name]:
        try:
            for location, coord in loc.items():
                loc_name.append(location)
                lats.append(float(coord[0]))
                lons.append(float(coord[1]))
        except:
            continue

    location_df = pd.DataFrame(
        {'Location Extracted': loc_name,
         'Latitude': lats,
         'Longitude': lons})

    return location_df

def generate_overlay_gdf(tweet_df, filename=state_file.__path__[0] + "/states.shp", column_name='locs'):
    location_df = create_new_df(tweet_df, column_name)
    loc_gdf = geopandas.GeoDataFrame(
        location_df, geometry=geopandas.points_from_xy(location_df.Longitude, location_df.Latitude))

    gdf = geopandas.read_file(filename)
    return gdf

def plot_gdf(gdf):
    # Plot correctly
    fig, ax = plt.subplots(figsize = (75, 75))
    ax.set_aspect('equal')
    basemap = gdf.plot(ax=ax, edgecolor='black')
    return ax, gdf.plot(ax=ax, marker='o', color='orange', markersize=35);

def lat_lon_to_points(lat_lon_list):
    point_list = []
    for x in lat_lon_list:
        point_list.append(Point(x))

    return point_list

def points_in_shp(points_list, shapefile_gpd):

    pnts = geopandas.GeoDataFrame(geometry=points_list, index=range(0, len(points_list)))
    pointInPolys = sjoin(pnts, shapefile_gpd, how='left')
    grouped = pointInPolys.groupby('index_right', as_index=False)

    return pointInPolys, grouped

def get_loc_gdf(tweet_df, column_name='locs'):
    gdf = create_new_df(tweet_df, column_name=column_name)
    loc_gdf = geopandas.GeoDataFrame(gdf, geometry=geopandas.points_from_xy(gdf.Longitude, gdf.Latitude))
    return loc_gdf
