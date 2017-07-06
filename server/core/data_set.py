import csv
import json
from print_utils import PU

class DataSet:
    def __init__(self, train_category):
        self.headers_map = {} # header str -> index
        self.matrix =[] # the csv loaded in memory
        self.categories = [] # for each header, a map from str -> category num
        self.phones_categories = [] # for each phone (row) and each header, returns which category the cell phone belongs to
        self.categories_count = [] # exclusive number of categories for each header
        self.train_category = train_category
        self.tc = -1000 # train category col
        self.train_col = []

    def filter_none(self, row):
        row = [v if v != '' else None for v in row]
        return row

    def populate_headers(self, row):
        c = 0
        for i in range(len(row)):
            if row[i] == self.train_category:
                self.tc = i
            else:
                self.headers_map[row[i]] = c
                c += 1


    def init_maps(self):
        self.phones_categories = [{} for r in self.matrix]
        self.categories = [{} for h in self.headers_map]

    def count_categories(self, col):
        self.categories[col] = {}
        count = 0
        for i in range(len(self.matrix)):
            val = self.matrix[i][col]
            if val == None:
                self.phones_categories[i][col] = -1
                continue

            if val not in self.categories[col]:
                self.categories[col][val] = count
                count += 1
            #print ("i: " + str(i) + " | col: " + str(col) + " | mark: " + str(mark[val]) )
            self.phones_categories[i][col] = self.categories[col][val]

        return count

    def read(self, file_path):
        with open(file_path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            count = 0
            first = True
            for row in spamreader:
                row = self.filter_none(row)
                if first:
                    self.populate_headers(row)
                    first = False
                    continue
                self.train_col.append(row[self.tc])
                del row[self.tc]

                self.matrix.append(row)
                count += 1
                if count >= 15111111:
                    # break
                    pass

    def print_config(self):
        # print("train category: " + str(self.train_category) + " | id: " + str(self.tc))
        # print("headers: " + str(self.headers_map))
        # print("matrix length: " + str(len(self.matrix)))
        # print("headers length: " + str(len(self.headers_map)))
        # print("matrix col size: " + str(len(self.matrix[0])))
        # print("Categories count: " + str(self.categories_count))
        PU.pmat(self.phones_categories, "Phones Categories")

        # # print("Matrix:" + str(self.matrix))

    # access train vector for row index (ri)
    def get_train_value(self, ri):
        if self.train_col[ri] is None:
            return None
        return float(self.train_col[ri])

    @staticmethod
    def init_from_file(csv_file, train_category):
        ds = DataSet(train_category)
        ds.read(csv_file)
        ds.init_maps()
        for i in range(len(ds.headers_map)):
            ds.categories_count.append(ds.count_categories(i))
#        # print("phones categories: " + str(ds.phones_categories))

        return ds




# ds = DataSet.init_from_file("data.csv", "preco")
# ds.print_config()

