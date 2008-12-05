import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    # DO NOT DELETE or CHANGE any of those variables!
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter
    self.automaticTuning = False # Flat for automatic tuning of the parameters
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  

    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Train the classifier by collecting counts over the training data 
    and choose the smoothing parameter among the choices in kgrid by
    using the validation data. This method stores the right parameters
    as a side-effect and should return the best smoothing parameters.

    See the project description for details.
    
    Note that trainingData is a list of feature Counters.
    
    Assume that we do not use sparse encoding (normally we would); so that you can
    figure out what are the list of possible features by just looking
    at trainingData[0].keys() generically. Your code should not make any assumption
    about the feature keys apart that they are all in trainingData[0].keys().
    
    If you want to simplify your code, you can assume that each feature is binary
    (can only take the value 0 or 1).

    You should also keep track of the priors and conditional probabilities for
    further usage in calculateLogJointProbabilities method
    """
    for i in range (0,len(trainingData) ):
        self.probs[trainingLabels[i]] += 1.00
        for data in trainingData[i].keys():
            if trainingData[i][data] == 0:
                currCondProb = self.condProbs[trainingLabels[i]][0]
                currCondProb[data] = currCondProb.getCount(data) + 1.00
            else:
                currCondProb = self.condProbs[trainingLabels[i]][1]
                currCondProb[data] = currCondProb.getCount(data) + 1.00
    
    """at this point, self.probs[i] is the count of number of times we saw label i in the
    training set, and self.condProbs[i][val][j] is the number of times that data j was of value val"""
    
    maxk = kgrid[0]
    maxProb = 0.0
    oldProbs = self.probs
    maxProbs = []
    maxCondProbs = []
    oldCondProbs = self.condProbs
    self.condProbs = []
    for condProb in oldCondProbs:
        self.condProbs.append( (util.Counter({}), util.Counter({})) )
    numToEval = len(validationLabels)*1.0
    
    for k in kgrid:
        self.k = k
        
        self.condProbs = []
        for condProb in oldCondProbs:
            self.condProbs.append( (util.Counter({}), util.Counter({})) )
        self.probs = oldProbs.copy()
        
        for i in range (0, len(self.legalLabels)):
           label = self.legalLabels.index(i)
           for feature in self.features:
               total = oldCondProbs[label][0].getCount(feature) + oldCondProbs[label][1].getCount(feature)
               self.condProbs[label][0][feature] = (oldCondProbs[label][0].getCount(feature) + self.k) / (total + 2*self.k)
               self.condProbs[label][1][feature] = (oldCondProbs[label][1].getCount(feature) + self.k) / (total + 2*self.k)
           self.probs[label] = (oldProbs[label]) / (len(trainingData))
        
        guesses = self.classify(validationData)   
        numCorrect = 0.0
        for i in range (0, len(validationLabels)):
            if guesses[i] == validationLabels[i]:
                numCorrect += 1
                
        if (numCorrect/numToEval) > maxProb:
            maxProb = (numCorrect/numToEval)
            maxk = k
            maxProbs = self.probs
            maxCondProbs = self.condProbs
            
    self.k = maxk
    self.probs = maxProbs
    self.condProbs = maxCondProbs
    return self.k
    
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint['face'] = <Estimate of log( P(Label = face, datum) )>
    """
    for i in self.legalLabels:
        label = self.legalLabels[i]
        condProbs = self.condProbs[label]
        logJoint[label] = math.log(self.probs[label])
        for data in datum.keys():
            if datum[data] == 0:
                logJoint[label] += math.log(condProbs[0][data])
            else:
                logJoint[label] += math.log(condProbs[1][data])
    
    return logJoint
    ## YOUR CODE HERE
    # example of type of values: logJoint["SomeLabel"] = math.log(1e-301) 
  
  def findHighOddsFeatures(self, class1, class2):
    """
    Returns: 
    featuresClass1 -- the 100 best features for P(feature=on|class1) (as a list)
    featuresClass2 -- the 100 best features for P(feature=on|class2)
    featuresOdds -- the 100 best features for the odds ratio 
                     P(feature=on|class1)/P(feature=on|class2) 
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
    

    
      
