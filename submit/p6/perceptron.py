# Perceptron implementation
import util

class PerceptronClassifier:
  """
  Perceptron classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__( self, legalLabels, max_iterations):
    self.legalLabels = legalLabels
    self.type = "perceptron"
    self.max_iterations = max_iterations
    self.weights = {}
    for label in legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use
      
  def train( self, trainingData, trainingLabels, validationData, validationLabels ):
    """
    The training loop for the perceptron passes through the training data several
    times and updates the weight vector for each label based on classification errors.
    See the project description for details. 
    
    Use the provided self.weights[label] datastructure so that 
    the classify method works correctly. Also, recall that a
    datum is a counter from features to values for those features
    (and thus represents a vector a values).
    """
    
    self.features = trainingData[0].keys() # could be useful later
    
    for iteration in range(self.max_iterations):
      print "Starting iteration ", iteration, "..."
      for i in range(len(trainingData)):
            guess = self.classify( [trainingData[i]])[0]
            if trainingLabels[i] != guess:
                self.weights[guess] = self.weights[guess].__sub__(trainingData[i])
                self.weights[trainingLabels[i]] = self.weights[trainingLabels[i]].__add__(trainingData[i])
    
  def classify(self, data ):
    """
    Classifies each datum as the label that most closely matches the prototype vector
    for that label.  See the project description for details.
    
    Recall that a datum is a util.counter... Do not modify this method.
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

    ## YOUR CODE HERE
    weights1 = util.Counter(self.weights[class1].copy()).sortedKeys()
    weights2 = util.Counter(self.weights[class2].copy()).sortedKeys()
    for i in range (0, 100):
        featuresClass1.append(weights1[i])
        featuresClass2.append(weights2[i])
    weights1 = util.Counter(self.weights[class1].copy())
    weights2 = util.Counter(self.weights[class2].copy())
    for i in range (0, 100):
        weightKeys = weights1.sortedKeys()
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

