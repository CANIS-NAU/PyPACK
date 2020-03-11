import pytest
from libpypack.locations import fcc_api
import json

def block_test():
    results = fcc_api.block_query(lat=35.1983, lon=-111.6513)
    json_r = json.loads(results)
    assert json_r['Block']['FIPS'] == '040050015003339'
