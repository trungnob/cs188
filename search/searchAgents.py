"""
This file contains all of the agents that can be selected to 
control Pacman.  To select an agent, simple use the '-p' option
when running pacman.py.  That is, to load your DepthFirstSearchAgent,
just run the following command from the command line:

> python pacman.py -p DepthFirstSearchAgent

Please only change the parts of the file where you are asked; look
for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""
from game import Directions
from game import Agent
from game import Actions
from util import manhattanDistance
import util
import time
import search

class GoWestAgent(Agent):
  """
  An agent that goes West until it can't.
  """
  def getAction(self, state):
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP
    
class TinyMazeAgent(Agent):
  """
  An agent that can solve tinyMaze, using the command
  
    python pacmany.py --layout tinyMaze --pacman TinyMazeAgent
    
  """
  def __init__(self):
    """
    Here, you can define any data that will persist through the
    life of the agent using
    
    self.whatever = valueToKeepAround
    """
    "*** YOUR CODE HERE ***"
    
  def getAction(self, state):
    """
    This method must return one of the five Directions (STOP not recommended)
    """
    "*** YOUR CODE HERE ***"
    if Directions.SOUTH in state.getLegalPacmanActions():
      return Directions.SOUTH
    else:
      if Directions.WEST in state.getLegalPacmanActions():
          return Directions.WEST

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class PositionSearchProblem(search.SearchProblem):
  """
  A search problem defines the state space, start state, goal test,
  successor function and cost function.  This search problem can be 
  used to find paths to a particular point on the pacman board.
  
  The state space consists of (x,y) positions in a pacman game.
  
  This search problem is fully specified and should not require change.
  """
  
  def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1)):
    """
    Stores the start and goal.  
    """
    self.walls = gameState.getWalls()
    self.startState = gameState.getPacmanPosition()
    self.goal = goal
    self.costFn = costFn
    if gameState.getNumFood() != 1 or not gameState.hasFood(*goal):
      print 'Warning: this does not look like a regular search maze'

    # For display purposes
    self._visited, self._visitedlist, self._expanded = {}, [], 0

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
     isGoal = state == self.goal 
     
     # For display purposes only
     if isGoal:
       print 'Goal found after expanding %d nodes.' % self._expanded
       self._visitedlist.append(state)
       import __main__
       if '_display' in dir(__main__):
         if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
           __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable
       
     return isGoal   
   
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    
     As noted in search.py:
         For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append( ( nextState, action, cost) )
        
    # Bookkeeping for display purposes
    self._expanded += 1 
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
      
    return successors
  
class SearchAgent(Agent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.
  
  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
  """
    
  def __init__(self, searchFunction=None, searchType=PositionSearchProblem):
    self.searchFunction = searchFunction
    self.searchType = searchType
    
  def registerInitialState(self, state):
    """
    Chooses the path to the goal
    """
    if self.searchFunction == None:
      import sys
      print "No search function provided for SearchAgent"
      sys.exit(1)

    problem = self.searchType(state) # Makes a new search problem
    starttime = time.time()
    self.path, self.actions, totalCost = self.searchFunction(problem)
    print 'Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime)
    
  def getAction(self, state):
    if 'actionIndex' not in dir(self): self.actionIndex = 0
    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]    
    else:
      return Directions.STOP
      
class DepthFirstSearchAgent(SearchAgent):
  """
  An agent that first computes a path to the goal using DFS, then
  follows that path.
  """
  def __init__(self):
    SearchAgent.__init__(self, search.depthFirstSearch)  

class BreadthFirstSearchAgent(SearchAgent):
  """
  An agent that first computes a path to the goal using BFS, then
  follows that path.
  """
  def __init__(self):
    SearchAgent.__init__(self, search.breadthFirstSearch)  
    
class UniformCostSearchAgent(SearchAgent):
  """
  An agent that computes a path to the goal position using UCS.
  """
  def __init__(self):
    SearchAgent.__init__(self, search.uniformCostSearch)  

class StayEastSearchAgent(SearchAgent):
  """
  An agent that computes a path to the goal position using UCS, but
  lets its cost function guide it eastward.
  """
  def __init__(self):
    problem = lambda x: PositionSearchProblem(x, stayEastCost)
    SearchAgent.__init__(self, search.uniformCostSearch, problem)  
    
class StayWestSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using UCS, but
  lets its cost function guide it westward.

  """
  def __init__(self):
    problem = lambda x: PositionSearchProblem(x, stayWestCost)
    SearchAgent.__init__(self, search.uniformCostSearch, problem)  

def stayEastCost(position):
  """
  Gives a cost for each (x,y) position that guides a search agent eastward
  """
  return .5 ** position[0]  
  
def stayWestCost(position):
  """
  Gives a cost for each (x,y) position that guides a search agent westward
  """
  return 2 ** position[0]  

class FoodSearchProblem:
  """
  A search problem associated with finding the a path that collects all of the 
  food (dots) in a Pacman game.  Be thoughtful in selecting your state space.
  """
  def __init__(self, state):
    self.start = (state.getPacmanPosition(), state.getFood())
    self.walls = state.getWalls()
    self._expanded = 0
      
  def getStartState(self):
    return self.start
  
  def isGoalState(self, state):
    if state[1].count() == 0:
      print 'Goal found after expanding %d nodes.' % self._expanded
      return True
    return False

  def getSuccessors(self, state):
    successors = []
    self._expanded += 1
    for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state[0]
      dx, dy = Actions.directionToVector(direction)
      nextx, nexty = int(x + dx), int(y + dy)
      if not self.walls[nextx][nexty]:
        nextFood = state[1].copy()
        nextFood[nextx][nexty] = False
        successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
    return successors
     
class UniformCostFoodSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using UCS.
  """
  def __init__(self):
    SearchAgent.__init__(self, search.uniformCostSearch, FoodSearchProblem)  

def manhattanAStar(problem):
  """
  A wrapper for A* that uses the Manhattan distance heuristic.
  """
  return search.aStarSearch(problem, lambda x: manhattanDistance(x, problem.goal))

class ManhattanAStarSearchAgent(SearchAgent):
  """
  An agent that computes a path to the goal position using AStar and
  the Manhattan distance heuristic.
  """
  def __init__(self):
    SearchAgent.__init__(self, manhattanAStar, PositionSearchProblem)  

###########################################################    
# You have to fill in several parts of the following code #
###########################################################    

def getFoodHeuristic(gameState):
  """
  Instead of filling in the foodHeuristic function directly, you can fill in 
  this function which takes a full gameState for Pacman (see pacman.py) and
  returns a heuristic function.  The heuristic function must
    - take a single parameter, a search state
    - return a non-negative number that is the value of the heuristic at that state

  This function is *only* here for students who want to create more complex 
  heuristics that use aspects of the gameState other than the food Grid and
  Pacman's location (such as where the walls are, etc.)
    
  Note: The state that will be passed to your heuristic function is a tuple 
  ( pacmanPosition, foodGrid ) where foodGrid is a Grid (see game.py) of either 
  True or False.
  """
  # If you don't want to implement this method, you can leave this default implementation
  return foodHeuristic

def foodHeuristic(state):
  """
  Here, you can write your food heuristic function instead of using getFoodHeuristic.
  This heuristic must be admissible (if your AStarFoodSearchAgent and your 
  UniformCostSearchAgent *ever* find solutions of different length, your heuristic 
  is *not* admissible).  
  
  The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a 
  Grid (see game.py) of either True or False.
  
  Note that this function *does not* have access to the location of walls, capsules,
  ghosts, etc.  If you want to work with this information, you should implement
  getFoodHeuristic instead of this function.
  
  Hint: getFoodHeuristic can return a heuristic that encapsulates data through a 
  function closure (like the manhattanAStar function above).  If you don't know how 
  this works, come to office hours.
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

class AStarFoodSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using AStar.
  
  You should use either foodHeuristic or getFoodHeuristic in your code here.
  """
  "*** YOUR CODE HERE ***"

class GreedyFoodSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using greedy search.
  """
  "*** YOUR CODE HERE ***"
  
  
class SafeSearchAgent(SearchAgent):  
  """
  A SafeSearchAgent eats all of the dots while keeping the ghosts scared.
  A default implementation is provided here, which runs greedy search with
  a null heuristic.  To solve the most challenging safe search mazes, you
  will need to edit this implementation.
  
  You are welcome to edit this in any way you see fit.
  """
  
  def __init__(self):
    SearchAgent.__init__(self, lambda x : search.greedySearch(x, self.heuristic), SafeSearchProblem)

  def heuristic(self, state):
    return 0
  
      
class SafeSearchProblem(search.SearchProblem):
  """
  The search problem of finding a path to eat all the food while
  making sure that the ghosts are always scared.
  
  When Pacman eats a capsule (power pellet), the ghosts stay scared 
  for the next SCARED_TIME moves, a global variable that has been imported
  for you below.
  
  Your search problem should encode the requirement that after each move,
  Pacman needs to have eaten a capsule in the last SCARED_TIME moves to
  guarantee his safety.
  """
  
  def __init__(self, gameState):
    """
    Please keep the first two lines provided for you that import SCARED_TIME and
    store it locally.  You will want to refer to this quantity elsewhere in your
    search problem definition.  
    
    You may add anything to this method that you see fit.  Look in pacman.py for
    functions that give you relevant information about a GameState.
    """
    from pacman import SCARED_TIME
    self.safeTime = SCARED_TIME # The number of moves that a capsule lasts
    
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def getStartState(self):
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def isGoalState(self, state):
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
   
  def getSuccessors(self, state):
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
