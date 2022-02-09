import sys
import numpy as np
import arcade
import random
print("Python version " + sys.version)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 80 #please only divide/multiply this by 2s
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

#warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, sprite, warehouseFloor):
      self.x = 0
      self.y = 0
      self.sprite = sprite
      warehouseFloor[self.x][self.y] = 1

class Parcel():
    def __init__(self, sprite, warehouseFloor):
      self.x = random.randint(0, COLUMN_COUNT-1)
      self.y = random.randint(0, ROW_COUNT-1)
      while(warehouseFloor[self.x][self.y]): #if there is already an object there, rerandomise the location of the parcel
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)
      warehouseFloor[self.x][self.y] = 2
      self.sprite = sprite

  
class Destination():
    def __init__(self, sprite, warehouseFloor):
      self.x = random.randint(0, COLUMN_COUNT-1)
      self.y = random.randint(0, ROW_COUNT-1)
      while(warehouseFloor[self.x][self.y]): #if there is already an object there, rerandomise the location of the parcel
        self.x = random.randint(0, COLUMN_COUNT-1)
        self.y = random.randint(0, ROW_COUNT-1)
      warehouseFloor[self.x][self.y] = 3
      self.sprite = sprite

class GameWindow(arcade.Window):
  
  def __init__(self):
    """ Initialise object here"""
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.WHITE)
    self.warehouseFloor = np.zeros([COLUMN_COUNT,ROW_COUNT],dtype=int)
    self.robotList = None
    self.parcelList = None
    self.destinationList = None
    self.gridSpriteList = None

  def setup(self):
    """ Set up the game here. Call this function to restart the game. """
    self.robotList = arcade.SpriteList()
    self.parcelList = arcade.SpriteList()
    self.destinationList = arcade.SpriteList()
    self.gridSpriteList = arcade.SpriteList()

    
    """Generating individual Grid Spites"""
    self.gridSprites = []
    for row in range(ROW_COUNT):
      self.gridSprites.append([])
      for column in range(COLUMN_COUNT):
        x = column * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
        y = row * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
        sprite = arcade.SpriteSolidColor(BOX_LENGTH, BOX_LENGTH, arcade.color.BLACK)
        sprite.center_x = x
        sprite.center_y = y
        self.gridSpriteList.append(sprite)
        self.gridSprites[row].append(sprite)

    #robot sprite
    sprite = arcade.Sprite("Resources/loader.png")
    self.robot = Robot(sprite,self.warehouseFloor)
    self.robot.sprite.center_x = self.robot.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.robot.sprite.center_y = self.robot.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.robot.sprite.scale = SCALE
    self.robotList.append(self.robot.sprite)

    #destination sprite
    sprite = arcade.Sprite("Resources/destination.png")
    self.desti = Destination(sprite,self.warehouseFloor)
    self.desti.sprite.center_x = self.desti.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.desti.sprite.center_y = self.desti.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.desti.sprite.scale = SCALE
    self.destinationList.append(self.desti.sprite)

    sprite = arcade.Sprite("Resources/parcel.png")
    self.parcel = Parcel(sprite,self.warehouseFloor)
    self.parcel.sprite.center_x = self.parcel.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.parcel.sprite.center_y = self.parcel.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.parcel.sprite.scale = SCALE
    self.parcelList.append(self.parcel.sprite)
    

  def on_draw(self):
    """Render the screen."""
    arcade.start_render()
    
    # Code to draw the screen goes here
    self.gridSpriteList.draw()
    self.robotList.draw()
    self.parcelList.draw()
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
        self.robot.sprite.center_y = self.robot.sprite.center_y + GRID_SIZE
    elif key == arcade.key.DOWN:
        self.robot.sprite.center_y = self.robot.sprite.center_y - GRID_SIZE
    elif key == arcade.key.LEFT:
        self.robot.sprite.center_x = self.robot.sprite.center_x-GRID_SIZE
    elif key == arcade.key.RIGHT:
        self.robot.sprite.center_x = self.robot.sprite.center_x+GRID_SIZE
    
  def on_key_release(self, key, modifiers):
    """Called when the user releases a key. """

    # If a player releases a key, zero out the speed, then the robot sprite will stop moving

