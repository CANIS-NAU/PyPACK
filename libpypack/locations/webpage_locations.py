from mordecai import Geoparser
import pandas as pd
import bs4
import urllib.request
import re
import os

def extract_webpage_locations(csv_file, output_dir='', sep="\t", column_name="URLs"):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ Website Information Extracted

    '''
    web_df = pd.read_csv(csv_file, sep=sep)
    url_df = web_df[web_df[column_name] != '[]']

    link_dict = {}

    for link in url_df[column_name]:

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
    web_df.to_csv(os.path.join(output_dir, 'scraped_website_data.csv'), sep=sep, index=False)
    return web_df

def parse_web_data(df, column_name, geoparser):
    '''
    Input: df: Pandas DataFrame
           column_name: Column name to be analyzed

    Output: Pandas DataFrame w/ Website Information Extracted
    '''
    loc_list = {}

    for section in df[column_name]:
        locations = geoparser.geoparse(str(section))
        if locations:
            for loc in locations:
                try:
                    if(loc['country_predicted'] == "USA"):
                        loc_list[loc['geo']['place_name']] = (loc['geo']['lat'], loc['geo']['lon'])
                except:
                    continue
    return loc_list

def map_web_locations(web_df, sep="\t", output_dir='', column_name="Paragraphs", port=9200, host='127.0.0.1'):
    '''
    Input: Pandas DataFrame

    Output: Pandas DataFrame w/ Website Locations Mapped
    '''
    geo = Geoparser(es_port=int(port), es_host=host)

    web_df['Web_Locs'] = web_df.apply(parse_web_data, column_name=column_name, geoparser=geo, axis=1)
    web_df.to_csv(os.path.join(output_dir, 'scraped_website_data_locs.csv'), sep=sep, index=False)
    return web_df
