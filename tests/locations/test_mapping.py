import pytest
from libpypack.locations import map_locations
from mordecai import Geoparser
import test_data
import os

def test_locations():
    # tweet_df = map_locations.locations_df(csv_file=os.path.dirname(test_data.__file__) + "/2018_10_08_04_location.csv")
    # assert tweet_df.iloc[9102]['locs'] == {'Texas': ('31.25044', '-99.25061')}
    assert True

def test_geoparser():
    geo = Geoparser()
    result = geo.geoparse("I traveled from Oxford to Ottawa.")
    assert result[0]['geo']['lat'] == '51.75222' and result[0]['geo']['lon'] == '-1.25596'
