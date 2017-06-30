import time

import logging

import sys

from crawler.csv_writer import CSVWriter
from crawler.extractor import Extractor


class BuscapeCrawler(object):
    LIST_PAGE_URL = "http://www.buscape.com.br/celular-e-smartphone?"
    DATA_CLASS = "bui-product__link--outer"
    DATA_GAACTION = "Card de Produto"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    def __init__(self, start_page_number, last_page_number):
        self.__cur_page = start_page_number
        self.__cur_item = 0
        self.__cur_list = None
        self.__last_page = last_page_number
        self.__update_list()
        self.__extractor = Extractor()
        self.__logger = logging.root.getChild(self.__class__.__module__ + "." +
                                              self.__class__.__name__)

    def __get_link(self):
        bs4_obj = self.__cur_list[self.__cur_item]
        return bs4_obj.get("href", "")

    def __update_list(self):
        bs4_obj = Extractor.extract_page_as_bs(self.LIST_PAGE_URL +
                                               "pagina={}".format(self.__cur_page))
        self.__cur_list = bs4_obj.find_all("a",
                                           class_=self.DATA_CLASS,
                                           attrs={"data-gaaction": self.DATA_GAACTION})
        self.__cur_item = 0

    def __next_item(self):
        item = None
        if self.__cur_page <= self.__last_page:
            if self.__cur_item < len(self.__cur_list):
                item = self.__get_link()
                self.__cur_item += 1
            else:
                self.__cur_page += 1
                self.__update_list()
                item = self.__next_item()

        self.__logger.info("Page: {} \ item: {}".format(self.__cur_page, self.__cur_item))
        return item

    def run_crawler(self):
        item_link = self.__next_item()
        final_items = []

        while item_link is not None:
            self.__logger.info("Capturando item do link: {}". format(item_link))
            bs4_obj = self.__extractor.extract_page_as_bs(item_link)
            final_items.append(self.__extractor.extract_obj(bs4_obj))

            item_link = self.__next_item()
            time.sleep(0.5)

        return final_items

    def save_into_csv(self, objs, path):
        csvwriter = CSVWriter(path)
        csvwriter.write_objs(objs)
