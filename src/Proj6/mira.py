# Mira implementation
import util
PRINT = True

class MiraClassifier:
  """
  Mira classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "mira"
    self.automaticTuning = False # Look at this flag to decide whether to choose C automatically ** use this in your train method **
    self.C = 0.001
    self.max_iterations = max_iterations
    self.weights = {}
    for label in legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use
  
  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        Cgrid = [0.001, 0.002, 0.003, 0.004, 0.005]
    else:
        Cgrid = [self.C]
        
    return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
    """
    See the project description for details how to update weight vectors for each label in training step. 
    
    Use the provided self.weights[label] datastructure so that 
    the classify method works correctly. Also, recall that a
    datum is a counter from features to values for those features
    (and thus represents a vector a values).

    This method needs to return the best parameter found in the list of parameters Cgrid
    (i.e. the parameter that yeilds best accuracy for the validation dataset)
    """
    maxC = Cgrid[0]
    maxCorrect = -1
    maxWeights = []
    
    for C in Cgrid:
        self.C = C
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter()
        for iteration in range(self.max_iterations):
          print "Starting iteration ", iteration, " with C ", C, "..."
          for i in range(len(trainingData)):
              guess = self.classify( [trainingData[i]]) [0]
              if trainingLabels[i] != guess:
                  factor = ((self.weights[guess].__sub__(self.weights[trainingLabels[i]]))*trainingData[i]+1)
                  if ((trainingData[i]*trainingData[i])*2) != 0:
                      factor /= ((trainingData[i]*trainingData[i])*2)
                  t = min(self.C, factor)
                  toDiff = util.Counter(trainingData[i].copy()).multiplyAll(t)
                  self.weights[guess] = self.weights[guess].__sub__(toDiff)
                  self.weights[trainingLabels[i]] = self.weights[trainingLabels[i]].__add__(toDiff)
                  
        guesses = self.classify(validationData)
        rightSoFar = 0
        for i in range(len(guesses)):
            if guesses[i] == validationLabels[i]:
                rightSoFar += 1
                    
        if rightSoFar > maxCorrect:
            maxCorrect = rightSoFar
            maxC = self.C
            maxWeights = self.weights.copy()
                
            
    self.C = maxC
    self.weights = maxWeights
    return maxC

  def classify(self, data ):
    """
    Classifies each datum as the label that most closely matches the prototype vector
    for that label.  See the project description for details.
    
    Recall that a datum is a util.counter... 
    """
    guesses = []
    for datum in data:
      vectors = util.Counter()
      for l in self.legalLabels:
        vectors[l] = self.weights[l] * datum
      guesses.append(vectors.argMax())
    return guesses

  
  def findHighOddsFeatures(self, class1, class2):
    """
    Returns:
    featuresClass1 -- the 100 largest weight features for class1 (as a list)
    featuresClass2 -- the 100 largest weight features for class2
    featuresOdds -- the 100 best features for difference in feature values
                     w_class1 - w_class2

    """

    featuresClass1 = []
    featuresClass2 = []
    featuresOdds = []
    
    weights1 = util.Counter(self.weights[class1].copy())
    weights2 = util.Counter(self.weights[class2].copy())
    
    for i in range (0, 100):
        max1 = weights1.argMax()
        max2 = weights2.argMax()
        featuresClass1.append(max1)
        featuresClass2.append(max2)
        weights1.pop(max1)
        weights2.pop(max2)
        
    weights1 = util.Counter(self.weights[class1].copy())
    weights2 = util.Counter(self.weights[class2].copy())
    
    for i in range (0, 100):
        weightKeys = weights1.keys()
        if len(weightKeys) > 0:
            maxDiff = 0
            maxFeat = weights1[weightKeys[0]]
            for feature in weightKeys:
                if (weights1[feature] - weights2[feature]) > maxDiff:
                    maxFeat = feature
                    maxDiff = weights1[feature] - weights2[feature]
            weights1.pop(maxFeat)
            featuresOdds.append(maxFeat)

    return featuresClass1,featuresClass2,featuresOdds


