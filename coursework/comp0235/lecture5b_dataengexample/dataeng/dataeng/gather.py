import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

bl_prefix = "https://bl.iro.bl.uk"

def parse_index_entry():
    parser = ArgumentParser(description="Process the BL index file for the relevant files to download")

    parser.add_argument('file_path')

    arguments = parser.parse_args()
    with open(arguments.file_path) as source:
        for url in parse_index(source):
            cover_page = requests.get(url).text
            data_source = parse_cover_page(cover_page)
            print(data_source)

def parse_index(source):
    soup=BeautifulSoup(source,'html.parser')
    for element in soup.select('h4.search-result-title a'):
        yield bl_prefix+element['href']


def parse_cover_page(source):
    soup=BeautifulSoup(source,'html.parser')
    results= soup.select('tr.file_set a[data-context-href]')
    return bl_prefix+results[0]['href']
