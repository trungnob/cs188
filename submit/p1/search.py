import util
## Abstract Search Classes

class SearchProblem:
  """
  Abstract SearchProblem class. Your classes
  should inherit from this class and override 
  all the methods below
  """
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze"""
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first. [p 74].
  
  Your search algorithm needs to return a 3-item tuple (path, actions, totalcost)
    path: a list of states in the search problem from start to goal
    actions: the sequence of actions that reaches the goal
    totalcost: the total cost of the path
    
  Of course, the actions are the most important by far; we will use these
  to determine the correctness of your algorithm.
  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  visitedStates=set()
  fringe=util.Stack()
  listActions=[];
  state=problem.getStartState()
  cost=0;
  node=stateNode(state)
  fringe.push(node)
  while (1):
      if fringe.isEmpty(): return None
      node=fringe.pop()
      state,listActions,cost=node.state,node.listActions,node.cost
      if problem.isGoalState(state):
          return listActions
      if state not in visitedStates:
              visitedStates.add(state)
              listSucessors=problem.getSuccessors(state);
              saveCost=cost
              for sucFn in listSucessors:
                  nxtState, nxtAction, newCost=sucFn
                  cost=saveCost 
                  newListActions=list(listActions)
                  newListActions.append(nxtAction)
                  cost+=newCost
                  newNode=stateNode(nxtState,newListActions,cost)
                  fringe.push(newNode)
      
    
    
      

def breadthFirstSearch(problem):
  from game import Directions
  visitedStates=set()
  fringe=util.Queue()
  listActions=[];
  state=problem.getStartState()
  cost=0;
  node=stateNode(state)
  fringe.push(node)
  visitedStates.add(state)
  while (1):
      if fringe.isEmpty(): return None
      node=fringe.pop()
      state,listActions,cost=node.state,node.listActions,node.cost
      if problem.isGoalState(state):
          return listActions
      listSucessors=problem.getSuccessors(state);
      saveCost=cost 
      for sucFn in listSucessors:
          nxtState, nxtAction, newCost=sucFn
          cost=saveCost 
          if nxtState not in visitedStates:
              visitedStates.add(nxtState)
              newListActions=[]
              for stuffs in listActions: 
                newListActions.append(stuffs)
              newListActions.append(nxtAction)
              cost+=newCost
              newNode=stateNode(nxtState,newListActions,cost)
              fringe.push(newNode)
              
def uniformCostSearch(problem):
  from game import Directions

  visitedStates=set()
  fringe=util.PriorityQueue()
  listActions=[];
  state=problem.getStartState()
  cost=0;
  node=stateNode(state)
  fringe.push(node,cost)
  while (1):
      if fringe.isEmpty(): return None
      node=fringe.pop()
      state,listActions,cost=node.state,node.listActions,node.cost
      if problem.isGoalState(state):
          return listActions
      if state not in visitedStates:
              visitedStates.add(state)
              listSucessors=problem.getSuccessors(state);
              saveCost=cost
              for sucFn in listSucessors:
                  nxtState, nxtAction, newCost=sucFn
                  cost=saveCost 
                  newListActions=list(listActions)
                  newListActions.append(nxtAction)
                  cost+=newCost
                  newNode=stateNode(nxtState,newListActions,cost)
                  fringe.push(newNode,cost)
                  
      

def nullHeuristic(state):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided searchProblem.  This one is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  from game import Directions
  
  visitedStates=set()
  fringe=util.FasterPriorityQueue()
  listActions=[];
  state=problem.getStartState()
  cost=0;
  
  Hvalue=heuristic(state)
  priorityVal=Hvalue+cost
  node=stateNode(state,listActions,cost,Hvalue)
  fringe.push(node,priorityVal)
  while (1):
      if fringe.isEmpty(): return None
      node=fringe.pop()
      
      state,listActions,cost,Hvalue=node.state,node.listActions,node.cost,node.Hvalue
      if problem.isGoalState(state):
          return listActions
      if state not in visitedStates:
              visitedStates.add(state)
              listSucessors=problem.getSuccessors(state);
              saveCost=cost
              for sucFn in listSucessors:
                  nxtState, nxtAction, newCost=sucFn
                  cost=saveCost 
                  newListActions=list(listActions)
                  newListActions.append(nxtAction)
                  cost+=newCost
                  newHvalue=heuristic(nxtState) 
                #  if (newHvalue-Hvalue)>1 :
                #       print('Here:')
                #       print(cost+newHvalue)
                #       print(Hvalue,newHvalue)
                #       print(state[0])
                #       print(state[1])
                #       print(nxtState[0])
                #       print(nxtState[1])  
                #       Hvalue=heuristic(state)
                #       newHvalue=heuristic(nxtState) 
                       
                  priorityVal=newHvalue+cost
                  newNode=stateNode(nxtState,newListActions,cost,newHvalue)
                  fringe.push(newNode,priorityVal)
      
      
      
class stateNode(object):
    def __init__(self,state=None,listActions=[],cost=0,Hvalue=9999):
        self.state=state
        self.listActions=listActions
        self.cost=cost
        self.Hvalue=Hvalue
    def __eq__(self, other):
        if other == None: return False
        return (self.state == other.state)&(self.listActions==other.listActions)
    
def greedySearch(problem, heuristic=nullHeuristic):
  from game import Directions
  
  visitedStates=set()
  fringe=util.FasterPriorityQueue()
  listActions=[];
  state=problem.getStartState()
  cost=0;
  
  Hvalue=heuristic(state)
  priorityVal=Hvalue
  node=stateNode(state,listActions,cost,Hvalue)
  fringe.push(node,priorityVal)
  while (1):
      if fringe.isEmpty(): return None
      node=fringe.pop()
      
      state,listActions,cost,Hvalue=node.state,node.listActions,node.cost,node.Hvalue
      if problem.isGoalState(state):
          return listActions
      if state not in visitedStates:
              visitedStates.add(state)
              listSucessors=problem.getSuccessors(state);
              saveCost=cost
            
              for sucFn in listSucessors:
                  nxtState, nxtAction, newCost=sucFn
                  cost=saveCost 
                  newListActions=[]
                  newListActions=list(listActions)
                  newListActions.append(nxtAction)
                  cost+=newCost
                  newHvalue=heuristic(nxtState) 
#                  if (Hvalue-newHvalue)>1 :
#                      print('Here:')
#                      print(Hvalue,newHvalue)
#                      print(state[0])
#                      print(state[1])
#                      print(nxtState[0])
#                      print(nxtState[1])  
                  priorityVal=newHvalue
                  newNode=stateNode(nxtState,newListActions,cost,newHvalue)
                  fringe.push(newNode,priorityVal)


