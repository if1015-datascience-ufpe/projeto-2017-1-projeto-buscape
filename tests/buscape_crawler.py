import pprint

import crawler.buscape_crawler

buscape_crawler = crawler.buscape_crawler.BuscapeCrawler(1, 2)
items = buscape_crawler.run_crawler()

pprinter = pprint.PrettyPrinter()
pprinter.pprint(items)
