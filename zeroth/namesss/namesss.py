import requests
from bs4 import BeautifulSoup
session = requests.Session()

soupen = lambda response:BeautifulSoup(response.text, 'html5lib')
baseUrl = 'https://www.ssa.gov/OACT/babynames/index.html'
postUrl = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'

def getNamesForYear(year:int, count:int = 1000, meta:str = None):
    """ Downloads the Social Security top N names for the given year.

    :param year: A value from 1880 to (currently) 2016.
    :param count: How many names to return; max is 1000.
    :param meta: if 'number', include the number of children given each
        name; if 'percent', include the percentage.
    """
    request = {'year': year, 'top': count, 'number': meta or ''}

    soup = soupen(session.post(postUrl, data = request))
    # Our target table is the only one with a caption
    table = soup.find('caption').find_parent('table')
    header = table.find('tr')
    columns = [th.text for th in header.findAll('th')]

    data = []
    for tr in header.findNextSiblings('tr')[:-1]:
        data.append(dict(zip(columns, [td.text for td in tr.findAll('td')])))
    return data



