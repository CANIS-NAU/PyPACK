import pytest
from libpypack.fcc_wrapper import fcc_api
import json

def test_block():
    results = fcc_api.block_query(lat=35.1983, lon=-111.6513)
    json_r = json.loads(results)
    assert json_r['Block']['FIPS'] == '040050015003339'
