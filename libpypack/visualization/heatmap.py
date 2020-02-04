import folium
import os
from folium.plugins import HeatMap


def heatmap(loc_gdf, column="Location Extracted", heat_value = None, normalize_data=True, output_name='heatmap.html', output_dir=''):

    locations = loc_gdf[column].value_counts().values

    max_amount = float(locations.max())

    if(normalize_data):
        locations = loc_gdf['Location Extracted'].value_counts().values

        normalized = (locations-locations.min())/(locations.max()-locations.min())

        hmap = folium.Map(zoom_start=7)

        hm_wide = HeatMap( list(zip(loc_gdf.Latitude.values, loc_gdf.Longitude.values, normalized)),
                           min_opacity=0.2,
                           radius=17, blur=15,
                           max_zoom=1,
                         )

        hmap.add_child(hm_wide)
        hmap.save(os.path.join(output_dir, 'heatmap.html'))

        return hmap

    else:

        max_amount = float(locations.max())

        hmaps = folium.Map(zoom_start=7)

        hm_wides = HeatMap( list(zip(loc_gdf.Latitude.values, loc_gdf.Longitude.values, locations)),
                           min_opacity=0.2,
                           max_val=max_amount,
                           radius=17, blur=15,
                           max_zoom=1,
                         )

        hmaps.add_child(hm_wide)
        hmap.save(os.path.join(output_dir, 'heatmap.html'))

        return hmap
