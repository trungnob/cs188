from battleship import *
from util import *
import random

"""
Classes for battleship agents.  See the write-up for details on what to do.

CODING HINTS:
  -- You can get (location, reading) pairs from an observation map using observations.items()
  -- util.py has utility methods and classes for working with probabilities that will save
     you a LOT of time:
       ** Counters manage counts and distributions better than dictionaries (they give zero
          rather than an exception if you ask for the count of something not in the key set
       ** sample() and sampleMultiple() draw from a distribution encoded as a Counter
       ** normalize() produces a normalized copy of a Counter
       ** listToDistribution() makes a distribution from a list, where each occurence in the
          list has a count of 1.0
       ** maxes() takes a counter and returns the max value along with a list of keys which
          have that value
  -- Most lists and distributions you need can be gotten from self.game objects; see battleship.Game
  -- Some lists come straight from other classes, such as Readings.getReadings() = ['RED', 'ORANGE', ...]
"""

class BattleshipAgent:
  """
  Abstract class for all battleship agents.
  
  You do not need to modify this class.
  """
  
  def observe(self, observation):
    """
    Update beliefs in response to an observation.
    
    Observations are (location, reading pairs).
    
    Note that it is the responsibility of the game
    to not send a repeat observation in a given time
    step, so the agent can assume each observation
    is of an random variable which is unknown in the
    current time step.
    """
    abstract
    
  def elapseTime(self):
    """
    Update beliefs in response to the passage of a time
    step.  This should produce an exception for agents
    for the static game, in which time does not pass.
    """
    abstract

  def getAction(self):
    """
    Select an action.
    
    Actions for battleship game are of the form:
      -- ('sense', location)
      -- ('bomb', shipTuple)
      -- ('wait', None)
    Actions can be constructed using the
    battleship.Actions class methods.
      
    In the static game, 'wait' is always invalid.
    """
    abstract
    
  def getExpectedShipCounts(self):
    """
    Form the joint distribution over ship position tuples, and extract the expected
    number of ships at each position.  Note that the expectation at a position may be
    more than one if multiple ships are in play.
    
    This method is used by the gui to display agent beliefs in each square.
    """
    abstract
    
  
class StaticBattleshipAgent(BattleshipAgent):
  """
  Abstract class for agents which do not model the passage of time.
  
  Static agents accumulate all observations to date, and they always do inference
  over ship positions from scratch, calculating P(ships | observations) directly
  rather than incrementally.
  
  You do not need to modify this class.
  """
  
  def __init__(self, inferenceModule, game):
    """
    Static agents have an inference module which does their belief calculations,
    and they know what game they are in.  Most information about how battleship
    works (conditional probabilities, etc) is available from the game object.
    
    Note that Python allows you to access game.gameState, but you should pretend
    that you cannot -- solution which use this true state information will be
    incorrect.
    """
    self.inferenceModule = inferenceModule
    self.game = game
    self.observations = {}
    
  def observe(self, observation):
    """
    Put the newest observation into the list of observations, but do no
    other computation (i.e. no incremental belief updates) for the static agent.
    
    Observations are (location, reading pairs).
    
    Note that in static battleship, there is no concept of re-sensing a location
    to get another reading.  The readings at each location are fixed (though perhaps
    noisy).
    """
    location, reading = observation
    self.observations[location] = reading
    
  def elapseTime(self):
    raise 'Static agents cannot elapse time!'

  def getExpectedShipCounts(self):
    """
    Form the joint distribution over ship position tuples, and extract the expected
    number of ships at each position.  Note that the expectation at a position may be
    more than one if multiple ships are in play.
    
    This method is used by the gui to display agent beliefs in each square.
    """
    p_ShipTuples_given_observations = self.inferenceModule.getShipTupleDistributionGivenObservations(self.observations)
    expectedCounts = Counter()
    for shipTuple in p_ShipTuples_given_observations.keys():
      probability = p_ShipTuples_given_observations[shipTuple]
      for ship in shipTuple:
        expectedCounts.incrementCount(ship, probability)
    return expectedCounts
    

class KeyboardActionSelector:
  """
  GUI interface code which gets an action from the user.
  
  Suitable for use in the static or the dynamic game.
  
  You should not modify this code.
  """
  
  def __init__(self, game):
    self.game = game

  def getAction(self):
    eventType, details = self.__getValidEvent()
    if eventType == 'location':
      return Actions.makeSensingAction(details)
    elif eventType == 'button' and details == 'time-button':
      return Actions.makeWaitAction()
    locations = []
    while len(locations) < self.game.getNumShips():
      eventType, details = self.__getValidEvent()
      if eventType == 'location':
        locations.append(details)
        msg = 'bomb at ' + str(details)
        self.game.display.infoPane.updateMessages(msg)      
        self.game.bombs -= 1
        self.game.display.infoPane.updateScore(self.game.state, self.game.bombs)
    return Actions.makeBombingAction(locations)
      
  def __getValidEvent(self):
    while True:
      event = self.__getEvent()
      if event != None:
        return event

  def __getEvent(self):
    import gui
    point, button = gui.wait_for_click()
    object, position = gui.getEvent(point)
    if object == 'grid':
      return 'location', position
    elif object == 'bomb-button':
      self.game.display.infoPane.drawBombButton('clicked')
      self.game.display.infoPane.drawTimeButton('unclickable')      
      return 'button', object
    elif object == 'time-button':
      return 'button', object
    else:
      return None


class StaticKeyboardAgent(StaticBattleshipAgent):
  """
  Agent which plays the static game using user-selected actions.
  
  You do not need to modify this class.
  """
  def __init__(self, inferenceModule, game):
    StaticBattleshipAgent.__init__(self, inferenceModule, game)
    self.actionSelector = KeyboardActionSelector(game)
    
  def getAction(self):
    return self.actionSelector.getAction()


class StaticVPIAgent(StaticBattleshipAgent):
  """
  Computer-controlled battleship agent.
  
  This agent plays using value of (perfect) information calculations.
  
  The initial implementation is broken, always taking a random bombing action
  without sensing.  You will rewrite it to greedily sense if any sensing action
  has an expected gain in utility / score (taking into account the cost of
  sensing).  If no sensing action has a greedy gain, then you will select a
  position tuple to bomb.  In this case, your agent should bomb the tuple with
  the highest expected utility / score according to its current beliefs.
  """

  def getAction(self):
    
    # BEGIN SOLUTION
    
    self.game.display.pauseGUI()
    observations = self.observations
    expectedUtilities = self.getExpectedUtilities(observations)
    currentBestEU, currentBestBombingOptions = maxes(expectedUtilities)
    utilityGain = Counter()
    for location in self.game.getLocations():
      expectedNewMEU = 0
      p_Reading_given_observations = self.inferenceModule.getReadingDistributionGivenObservations(observations, location)
      for reading in Readings.getReadings():
        outcomeProbability = p_Reading_given_observations.getCount(reading)
        if outcomeProbability == 0.0: continue
        newObservations = dict(observations)
        newObservations[location] = reading
        outcomeExpectedUtilities = self.getExpectedUtilities(newObservations)
        outcomeBestEU, outcomeBestActions = maxes(outcomeExpectedUtilities)
        expectedNewMEU += outcomeBestEU * outcomeProbability
      utilityGain[location] = expectedNewMEU - currentBestEU - abs(SENSOR_SCORE)
      #print 'gain', utilityGain[location], 'location', location
    bestGain, bestSensorLocations = maxes(utilityGain)
    if bestGain > 0:
      return Actions.makeSensingAction(random.choice(bestSensorLocations))
    return Actions.makeBombingAction(random.choice(currentBestBombingOptions))
  
    # END SOLUTION
    # return Actions.makeBombingAction(random.choice(self.game.getBombingOptions()))
    
  # BEGIN SOLUTION
  def getExpectedUtilities(self, observations):
    
    p_ShipTuples = self.inferenceModule.getShipTupleDistributionGivenObservations(observations)
    expectedUtilities = Counter()
    for option in self.game.getBombingOptions():
      expectedUtility = 0
      for ships in p_ShipTuples.keys():
        p = p_ShipTuples[ships]
        utility = BATTLESHIP_SCORE * self.numMatches(option, ships)
        expectedUtility += p * utility
      expectedUtilities[option] = expectedUtility
    return expectedUtilities
  
  def numMatches(self, option, ships):
    matches = 0
    for ship in ships:
      if ship in option:
        matches += 1
    return matches

  # END SOLUTION
  

class StaticInferenceModule:
  """
  A static inference module must compute two quantities, conditioned on provided observations:
  
    -- The posterior distribution over ship locations.  This will be a distribution over tuples of
       where the ships are.  If there is only one ship, this distribution will be over the
       (singleton tuples of) the board locations.  If there are two ships, this distribution will
       assign a probability to each pair of locations, and so on.  Since the ships are interchangeable,
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
  
  def getShipTupleDistributionGivenObservations(self, observations):
    """
    Compute the distribution over ship tuples, given the evidence.
    
    Note that the observations are given as a dictionary.
    """
    abstract
    
  def getReadingDistributionGivenObservations(self, observations, newLocation):
    """
    Compute the distribution over readings for the new location, given the
    current observations (given as a dictionary).
    """
    abstract


class ExactStaticInferenceModule(StaticInferenceModule):
  """
  You will implement an exact inference module for the static battleship game.
  
  See the abstract 'StaticInferenceModule' class for descriptions of the methods.
  
  The current implementation below is broken, returning all uniform distributions.
  """
  
  def getShipTupleDistributionGivenObservations(self, observations):
    
    # BEGIN SOLUTION
    
    p_ShipTuple_and_observations = Counter()
    p_ShipTuple = self.game.getShipTupleDistribution()
    for shipTuple in self.game.getShipTuples():
      p = p_ShipTuple.getCount(shipTuple)
      for observation in observations.items():
        sensor, reading = observation
        p_Reading_given_shipTuple = self.game.getReadingDistributionGivenShipTuple(shipTuple, sensor)
        p_reading_given_shipTuple = p_Reading_given_shipTuple.getCount(reading)
        p *= p_reading_given_shipTuple
      p_ShipTuple_and_observations.setCount(shipTuple, p)
    p_ShipTuple_given_observations = normalize(p_ShipTuple_and_observations)
    return p_ShipTuple_given_observations
  
    # END SOLUTION
    # # BROKEN
    # return listToDistribution(self.game.getShipTuples())

  def getReadingDistributionGivenObservations(self, observations, newLocation):
    
    # BEGIN SOLUTION
    
    oldReadingForNewLocation = self.fetch(newLocation, observations)
    p_NewReading_and_observations = Counter()
    p_ShipTuple_given_observations = self.getShipTupleDistributionGivenObservations(observations)
    for shipTuple, p_shipTuple_given_observations in p_ShipTuple_given_observations.items():
      p_Reading_given_shipTuple = self.game.getReadingDistributionGivenShipTuple(shipTuple, newLocation)
      for reading in Readings.getReadings():
        p_reading_given_shipTuple = p_Reading_given_shipTuple.getCount(reading)
        if oldReadingForNewLocation != None:
          p_observation_given_ship = 0.0
          if oldReadingForNewLocation == reading:
            p_observation_given_ship = 1.0
        p_NewReading_and_observations.incrementCount(reading, p_shipTuple_given_observations * p_reading_given_shipTuple)
    p_NewReading_given_observations = normalize(p_NewReading_and_observations)
    return p_NewReading_given_observations
  
    # END SOLUTION
    # # BROKEN
    # return listToDistribution(Reading.getReadings())
  
  # BEGIN SOLUTION
  
  def fetch(self, key, pairList):
    for key2, value2 in pairList:
      if key == key2: return value2
    return None
  
  # END SOLUTION

    