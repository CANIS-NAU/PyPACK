from mordecai import Geoparser
import pandas as pd
import bs4
import urllib.request
import re

def extract_webpage_locations(web_df):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ Website Information Extracted
    '''
    url_df = web_df[web_df['URLs'] != '[]']

    link_dict = {}

    for link in url_df['URLs']:

        try:
            webpage=str(urllib.request.urlopen(link.strip("[]''")).read())
            soup = bs4.BeautifulSoup(webpage, 'html.parser')
            paragraphs = []
            headers = []

            link_dict[link.strip("[]''")] = {'Headers': [], 'Paragraphs': []}

            for h in soup.find_all(re.compile('^h[1-6]$')):
                headers.append(h.get_text().strip('\n ') + "\n")

            link_dict[link.strip("[]''")]['Headers'] = headers

            for p in soup.find_all('p'):
                paragraphs.append(p.get_text().strip('\n ') + "\n")

            link_dict[link.strip("[]''")]['Paragraphs'] = paragraphs

        except Exception as e:
            print(e)
            continue

    web_df = pd.DataFrame.from_dict(link_dict, orient='index')

    return web_df

def parse_web_data(df, **kwargs):
    '''
    Input: df: Pandas DataFrame
           column_name: Column name to be analyzed

    Output: Pandas DataFrame w/ Website Information Extracted
    '''
    loc_list = {}

    for section in df[kwargs['column_name']]:
        locations = kwargs['geoparser'].geoparse(section)
        if locations:
            for loc in locations:
                try:
                    if(loc['country_predicted'] == "USA"):
                        loc_list[loc['geo']['place_name']] = (loc['geo']['lat'], loc['geo']['lon'])
                except:
                    continue
    return loc_list

def map_web_locations(web_df, column_name="Paragraphs"):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ Website Locations Mapped
    '''
    geo = Geoparser()

    web_df['Para_Locs'] = web_df.apply(parse_web_data, column_name=column_name, geoparser=geo, axis=1)

    return web_df
