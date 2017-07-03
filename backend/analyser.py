from data_set import DataSet
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model


class Analyser:

    #
    # dict with filters and category ex: {0: 1, 1: 3}
    # category id
    # dataset object
    @staticmethod
    def analyse(filters_dict, category, dataset):
        matrix, train_vector = Analyser.gen_matrix(filters_dict, category, dataset)
        # print ("Dimensions:\n")
        # print("Matrix: " + str(len(matrix)) +"x" + str(len(matrix[0])))
        # print("Vector: " + str(len(train_vector)) +"x1")
        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets

        # print("### Matrix ####" + str(matrix) + "\n" + "#### train vector ####" + str(train_vector))
        regr.fit(matrix, train_vector)

        # The coefficients
        # print('Coefficients: \n', regr.coef_)
        # The mean squared error
        # print("Mean squared error: %.2f"
        #     % np.mean((regr.predict(matrix) - train_vector) ** 2))
        # Explained variance score: 1 is perfect prediction
        # print('Variance score: %.2f' % regr.score(matrix, train_vector))

        return  regr.coef_


    @staticmethod
    def gen_matrix(filters_dict, category, dataset):
        # print("Category: " + str(category) + " | count: " + str(dataset.categories_count[category]))
        r_matrix = []
        r_vector = []
        for i in range(len(dataset.matrix)):
            row = dataset.matrix[i]
            should_jump = False

            # filtering row
            for k,v in filters_dict.items():
                if dataset.phones_categories[i][k] != v:
                    should_jump = True

            t_value = dataset.get_train_value(i)
            should_jump = should_jump or t_value == None

            if should_jump:
               # print ("Filtering row: " + str(i) + " | for cat: " + str(k) + " | value: " + str(dataset.phones_categories[i][k]) + " | expected: " + str(v))

                continue


            r_row = [0 for k in range(dataset.categories_count[category])]

            r_row[dataset.phones_categories[i][category]] = 1
            r_row.append(1) # constant value

            r_matrix.append(r_row)
            r_vector.append(t_value)

        # print("### r_matrix ###\n" + str(r_matrix))
        # print("### r_vector ###\n" + str(r_vector))
        return (r_matrix, r_vector)

# a = False
a = False

if a:
    ds = DataSet.init_from_file("data.csv", "preco")
    ds.print_config()

    print("matrix[0]: " + str(ds.matrix[0]))
    print("matrix[0][9]: " + str(ds.matrix[0][9]))

    coef = Analyser.analyse({}, 6, ds)


