import pytest
from libpypack.locations import map_locations
from libpypack.locations.start_docker import run_docker
from mordecai import Geoparser
import test_data
import os

def test_geoparser():
    run_docker()
    geo = Geoparser()
    result = geo.geoparse("I traveled from Oxford to Ottawa.")
    assert result[0]['geo']['lat'] == '51.75222' and result[0]['geo']['lon'] == '-1.25596'
