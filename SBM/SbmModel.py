import numpy as np

class SbmModel:
  def __init__(self, rates, probas, directed):
    self.rates = np.array(rates, dtype= float)
    self.probas = np.array(probas, dtype= float)
    self.directed = directed
