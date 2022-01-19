import numpy as np
from SBM.Graph import Graph


class SbmGraphGenerator:
    def __init__(self, sbm_model):
        self.sbm_model = sbm_model

    def generate_sbmgraph(self, n):
        rates = self.sbm_model.rates
        probas = self.sbm_model.probas
        q = len(rates)
        nodes_classes = []
        X = np.zeros((n, n))
        for i in range(0, n):
            nodes_classes.append({"index": i, "classes": np.random.multinomial(1, rates)})
        for i in range(0, n):
            for j in range(0, n):
                if self.sbm_model.directed == 0:
                    if j > i:
                        i_c = np.where(nodes_classes[i]["classes"] == 1)[0][0]
                        j_c = np.where(nodes_classes[j]["classes"] == 1)[0][0]
                        X[i][j] = X[j][i] = np.random.binomial(1, probas[i_c][j_c])
                else:
                    i_c = np.where(nodes_classes[i]["classes"] == 1)[0][0]
                    j_c = np.where(nodes_classes[j]["classes"] == 1)[0][0]
                    X[i][j] = np.random.binomial(1, probas[i_c][j_c])
        g = Graph(n, X, self.sbm_model.directed, nodes_classes)
        return g
