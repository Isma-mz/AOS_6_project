from SBM.SbmModel import SbmModel
from abc import ABC
import numpy as np


class Run(ABC):
    def __init__(self, graph):
        self.graph = graph

    def compute(self, params):
        return self.method

    def method(self):
        pass


class RunLgMethod(Run):
    def __init__(self, graph):
        Run.__init__(self, graph)


    def compute(self, params):
        rd = RunComputeDegree(self.graph)
        n = self.graph.n
        q = params["class_numbers"]
        degrees = np.array(rd.compute({}))
        scaled_degrees = []
        for j in range(0, n):
            scaled_degrees.append(degrees[j])
            scaled_degrees[j]["degree"] = scaled_degrees[j]["degree"] / (n - 1)
        scaled_degrees.sort(key= lambda x : x["degree"])

        consecutive_dif = []
        for i in range(0, n - 1):
            consecutive_dif.append(
                {"i+1_sorted": i+1, "i_sorted": i , "i+1": scaled_degrees[i + 1]["index"], "i": scaled_degrees[i]["index"], "gap": scaled_degrees[i + 1]["degree"] - scaled_degrees[i]["degree"]})
        consecutive_dif.sort(key = lambda x : x["gap"])
        q_higher = []
        for c in range(q-1 , 0, -1):
            q_higher.append(consecutive_dif[n -1 - c])
        q_higher.sort(key= lambda x : x["i_sorted"])
        cluster_intervals = []
        cluster_intervals.append([0,q_higher[0]["i_sorted"]])
        for i in range(0,len(q_higher) - 1):
            cluster_intervals.append([q_higher[i]["i+1_sorted"],q_higher[i+1]["i_sorted"]])
        cluster_intervals.append([q_higher[q-2]["i+1_sorted"],n])
        nodes_classes =  []
        for i in range(0,n):
            index_sorted = i
            node_classe = np.zeros(q)
            for k in range(0,len(cluster_intervals)):
                interval = cluster_intervals[k]
                if index_sorted >= interval[0] and index_sorted <= interval[1]:
                    node_classe[k] = 1
                    nodes_classes.append({"index": i,"classes": node_classe})


        return nodes_classes


class RunComputeDegree(Run):
    def __init__(self, graph):
        Run.__init__(self, graph)

    def compute(self, params):
        A = self.graph.X
        degree = []
        rowsum = self.graph.X.sum(axis=1)

        for j in range(0, len(A)):
            degree.append({"index": j, "degree": rowsum[j]})
        return degree



class RunEm(Run):
    def __init__(self,graph):
        Run.__init__(self,graph)
    def compute(self,params):
        directedx = self.graph.X
        n = self.graph.n
        K = params["q"]
        classLabel = []
        for i in range(0,n):
            classe = -1
            for k in range(0,len(self.graph.classes[i]["classes"])):
                if self.graph.classes[i]["classes"][k] == 1:
                    classe = k
            classLabel.append(classe)
        # initialisation
        epsilon = 0.2
        tau = np.ones((n, K)) * epsilon
        for i in range(n):
            tau[i][classLabel[i]] = 1 - 2 * epsilon

        # M-step
        alpha_EM = np.mean(tau, axis=0)
        pi_EM = np.zeros((K, K))
        for k in range(K):
            for l in range(K):
                numerator = 0
                denominator = 0
                for i in range(n):
                    for j in range(n):
                        numerator = numerator + tau[i][k] * tau[j][l] * directedx[i][j]
                        denominator = denominator + tau[i][k] * tau[j][l]
                pi_EM[k][l] = numerator / denominator

        # E-step
        new_tau = np.zeros((n, K))
        for i in range(n):
            for k in range(K):
                product = 1
                for j in range(n):
                    for l in range(K):
                        product = product * (
                                    pi_EM[k][l] ** directedx[i][j] * (1 - pi_EM[k][l]) ** (1 - directedx[i][j])) ** \
                                  tau[j][l]
                new_tau[i][k] = alpha_EM[k] * product
        # scale new_tau to make each row sum == 1
        sum_col = new_tau.sum(axis=1)
        for i in range(n):
            new_tau[i, :] = new_tau[i, :] * 1 / sum_col[i]
        new_tau[new_tau < 1e-20] = 0
        tau = new_tau

        old_pi_EM = np.zeros((K, K))
        old_alpha_EM = np.zeros(K)
        pi_EM_difference = 0
        alpha_EM_difference = 0
        real_pi_difference = 0
        real_alpha_difference = 0

        for it in range(20):
            # M-step
            old_alpha_EM = alpha_EM
            alpha_EM = np.mean(tau, axis=0)
            old_pi_EM = pi_EM
            for k in range(K):
                for l in range(K):
                    numerator = 0
                    denominator = 0
                    for i in range(n):
                        for j in range(n):
                            numerator = numerator + tau[i][k] * tau[j][l] * directedx[i][j]
                            denominator = denominator + tau[i][k] * tau[j][l]
                    pi_EM[k][l] = numerator / denominator

            # compute difference
            pi_EM_difference = np.abs(pi_EM - old_pi_EM).sum()
            alpha_EM_difference = np.abs(alpha_EM - old_alpha_EM).sum()


            # E-step
            new_tau = np.zeros((n, K))
            for i in range(n):
                for k in range(K):
                    product = 1
                    for j in range(n):
                        for l in range(K):
                            product = product * (
                                        pi_EM[k][l] ** directedx[i][j] * (1 - pi_EM[k][l]) ** (1 - directedx[i][j])) ** \
                                      tau[j][l]
                    new_tau[i][k] = alpha_EM[k] * product
            # scale new_tau to make each row sum == 1
            sum_col = new_tau.sum(axis=1)
            for i in range(n):
                new_tau[i, :] = new_tau[i, :] * 1 / sum_col[i]
            new_tau[new_tau < 1e-20] = 0
            tau = new_tau
            return alpha_EM, pi_EM