import os
import time

import logging

from crawler.csv_writer import CSVWriter
from crawler.extractor import Extractor, HTMLFormationNotImplemented


class BuscapeCrawler(object):
    LIST_PAGE_URL = "http://www.buscape.com.br/celular-e-smartphone?"
    DATA_CLASS = "bui-product__link--outer"
    DATA_GAACTION = "Card de Produto"
    logging.basicConfig(filename=os.path.join(os.getcwd(), "crawler.log"),
                        level=logging.INFO)

    def __init__(self, start_page_number, last_page_number):
        self.__cur_page = start_page_number
        self.__cur_item = -1
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
        self.__cur_item = -1

    def __next_item(self):
        item = None
        if self.__cur_page <= self.__last_page:
            if self.__cur_item + 1 < len(self.__cur_list):
                self.__cur_item += 1
                item = self.__get_link()
                self.__logger.info("Item #{}: {}".format(self.__cur_item, item))
            else:
                self.__cur_page += 1
                self.__logger.info("Page number: {}.".format(self.__cur_page))
                self.__update_list()
                item = self.__next_item()

        return item

    def __get_price(self):
        bs4_obj = self.__cur_list[self.__cur_item]
        try:
            return float(bs4_obj.get("data-preco", -1))
        except ValueError:
            self.__logger.warning("Não foi possível extrair preço do item {}.".format(
                self.__get_link()
            ))
            return ""

    def run_crawler(self):
        logging.info("Running crawler from page 1 to {}".format(self.__last_page))
        final_items = []

        while self.__cur_page <= self.__last_page:
            item_link = self.__next_item()
            if item_link:
                self.__logger.info("Capturando item do link: {}". format(item_link))
                bs4_obj = self.__extractor.extract_page_as_bs(item_link)
                try:
                    new_item = self.__extractor.extract_obj(bs4_obj)
                    new_item["url"] = item_link
                    new_item["preco"] = self.__get_price()
                    final_items.append(new_item)
                except HTMLFormationNotImplemented:
                    self.__logger.warning("Formato de HTML da link {} não suportado.".format(
                        item_link
                    ))

            time.sleep(1)

        return final_items

    def save_into_csv(self, objs, path):
        csvwriter = CSVWriter(path)
        csvwriter.write_objs(objs)
