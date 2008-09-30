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
    GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates]
    if len(GhostPositions) ==0 : GhostScore=0
    else: 
        # Sort ghost by their distances from Pacman
        GhostPositions.sort(lambda x,y: disCmp(x,y,newPos))
        if util.manhattanDistance(newPos, GhostPositions[0])==0: return -99 
        else:
            GhostScore=2*-1.0/util.manhattanDistance(newPos, GhostPositions[0])
    if foodScore==0: returnScore=2.0+GhostScore
    else: returnScore=GhostScore+1.0/float(foodScore)
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
    betterEvaluationFunction.NumOriginal=0;
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
    
    # Max of all miniMax Values
    v=[self.MiniMax_Value(numOfAgent,1,nextGameState,trueDepth-1) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    
    # obtain the index of MaxV
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    # random when there is a tie
    i = random.randint(0,len(listMax)-1)
    action=LegalActions[listMax[i]]
    return action

  def MiniMax_Value(self,numOfAgent,agentIndex, gameState, depth):
      LegalActions=gameState.getLegalActions(agentIndex)
      listNextStates=[gameState.generateSuccessor(agentIndex,action) for action in LegalActions ]
      # terminal state is whether the final depth is reached or Pacman dies or loses
      if (gameState.isLose() or gameState.isWin() or depth==0): 
              return self.evaluationFunction(gameState)
      else:
          # if it's Pacman then it's a max layer
          if (agentIndex==0):
              return max([self.MiniMax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
          # else if it's a ghost, then it's a min layer
          else :
              return min([self.MiniMax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates])

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def Alpha_Beta_Value(self, numOfAgent, agentIndex, gameState, depth, alpha, beta):
      LegalActions=gameState.getLegalActions(agentIndex)
      if (agentIndex==0): 
         if Directions.STOP in LegalActions: 
             LegalActions.remove(Directions.STOP)
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
                  if (v <=  alpha):
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
    # as long as beta is above the upper bound of the eval function
    v = [self.Alpha_Beta_Value(numOfAgent,1,nextGameState,trueDepth-1, -1e307, 1e307) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    # random when there is a tie    
    i = random.randint(0,len(listMax)-1)
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
          # if it's Pacman then it's a max node
          if (agentIndex==0):
              return max([self.Expectimax_Value(numOfAgent,(agentIndex+1)%numOfAgent,nextState,depth-1) for nextState in listNextStates] )
          # if it's a Ghost then it's a chance node
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
    v=[self.Expectimax_Value(numOfAgent,1,nextGameState,trueDepth-1) for nextGameState in listNextStates] 
    MaxV=max(v)
    listMax=[]
    for i in range(0,len(v)):
        if v[i]==MaxV:
             listMax.append(i)
    # random when there is a tie
    i = random.randint(0,len(listMax)-1)
    action=LegalActions[listMax[i]]
    return action

# Obtain actual ghost distance using A* Search with Heuristic function equals the manhanttan distance
def actualGhostDistance(gameState, ghostPosition):
    from game import Directions
    from game import Actions
    visited = {}
    ghostPosition=util.nearestPoint(ghostPosition)
    curState=startPosition = gameState.getPacmanPosition()
    fringe = util.FasterPriorityQueue()
    Hvalue=util.manhattanDistance(startPosition,ghostPosition)
    curDist=0;
    priorityVal=Hvalue+curDist
    fringe.push(tuple((startPosition,curDist)), priorityVal)
    visited[startPosition] = True
    walls    = gameState.getWalls()
    foodGrid = gameState.getFood()
    isFood   = lambda(x, y): foodGrid[x][y]

    while not fringe.isEmpty():
        curState,curDist = fringe.pop()
        
        # terminal test: if the position has a ghost
        if (curState==ghostPosition):
            return (curState, curDist)
            break

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = curState
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            nextState = (nextx, nexty)
            if ((not walls[nextx][nexty]) and (nextState not in visited)):
                newcurDist = curDist + 1
                priorityVal=util.manhattanDistance(nextState,ghostPosition)+newcurDist
                visited[nextState] = True
                fringe.push(tuple((nextState,newcurDist)), priorityVal)    
    return (curState,curDist)

# Obtain actual food distance using A* Search with Heuristic function equals the manhanttan distance
def actualFoodDistance(gameState, targetFood):
    from game import Directions
    from game import Actions
    visited = {}
    curState=startPosition = gameState.getPacmanPosition()
    fringe = util.FasterPriorityQueue()
    Hvalue=util.manhattanDistance(startPosition,targetFood)
    curDist=0;
    priorityVal=Hvalue+curDist
    fringe.push(tuple((startPosition,curDist)), priorityVal)
    visited[startPosition] = True
    walls    = gameState.getWalls()
    foodGrid = gameState.getFood()
    isFood   = lambda(x, y): foodGrid[x][y]
    while not fringe.isEmpty():
        curState,curDist = fringe.pop()
        
        # terminal test: if you found the food
        if (curState==targetFood):
            return (curState, curDist)
            break
      
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = curState
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            nextState = (nextx, nexty)
            if ((not walls[nextx][nexty]) and (nextState not in visited)):
                newcurDist = curDist + 1
                priorityVal=util.manhattanDistance(nextState,targetFood)+newcurDist
                visited[nextState] = True
                fringe.push(tuple((nextState,newcurDist)), priorityVal)    
    return (curState,curDist)

def betterEvaluationFunction(currentGameState):
      """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).
    
        DESCRIPTION: Simple Idea but very impressive performance. (read inline)
      """
      if (betterEvaluationFunction.firstCalled): 
          #This indicates the function whether first called or not
          #use this to initialize any variable which you wish don't do this again and again
          betterEvaluationFunction.NumOrginal=currentGameState.getFood().count()
          print "betterEvaluationFunction is at first Called"
      if currentGameState.isLose():
          return -1e307
      if currentGameState.isWin() : 
          return 1e307         
      returnScore= 0.0
      newPos = currentGameState.getPacmanState().getPosition()
      
      # Obtain all ghost positions on the board
      GhostStates = currentGameState.getGhostStates()
      GhostStates.sort(lambda x,y: disCmp(x.getPosition(),y.getPosition(),newPos))
      GhostPositions = [Ghost.getPosition() for Ghost in GhostStates]
      
      # Obtain scared Ghosts informations
      newScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
      closestGhost=GhostStates[0]
      
      # Sort the food list and find the closest food to Pacman
      FoodList = currentGameState.getFood().asList()
      minPos = FoodList[0]
      minDist = util.manhattanDistance(minPos, newPos)
      for food in FoodList:
         curDist = util.manhattanDistance(food, newPos)
         if curDist==1 : 
             minPos=food
             minDist=curDist
             break
         if (curDist < minDist):
             minDist = curDist
             minPos = food  
             
      # Find the actual distance to that food
      targetFoodPosition, closestFoodDistance = actualFoodDistance(currentGameState, minPos)
      
      # Find the actual distance to the closest Scared Ghost and the closest Normal Ghost 
      closestScaredGhostDist=1e307
      closestScaredGhost=None
      closestNormalGhostDist=1e307
      closestNormalGhost=None
      allScaredGhost=[Ghost for Ghost in GhostStates if Ghost.scaredTimer>0]
      allRealScaredGhostDistance=[actualGhostDistance(currentGameState,Pos) for Pos in [ScaredGhost.getPosition() for ScaredGhost in allScaredGhost]]
      allDistScaredGhosts=[Ghost[1] for Ghost in allRealScaredGhostDistance]
      if len(allDistScaredGhosts)!=0:
          closestScaredGhostDist=min(allDistScaredGhosts)
          closestScaredGhost=allScaredGhost[allDistScaredGhosts.index(closestScaredGhostDist)]
      allNormalGhost=[Ghost for Ghost in GhostStates if Ghost.scaredTimer<=0]
      allRealNormalGhostDistance=[actualGhostDistance(currentGameState,Pos) for Pos in [NormalGhost.getPosition() for NormalGhost in allNormalGhost]]
      allDistNormalGhosts=[Ghost[1] for Ghost in allRealNormalGhostDistance]
      if len(allDistNormalGhosts)!=0:
          closestNormalGhostDist=min(allDistNormalGhosts)
          closestNormalGhost=allNormalGhost[allDistNormalGhosts.index(closestNormalGhostDist)]
      
      # Default weights on Food, Normal Ghost, Scared Ghost
      wFood, wGhost, wScaredGhost       = [2.0, -6.0, 4.0];
      
      # if the closest ghost ate Pacman
      if (closestNormalGhostDist==0):
          return -1e307
      if (closestScaredGhostDist==0):
          closestScaredGhostDist=0.1
          
      # if the closest normal ghost is further away than 2 steps
      # different weights are assigned whether they are < 7, or < 12
      # of whether it is possible to eat a scared ghost before it recovers
      if (closestNormalGhostDist > 2):
        if closestScaredGhost!=None:
          if (closestScaredGhostDist<closestScaredGhost.scaredTimer):
            if(closestScaredGhostDist<7):
              wFood, wGhost, wScaredGhost= [0.0, -0.0,10.0];
            else:
              if(closestScaredGhostDist<12):
                wFood, wGhost, wScaredGhost= [3.0, 0.0, 8.0]; 
              else :
                wFood, wGhost, wScaredGhost= [3.0, 0.0, 0.0];    
          else:
               wFood, wGhost, wScaredGhost = [4.0, -0.0, 0.0];
        else :
               wFood, wGhost, wScaredGhost = [4.0, -0.0, 0.0];     
      else:
          if (closestScaredGhostDist<5):
              if (closestScaredGhost.scaredTimer>5):
               wFood, wGhost, wScaredGhost= [1.0, -6.0, 4.0];
              else:
               wFood, wGhost, wScaredGhost= [1.0, -6.0, -3.0]; 
          else:
              wFood, wGhost, wScaredGhost= [1.0, -6.0, 1.0];
      # if there are only a few food left there should be more weights on food
      if len(FoodList) < 3   :
          wFood, wGhost, wScaredGhost= [6.0, -8.0, 0.0];
      else: 
         if len(FoodList) < 2:
             wFood, wGhost, wScaredGhost= [10.0, -8.0, 0.0];
      returnScore=(wFood/(closestFoodDistance)+(wGhost)/closestNormalGhostDist+(wScaredGhost)/(closestScaredGhostDist))+currentGameState.getScore()
      betterEvaluationFunction.firstCalled=False;
      return returnScore

DISTANCE_CALCULATORS = {}
