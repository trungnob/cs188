class Game:
  """
  The Game manages the control flow, soliciting actions from agents.
  """
  
  def __init__( self, agents, display=1, rules=2 ):
    self.agents = agents
    self.display = display
    self.rules = rules
    self.gameOver = False
    self.moveHistory = []
    
  def run( self ):
    """
    Main control loop for game play.
    """
    print(self.agents,self.display,self.rules)
    ###self.display.initialize(self.state.makeObservation(1).data)
    # inform learning agents of the game start
   
