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
def main():
    model = SbmModel([0.1, 0.3,0.6], [[0.2, 0.05,0.08],
                                      [0.05, 0.30,0.24],
                                    [0.08, 0.24,0.5]], 0)
    n1,n2, n3, n4, n5,n6 = 50,100,200,300,500,700
    gen = SbmGraphGenerator(model)
    g1,g2,g3 = gen.generate_sbmgraph(n1),gen.generate_sbmgraph(n2),gen.generate_sbmgraph(n3)
    g4,g5,g6 = gen.generate_sbmgraph(n4),gen.generate_sbmgraph(n5),gen.generate_sbmgraph(n6)
    rd1, rd2, rd3 = RunLgMethod(g1), RunLgMethod(g2), RunLgMethod(g3)
    rd4, rd5, rd6 = RunLgMethod(g4), RunLgMethod(g5), RunLgMethod(g6)

    start = timeit.default_timer()
    nc1 = rd1.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG1 = stop - start

    start = timeit.default_timer()
    nc2 = rd2.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG2 = stop - start

    start = timeit.default_timer()
    nc3 = rd3.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG3 = stop - start

    start = timeit.default_timer()
    nc4 = rd4.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG4 = stop - start

    start = timeit.default_timer()
    nc5 = rd5.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG5 = stop - start

    start = timeit.default_timer()
    nc6 = rd6.compute({"class_numbers": 3})
    stop = timeit.default_timer()
    timeLG6 = stop - start

    ra1, ra2, ra3 = ResultAnalyzer(model, g1.X, g1.classes, nc1), ResultAnalyzer(model, g2.X, g2.classes, nc2), ResultAnalyzer(model, g3.X, g3.classes, nc3)
    ra4, ra5, ra6 = ResultAnalyzer(model, g4.X, g4.classes, nc4), ResultAnalyzer(model, g5.X, g5.classes, nc5), ResultAnalyzer(model, g6.X, g6.classes, nc6)
    true1,estimated1 = ra1.class_count()
    true2, estimated2 = ra2.class_count()
    true3, estimated3 = ra3.class_count()
    true4,estimated4 = ra4.class_count()
    true5, estimated5 = ra5.class_count()
    true6, estimated6 = ra6.class_count()

    print("LG run1: True: " + str(true1) + " Estimated: " + str(estimated1) + " time: " + str(timeLG1))
    print("LG run2: True: " + str(true2) + " Estimated: " + str(estimated2) + " time: " + str(timeLG2))
    print("LG run3: True: " + str(true3) + " Estimated: " + str(estimated3) + " time: " + str(timeLG3))
    print("LG run4: True: " + str(true4) + " Estimated: " + str(estimated4) + " time: " + str(timeLG4))
    print("LG run5: True: " + str(true5) + " Estimated: " + str(estimated5) + " time: " + str(timeLG5))
    print("LG run6: True: " + str(true6) + " Estimated: " + str(estimated6) + " time: " + str(timeLG6))

    #EM
    rem1 = RunEm(g1)
    rem2 = RunEm(g2)
    rem3 = RunEm(g3)
    rem4 = RunEm(g4)
    rem5 = RunEm(g5)
    rem6 = RunEm(g6)
    start = timeit.default_timer()
    alpha_estimation1, pi_estimation1 = rem1.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM1 = stop - start

    start = timeit.default_timer()
    alpha_estimation2, pi_estimation2 = rem2.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM2 = stop - start

    start = timeit.default_timer()
    alpha_estimation3, pi_estimation3 = rem3.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM3 = stop - start

    start = timeit.default_timer()
    alpha_estimation4, pi_estimation4 = rem4.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM4 = stop - start

    start = timeit.default_timer()
    alpha_estimation5, pi_estimation5 = rem5.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM5 = stop - start

    start = timeit.default_timer()
    alpha_estimation6, pi_estimation6 = rem6.compute({"q": 3})
    stop = timeit.default_timer()
    timeEM6 = stop - start

    print("EM run1: True: " + str(true1) + " Estimated: " + str(alpha_estimation1) + " time: " + str(timeEM1))
    print("EM run2: True: " + str(true2) + " Estimated: " + str(alpha_estimation2) + " time: " + str(timeEM2))
    print("EM run3: True: " + str(true3) + " Estimated: " + str(alpha_estimation3) + " time: " + str(timeEM3))
    print("EM run4: True: " + str(true4) + " Estimated: " + str(alpha_estimation4) + " time: " + str(timeEM4))
    print("EM run5: True: " + str(true5) + " Estimated: " + str(alpha_estimation5) + " time: " + str(timeEM5))
    print("EM run6: True: " + str(true6) + " Estimated: " + str(alpha_estimation6) + " time: " + str(timeEM6))
    run = {
        "proportions": model.rates,
        "probas": model.probas,
        "true proportions": [true1,true2,true3,true4,true5,true6],
        "LG estimated proportions": [estimated1, estimated2,estimated3,estimated4,estimated5,estimated6],
        "LG run time":  [timeLG1, timeLG2,timeLG3, timeLG4, timeLG5, timeLG6],
        "EM estimated proportions": [alpha_estimation1, alpha_estimation2,alpha_estimation3,alpha_estimation4, alpha_estimation4,alpha_estimation5,alpha_estimation6],
        "EM run time": [timeEM1, timeEM2, timeEM3, timeEM4, timeEM5, timeEM6]
    }
    json_string = json.dumps(run)
    with open('json_data.json', 'w') as outfile:
        json.dump(json_string, outfile)

    # Using a JSON string
    with open('json_data2.json', 'w') as outfile:
        outfile.write(json_string)
main()