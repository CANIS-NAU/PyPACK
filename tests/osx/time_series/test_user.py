import pytest
import libpypack.examples.location_files as loc_file
from libpypack.time_series.user_info import get_user_df
import pandas as pd

def test_map_generator():
    tweet_df = pd.read_csv(loc_file.__path__[0] + '/sample_parsed_locs.csv')
    user_df = get_user_df(tweet_df, 12759492)
    assert len(user_df) == 3
