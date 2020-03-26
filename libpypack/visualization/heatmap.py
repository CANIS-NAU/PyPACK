import folium
import os
from folium.plugins import HeatMap


def heatmap(loc_gdf, column="Location Extracted", heat_value=None, normalize_data=False, output_name='heatmap.html', output_dir=''):
    locations = loc_gdf[column].value_counts().values
    max_amount = float(locations.max())

    try:
        locations = loc_gdf['Location Extracted'].value_counts().values
        normalized = (locations-locations.min())/(locations.max()-locations.min())

        hmap = folium.Map(zoom_start=7)

        hm_wides = HeatMap( list(zip(loc_gdf.Latitude.values, loc_gdf.Longitude.values, normalized)),
                           min_opacity=0.2,
                           radius=17, blur=15,
                           max_zoom=1,
                         )

        hmap.add_child(hm_wides)
        hmap.save(os.path.join(output_dir, output_name))

        return hmap

    except ValueError:

        max_amount = float(locations.max())

        hmap = folium.Map(zoom_start=7)
        print(list(zip(loc_gdf.Latitude.values, loc_gdf.Longitude.values, locations)))
        hm_wides = HeatMap( list(zip(loc_gdf.Latitude.values, loc_gdf.Longitude.values)),
                           min_opacity=0.2,
                           max_val=max_amount,
                           radius=17, blur=15,
                           max_zoom=1,
                         )

        hmap.add_child(hm_wides)
        hmap.save(os.path.join(output_dir, output_name))

        return hmap

    except Exception as e:
        assert e
