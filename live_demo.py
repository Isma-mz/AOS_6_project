import networkx as nx
import numpy as np
from SBM.Graph import Graph
from SBM.SbmModel import SbmModel
from SBM.SbmGraphGenerator import SbmGraphGenerator
from SBM.Run import RunLgMethod
from SBM.Run import RunEm
from SBM.ResultAnalyzer import ResultAnalyzer
import timeit
import json
import sys
def main():
    model = SbmModel([0.2, 0.2,0.6], [[0.2, 0.05,0.08],
                                      [0.05, 0.30,0.24],
                                    [0.08, 0.24,0.5]], 0)
    n1 = int(sys.argv[1])
    gen = SbmGraphGenerator(model)
    g1= gen.generate_sbmgraph(n1)
    rd1 = RunLgMethod(g1)

    start = timeit.default_timer()
    nc1 = rd1.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG1 = stop - start

    ra1= ResultAnalyzer(model, g1.X, g1.classes, nc1)
    true1,estimated1 = ra1.class_count()
    true1.sort()
    estimated1.sort()
    true1 = np.array(true1)
    estimated1 = np.array(estimated1)
    dif = true1 - estimated1
    dif = np.abs(dif)
    total_dif = np.sum(dif)
    total_dif = total_dif / n1
    print("LG run: True: " + str(true1) + " Estimated: " + str(estimated1) + " time: " + str(timeLG1) + " error rate: "+ str(total_dif))

main()