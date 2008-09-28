from graphicsUtils import *        
import math, time

###########################
#  GRAPHICS DISPLAY CODE  #
###########################

# Most code by Dan Klein and John Denero written or rewritten for cs188, UC Berkeley.
# Some code from a Pacman implementation by LiveWires, and used / modified with permission.

FRAME_TIME=0.1# This can get overwritten

GRID_SIZE = 30.0
INFO_PANE_HEIGHT = 35
MARGIN = GRID_SIZE
BACKGROUND_COLOR = formatColor(0,0,0)    
WALL_COLOR = formatColor(0.0/255.0, 51.0/255.0, 255.0/255.0)
INFO_PANE_COLOR = formatColor(.4,.4,0)
SCORE_COLOR = formatColor(.9, .9, .9)

GHOST_COLORS = []                       
GHOST_COLORS.append(formatColor(221.0/255.0,0,0))
GHOST_COLORS.append(formatColor(102.0/255.0,255.0/255.0,255.0/255.0))
GHOST_COLORS.append(formatColor(255.0/255.0,153.0/255.0,153.0/255.0))
GHOST_COLORS.append(formatColor(255.0/255.0,153.0/255.0,0))
GHOST_SHAPE = [                
    ( 0,    0.3 ),            
    ( 0.25, 0.75 ),           
    ( 0.5,  0.3 ),
    ( 0.75, 0.75 ),
    ( 0.75, -0.5 ),
    ( 0.5,  -0.75 ),
    (-0.5,  -0.75 ),
    (-0.75, -0.5 ),
    (-0.75, 0.75 ),
    (-0.5,  0.3 ),
    (-0.25, 0.75 )
  ]
GHOST_SIZE = 0.65
SCARED_COLOR = formatColor(1,1,1)    

GHOST_VEC_COLORS = map(colorToVector, GHOST_COLORS)

PACMAN_COLOR = formatColor(255.0/255.0,255.0/255.0,61.0/255)  
PACMAN_SIZE = 0.5  
#pacman_speed = 0.25    

# Food
FOOD_COLOR = formatColor(1,1,1)     
FOOD_SIZE = 0.1   

# Laser
LASER_COLOR = formatColor(1,0,0)     
LASER_SIZE = 0.02   
        
# Capsule graphics
CAPSULE_COLOR = formatColor(1,1,1)
CAPSULE_SIZE = 0.25 

# Drawing walls
WALL_RADIUS = 0.15

class InfoPane:
  def __init__(self, layout):
    self.width = (layout.width) * GRID_SIZE
    self.base = MARGIN + (layout.height) * GRID_SIZE
    self.height = INFO_PANE_HEIGHT
    self.drawPane()

  def toScreen(self, pos, y = None):
    """
      Translates a point relative from the bottom left of the info pane.
    """
    if y == None:
      x,y = pos
    else:
      x = pos
      
    x = MARGIN + x
    y = self.base + y + MARGIN / 2
    return x,y

  def drawPane(self):
    color = INFO_PANE_COLOR
    scr = self.toScreen
    
    color = PACMAN_COLOR
    size = 24
    if self.width < 240:
      size = 16
    if self.width < 160:
      size = 12
    self.scoreText = text( scr(0, 0), color, "SCORE:    0", "Times", size, "bold")
    
  def updateScore(self, score):
    changeText(self.scoreText, "SCORE: % 4d" % score)
  
  def initializeGhostDistances(self, distances):
    self.ghostDistanceText = []
    
    size = 20
    if self.width < 240:
      size = 12
    if self.width < 160:
      size = 10
      
    for i, d in enumerate(distances):
      t = text( self.toScreen(self.width/2 + self.width/8 * i, 0), GHOST_COLORS[i], d, "Times", size, "bold")
      self.ghostDistanceText.append(t)
      
  def updateGhostDistances(self, distances):
    for i, d in enumerate(distances):
      changeText(self.ghostDistanceText[i], d)
    
  def drawGhost(self):
    pass
  
  def drawPacman(self):
    pass
    
  def drawWarning(self):
    pass
    
  def clearIcon(self):
    pass
    
  def updateMessage(self, message):
    pass
    
  def clearMessage(self):
    pass


class PacmanGraphics:
  def __init__(self):  
    self.have_window = 0
    self.currentGhostImages = {}
    self.pacmanImage = None
  
  def initialize(self, state):
    self.startGraphics(state)
    self.drawInitialObjects(state)
    
  def startGraphics(self, state):
    self.layout = state.layout
    layout = self.layout
    self.width = layout.width
    self.height = layout.height
    self.make_window(self.width, self.height)
    self.infoPane = InfoPane(layout)
    self.currentState = layout
    
  def drawInitialObjects(self, state):
    layout = self.layout
    self.drawWalls(layout.walls)
    self.food = self.drawFood(layout.food)
    self.capsules = self.drawCapsules(layout.capsules)
    self.ghostPositions = []
    refresh
    for index, agent in enumerate(state.agentStates):
      if agent.isPacman:
        self.drawPacman(agent)
        self.previousPacman = agent
      else:  
        self.ghostPositions.append(None)
        self.drawGhost(agent, index - 1)
    refresh
    
  def update(self, newState):
    agentIndex = newState._agentMoved
    agentState = newState.agentStates[agentIndex]
    if agentState.isPacman:
      self.animatePacman(agentState)
      self.previousPacman = agentState
    else:
      index = agentIndex - 1
      self.moveGhost(agentState, index)
    if newState._foodEaten != None:
      self.removeFood(newState._foodEaten, self.food)
    if newState._capsuleEaten != None:
      self.removeCapsule(newState._capsuleEaten, self.capsules)
    self.infoPane.updateScore(newState.score)
      
  def make_window(self, width, height):
    grid_width = (width-1) * GRID_SIZE   
    grid_height = (height-1) * GRID_SIZE
    screen_width = 2*MARGIN + grid_width
    screen_height = 2*MARGIN + grid_height + INFO_PANE_HEIGHT 

    begin_graphics(screen_width,    
                   screen_height,
                   BACKGROUND_COLOR,
                   "CS188 Pacman")
    
  def drawPacman(self, pacman):
    position = pacman.configuration.getPosition()
    screen_point = self.to_screen(position)
    endpoints = self.getEndpoints(pacman.configuration.direction)
    self.pacmanImage = circle(screen_point, PACMAN_SIZE * GRID_SIZE, 
                       color = PACMAN_COLOR,
                       filled = 1,
                       endpoints = endpoints,
                       width = 1)

  def getEndpoints(self, direction, position=(0,0)):
    x, y = position
    pos = x - int(x) + y - int(y)
    width = 30 + 80 * math.sin(math.pi*pos)
    
    delta = width / 2
    if (direction == 'West'):
      endpoints = (180+delta, 180-delta)
    elif (direction == 'North'):
      endpoints = (90+delta, 90-delta)
    elif (direction == 'South'):
      endpoints = (270+delta, 270-delta)
    else:
      endpoints = (0+delta, 0-delta)
    return endpoints

  def movePacman(self, position, direction):
    screenPosition = self.to_screen(position)
    endpoints = self.getEndpoints( direction, position )
    r = PACMAN_SIZE * GRID_SIZE
    moveCircle(self.pacmanImage, screenPosition, r, endpoints)
    refresh
    
  def animatePacman(self, pacman):
    if FRAME_TIME > 0.01:
      start = time.time()
      fx, fy = self.previousPacman.configuration.getPosition()
      px, py = pacman.configuration.getPosition()
      frames = 8.0
      for i in range(int(frames)):
        pos = px*i/frames + fx*(frames-i)/frames, py*i/frames + fy*(frames-i)/frames 
        self.movePacman(pos, pacman.configuration.direction)
        # if time.time() - start > FRAME_TIME: return
        sleep(FRAME_TIME / 2 / frames)
    else:
      self.movePacman(pacman.configuration.pos, pacman.configuration.direction)

  def getGhostColor(self, ghost, ghostIndex):
    if ghost.scaredTimer > 0:
      return SCARED_COLOR
    else:
      return GHOST_COLORS[ghostIndex]

  def drawGhost(self, ghost, agentIndex):
    pos = ghost.configuration.getPosition()
    dir = ghost.configuration.direction
    (screen_x, screen_y) = (self.to_screen(pos) ) 
    coords = []          
    for (x, y) in GHOST_SHAPE:
      coords.append((x*GRID_SIZE*GHOST_SIZE + screen_x, y*GRID_SIZE*GHOST_SIZE + screen_y))

    colour = self.getGhostColor(ghost, agentIndex)
    body = polygon(coords, colour, filled = 1)
    WHITE = formatColor(1.0, 1.0, 1.0)
    BLACK = formatColor(0.0, 0.0, 0.0)
    
    dx = 0
    dy = 0
    if dir == 'North':
      dy = -0.2
    if dir == 'South':
      dy = 0.2
    if dir == 'East':
      dx = 0.2
    if dir == 'West':
      dx = -0.2
    leftEye = circle((screen_x+GRID_SIZE*GHOST_SIZE*(-0.3+dx/1.5), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy/1.5)), GRID_SIZE*GHOST_SIZE*0.2, WHITE)
    rightEye = circle((screen_x+GRID_SIZE*GHOST_SIZE*(0.3+dx/1.5), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy/1.5)), GRID_SIZE*GHOST_SIZE*0.2, WHITE)
    leftPupil = circle((screen_x+GRID_SIZE*GHOST_SIZE*(-0.3+dx), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy)), GRID_SIZE*GHOST_SIZE*0.08, BLACK)
    rightPupil = circle((screen_x+GRID_SIZE*GHOST_SIZE*(0.3+dx), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy)), GRID_SIZE*GHOST_SIZE*0.08, BLACK)
    ghostImageParts = []
    ghostImageParts.append(body)
    ghostImageParts.append(leftEye)
    ghostImageParts.append(rightEye)
    ghostImageParts.append(leftPupil)
    ghostImageParts.append(rightPupil)
    
    self.currentGhostImages[agentIndex] = ghostImageParts
    self.ghostPositions[agentIndex] = self.to_screen(pos)
    
  def moveEyes(self, pos, dir, eyes):
    (screen_x, screen_y) = (self.to_screen(pos) ) 
    dx = 0
    dy = 0
    if dir == 'North':
      dy = -0.2
    if dir == 'South':
      dy = 0.2
    if dir == 'East':
      dx = 0.2
    if dir == 'West':
      dx = -0.2
    moveCircle(eyes[0],(screen_x+GRID_SIZE*GHOST_SIZE*(-0.3+dx/1.5), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy/1.5)), GRID_SIZE*GHOST_SIZE*0.2)
    moveCircle(eyes[1],(screen_x+GRID_SIZE*GHOST_SIZE*(0.3+dx/1.5), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy/1.5)), GRID_SIZE*GHOST_SIZE*0.2)
    moveCircle(eyes[2],(screen_x+GRID_SIZE*GHOST_SIZE*(-0.3+dx), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy)), GRID_SIZE*GHOST_SIZE*0.08)
    moveCircle(eyes[3],(screen_x+GRID_SIZE*GHOST_SIZE*(0.3+dx), screen_y-GRID_SIZE*GHOST_SIZE*(0.3-dy)), GRID_SIZE*GHOST_SIZE*0.08)
    
  def moveGhost(self, ghost, ghostIndex):
    old_x, old_y = self.ghostPositions[ghostIndex]
    new_x, new_y = self.to_screen(ghost.configuration.getPosition())
    delta = new_x - old_x, new_y - old_y
    
    ghostImageParts = self.currentGhostImages[ghostIndex]
    for ghostImagePart in ghostImageParts:
      move_by(ghostImagePart, delta)
    
    if ghost.scaredTimer > 0:
      color = SCARED_COLOR
    else:
      color = GHOST_COLORS[ghostIndex]
    edit(ghostImageParts[0], ('fill', color), ('outline', color))  
    self.moveEyes(ghost.configuration.getPosition(), ghost.configuration.direction, ghostImageParts[-4:])
    self.ghostPositions[ghostIndex] = (new_x, new_y)
    refresh
    
  def finish(self):
    end_graphics()
  
  def to_screen(self, point):
    ( x, y ) = point
    #y = self.height - y
    x = x*GRID_SIZE + MARGIN
    y = (self.height - 1 - y)*GRID_SIZE + MARGIN 
    return ( x, y )
  
  # Fixes some TK issue with off-center circles
  def to_screen2(self, point):
    ( x, y ) = point
    #y = self.height - y
    x = x*GRID_SIZE + MARGIN
    y = (self.height -1 - y)*GRID_SIZE + MARGIN
    return ( x, y )
  
  def drawWalls(self, wallMatrix):
    for xNum, x in enumerate(wallMatrix):
      for yNum, cell in enumerate(x):
        if cell: # There's a wall here
          pos = (xNum, yNum)
          screen = self.to_screen(pos)
          screen2 = self.to_screen2(pos)
          
          # draw each quadrant of the square based on adjacent walls
          wIsWall = self.isWall(xNum-1, yNum, wallMatrix)
          eIsWall = self.isWall(xNum+1, yNum, wallMatrix)
          nIsWall = self.isWall(xNum, yNum+1, wallMatrix)
          sIsWall = self.isWall(xNum, yNum-1, wallMatrix)
          nwIsWall = self.isWall(xNum-1, yNum+1, wallMatrix)
          swIsWall = self.isWall(xNum-1, yNum-1, wallMatrix)
          neIsWall = self.isWall(xNum+1, yNum+1, wallMatrix)
          seIsWall = self.isWall(xNum+1, yNum-1, wallMatrix)
          
          # NE quadrant
          if (not nIsWall) and (not eIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * GRID_SIZE, WALL_COLOR, 0, (0,91), 'arc')
          if (nIsWall) and (not eIsWall):
            # vertical line
            line(add(screen, (GRID_SIZE*WALL_RADIUS, 0)), add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(-0.5)-1)), WALL_COLOR)
          if (not nIsWall) and (eIsWall):
            # horizontal line
            line(add(screen, (0, GRID_SIZE*(-1)*WALL_RADIUS)), add(screen, (GRID_SIZE*0.5+1, GRID_SIZE*(-1)*WALL_RADIUS)), WALL_COLOR)
          if (nIsWall) and (eIsWall) and (not neIsWall):
            # outer circle
            circle(add(screen2, (GRID_SIZE*2*WALL_RADIUS, GRID_SIZE*(-2)*WALL_RADIUS)), WALL_RADIUS * GRID_SIZE-1, WALL_COLOR, 0, (180,271), 'arc')
            line(add(screen, (GRID_SIZE*2*WALL_RADIUS-1, GRID_SIZE*(-1)*WALL_RADIUS)), add(screen, (GRID_SIZE*0.5+1, GRID_SIZE*(-1)*WALL_RADIUS)), WALL_COLOR)
            line(add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(-2)*WALL_RADIUS+1)), add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(-0.5))), WALL_COLOR)
          
          # NW quadrant
          if (not nIsWall) and (not wIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * GRID_SIZE, WALL_COLOR, 0, (90,181), 'arc')
          if (nIsWall) and (not wIsWall):
            # vertical line
            line(add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, 0)), add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(-0.5)-1)), WALL_COLOR)
          if (not nIsWall) and (wIsWall):
            # horizontal line
            line(add(screen, (0, GRID_SIZE*(-1)*WALL_RADIUS)), add(screen, (GRID_SIZE*(-0.5)-1, GRID_SIZE*(-1)*WALL_RADIUS)), WALL_COLOR)
          if (nIsWall) and (wIsWall) and (not nwIsWall):
            # outer circle
            circle(add(screen2, (GRID_SIZE*(-2)*WALL_RADIUS, GRID_SIZE*(-2)*WALL_RADIUS)), WALL_RADIUS * GRID_SIZE-1, WALL_COLOR, 0, (270,361), 'arc')
            line(add(screen, (GRID_SIZE*(-2)*WALL_RADIUS+1, GRID_SIZE*(-1)*WALL_RADIUS)), add(screen, (GRID_SIZE*(-0.5), GRID_SIZE*(-1)*WALL_RADIUS)), WALL_COLOR)
            line(add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(-2)*WALL_RADIUS+1)), add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(-0.5))), WALL_COLOR)
          
          # SE quadrant
          if (not sIsWall) and (not eIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * GRID_SIZE, WALL_COLOR, 0, (270,361), 'arc')
          if (sIsWall) and (not eIsWall):
            # vertical line
            line(add(screen, (GRID_SIZE*WALL_RADIUS, 0)), add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(0.5)+1)), WALL_COLOR)
          if (not sIsWall) and (eIsWall):
            # horizontal line
            line(add(screen, (0, GRID_SIZE*(1)*WALL_RADIUS)), add(screen, (GRID_SIZE*0.5+1, GRID_SIZE*(1)*WALL_RADIUS)), WALL_COLOR)
          if (sIsWall) and (eIsWall) and (not seIsWall):
            # outer circle
            circle(add(screen2, (GRID_SIZE*2*WALL_RADIUS, GRID_SIZE*(2)*WALL_RADIUS)), WALL_RADIUS * GRID_SIZE-1, WALL_COLOR, 0, (90,181), 'arc')
            line(add(screen, (GRID_SIZE*2*WALL_RADIUS-1, GRID_SIZE*(1)*WALL_RADIUS)), add(screen, (GRID_SIZE*0.5, GRID_SIZE*(1)*WALL_RADIUS)), WALL_COLOR)
            line(add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(2)*WALL_RADIUS-1)), add(screen, (GRID_SIZE*WALL_RADIUS, GRID_SIZE*(0.5))), WALL_COLOR)
          
          # SW quadrant
          if (not sIsWall) and (not wIsWall):
            # inner circle
            circle(screen2, WALL_RADIUS * GRID_SIZE, WALL_COLOR, 0, (180,271), 'arc')
          if (sIsWall) and (not wIsWall):
            # vertical line
            line(add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, 0)), add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(0.5)+1)), WALL_COLOR)
          if (not sIsWall) and (wIsWall):
            # horizontal line
            line(add(screen, (0, GRID_SIZE*(1)*WALL_RADIUS)), add(screen, (GRID_SIZE*(-0.5)-1, GRID_SIZE*(1)*WALL_RADIUS)), WALL_COLOR)
          if (sIsWall) and (wIsWall) and (not swIsWall):
            # outer circle
            circle(add(screen2, (GRID_SIZE*(-2)*WALL_RADIUS, GRID_SIZE*(2)*WALL_RADIUS)), WALL_RADIUS * GRID_SIZE-1, WALL_COLOR, 0, (0,91), 'arc')
            line(add(screen, (GRID_SIZE*(-2)*WALL_RADIUS+1, GRID_SIZE*(1)*WALL_RADIUS)), add(screen, (GRID_SIZE*(-0.5), GRID_SIZE*(1)*WALL_RADIUS)), WALL_COLOR)
            line(add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(2)*WALL_RADIUS-1)), add(screen, (GRID_SIZE*(-1)*WALL_RADIUS, GRID_SIZE*(0.5))), WALL_COLOR)
          
  def isWall(self, x, y, walls):
    if x < 0 or y < 0:
      return False
    if x >= walls.width or y >= walls.height:
      return False
    return walls[x][y]
  
  def drawFood(self, foodMatrix ):
    foodImages = []
    for xNum, x in enumerate(foodMatrix):
      imageRow = []
      foodImages.append(imageRow)
      for yNum, cell in enumerate(x):
        if cell: # There's food here
          screen = self.to_screen((xNum, yNum ))
          dot = circle( screen, 
                        FOOD_SIZE * GRID_SIZE, 
                        color = FOOD_COLOR, 
                        filled = 1,
                        width = 1)
          imageRow.append(dot)
        else:
          imageRow.append(None)
    return foodImages
  
  def drawCapsules(self, capsules ):
    capsuleImages = {}
    for capsule in capsules:
      ( screen_x, screen_y ) = self.to_screen(capsule)
      dot = circle( (screen_x, screen_y), 
                        CAPSULE_SIZE * GRID_SIZE, 
                        color = CAPSULE_COLOR, 
                        filled = 1,
                        width = 1)
      capsuleImages[capsule] = dot
    return capsuleImages
  
  def removeFood(self, cell, foodImages ):
    x, y = cell
    remove_from_screen(foodImages[x][y])
    
  def removeCapsule(self, cell, capsuleImages ):
    x, y = cell
    remove_from_screen(capsuleImages[(x, y)])

  def drawExpandedCells(self, cells):
    """
    Draws an overlay of expanded grid positions for search agents
    """
    n = float(len(cells))
    baseColor = [1.0, 0.0, 0.0]
    self.clearExpandedCells()
    self.expandedCells = []
    for k, cell in enumerate(cells):
       screenPos = self.to_screen( cell)
       cellColor = formatColor(*[(n-k) * c * .5 / n + .25 for c in baseColor])
       block = square(screenPos, 
                0.5 * GRID_SIZE, 
                color = cellColor, 
                filled = 1, behind=True)
       self.expandedCells.append(block)
  
  def clearExpandedCells(self):
    if 'expandedCells' in dir(self) and len(self.expandedCells) > 0:
      for cell in self.expandedCells:
        remove_from_screen(cell)

class FirstPersonPacmanGraphics(PacmanGraphics):
  def initialize(self, state):
    
    PacmanGraphics.startGraphics(self, state)
    # Initialize distribution images
    walls = state.layout.walls
    dist = []
    self.layout = state.layout
    
    for x in range(len(walls)):
      distx = []
      dist.append(distx)
      for y in range(len(walls[0])):
          ( screen_x, screen_y ) = self.to_screen( (x, y) )
          block = square( (screen_x, screen_y), 
                          0.5 * GRID_SIZE, 
                          color = BACKGROUND_COLOR, 
                          filled = 1)
          distx.append(block)
    self.distributionImages = dist

    # Draw the rest
    PacmanGraphics.drawInitialObjects(self, state)
    
    # Information
    self.laserImage = None
    self.infoPane.initializeGhostDistances(state.getGhostDistances())
    self.previousState = state
    
  def updateDistribution(self, distributions, pacConfiguration):
    (pacRow, pacCol), pacVec = pacConfiguration.getPosition(), pacConfiguration.getDirection()
    for x in range(len(self.distributionImages)):
      for y in range(len(self.distributionImages[0])):
        image = self.distributionImages[x][y]
        weights = distributions[x][y]
        
        # Fog of war
        color = [0.0,0.0,0.0]
        for weight, gcolor in zip(weights, GHOST_VEC_COLORS):
          color = [min(1.0, c + 0.95 * g * weight ** .3) for c,g in zip(color, gcolor)]
        changeColor(image, formatColor(*color))
    
  def drawLaser(self, config, state):
    if config.getDirection() == 'Stop':
      return
    else:
      self.laserImage = [] 
      x, y = config.getPosition()
      direction = config.getDirection()
      for cell in state.layout.visibility[int(x)][int(y)][direction]:
        ( screen_x, screen_y ) = self.to_screen(cell)
        dot = circle( (screen_x, screen_y), 
                        LASER_SIZE * GRID_SIZE, 
                        color = LASER_COLOR, 
                        filled = 1,
                        width = 1)
        self.laserImage.append(dot)

  def lookAhead(self, config, state):
    if config.getDirection() == 'Stop':
      return
    else:
      pass
      # Draw relevant ghosts
      allGhosts = state.getGhostStates()
      visibleGhosts = state.getVisibleGhosts()
      for i, ghost in enumerate(allGhosts):
        if ghost in visibleGhosts:
          self.drawGhost(ghost, i)
        else:
          self.currentGhostImages[i] = None
    
  def update(self, newState):
    agentIndex = newState._agentMoved
    if agentIndex != 0:
      return
    
    # Update laser
    if self.laserImage != None:
      for part in self.laserImage:
        remove_from_screen(part)
    self.drawLaser(newState.getPacmanState().configuration, newState)
        

    # Erase old field of view
    for index, image in self.currentGhostImages.items():
      if image != None:
        for part in image:
          remove_from_screen(part)
    
    # Draw visible ghosts and laser sight
    self.lookAhead(newState.getPacmanState().configuration, newState)
    
    # Move pacman
    self.animatePacman(newState.getPacmanState())
    self.previousPacman = newState.getPacmanState()
    
    if newState._foodEaten != None:
      self.removeFood(newState._foodEaten, self.food)
    if newState._capsuleEaten != None:
      self.removeCapsule(newState._capsuleEaten, self.capsules)
      
    # Information
    self.infoPane.updateScore(newState.score)
    self.infoPane.updateGhostDistances(newState.getGhostDistances())

  def getGhostColor(self, ghost, ghostIndex):
    return GHOST_COLORS[ghostIndex]

def add(x, y):
  return (x[0] + y[0], x[1] + y[1])
