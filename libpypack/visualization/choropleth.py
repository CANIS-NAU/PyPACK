import numpy as np
import libpypack.examples.states_21basic as state_file
import matplotlib.pyplot as plt
import geopandas
from shapely.geometry import Point, Polygon
import os

def choropleth_map(loc_gdf, shp_path=state_file.__path__[0] + "/states.shp"):

    xdf = geopandas.read_file(shp_path)

    xdf['Count'] = 0

    count_df = loc_gdf['Location Extracted'].value_counts()

    country = dict(zip(count_df.index.tolist(), zip(loc_gdf['Location Extracted'].value_counts(), loc_gdf['geometry'])))

    def parse_poly(df):
        count = 0
        for x, val in country.items():
            if(val[1].within(df)):
                count += int(val[0])
        return count


    xdf['Count'] = list(map(lambda x: parse_poly(x), xdf['geometry']))

    return xdf

def plot_map(xdf, output_dir=''):

    fig, ax = plt.subplots(1, 1)

    # xdf.plot(column='Count', ax=ax, legend=True)
    choropleth_plot = xdf.plot(column='Count',
               ax=ax,
               legend=True,
               legend_kwds={'label': "Number of Locations",
                               'orientation': "horizontal"})

    plt.savefig(os.path.join(output_dir, "choropleth_map.png"))

    return choropleth_plot
