import csv


class CSVWriter(object):
    def __init__(self, path):
        self.__path = path

    @staticmethod
    def __get_fieldnames(objs):
        set_of_fields = set()
        for obj in objs:
            set_of_fields.update(obj.keys())
        return set_of_fields

    def write_objs(self, objs):
        with open(self.__path, "w", encoding="utf-8") as f:
            fieldnames = CSVWriter.__get_fieldnames(objs)
            writer = csv.DictWriter(f, fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(objs)
