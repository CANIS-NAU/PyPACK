import requests
import json

def area_query(lat, lon, format='json'):
    """
    Name: Block API

    From: https://geo.fcc.gov/api/census/
    Why: Get census block, county, state, and market area information based on latitude/longitude input.
    Parameters
    ----------
    Latitude: float / str
              [-90 90] in decimal or DMS (degrees:minutes:seconds)
              Examples: 38.26 or 38:15:36N

    Longitude: float / str
               [-180 180] in decimal or DMS (degrees:minutes:seconds)
               Examples: -77.51 or 77:30:36W

    format: str
            Examples: 'json' / 'jsonp' / 'xml'


    Returns
    -------
    : County FIPS, BoundingBox, State FIPS
      Format type response
    """
    url = "https://geo.fcc.gov/api/census/block/find?latitude={}&longitude={}&showall=true&format={}".format(float(lat), float(lon), str(format))
    r = requests.get(url)
    return r.text

def block_query(lat, lon, censusYear='2019', format='json', showall=False):
    """
    Name: Block API

    From: https://geo.fcc.gov/api/census/
    Why: Get census block, county, and state FIPS based on latitude/longitude input.
    Parameters
    ----------
    Latitude: float / str
              [-90 90] in decimal or DMS (degrees:minutes:seconds)
              Examples: 38.26 or 38:15:36N

    Longitude: float / str
               [-180 180] in decimal or DMS (degrees:minutes:seconds)
               Examples: -77.51 or 77:30:36W

    censusYear: str
                Returns results based on census year.
                Valid values: 2019 (default)

    format: str
            Examples: 'json' / 'jsonp' / 'xml'

    showall: boolean
             If the coordinate lies on the boundary
             of multiple geographies, for a complete list use
             showall=true.

    Returns
    -------
    : County FIPS, BoundingBox, State FIPS
      Format type response
    """

    url = "https://geo.fcc.gov/api/census/block/find?latitude={}&longitude={}&censusYear={}&showall={}&format={}".format(int(lat), int(lon), censusYear, str(showall), str(format))
    r = requests.get(url)
    return r.text
