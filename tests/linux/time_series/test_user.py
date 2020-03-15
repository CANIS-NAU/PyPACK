import pytest
import libpypack.examples.location_files as loc_file
import libpypack.time_series.user_info as ts
from libpypack.locations import map_locations
import pandas as pd

def test_map_generator():
    tweet_df = pd.read_csv(loc_file.__path__[0] + '/sample_parsed_locs.csv')
    user_df = ts.get_user_df(tweet_df, 12759492)
    assert len(user_df) == 3
