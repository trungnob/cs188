from ghostbusters import *
from util import *
import util
import random

class StaticInferenceModule:
  """
  A static inference module must compute two quantities, conditioned on provided observations:
  
    -- The posterior distribution over ghost locations.  This will be a distribution over tuples of
       where the ghosts are.  If there is only one ghost, this distribution will be over the
       (singleton tuples of) the board locations.  If there are two ghosts, this distribution will
       assign a probability to each pair of locations, and so on.  Since the ghosts are interchangeable,
       the probability for, say, ((0,1), (3,2)) will be the same as that for ((3,2), (0,1)).
       
    -- The posterior distribution over the readings at a location, given the existing readings.  Be
       careful that your computation does the right thing when the 'new' location is actually in the
       existing observations, at which point the posterior should put probability one of the known
       reading.

  This is an abstract class, which you should not modify.
  """
  
  def __init__(self, game):
    """
    Inference modules know what game they are reasoning about.
    """
    self.game = game
  
  def getGhostTupleDistributionGivenObservations(self, observations):
    """
    Compute the distribution over ghost tuples, given the evidence.
    
    Note that the observations are given as a dictionary.
    """
    util.raiseNotDefined()
    
  def getReadingDistributionGivenObservations(self, observations, newLocation):
    """
    Compute the distribution over readings for the new location, given the
    current observations (given as a dictionary).
    """
    util.raiseNotDefined()

class ExactStaticInferenceModule(StaticInferenceModule):
  """
  You will implement an exact inference module for the static ghostbusters game.
  
  See the abstract 'StaticInferenceModule' class for descriptions of the methods.
  
  The current implementation below is broken, returning all uniform distributions.
  """
  def getGhostTupleDistributionGivenObservations(self, observations):    
    "*** YOUR CODE HERE ***"

    NewDistributions = util.Counter()
    PreviousDistrubutions = self.game.getInitialDistribution()
    for eachGhost in self.game.getGhostTuples():
        p_eachGhost = PreviousDistrubutions.getCount(eachGhost)
        for eachObservation in observations.items():
            valueOfSensor= self.ValueOfSensorReadingGivenGhostPosition(eachGhost, eachObservation)
            #print eachGhost,"blah ",eachObservation,"has ",valueOfSensor
            p_eachGhost *= valueOfSensor
        if p_eachGhost==0: continue
        NewDistributions.setCount(eachGhost, p_eachGhost)
   
    NewDistributions = normalize(NewDistributions)
    return NewDistributions    
  def ValueOfSensorReadingGivenGhostPosition(self,Ghost,Observation):
       sensorLocation, sensorReading = Observation#Reading = Green , Blue
       Distribution_ReadingSensor_ghostPosition = self.game.getReadingDistributionGivenGhostTuple(Ghost, sensorLocation)
       p_Sensor_ghostPostion = Distribution_ReadingSensor_ghostPosition.getCount(sensorReading)
       return p_Sensor_ghostPostion
   
  def getReadingDistributionGivenObservations(self, observations, newLocation):
    "*** YOUR CODE HERE ***"

    new_reading_obs = Counter()
    Ghost_tups_given_obs = self.getGhostTupleDistributionGivenObservations(observations)
    for ghost_tup, ghost_tups_given_obs in Ghost_tups_given_obs.items():
        Reading_given_tup = self.game.getReadingDistributionGivenGhostTuple(ghost_tup, newLocation)
#        print Reading_given_tup
        for reading in Readings.getReadings():
            reading_given_tup = Reading_given_tup.getCount(reading)
            new_reading_obs.incrementCount(reading, ghost_tups_given_obs * reading_given_tup)
    new_reading_given_obs = normalize(new_reading_obs)
#    print Ghost_tups_given_obs
#    print observations
#    print newLocation
#    print new_reading_given_obs
    
    return new_reading_given_obs                 


