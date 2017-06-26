import pprint

import requests
from bs4 import BeautifulSoup

import crawler.extractor

URL = "http://www.buscape.com.br/smartphone-samsung-galaxy-j7-prime-sm-g610m"
response = requests.get(URL)

extractor = crawler.extractor.Extractor()
bs = BeautifulSoup(response.text, "html.parser")
raw_obj = extractor.extract_obj(bs)

pprinter = pprint.PrettyPrinter()
pprinter.pprint(raw_obj)
