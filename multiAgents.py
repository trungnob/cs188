from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change it
    in any way you see fit.
  """
  
    
  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.
    
    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()
    
    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices)
    
    "Add more of your code here if you want to"
    print(chosenIndex)
    print(legalMoves)
    print(legalMoves[chosenIndex])
    return legalMoves[chosenIndex]
  
  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here. 
    
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.
    """
    # Useful information you can extract from a GameState (pacman.py)
    returnScore=float(0)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanState().getPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates() 
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    "*** YOUR CODE HERE ***"
    foodList=oldFood.asList()
   
    foodList.sort(lambda x,y: util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))
    foodScore=util.manhattanDistance(newPos, foodList[0])
    #print(dir(newGhostStates[0]))
    GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates]
    if len(GhostPositions) ==0 : GhostScore=0
    else: 
        GhostPositions.sort(lambda x,y: disCmp(x,y,newPos))
        if util.manhattanDistance(newPos, GhostPositions[0])==0: return -99 
        else:
            GhostScore=2*-1.0/util.manhattanDistance(newPos, GhostPositions[0])
    if foodScore==0: returnScore=2.0+GhostScore
    else: returnScore=GhostScore+1.0/float(foodScore)
    print('GhostScore')
    print(GhostScore)
    print('FoodScore')
    print(foodScore)
    print('ReturnScore:')
    print(returnScore)
    return returnScore
def disCmp(x,y,newPos):
    if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))<0: return -1
    else: 
        if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))>0: return 1
        else:
            return 0
def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This abstract class** provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    
    **An abstract class is one that is not meant to be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.  
  """
  
  def __init__(self, evalFn = scoreEvaluationFunction):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = evalFn
  def setDepth(self, depth):
    """
      This is a hook for feeding in command line argument -d or --depth
    """
    self.depth = depth # The number of search plies to explore before evaluating
    
  def useBetterEvaluation(self):
    """
      This is a hook for feeding in command line argument -b or --betterEvaluation
    """
    print("I was here")
    betterEvaluationFunction.firstCalled=True;
    self.evaluationFunction = betterEvaluationFunction
    

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth 
      and self.evaluationFunction.
    """
    "*** YOUR CODE HERE ***"
    numOfAgent=gameState.getNumAgents();
    trueDepth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
    listNextStates=[gameState.generateSuccessor(0,action) for action in LegalActions ]
    #print(self.MiniMax_Value(numOfAgent,0,gameState,trueDepth))
    v=[self.MiniMax_Value(numOfAgent,1,nextGameState,trueDepth-1) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    i = random.randint(0,len(listMax)-1)
    
    print(LegalActions)
    print(v)
    print(listMax)
    action=LegalActions[listMax[i]]
    return action

  def MiniMax_Value(self,numOfAgent,agentIndex, gameState, depth):
      LegalActions=gameState.getLegalActions(agentIndex)
      listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in LegalActions ]
      if (gameState.isLose() or gameState.isWin() or depth==0): 
              return self.evaluationFunction(gameState)
      else:
          if (agentIndex==0):
              return max([self.MiniMax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
          else :
              return min([self.MiniMax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates])

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def Alpha_Beta_Value(self, numOfAgent, agentIndex, gameState, depth, alpha, beta):
      LegalActions=gameState.getLegalActions(agentIndex)
      listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in LegalActions ]
      
      # terminal test      
      if (gameState.isLose() or gameState.isWin() or depth==0): 
              return self.evaluationFunction(gameState)
      else:
          # if Pacman
          if (agentIndex == 0):
              v=-1e308
              for nextState in listNextStates:
                  v = max(self.Alpha_Beta_Value(numOfAgent, (agentIndex+1)%numOfAgent, nextState, depth-1, alpha, beta), v)
                  if (v >= beta):
                      return v
                  alpha = max(alpha, v)
              return v
          # if Ghost
          else:
              v=1e308
              for nextState in listNextStates:
                  v = min(self.Alpha_Beta_Value(numOfAgent, (agentIndex+1)%numOfAgent, nextState, depth-1, alpha, beta), v)
                  if (v <= alpha):
                      return v
                  beta = min(beta, v)
              return v
              
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    numOfAgent=gameState.getNumAgents();
    trueDepth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    
    # remove stop action from list of legal actions
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
    
    listNextStates = [gameState.generateSuccessor(0,action) for action in LegalActions ]
    
    # check whether minimax value for -l minimaxClassic are 9, 8 , 7, -492
    # print(self.Alpha_Beta_Value(numOfAgent,0,gameState,trueDepth))
    
    # as long as beta is above the upper bound of the eval function
    v = [self.Alpha_Beta_Value(numOfAgent,1,nextGameState,trueDepth-1, -1e308, 1e308) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    i = random.randint(0,len(listMax)-1)
    
    print(LegalActions)
    print(v)
    print(listMax)
    action=LegalActions[listMax[i]]
    return action

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def Expectimax_Value(self,numOfAgent,agentIndex, gameState, depth):
      LegalActions=gameState.getLegalActions(agentIndex)
      listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in LegalActions ]
      if (gameState.isLose() or gameState.isWin() or depth==0): 
              return self.evaluationFunction(gameState)
      else:
          if (agentIndex==0):
              return max([self.Expectimax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
          else :
              listStuff=[self.Expectimax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates]
              return sum(listStuff)/len(listStuff)

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction
      
      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    numOfAgent=gameState.getNumAgents();
    trueDepth=numOfAgent*self.depth
    LegalActions=gameState.getLegalActions(0)
    if Directions.STOP in LegalActions: 
        LegalActions.remove(Directions.STOP)
    listNextStates=[gameState.generateSuccessor(0,action) for action in LegalActions ]
    #print(self.Expectimax_Value(numOfAgent,0,gameState,trueDepth))
    v=[self.Expectimax_Value(numOfAgent,1,nextGameState,trueDepth-1) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    i = random.randint(0,len(listMax)-1)
    
    print(LegalActions)
    print(v)
    print(listMax)
    action=LegalActions[listMax[i]]
    return action

def actualGhostDistance(gameState, ghostPositions):
    from game import Directions
    from game import Actions
    visited = {}
    startPosition = gameState.getPacmanPosition()
    fringe = util.FasterPriorityQueue()
    ghost_fringe = util.FasterPriorityQueue()
    for ghost in ghostPositions:
        ghost_fringe.push(ghost, util.manhattanDistance(ghost, startPosition))
    curDist = 0
    fringe.push(startPosition, curDist)
    visited[startPosition] = True
    
    walls    = gameState.getWalls()
    foodGrid = gameState.getFood()
    isFood   = lambda(x, y): foodGrid[x][y]
    isGhost  = lambda(x, y): (x, y) in ghostPositions
    GhostList = []
    while not ghost_fringe.isEmpty():
        curGhost = ghost_fringe.pop()
        while not fringe.isEmpty():
            curState = fringe.pop()
            # if goal state is found return the distance
            if (curState == curGhost):
                #print "returned: %d" % curDist
                GhostList = GhostList + [curDist]
                break
            curDist = curDist + 1
            for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
                x,y = curState
                dx, dy = Actions.directionToVector(action)
                nextx, nexty = int(x + dx), int(y + dy)
                nextState = (nextx, nexty)
                if ((not walls[nextx][nexty]) and (nextState not in visited)):
                    thisDist = curDist + util.manhattanDistance(curGhost, nextState)
                    visited[nextState] = True
                    fringe.push(nextState, thisDist)
    return GhostList

def actualFoodDistance(gameState, targetFood):
    from game import Directions
    from game import Actions
    visited = {}
    startPosition = gameState.getPacmanPosition()
    fringe = util.FasterPriorityQueue()
    curDist = 0
    fringe.push(startPosition, curDist)
    visited[startPosition] = True
    
    walls    = gameState.getWalls()
    foodGrid = gameState.getFood()
    isFood   = lambda(x, y): foodGrid[x][y]
    #isGhost  = lambda(x, y): (x, y) in ghostPositions
    
    while not fringe.isEmpty():
        curState = fringe.pop()
        # if goal state is found return the distance
        if (isFood(curState)):
            #print "returned: %d" % curDist
            return (curState, curDist)
            break
        # if you find a ghost before you find your closest food!! you are screwed =(
        #if (isGhost(curState)):
        #    ghostInRange = True
        curDist = curDist + 1
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = curState
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            nextState = (nextx, nexty)
            if ((not walls[nextx][nexty]) and (nextState not in visited)):
                thisDist = curDist + util.manhattanDistance(targetFood, nextState)
                visited[nextState] = True
                fringe.push(nextState, thisDist)    
    return None

class Node:
    def __init__(self, state, walls, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.walls = walls
        if parent:
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            self.path_cost = path_cost
            self.depth = 0
    
    def giveNodePath(self):
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result.reverse()
      
    def path(self):
      states, actions, cost = [], [], 0.0
      CurrentNode = self
      cost = CurrentNode.path_cost
      while CurrentNode.parent:
        states = [CurrentNode.state] + states
        actions = [CurrentNode.action] + actions
        CurrentNode = CurrentNode.parent
      return actions
    
    def expand(self, problem):
        return [Node(next, self, act, cost)
          for (next,act,cost) in getSuccessors(self.state.getPacmanPosition(), self.walls, )]

def getSuccessors(self, state, walls, costFn):
    successors = []
    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
      x,y = state
      dx, dy = Actions.directionToVector(action)
      nextx, nexty = int(x + dx), int(y + dy)
      if not walls[nextx][nexty]:
        nextState = (nextx, nexty)
        cost = self.costFn(nextState)
        successors.append((nextState, action, cost))
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
    return successors

def myGraphSearch(gameState, fringe, g, h):
  visited = {}
  startnode = Node(gameState.getPacmanPosition(), gameState.getWalls())
  if g or h:
    fringe.push(startnode, g(startnode) + h(startnode.state))
  else:
    fringe.push(startnode)
  while not fringe.isEmpty():
    node = fringe.pop()
    foodGrid = gameState.getFood()
    isFood   = lambda(x, y): foodGrid[x][y]
    if (isFood(node.state)):
    #if problem.isGoalState(node.state): 
      return node.path()
    if node.state not in visited:
      visited[node.state] = True
      for nextnode in node.expand(node):
        if g or h:
          fringe.push(nextnode, g(nextnode) + h(nextnode.state))
        else:
          fringe.push(nextnode)
  return None

def truePathCost(node):
  return node.path_cost
  
def nullHeuristic(state):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided searchProblem.  This one is trivial.
  """
  return 0

def betterEvaluationFunction(currentGameState):
      """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).
    
        DESCRIPTION: <write something here so we know what you did>
      """
      if (betterEvaluationFunction.firstCalled): 
          #This indicates the function whether first called or not
          #use this to initialize any variable which you wish don't do this again and again
          print "betterEvaluationFunction is at first Called"
      if currentGameState.isLose():
          return -1e308
      if currentGameState.isWin() : 
          return 1e308          
      returnScore= 0.0
      newPos = currentGameState.getPacmanState().getPosition()
      GhostStates = currentGameState.getGhostStates()
      GhostStates.sort(lambda x,y: disCmp(x.getPosition(),y.getPosition(),newPos))
      GhostPositions = [Ghost.getPosition() for Ghost in GhostStates]
      newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
      closestGhost=GhostStates[0]
      closestGhostDistance=util.manhattanDistance(GhostStates[0].getPosition(), newPos)
      capsules = currentGameState.getCapsules()
      #print "%d" % len(capsules)

      FoodList = currentGameState.getFood().asList()
      minPos = FoodList[0]
      min = util.manhattanDistance(minPos, newPos)
      for food in FoodList:
        curDist = util.manhattanDistance(food, newPos)
        if (curDist < min):
            min = curDist
            minPos = food
      
      #actualGhostList = actualGhostDistance(currentGameState, GhostPositions)
      actualActions = myGraphSearch(currentGameState, util.PriorityQueue(), truePathCost, lambda(Pos):util.manhattanDistance(Pos, minPos))
      # for any centers of mass created by any two ghosts will be recorded
      # the closest one from Pacman will be noted and a special weight will be assigned.
      allTwoGhosts = allCombo(GhostPositions)
      centerOfGhosts = []
      for pair in allTwoGhosts:
          g1, g2 = pair
          x = (g1[0] + g2[0])/2
          y = (g1[1] + g2[1])/2
          centerOfGhosts = centerOfGhosts + [(x,y)]
      centerDistOfGhosts = [util.manhattanDistance(center, newPos) for center in centerOfGhosts]
      #fearful = min(centerDistOfGhosts)
      
      # all ghost distances from Pacman
      allDistOfGhosts = [util.manhattanDistance(Pos, newPos) for Pos in GhostPositions]
      crisis = sum(allDistOfGhosts)
      
      wFood, wGhost, wScaredGhost       = [2.0, -4.0, 4.0];
      #if (closestGhostDistance > 3):#Ghost too far ignore Ghost
      if (closestGhostDistance > 1):
         if (closestGhost.scaredTimer > 3):
            wFood, wGhost, wScaredGhost = [2.0, -0.0, 4.0];
         else:
            wFood, wGhost, wScaredGhost = [2.0, -0.0, 4.0];
      #if (ghostInRange and closestFoodDistance < 5): 
      #   wFood, wGhost, wScaredGhost    = [2.0, -5.0, 4.0];
      # you are gonna die anyway, why not die fat
      #if (fearful < 3 and crisis < (currentGameState.getNumAgents()-1)*3):
      #   wFood, wGhost, wScaredGhost    = [9.0, -7.0, 9.0];   
      if (closestGhost.scaredTimer > 3):
          returnScore = wFood/closestFoodDistance+wScaredGhost/closestGhostDistance+currentGameState.getScore()
      else: 
          returnScore=wFood/closestFoodDistance+wGhost/closestGhostDistance+currentGameState.getScore()
      betterEvaluationFunction.firstCalled = False;
      return returnScore

def allCombo(myList):
    all = []
    if len(myList) == 0:
        return []
    head = myList.pop()
    for i in myList:
        all = all + [(head, i)]
    return all + allCombo(myList)

DISTANCE_CALCULATORS = {}
