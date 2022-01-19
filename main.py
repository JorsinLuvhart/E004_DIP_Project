import sys
import numpy as np
import arcade
import random
print("Python version " + sys.version)



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOX_LENGTH = 78
MARGIN = 2
COLUMN_COUNT = int(SCREEN_WIDTH/(BOX_LENGTH+MARGIN))
ROW_COUNT = int(SCREEN_WIDTH/(BOX_LENGTH+MARGIN))
SCREEN_TITLE = "Cooperative Bots Design"
MOVEMENT_SPEED = 1
NUM_BOTS = 1
NUM_DESTI = 1
NUM_PARCEL = 1

#warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, sprite):
      self.x = 0
      self.y = 0
      self.sprite = sprite

class Parcel():
    def __init__(self, sprite):
      self.x = random.randint(1, ROW_COUNT)
      self.y = random.randint(1, COLUMN_COUNT)
      self.sprite = sprite
  
class Destination():
    def __init__(self, sprite):
      self.x = random.randint(1, ROW_COUNT)
      self.y = random.randint(1, COLUMN_COUNT)
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
    sprite = arcade.Sprite("Resources/robot.png")
    self.robot = Robot(sprite)
    self.robot.sprite.center_x = self.robot.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.robot.sprite.center_y = self.robot.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.robotList.append(self.robot.sprite)

    #destination sprite
    sprite = arcade.Sprite("Resources/destination.png")
    self.desti = Destination(sprite)
    self.desti.sprite.center_x = self.desti.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.desti.sprite.center_y = self.desti.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.destinationList.append(self.desti.sprite)

    sprite = arcade.Sprite("Resources/parcel.png")
    self.parcel = Parcel(sprite)
    self.parcel.sprite.center_x = self.parcel.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.parcel.sprite.center_y = self.parcel.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN)/2
    self.parcelList.append(self.parcel.sprite)

  def on_draw(self):
    """Render the screen."""
    arcade.start_render()
    
    # Code to draw the screen goes here
    self.gridSpriteList.draw()
    self.robotList.draw()
    self.parcelList.draw()
    self.destinationList.draw()


  def on_key_press(self, key, modifiers):
    """Called whenever a key is pressed. """
    if key == arcade.key.UP:
        self.player_sprite.change_y = MOVEMENT_SPEED
    elif key == arcade.key.DOWN:
        self.player_sprite.change_y = -MOVEMENT_SPEED
    elif key == arcade.key.LEFT:
        self.player_sprite.change_x = -MOVEMENT_SPEED
    elif key == arcade.key.RIGHT:
        self.player_sprite.change_x = MOVEMENT_SPEED

def main():
    """Main function"""
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
  main()