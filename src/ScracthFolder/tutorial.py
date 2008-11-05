from battleship import *
import util, sensorDistributions, battleshipAgent

"""
Battleship Tutorial

This tutorial is intended to help you get started with the project 
by introducing you to the game objects and command line options. 

1. Examine the setup below. We begin by specifying an instance
   of the Game class. Note that we specify some agent arguments
   and let the Game instance build an agent. For more details
   about what each option does, run battleship.py -h from the
   command line.
   
2. Run the code below and examine the Game Basics output. Note that 
   possible ship positions and bombing options are the same and that 
   they are each a list of (tuple of tuples). This is because a ship
   object is really a tuple of ships, though currently there is
   only 1 ship. Try setting numships=2 and look at the output.
   Note that now there are more ship positions than bombing options.
   This is because you multiple ships can occupy the same square
   but you can only bomb a square once. These data-structures are
   created by the functions util.factorials and util.choices.
   
3. Next, set numships back to 1 and run again, paying attention to
   the 3 output distributions. These are the three ways in which
   we can access the distributions underlying our game.
   
   game.getShipsDistribution() gets the prior probability of a ship
   variable being true. Notice that the prior distribution over ship 
   positions are uniform. Try setting numShips=2. What happens to
   the priors?
   
   game.getReadingDistributionGivenShipTuple(shipTuple, observation)
   returns the probability distribution over possible sensor readings
   given a shipTuple (tuple of ship positions) and an observation
   (a board position). This function represents our knowledge of
   the underlying sensor quality. With a deterministic sensor, these
   probabilities are either 1 or 0 since the sensors give perfect
   information. Try changing the sensor to the noisy distribution
   (uncomment the line of code, below) and look at how the 
   distributions change.
      
   If you are curious, take a look at these functions in
   battleship.Game to see how they work, though you actually
   don't need to understand this code to do the project.
   
4. Lastly, open up a command line window and try some of these
   sample battleship runs:
     
   python battleship.py
   python battleship.py -w
   python battleship.py -w -k 2
   python battleship.py -w -s noisy
   python battleship.py -h
   
5. Ok. You are now ready for anything. Good luck with your coding.
   
"""

# game settings
layout = Layout((2, 2))
numships = 1
sensors = Sensors(sensorDistributions.deterministicSensorReadingDistribution)
#sensor = Sensor(sensorDistributions.noisySensorReadingDistribution)
noise = 0

# set up agent to be created by the game
player = 'human'
inference = 'exact'

agentBuilder = None
if player == 'human':
   agentBuilder = lambda game: battleshipAgent.StaticKeyboardAgent(battleshipAgent.ExactStaticInferenceModule(game), game)
if player == 'vpi':
   agentBuilder = lambda game: battleshipAgent.StaticVPIAgent(battleshipAgent.ExactStaticInferenceModule(game), game)
if agentBuilder == None:
  raise 'Agent not specd correctly!'

game = Game(agentBuilder, layout, numships, sensors)

print 'Game Basics:'
print 'ships:', game.getNumShips()
print 'board positions:', game.getLocations()
print 'number of board positions:', game.getNumLocations() 
print 'possible ship positions:', game.getShipTuples()
print 'bombing options:', game.getBombingOptions()
print 'possible sensor readings:', Readings.getReadings()
print

print 'Priors P(true position):'
priors = game.getShipTupleDistribution()
for pos in priors.keys():
  print 'position', pos, ': prior =', priors[pos]
print

print 'P(observation | ship positions)'
observationPosition = (0, 0)
print 'observing:', observationPosition
for ship in game.getShipTuples():
  dist = game.getReadingDistributionGivenShipTuple(ship, observationPosition)
  print 'ship(s) at', ship, ':', dist
print

