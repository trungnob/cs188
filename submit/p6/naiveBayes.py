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
    self.weights = {}
    for label in self.legalLabels:
      self.weights[label] = util.Counter() # this is the data-structure you should use
    self.Counts = {}
    self.condCounts = util.Counter()
#    for label in self.legalLabels:
#        self.condCounts[label] = [util.Counter(), util.Counter()]
    for label in self.legalLabels:
        self.Counts[label]=0;
#        self.condCounts[label][0]=util.Counter()
#        self.condCounts[label][1]=util.Counter()   
        
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
    for i in range (0,len(trainingLabels)):
        self.Counts[trainingLabels[i]] += 1.00
        for data in trainingData[i].keys():
            if trainingData[i].getCount(data) == 0:
#                self.condCounts[trainingLabels[i]][0].incrementCount(data, 1.00)
                self.condCounts.incrementCount((data,0,trainingLabels[i]),1) #condCounts as c(Fi=fi|Y=trainingLabels[i])
            else:
                self.condCounts.incrementCount((data,1,trainingLabels[i]),1)
   
    self.Probs = util.Counter()
    self.condProbs = util.Counter()
    currentMaxProb = 0.0
#    currentMaxProbs =
#    currentMaxCondProbs = []
#    for label in self.legalLabels:
#        self.condProbs[label] = [util.Counter(), util.Counter()]
#    for label in self.legalLabels:
#        self.Probs[label]=0;
#        self.condProbs[label][0]=util.Counter()
#        self.condProbs[label][1]=util.Counter()   
    for k in kgrid:
        for label in self.legalLabels:
            for feature in self.features:
                #sum = self.condCounts[label][0].getCount(feature) + self.condCounts[label][1].getCount(feature)
                sum=self.condCounts.getCount((feature,0,label))+self.condCounts.getCount((feature,1,label))
                self.condProbs[(feature,0,label)] = (self.condCounts.getCount((feature,0,label))+ self.k) / (sum + 1.0*self.k)
                self.condProbs[(feature,1,label)] = (self.condCounts.getCount((feature,1,label)) + self.k) / (sum +1.0*self.k)
            self.Probs[label] = (self.Counts[label]) / (len(trainingLabels))
        guesses = self.classify(validationData)
        correctGuesses = 0.0
        for i in range(0, len(validationLabels)):
            if guesses[i] == validationLabels[i]:
                correctGuesses += 1.0
        currentProb = 1.0*(correctGuesses/len(validationLabels))
        if currentProb > currentMaxProb:
            currentMaxProb = currentProb
            self.k = k

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
    logJoint = util.Counter()
    for label in self.legalLabels:
        logJoint[label] = math.log(self.Probs[label])
        for data in datum.keys():
            if datum[data] == 0:
                logJoint[label] += math.log(self.condProbs[(data,0,label)])
            else:
            
                logJoint[label] += math.log(self.condProbs[(data,1,label)])
    return logJoint
  
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
    weights1 = util.Counter()
    weights2 = util.Counter()
    for feature, i, label in self.condProbs.keys():
        if i==1 and label==class1:
            weights1.setCount(feature, self.condProbs.getCount((feature, i, label)))
        elif i==1 and label==class2:
            weights2.setCount(feature, self.condProbs.getCount((feature, i, label)))
    w1 = weights1.sortedKeys()
    w2 = weights2.sortedKeys()
    for i in range (0, 100):
        featuresClass1.append(w1[i])
        featuresClass2.append(w2[i])
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
    

    
      
