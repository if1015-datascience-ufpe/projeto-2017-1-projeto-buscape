


class PU:

    @staticmethod
    def pmat(matrix, namespace=None):
        if namespace is not None:
            print("## Printing matrix(" + namespace + ") ##")
        for r in matrix:
            print(r)

