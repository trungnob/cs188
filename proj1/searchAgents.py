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
Walls=[]
listTransverse=[]
listMahantan=[]
totalPath=0
startHeuristic=0
class GoWestAgent(Agent):
  """
  An agent that goes West until it can't.
  """
  def getAction(self, state):
    """
      The agent receives a GameState (pacman.py).
    """
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP
    
#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py and      #
#           complete the SearchAgent class            #
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
    
    gameState: A GameState object (pacman.py)
    costFn: A function from a search state (tuple) to a non-negative number
    goal: A position in the gameState
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

  def getCostOfActions(self, actions):
    """Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999"""
    if not actions:
      return 999999
    x,y= self.getStartState()
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += self.costFn((x,y))
    return cost
    
  
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
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.
    
    state: a GameState object (pacman.py)
    """
    if self.searchFunction == None:
      import sys
      print "No search function provided for SearchAgent"
      sys.exit(1)

    # If you wrap your solution in the timing code provided, you'll know how long the pathfinding takes.
    starttime = time.time()
    "*** YOUR CODE HERE ***"
    print('This is state 0')
    print(state)
    print('---Start Finding Solutions-------')
    problem =self.searchType(state)
    self.actions=self.searchFunction(problem);
    
     
    print 'Path found with total cost of %d in %.1f seconds' % (problem.getCostOfActions(self.actions), time.time() - starttime)
    
    
  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier (in registerInitialState).  Return
    Directions.STOP if there is no further action to take.
    
    state: a GameState object (pacman.py)
    """
    "*** YOUR CODE HERE ***"
    if 'actionsIter' not in dir(self): 
        self.actionsIter=0;
    
    if self.actionsIter< len(self.actions):
        nextAct=self.actions[self.actionsIter]
        self.actionsIter+=1 
    else: 
        nextAct=Directions.STOP
    return nextAct;
    
    util.raiseNotDefined()
      
class TinyMazeSearchAgent(SearchAgent):
  """
  An agent which uses tinyClassSearch to find a path (which only returns a
  correct path for tinyMaze) and follows that path.
  """
  def __init__(self):
    SearchAgent.__init__(self, search.tinyMazeSearch)  


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
  food (dots) in a Pacman game.
  
  A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
    pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
    foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food 
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

  def getCostOfActions(self, actions):
    """Returns the cost of a particular sequence of actions.  If those actions
    include an illegal move, return 999999"""
    x,y= self.getStartState()[0]
    cost = 0
    for action in actions:
      # Check figure out the next state and see whether its' legal
      dx, dy = Actions.directionToVector(action)
      x, y = int(x + dx), int(y + dy)
      if self.walls[x][y]:
        return 999999
      cost += 1
    return cost
     
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

def trivialFoodHeuristic(state):
  """
   A trivial heuristic for the all-food problem,  which returns 0 for goal states and 1 otherwise.
  """
  if(state[1].count() == 0):
    return 0
  else:
    return 1

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
  #global  listTransverse,listMahantan,totalPath,startHeuristic
  #print(gameState)
  #Walls=gameState.getWalls()
  #print(Walls)
  #state=(gameState.getPacmanPosition(),gameState.getFood())
  #listTransverse,listMahantan,totalPath=buildListFood(state)
  #startHeuristic=totalPath
  return foodHeuristic
def someFunction(gamestate,state):
    print(gameState)
    return  
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
  
  
  return myFunc6(state)
def myFunc(state):
    PMpos=state[0]
    foodGrid=state[1]
    if foodGrid.count()<3:
        return findFoods(PMpos,3,foodGrid)
    else:
        return findFoods(PMpos,3,foodGrid)
def buildGraph(foodGrid):
    V=set()
    E=set() 
    listFood=foodGrid.asList()
    while len(listFood)!=0:
        verTex=listFood.pop()
        V.add(verTex)
        for restVertex in listFood:
            W=manhattanDistance(verTex,restVertex)
            pair =(verTex,restVertex)
            E.add((pair,W))
    return (E,V)
def buildListFood(state):
    PMpos=state[0]
    foodGrid=state[1]
    listFood=foodGrid.asList()
    returnList=[]
    listDistance=[]
    startAt=PMpos
    totalpath=0
    #if len(listFood)<=5: return (listFood,[],len(listFood))
    while len(listFood)>0 :
        closestFood=listFood[0]
        min=manhattanDistance(startAt,listFood[0])
        for food in listFood:
            if  (manhattanDistance(startAt,food)<=min):
                min=manhattanDistance(startAt,food)
                closestFood=food
        returnList.append(closestFood)
        listFood.remove(closestFood)
        startAt=closestFood
        totalpath+=min
        listDistance.append(min)
    return (returnList,listDistance,totalpath)
def myFunc6(state):
    listTransverse,listMahantan,totalPath=buildListFood(state)
    if state[1].count() ==0 : return 0
    return totalPath
def myFunc5(state):
    global listTransverse
    global totalPath
    global listManhantan
    global startHeuristic
    savetotalPath=totalPath
    PMpos=state[0]
    foodGrid=state[1]
    if len(listTransverse)==0: return 0
    else:
        totalPath-=listMahantan[0]
        totalPath+=manhattanDistance(PMpos,listTransverse[0])
    food=listTransverse[0]
    x=food[0]
    y=food[1]
    if (foodGrid[x][y]==False): listTransverse.remove(listTransverse[0])
    return totalPath
    
def mst(G):
    E=G[0]
    V=G[1]
    n=len(E)
    mst_Tree=set()
    
               
def myFunc2(state):
    PMpos=state[0]
    foodGrid=state[1]
    if foodGrid.count()==0: return 0;
    return sumDistance(foodGrid,PMpos)/foodGrid.count()
def myFunc3(state):
    PMpos=state[0]
    foodGrid=state[1]
    return getClosestFood(PMpos,foodGrid)
def myFunc4(state):
    PMpos=state[0]
    foodGrid=state[1]
    return lookAhead(foodGrid,PMpos,3)+foodGrid.count()-1
def sumDistance(grid,pos):
    sum=0
    L=grid.height
    W=grid.width
    for i in range(0,W):
        for j in range(0,L):
            if grid[i][j] : 
                sum+=manhattanDistance((i,j),pos)
    return sum
def lookAheadWest(grid,pos,numStep):
    X=pos[0]
    Y=pos[1]
    count=0
    if (X-numStep<0): XLowLimit=0
    else: XLowLimit=X-numStep
    if (X+numStep>grid.width): XHighLimit=grid.width
    else : XHighLimit=X+numStep
    for i in range(X-1,XLowLimit,-1):
        count+=1
        if grid[i][Y]:
            return count         
    return None
def lookAheadEast(grid,pos,numStep):
    X=pos[0]
    Y=pos[1]
    count=0
    if (X-numStep<0): XLowLimit=0
    else: XLowLimit=X-numStep
    if (X+numStep>grid.width): XHighLimit=grid.width
    else : XHighLimit=X+numStep
    for i in range(X+1,XHighLimit,+1):
        count+=1
        if grid[i][Y]:
            return count         
    return None
def lookAheadNorth(grid,pos,numStep):
    X=pos[0]
    Y=pos[1]
    count=0
    if (Y-numStep<0): YLowLimit=0
    else: YLowLimit=Y-numStep
    if (Y+numStep>grid.height): YHighLimit=grid.height
    else : YHighLimit=Y+numStep
    for i in range(Y+1,YHighLimit,+1):
        count+=1
        if grid[X][i]:
            return count         
    return None

def lookAheadSouth(grid,pos,numStep):
    X=pos[0]
    Y=pos[1]
    count=0
    if (Y-numStep<0): YLowLimit=0
    else: YLowLimit=Y-numStep
    if (Y+numStep>grid.height): YHighLimit=grid.height
    else : YHighLimit=Y+numStep
    for i in range(Y-1,YLowLimit,-1):
        count+=1
        if grid[X][i]:
            return count         
    return None
def lookAhead(grid,pos,numStep):
    lan= lookAheadNorth(grid, pos, numStep)
    if lan!=None: return lan
    law=lookAheadWest(grid,pos,numStep)
    if law!=None:return law
    las=lookAheadSouth(grid,pos,numStep)
    if las!=None:return las
    lae=lookAheadEast(grid,pos,numStep)
    if lae!=None:return lae
    return grid.count();
    
def sumDistance2(grid,pos):
    sumi=0
    sumj=0
    L=grid.height
    W=grid.width
    for i in range(0,W):
        for j in range(0,L):
            if grid[i][j] : 
                sumi+=i
                sumj+=j
    ai=sumi/grid.count()
    aj=sumj/grid.count()
    return manhattanDistance(pos,(ai,aj))

def getClosestFood(pos,foodGrid):
    for i in range(1,max(foodGrid.height,foodGrid.width)):
        foodFind=findFoodInRad(pos,i,foodGrid)
        if foodFind==None: continue
        else:
            return   manhattanDistance(pos,foodFind)
            
    return 0

def findFoodInRad(pos,rad,grid):
    count=0
    posx,posy=pos
    listFoods=[]
    limitOnX=grid.width
    limitOnY=grid.height
    if posx-rad <=0:
        startXAt=0
    else: 
        startXAt=posx-rad
    if posy-rad <=0:
        startYAt=0
    else: 
        startYAt=posy-rad    
    if posx+rad>=limitOnX:
        endX=limitOnX
    else:
        endX=posx+rad
    if posy+rad>=limitOnY:
        endX=limitOnY
    else:
        endX=posy+rad
    for i in range(startXAt,limitOnX-1):
        for j in range(startYAt,limitOnY-1):
          if grid[i][j]:
              return (i,j)     
    return None
def findFoods(pos,rad,grid):
    count=0
    posx,posy=pos
    listFoods=[]
    limitOnX=grid.width
    limitOnY=grid.height
    if posx-rad <=0:
        startXAt=0
    else: 
        startXAt=posx-rad
    if posy-rad <=0:
        startYAt=0
    else: 
        startYAt=posy-rad    
    if posx+rad>=limitOnX:
        endX=limitOnX
    else:
        endX=posx+rad
    if posy+rad>=limitOnY:
        endX=limitOnY
    else:
        endX=posy+rad
    for i in range(startYAt,limitOnY-1):
        for j in range(startXAt,limitOnX-1):
          if grid[j][i]:
              count+=1 
              listFoods.append((j,i))      
    return ((grid.count()-count),listFoods)    
         
    
class AStarFoodSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using AStar.
  
  You should use either foodHeuristic or getFoodHeuristic in your code here.
  """
  def __init__(self,searchFunction= None  ,searchType=FoodSearchProblem):
    self.searchType=searchType  
   
    self.searchFunction=lambda x: search.aStarSearch(x, getFoodHeuristic(None))
    SearchAgent.__init__(self, self.searchFunction,self.searchType)  
    
  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board. Here, we
    choose a path to the goal.  In this phase, the agent should compute the path to the
    goal and store it in a local variable.
    
    state: a GameState object (pacman.py)
    """
    if self.searchFunction == None:
      import sys
      print "No search function provided for SearchAgent"
      sys.exit(1)

    # If you wrap your solution in the timing code provided, you'll know how long the pathfinding takes.
    starttime = time.time()
    "*** YOUR CODE HERE ***"
    print('This is state 0')
    print(state)
    print(state.getPacmanPosition())
    print(state.getFood())
    print('---Start Finding Solutions-------')
    problem =self.searchType(state)
    
    self.searchFunction=lambda x: search.aStarSearch(x, getFoodHeuristic(state))
    self.actions=self.searchFunction(problem);
    
     
    print 'Path found with total cost of %d in %.1f seconds' % (problem.getCostOfActions(self.actions), time.time() - starttime)
   

class GreedyFoodSearchAgent(SearchAgent):
  """
  An agent that computes a path to eat all the dots using greedy search.
  """
  "*** YOUR CODE HERE ***"
  
  


class TrivialAStarFoodSearchAgent(AStarFoodSearchAgent):
  """
  An AStarFoodSearchAgent that uses the trivial heuristic instead of the one defined by getFoodHeuristic
  """
  def __init__(self, searchFunction=None, searchType=FoodSearchProblem):
    # Redefine getFoodHeuristic to return the trivial one.
    __import__(__name__).getFoodHeuristic = lambda gameState: trivialFoodHeuristic
    __import__(__name__).foodHeuristic    = trivialFoodHeuristic
    AStarFoodSearchAgent.__init__(self, searchFunction, searchType)
