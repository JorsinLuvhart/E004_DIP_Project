import sys
import numpy as np
import arcade
import random
print("Python version " + sys.version)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 80  # please only divide/multiply this by 2s
MARGIN = 2
SCALE = GRID_SIZE/80
BOX_LENGTH = GRID_SIZE - MARGIN
COLUMN_COUNT = int(SCREEN_WIDTH/(GRID_SIZE))
ROW_COUNT = int(SCREEN_HEIGHT/(GRID_SIZE))
SCREEN_TITLE = "Cooperative Bots Design"
MOVEMENT_SPEED = 1
NUM_BOTS = 1
NUM_DESTI = 1
NUM_PARCEL = 1

# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
  def __init__(self, warehouseFloor):
    self.x = 0
    self.y = 0
    self.loaded = 0
    self.sprite = arcade.Sprite("Resources/loader.png")
    self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.sprite.scale = SCALE
    warehouseFloor[self.x][self.y] = 1 + self.loaded

  def move_up(self, warehouseFloor):
    if(self.y < ROW_COUNT-1):
      self.y = self.y + 1
      self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2

  def move_down(self, warehouseFloor):
    if(self.y > 0):
      self.y = self.y - 1
      self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2

  def move_left(self,warehouseFloor):
    if(self.x > 0):
      self.x = self.x - 1
      self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2

  def move_right(self, warehouseFloor):
    if(self.x < COLUMN_COUNT-1):
      self.x = self.x + 1
      self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2

class Parcel():
    def __init__(self, warehouseFloor):
      self.x = random.randint(0, COLUMN_COUNT-1)
      self.y = random.randint(0, ROW_COUNT-1)
      while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)
      warehouseFloor[self.x][self.y] = 3
      self.sprite = arcade.Sprite("Resources/package.png")
      self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
      self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
      self.sprite.scale = SCALE

class Destination():
    def __init__(self, warehouseFloor):
      self.x = random.randint(0, COLUMN_COUNT-1)
      self.y = random.randint(0, ROW_COUNT-1)
      while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)
      warehouseFloor[self.x][self.y] = 4
      self.sprite = arcade.Sprite("Resources/warehouse.png")
      self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
      self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
      self.sprite.scale = SCALE*1.5

class Boulder():
  def __init__(self, warehouseFloor):
    self.x = random.randint(0, COLUMN_COUNT - 1)
    self.y = random.randint(0, ROW_COUNT - 1)
    while (warehouseFloor[self.x][self.y]):  # if there is already an object there, rerandomise the location of the boulder
      self.x = random.randint(0, COLUMN_COUNT - 1)
      self.y = random.randint(0, ROW_COUNT - 1)
    warehouseFloor[self.x][self.y] = 5
    self.sprite = arcade.Sprite("Resources/boulder.png")
    self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
    self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
    self.sprite.scale = SCALE

class GameWindow(arcade.Window):

  def __init__(self):
    """ Initialise object here"""
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)
    self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT], dtype=int)
    self.robotList = None
    self.parcelList = None
    self.boulderList = None
    self.destinationList = None
    self.gridSpriteList = None

  def setup(self):
    """ Set up the game here. Call this function to restart the game. """
    self.robotList = arcade.SpriteList()
    self.parcelList = arcade.SpriteList()
    self.boulderList = arcade.SpriteList()
    self.destinationList = arcade.SpriteList()
    self.gridSpriteList = arcade.SpriteList()

    """Generating individual Grid Spites"""
    self.gridSprites = []
    for row in range(ROW_COUNT):
      self.gridSprites.append([])
      for column in range(COLUMN_COUNT):
        x = column * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
        y = row * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
        sprite = arcade.SpriteSolidColor(BOX_LENGTH, BOX_LENGTH, arcade.color.WHITE)
        sprite.center_x = x
        sprite.center_y = y
        self.gridSpriteList.append(sprite)
        self.gridSprites[row].append(sprite)

    # robot sprite
    self.robot = Robot(self.warehouseFloor)
    self.robotList.append(self.robot.sprite)

    # destination sprite
    self.desti = Destination(self.warehouseFloor)
    self.destinationList.append(self.desti.sprite)

    self.parcel = Parcel(self.warehouseFloor)
    self.parcelList.append(self.parcel.sprite)

    i = 0
    for i in range(5):
      print(i)
      self.boulder = Boulder(self.warehouseFloor)
      self.boulderList.append(self.boulder.sprite)
      i = i + 1

  def on_draw(self):
    """Render the screen."""
    arcade.start_render()
    
    # Code to draw the screen goes here
    self.gridSpriteList.draw()
    self.robotList.draw()
    self.parcelList.draw()
    self.boulderList.draw()
    self.destinationList.draw()


  def on_update(self, delta_time):
      """ Movement and game logic """
      # Move the sprites
      self.robotList.update()
      self.parcelList.update()
      self.destinationList.update()

  def on_key_press(self, key, modifiers):
    """Called whenever a key is pressed. """
    if key == arcade.key.UP:
      if(self.robot.y < ROW_COUNT-1):
        if(self.warehouseFloor[self.robot.x][self.robot.y+1]!=5):
          self.robot.move_up(self.warehouseFloor)
    elif key == arcade.key.DOWN:
      if(self.robot.y > 0):
        if(self.warehouseFloor[self.robot.x][self.robot.y-1]!=5):
          self.robot.move_down(self.warehouseFloor)
    elif key == arcade.key.LEFT:
      if(self.robot.x > 0):
        if(self.warehouseFloor[self.robot.x-1][self.robot.y]!=5):
          self.robot.move_left(self.warehouseFloor)
    elif key == arcade.key.RIGHT:
      if(self.robot.x < COLUMN_COUNT-1):
        if(self.warehouseFloor[self.robot.x+1][self.robot.y]!=5):
          self.robot.move_right(self.warehouseFloor)
    elif key == arcade.key.A:
      self.printWHF()
    if(self.warehouseFloor[self.robot.x][self.robot.y]==3 and self.robot.loaded!=1):
      self.parcelCol()
    elif(self.warehouseFloor[self.robot.x][self.robot.y]==4 and self.robot.loaded==1):
      self.parcelDep()

    
  def on_key_release(self, key, modifiers):
    """Called when the user releases a key. """
    pass
    # If a player releases a key, zero out the speed, then the robot sprite will stop moving

  def printWHF(self):
    for i in range(COLUMN_COUNT):
      for j in range(ROW_COUNT):
        print(self.warehouseFloor[j][i]+" ")
      print("\n")

  def parcelCol(self):
    #need to eventually figure out which is the collected parcel\
    print("Col")
    self.parcelList.remove(self.parcel.sprite)
    self.robot.loaded = 1
    self.warehouseFloor[self.parcel.x][self.parcel.y] = 0				
    del self.parcel
    self.parcel = Parcel(self.warehouseFloor)
    self.parcelList.append(self.parcel.sprite)

  def parcelDep(self):
    print("Dep")
    self.robot.loaded = 0			  
				
						 
													   