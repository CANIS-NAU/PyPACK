from libpypack.locations import map_locations
from libpypack.visualization import generate_maps
from libpypack.visualization import heatmap
from libpypack.visualization import choropleth
import pandas as pd
import glob, os

def get_user_df(df, user_value, user_column='User_ID', time_column='Timestamp'):
    return df[df[user_column] == user_value].sort_values(by=time_column).reset_index(drop=True)

def get_min_max_date(aggregate_df, time_column='Timestamp'):
    min_date = min(time_df[time_column])
    max_date = max(time_df[time_column])
    return min_date, max_date

def create_user_gif(user_df, filepath, gif_filename, png_basename='map'):
    import imageio

    images = []
    filenames = []

    for i in range(0, len(user_df)):
        gdf, loc_gdf = generate_maps.generate_overlay_gdf(user_df[user_df.index == i])
        ax, plot, graph = generate_maps.plot_gdf(gdf, loc_gdf)
        plot.savefig(png_basename + '_{}.png'.format(i))

    for file in glob.glob(filepath + "*.png"):
        images.append(imageio.imread(file))

    if(gif_filename[-4:] != ".gif"):
        imageio.mimsave(gif_filename + '.gif', images)
    else:
        imageio.mimsave(gif_filename, images)

    return 1
