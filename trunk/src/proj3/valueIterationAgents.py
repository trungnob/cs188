import mdp, util

from abstractAgents import AbstractValueEstimationAgent

class ValueIterationAgent(AbstractValueEstimationAgent):
  """
      * Please read abstractAgents.py before reading this.*

      A ValueIterationAgent takes a markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations as well as a discount 
      value.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.myV=util.Counter();
#    for state in mdp.getStates():
#        self.myVector[state]=0
    
#    util.raiseNotDefined()
    
  def getValue(self, state):
    """
      Return the value of the state 
      (after the indicated number of value iteration passes).      
    """
    "*** YOUR CODE HERE ***"
    listOfState=self.mdp.getStates()
#    for eacState in listOfState :
#    print self.mdp.getTransitionStatesAndProbs()    
    print self.mdp.getPossibleActions(state)
    print self.mdp.getStartState()
    return 0;
#    util.raiseNotDefined()


  def getQValue(self, state, action):
    """
      Look up the q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    print self.discount
    print self.gamma
    listOfState=self.mdp.getStates()
    listOfStateandProbs=self.mdp.getTransitionStatesAndProbs(state,action) 
    sumTmp=0 
    for eachStateandProbs in listOfStateandProbs:
        nextState,tValue=eachStateandProbs
        sumTmp+=tValue*(self.mdp.getReward(state,action,nextState)+self.discount*self.myV[state])
#    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      Look up the policy's recommendation for the state
      (after the indicated number of value iteration passes).

      This method should return exactly one legal action for each state.
      You may break ties any way you see fit. The getPolicy method is used 
      for display purposes & in the getAction method below.
    """
    "*** YOUR CODE HERE ***"
    print self.mdp.getStates()
    listActions=self.mdp.getPossibleActions(state)
    for eachAction in listActions:
        print self.mdp.getTransitionStatesAndProbs(state,eachAction) 
    return 0;
#    util.raiseNotDefined()

  def getAction(self, state):
    """
      Return the action recommended by the policy.  We have provided this
      for you.
    """
    return self.getPolicy(state)