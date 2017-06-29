import re
import requests
from bs4 import BeautifulSoup


class Extractor(object):
    TABLE_CLS = "product-specs"
    TABLE_ROW_CLS = "product-specs__spec display"
    PRICE_CLS = "extra_params"
    PRICE_ID = "PriceProduct"
    FEATURES_NAME = [
            "marca",
            "linha",
            "modelo",
            "chips",
            "câmera traseira",
            "câmera frontal",
            "tamanho da tela",
            "resolução",
            "velocidade do processador",
            "memória interna",
            "memória ram"
        ]

    @staticmethod
    def __match_re(regex_str, group_name, value):
        match_obj = re.match(regex_str, value)
        if match_obj:
            return match_obj.group(group_name)
        else:
            raise RuntimeError("No match object for str `{}` with regex `{}`".format(
                value, regex_str))

    @staticmethod
    def __normalize_chip_value(value):
        return Extractor.__match_re("(?P<chip>\w+) chip", "chip", value.lower())

    @staticmethod
    def __normalize_back_camera(value):
        return float(Extractor.__match_re(
            "(?P<camera>\d+([\.,]\d+)?) megapixels",
            "camera", value.lower()))

    @staticmethod
    def __normalize_frontal_camera(value):
        return float(Extractor.__match_re(
            "(?P<camera>\d+([\.,]\d+)?) megapixels frontal",
            "camera", value.lower()))

    @staticmethod
    def __normalize_screen_size(value):
        return float(Extractor.__match_re(
            "(?P<size>\d+([\.,]\d+)?)( polegadas)?",
            "size", value.lower()))

    @staticmethod
    def __normalize_resolution(value):
        return Extractor.__match_re(
            "(?P<resolution>\d+ x \d+) pixels",
            "resolution", value.lower())

    @staticmethod
    def __normalize_proccessor(value):
        return float(Extractor.__match_re(
            "(?P<proc>\d+([\.,]\d+)?)\ ?ghz",
            "proc", value.lower()))

    @staticmethod
    def __normalize_internal_memory(value):
        return float(Extractor.__match_re(
            "(?P<mem>\d+([\.,]\d+)?)\ ?gb",
            "mem", value.lower()))
    
    @staticmethod
    def __normalize_ram_memory(value):
        return float(Extractor.__match_re(
            "(?P<mem>\d+([\.,]\d+)?)",
            "mem", value.lower()))

    @staticmethod
    def __normalize_value(key, value):
        key = key.lower()
        if key == "chips":
            return Extractor.__normalize_chip_value(value)
        elif key == "câmera traseira":
            return Extractor.__normalize_back_camera(value)
        elif key == "câmera frontal":
            return Extractor.__normalize_frontal_camera(value)
        elif key == "tamanho da tela":
            return Extractor.__normalize_screen_size(value)
        elif key == "resolução":
            return Extractor.__normalize_resolution(value)
        elif key == "velocidade do processador":
            return Extractor.__normalize_proccessor(value)
        elif key == "memória interna":
            return Extractor.__normalize_internal_memory(value)
        elif key == "memória ram":
            return Extractor.__normalize_ram_memory(value)
        else:
            return value

    @staticmethod
    def extract_page_as_bs(url):
        request_page = requests.get(url)
        return BeautifulSoup(request_page.text, "html.parser")

    @classmethod
    def __extract_price(cls, soup_obj):
        price_tag = soup_obj.find("input", class_=cls.PRICE_CLS, id=cls.PRICE_ID)
        return float(price_tag.get("value", -1))

    @classmethod
    def extract_obj(cls, soup_obj):
        table = soup_obj.find("table", class_=cls.TABLE_CLS)
        t_row = table.tbody.find_all("tr", class_=cls.TABLE_ROW_CLS)
        final_obj = {}

        for row in t_row:
            data = row.find_all("td")
            key = str(data[0].string)
            value = str(data[1].string)
            if key.lower() in cls.FEATURES_NAME:
                final_obj[key] = cls.__normalize_value(key, value)

        final_obj["preco"] = cls.__extract_price(soup_obj)

        return final_obj
