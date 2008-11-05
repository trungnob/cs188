"""
The game of battleship!

This file contains the main logic for the game.  You do not need to know about everything
in here.  The critical methods you need are in Game, so start with that class and with
the example code in battleshipAgent.py.  From a Game object, your agent can
get most of the important probability distributions, board layout information, and so on.

You should not change this file!
"""

from util import *
import sys, random

# SCORE CONSTANTS

SENSOR_SCORE = -1.0
BATTLESHIP_SCORE = 50.0


# GAME COMPONENTS

class Sensors:
  """
  A sensors object manages the distributions for each individual location's sensor.  In this
  implementation, all sensors share a single distribution where the reading is a noisy indicator
  of the true (manhattan) distance.
  """
  def __init__(self, distribution):
    """
    The conditional distribution family passed in maps distances to readings.  Any distance greater
    than the largest specified distance is clipped to the maximum.
    """
    self.readingDistribution = distribution
    self.farthestReading = max(distribution)
    self.distributionCache = {}

  def __getReadingDistribution(self, distance):
    """
    Return a reading distribution for a given distance.
    """
    clippedDistance = min(distance, self.farthestReading)
    return self.readingDistribution[clippedDistance]

  def getReadingDistributionGivenShipTuple(self, shipTuple, location):
    """
    The reading is a noisy indicator of the closest ship.
    
    Cached.
    """
    arg = (tuple(shipTuple), location)
    if arg not in self.distributionCache:
      distances = [manhattanDistance(location, ship) for ship in shipTuple]
      self.distributionCache[arg] = self.__getReadingDistribution(min(distances))
    return self.distributionCache[arg]



class Readings:
  """
  A reading is what you observe when you drop a sensor.
  Intuitively, RED corresponds to hot (close), ORANGE to warm, 
  YELLOW to cooler, and GREED to cold (distant)
  
  The specific meaning of a reading is specified in a 
  sensor reading conditional distribution, see sensorDistributions.py
  
  python usage note:
    staticmethod(getReadings), below, means that you can call
    Readings.getReadings() without instatiating a Readings object
  """

  RED = 'RED'
  ORANGE = 'ORANGE'
  YELLOW = 'YELLOW'
  GREEN = 'GREEN'
  
  def getReadings():
    return [Readings.RED, Readings.ORANGE, Readings.YELLOW, Readings.GREEN]
  getReadings = staticmethod(getReadings)
  
  
class Actions:
  """
  there are a few basic actions in battleship. they are:
  1. sense at <location> where location is a (row, col)
  2. bomb at <locations> where locations is a list of (row, col) tuples
     note that this is a list because you don't find out the result of
     your bombing actions until you are finished bombing
  """
  
  def makeSensingAction(location):
    return ('sense', location)
  makeSensingAction = staticmethod(makeSensingAction)

  def makeBombingAction(locations):
    return ('bomb', locations)
  makeBombingAction = staticmethod(makeBombingAction)


class Layout:
  def __init__(self, (rows, cols)):
    self.board = [[(row, col) for col in range(cols)] for row in range(rows)]
    self.rows = rows
    self.cols = cols
    self.locations = []
    for row in range(rows):
      for col in range(cols):
        self.locations.append((row, col))
    self.numLocations = len(self.locations)
    
  def getLocations(self):
    return self.locations

  def isLegalPos(self, pos):
    """
    returns True if the position is a legal position
    on the board
    """
    row, col = pos
    if (row < 0) or (col < 0) or (row >= self.rows) or (col >= self.cols):
      return False
    return True
    
class GameState:
  """
  controls the inner state of a battleship game. it primarily
  maintains ship locations 
  """
  def __init__(self):
    self.layout = None
    self.shipTuple = None
    self.score = 0
    
  def initialize(self, layout, numShips, sensors):
    """
    creates an initial game state with random start
    positions for each ship
    """
    self.layout = layout
    self.sensorReadings = [[0 for col in range(layout.cols)] for row in range(layout.rows)]
    ships = []
    for i in range(numShips):
      row = random.randint(0, self.layout.rows-1)
      col = random.randint(0, self.layout.cols-1)
      ships.append((row,col))
    self.shipTuple = tuple(ships)
    self.elapseTime(sensors)
      
  def dropBombs(self, bombPositions):
    """
    drop a each bomb, removing effected ships
    returns a list of (position, hit/miss) results
    """    
    results = []
    shipsToRemove = []
    hits = 0
    for pos in list(bombPositions):
      result = 'miss'
      for ship in self.shipTuple:
        if pos == ship:
          shipsToRemove.append(ship)
          result = 'hit'
          self.score += BATTLESHIP_SCORE          
      results.append((pos, result))
      
    shipsLeft = []
    for ship in self.shipTuple:
      if not ship in shipsToRemove:
        shipsLeft.append(ship)
    self.shipTuple = tuple(shipsLeft)

    return results
  
  def elapseTime(self, sensors):
    """
    precompute sensorReadings at each board position
    """
    for location in self.layout.locations:
      row, col = location
      self.sensorReadings[row][col] = sample(sensors.getReadingDistributionGivenShipTuple(self.shipTuple, location))
        
  def getShipTuple(self):
    """
    returns a tuple of all ship positions
    """
    return self.shipTuple
  
  def getNumShips(self):
    return len(self.shipTuple)
  
  def getContents(self, location):
    """
    returns a list of ships at the given position
    """
    contents = []
    for ship in self.ships:
      if location == ship:
        contents.append(ship)
  

class Game:
  """
  The Game object controls many aspects of a game of battleship, including control logic.
  
  A game takes the following arguments on construction:
  
    layout -- Specifics about the board size (see Layout class)
    
    numShips -- The number of ships to place on the board. Note that
                the ship location are maintained by the GameState class.

    sensors -- An instance of the Sensors class, specifying the
              sensor behavior, in the form of distributions over sensor readings.
                        
    agentBuilder -- Agents neet to know what game they are in, so are built
              in the Game constructor.
                 
  """

  def __init__(self, agentBuilder, layout, numShips, sensors):
    import gui
    self.gameOver = False
    self.state = GameState()
    self.state.initialize(layout, numShips, sensors)
    self.display = gui.BattleshipGraphics()
    self.sensors = sensors
    self.display.initialize(self.state)
    self.bombs = self.state.getNumShips()
    
    # create agent last
    self.agent = agentBuilder(self)
  
  #############################################################################
  #
  # BEGIN IMPORTANT CONVENIENCE METHODS FOR AGENTS -- READ THESE!
  #
  #############################################################################
  
  def getNumShips(self):
    """
    Return the number of ships in the current game.
    """
    return len(self.state.shipTuple)
  
  def getLocations(self):
    """
    Return the list of all possible locations (row, col) in the current layout.
    """
    return self.state.layout.locations

  def getNumLocations(self):
    """
    Return the number of possible locations in the current layout.
    """
    return self.state.layout.numLocations

  def getShipTuples(self):
    """
    Return the possible ship tuples in the current game.  A ship tuple is in the
    form (location1, location2, ..., locationN) when there are N ships.  NOTE: if
    there is only one ship, you will still get tuples, but they will be singleton
    tuples with only one position, like ((0,1),).
    """
    list = factorials(self.getNumShips(), self.getLocations())
    return [tuple(i) for i in list]
  
  def getShipTupleDistribution(self):
    """
    Return the prior distribution over ship tuples.  If there is only one ship,
    this will be a lot like a distribution over locations, except that each key
    will be a singleton tuple.  See getShipTuples().
    """
    shipTuples = self.getShipTuples()
    p_ShipTuples = Counter()
    for shipTuple in shipTuples:
      p_ShipTuples.setCount(shipTuple, 1.0)
    return normalize(p_ShipTuples)
  
  def getBombingOptions(self):
    """
    Return the list of all bombing options.  Each option is a tuple of locations,
    such as ((1,4), (5,2)).
    
    Note that if ((1,4), (5,2)) is in the list, ((5,2), (1,4)) will not be, since
    this option would represent the same bombing action (since the bombs are not
    distinguishable).
    
    Note also that an option is not a bombing action, just the details of an
    action: use Actions.makeBombingAction() to make a bombing action.
    """
    list = choices(self.getNumShips(), self.getLocations())
    return [tuple(i) for i in list]
    
  def getReadingDistributionGivenShipTuple(self, shipTuple, location):
    """
    Return the distribution over readings for a particular sensor, given a shipTuple.
    """
    return self.sensors.getReadingDistributionGivenShipTuple(shipTuple, location)
 
  #############################################################################
  #
  # END IMPORTANT CONVENIENCE METHODS FOR AGENTS
  #
  #############################################################################
  
  def run(self):
    """
    run a game
    """
    self.display.showState(self.state)
    self.display.showBeliefs(self.getLocations(), self.agent.getExpectedShipCounts(), self.state.shipTuple)
    observations = []
    while True:
      action = self.agent.getAction()
      if action[0] == 'sense':
        row, col = action[1]
        observation = ((row, col), self.state.sensorReadings[row][col])
        if observation in observations:
          continue
        self.state.score += SENSOR_SCORE
        self.display.infoPane.updateScore(self.state, self.bombs)
        self.display.showMove(observation)
        observations.append(observation)
        self.agent.observe(observation)
        self.display.showBeliefs(self.getLocations(), self.agent.getExpectedShipCounts(), self.state.shipTuple)
        
      elif action[0] == 'bomb':
        locations = action[1]
        self.display.infoPane.drawBombButton('clicked')
        bombResults = self.state.dropBombs(locations)
        self.display.infoPane.updateScore(self.state, self.bombs)
        self.display.endGame(bombResults)
        return True
        
        
    
def readCommand( argv ):
  """
  Processes the command used to run from the command line.
  """
  import getopt
  import gui
  
  # Set default options
  options = {'layout': 'small', 
             'numships': 1, 
             'sensortype': 'deterministic',
             'player': 'human',
             'inference': 'exact',
             'zoom' : None,
             'noise' : 0.0,
             'showships': False,
             'showbeliefs': True}
             
  args = {} # This dictionary will hold the objects used by the game
  
  # Read input from the command line
  commands = ['help', 
              'layout=', 
              'ships=', 
              'sensortype=', 
              'player',
              'inference',
              'zoom=',
              'showships',
              'hidebeliefs' ]
  try:
    opts = getopt.getopt( argv, "hl:k:s:p:i:z:n:m:wq", commands )
  except getopt.GetoptError:
    print USAGE_STRING
    sys.exit( 2 )
    
  for option, value in opts[0]:
    if option in ['--help', '-h']:
      print USAGE_STRING
      sys.exit( 0 )
    if option in ['--player', '-p']:
      options['player'] = value
    if option in ['--inference', '-i']:
      options['inference'] = value
    if option in ['--layout', '-l']:
      options['layout'] = value
    if option in ['--ships', '-k']:
      options['numships'] = int( value )
    if option in ['--sensortype', '-s']:
      options['sensortype'] = value
    if option in ['--zoom', '-z']:
      options['zoom'] = float( value )
    if option in ['--showships', '-w']:
      options['showships'] = True
    if option in ['--hidebeliefs', '-q']:
      options['showbeliefs'] = False
    
  # numships
  args['numships'] = options['numships']
      
  # Choose a layout
  boardSizes = { 'test': (3,3), 
                 'small': (4,6),
                 'medium': (6,10),
                 'large': (10,16) }
  args['layout'] = Layout( boardSizes[ options['layout'] ] )
  # auto-scaling the gui
  numSquares = args['layout'].cols
  if not options['zoom']:
    options['zoom'] = 1 - (numSquares / 32.0)

  # scale with zoom
  gui.scaleGridSize(options['zoom'])

  # sensor distribution
  import sensorDistributions
  if options['sensortype'] == 'deterministic':
    args['sensors'] = Sensors(sensorDistributions.deterministicSensorReadingDistribution)
  elif options['sensortype'] == 'noisy':
    args['sensors'] = Sensors(sensorDistributions.noisySensorReadingDistribution)

  import battleshipAgent
  agentBuilder = None
  if options['player'] == 'human':
    agentBuilder = lambda game: battleshipAgent.StaticKeyboardAgent(battleshipAgent.ExactStaticInferenceModule(game), game)
  if options['player'] == 'vpi':
    agentBuilder = lambda game: battleshipAgent.StaticVPIAgent(battleshipAgent.ExactStaticInferenceModule(game), game)
  if agentBuilder == None:
    raise 'Agent not specd correctly!'
  args['agent'] = agentBuilder
  
  # show ships, beliefs
  if options['showships']:
    gui.SHOW_SHIPS = True
  if not options['showbeliefs']:
    gui.SHOW_BELIEFS = False
  
  return args

USAGE_STRING = """
  USAGE:      python battleship.py <options>
  EXAMPLES:   (1) python battleship.py
                  - starts a default game
              (2) python battleship.py --layout large --ships 5
              OR  python battleship.py -l large -s 5
                  - starts a game on the large layout with 5 ships
  
  OPTIONS:    --layout, -l
                  sets the layout of the board to specified configuration
                  Legal values: test, small, medium, large
              --ships, -k
                  sets the number of ships
                  default: 1
              --player, -p
                  sets the decision-maker
                  legal values: human, vpi
                  default: human
              --inference, -i
                  use inference to calculate beliefs
                  legal values: dummy, correct
              --sensortype, -s
                  select the sensor distribution
                  legal values: deterministic, noisy
                  default: deterministic
              --showships, -w
                  show true ship positions (for testing, etc.)
                  default: False
              --hidebeliefs, -q
                  toggles belief display
                  default: True
              --zoom, -z
                  magnifies the GUI
                  default is adjusted for layout size
                 """
  
if __name__ == '__main__':
  """
  running battleship.py from the command line
  """
  
  # Get game components based on input
  args = readCommand( sys.argv[1:] ) 
  
  agentBuilder = args['agent']
  layout = args['layout']
  numships = args['numships']
  sensors = args['sensors']
  
  game = Game(agentBuilder, layout, numships, sensors)
  game.run()

  
  # TODO:
  #   grow margin a little on the right (mine still overflows the text off the window)
  #   improve comments
  #   put some big QUESTION 1 markers in comments in the battleshipAgent.py file
  #   test export and scraper
  #   options: say what options were invalid if failure
  #   optional: options package from 2.1 gives more sensible output, including defaults
