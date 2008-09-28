from game import Agent
from game import Directions

class KeyboardAgent(Agent):
  """
  An agent controlled by the keyboard.
  """
  # NOTE: Arrow keys also work.
  WEST_KEY  = 'a' 
  EAST_KEY  = 'd' 
  NORTH_KEY = 'w' 
  SOUTH_KEY = 's'

  def __init__( self ):
    
    self.lastMove = Directions.STOP
    self.keys = []
    
  def getAction( self, state):
    from graphicsUtils import keys_waiting
    from graphicsUtils import keys_pressed
    keys = keys_waiting() + keys_pressed()
    if keys != []:
      self.keys = keys
    
    legal = state.getLegalPacmanActions()
    move = Directions.STOP
    if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
    if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
    if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
    if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
    
    if move == Directions.STOP:
      # Try to move in the same direction as before
      if self.lastMove in legal:
        move = self.lastMove
        
    self.lastMove = move
    return move
  
