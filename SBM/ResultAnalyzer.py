import numpy as np



class ResultAnalyzer:
    def __init__(self, sbm_model, X, true_classes, estimated_classes):
        self.sbm_model = sbm_model
        self.true_classes = true_classes
        self.estimated_classes =estimated_classes

    def class_count(self):
        q = len(self.sbm_model.rates)
        estimated_count = np.zeros(q)
        true_count =  np.zeros(q)
        for i in range(0, len(self.true_classes)):
            true_classes_vector = self.true_classes[i]["classes"]
            estimated_classes_vector = self.estimated_classes[i]["classes"]
            for k in range(0, len(true_classes_vector)):
                if true_classes_vector[k] == 1:
                    true_count[k] = true_count[k] + 1
                if estimated_classes_vector[k] == 1:
                    estimated_count[k] = estimated_count[k] + 1
        return true_count, estimated_count
