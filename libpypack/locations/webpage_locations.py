from mordecai import Geoparser
from tqdm import tqdm, tqdm_pandas
import pandas as pd
import bs4
import urllib.request
import re
import os

def extract_webpage_locations(csv_file, output_dir='', sep="\t", column_name="URLs"):
    '''
    Given a CSV file this will parse each row of the column in 'column_name'
    and return the Headers / Paragraphs which is parsed by BeautifulSoup.

    Parameters
    ----------
    csv_file: str

    output_dir: str

    sep: str
            Examples: "\t" (tab)

    column_name: str
            Examples: 'URLs'

    Returns
    -------
    : dataframe
      Pandas DataFrame with associated web information

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
    Given a CSV file this will parse each row of the column in 'column_name'
    and return the Headers / Paragraphs which is parsed by BeautifulSoup.

    Parameters
    ----------
    df: Pandas DataFrame

    column_name: str

    geoparser: Mordecai instance

    Returns
    -------
    : list
      List of parsed locations

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
    Given a DataFrame generated above, this outputs a file named 'scraped_website_data_locs.csv'
    and returns DataFrame with associated information which can be used to generate maps.

    Parameters
    ----------
    web_df: Pandas DataFrame

    sep: str
            The delimeter for outputted CSV data.

    output_dir: str
            Output directory of files generated.

    column_name: str
            The column name to parse for locations.

    port: int
            Port to run location extractor.

    host: str
            The hostname to run location extractor.

    Returns
    -------
    : Pandas DataFrame
      Pandas DataFrame with 'Web_Locs' as a column, which contain parsed website locations.

    '''
    tqdm.pandas()

    geo = Geoparser(es_port=int(port), es_host=host)

    web_df['Web_Locs'] = web_df.progress_apply(parse_web_data, column_name=column_name, geoparser=geo, axis=1)
    web_df.to_csv(os.path.join(output_dir, 'scraped_website_data_locs.csv'), sep=sep, index=False)
    return web_df
