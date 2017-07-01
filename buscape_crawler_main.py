from crawler.buscape_crawler import BuscapeCrawler
import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("final_page", type=int)
args = parser.parse_args()

if __name__ == '__main__':
    crawler = BuscapeCrawler(1, args.final_page)
    crawler.save_into_csv(
        path=os.path.join(os.getcwd(), "output", "data.csv"),
        objs=crawler.run_crawler())
