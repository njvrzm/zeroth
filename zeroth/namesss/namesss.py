import requests
from typing import List, Union
from bs4 import BeautifulSoup

postUrl = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'
session = requests.Session()

def getNamesForYear(year:int, count:int = 1000, meta:str = None) -> List[dict]:
    """ Downloads the Social Security top N names for the given year.

    :param year: A value from 1880 to (currently) 2016.
    :param count: How many names to return; max is 1000.
    :param meta: if 'n', include the number of children given each name;
                 if 'p', include the percentage. if None or absent,
                 include neither.
    :return: A list of dictionaries
    """
    if meta and meta not in ('n', 'p'):
        raise ValueError("meta, if given, must be 'n' or 'p' or None.")

    request = {'year': str(year), 'top': str(count), 'number': meta or ''}

    response = session.post(postUrl, data=request)
    soup = BeautifulSoup(response.text, features='html5lib')
    # Our target table is the only one with a caption
    table = soup.find('caption').find_parent('table')
    header = table.find('tr')
    columns = [th.text for th in header.findAll('th')]
    # The last row is a non-data footer
    rows = header.findNextSiblings('tr')[:-1]
    def getData(row):
        return dict(zip(columns, [td.text for td in row.findAll('td')]))

    return list(map(transform, map(getData, rows)))


def transform(data:dict) -> dict:
    def transformValue(key:str, value:str) -> Union[str, int, float]:
        if key.startswith('Number') or key == 'Rank':
            return int(value.replace(',', ''))
        if key.startswith('Percent'):
            return float(value.rstrip('%'))
        return value
    return {k:transformValue(k, v) for k, v in data.items()}

