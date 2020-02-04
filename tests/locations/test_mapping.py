import pytest
from libpypack.locations import map_locations
import test_data
import os

def test_locations():
    tweet_df = map_locations.locations_df(csv_file=os.path.dirname(test_data.__file__) + "/2018_10_08_04_location.csv")
    assert tweet_df.iloc[9102]['locs'] == {'Texas': ('31.25044', '-99.25061')}
