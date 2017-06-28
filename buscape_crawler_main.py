from crawler.buscape_crawler import BuscapeCrawler
import os

if __name__ == '__main__':
    crawler = BuscapeCrawler(1, 2)
    crawler.save_into_csv(
        path=os.path.join(os.getcwd(), "output", "data.csv"),
        objs=crawler.run_crawler())
