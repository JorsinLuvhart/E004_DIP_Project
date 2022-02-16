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

# warehouse floor, 0=blank space, 1=robot, 3=parcel, 4=destination, 5=obstacle
class Robot():
  def __init__(self, warehouseFloor):
    self.x = 0
    self.y = 0
    self.loaded = 0
    self.loadedWith = None
    self.sprite = arcade.Sprite("Resources/loader.png")
    self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.sprite.scale = SCALE
    warehouseFloor[self.x][self.y] = 1 #setting spawn location to not generate anything

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
      #initializing coordinates
      self.x = random.randint(0, COLUMN_COUNT-1)
      self.y = random.randint(0, ROW_COUNT-1)
      while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)
      warehouseFloor[self.x][self.y] = 3
      #Sprite stuff
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
    while (
    warehouseFloor[self.x][self.y]):  # if there is already an object there, rerandomise the location of the boulder
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
    #Spritelist Declaration
    self.robotSpriteList = None
    self.parcelSpriteList = None
    self.boulderSpriteList = None
    self.destiSpriteList = None
    self.gridSpriteList = None
    #Object list Declaration
    self.robotObjList = []
    self.parcelObjList = []
    self.destiObjList = []
    self.boulderObjList = []


  def setup(self):
    """ Set up the game here. Call this function to restart the game. """
    #Spritelist Declaration
    self.robotSpriteList = arcade.SpriteList()
    self.parcelSpriteList = arcade.SpriteList()
    self.boulderSpriteList = arcade.SpriteList()
    self.destiSpriteList = arcade.SpriteList()
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

    # destination sprite
    desti = Destination(self.warehouseFloor)
    self.destiObjList.append(desti)
    self.destiSpriteList.append(desti.sprite)

    parcel = Parcel(self.warehouseFloor)
    self.parcelObjList.append(parcel)
    self.parcelSpriteList.append(parcel.sprite)

    boulder = Boulder(self.warehouseFloor)
    self.boulderObjList.append(boulder)
    self.boulderSpriteList.append(boulder.sprite)

    # robot sprite
    self.robot = Robot(self.warehouseFloor)
    self.robotSpriteList.append(self.robot.sprite)

  def on_draw(self):
    """Render the screen."""
    arcade.start_render()
    
    # Code to draw the screen goes here
    self.gridSpriteList.draw()
    self.robotSpriteList.draw()
    self.parcelSpriteList.draw()
    self.boulderSpriteList.draw()
    self.destiSpriteList.draw()

  def on_update(self, delta_time):
    """ Movement and game logic """
    # Move the sprites
    self.robotSpriteList.update()
    self.parcelSpriteList.update()
    self.destiSpriteList.update()
    self.boulderSpriteList.update()

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
    elif key == arcade.key.W:
      self.printWHF()
    elif key == arcade.key.Z:
      self.addBoulder()
    elif key == arcade.key.X:
      self.addDesti()
    elif key == arcade.key.C:
      self.addParcel()

    # Evaluation
    if(self.warehouseFloor[self.robot.x][self.robot.y]==3 and self.robot.loaded!=1):
      self.parcelCol(self.robot)
    elif(self.warehouseFloor[self.robot.x][self.robot.y]==4 and self.robot.loaded==1):
      self.parcelDep(self.robot)

    
  def on_key_release(self, key, modifiers):
    """Called when the user releases a key. """
    pass
    # If a player releases a key, zero out the speed, then the robot sprite will stop moving

  def printWHF(self):
    print(self.warehouseFloor)

  def addParcel(self):
    parcel = Parcel(self.warehouseFloor)
    self.parcelObjList.append(parcel)
    self.parcelSpriteList.append(parcel.sprite)

  def addDesti(self):
    desti = Destination(self.warehouseFloor)
    self.destiObjList.append(desti)
    self.destiSpriteList.append(desti.sprite)

  def addBoulder(self):
    boulder = Boulder(self.warehouseFloor)
    self.boulderObjList.append(boulder)
    self.boulderSpriteList.append(boulder.sprite)

  
  def parcelCol(self,robot):
    print("Col")
    for parcel in self.parcelObjList:
      if(parcel.x == robot.x and parcel.y == robot.y):
        tgtParcel = parcel
    self.parcelSpriteList.remove(tgtParcel.sprite)
    self.robot.loaded = 1
    self.warehouseFloor[tgtParcel.x][tgtParcel.y] = 0				
    self.parcelObjList.remove(tgtParcel)
    
  
  def parcelDep(self,robot):
    print("Dep")
    self.robot.loaded = 0
    
				
						 
													   