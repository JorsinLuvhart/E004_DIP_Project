import sys
import numpy as np
import arcade

print("Python version " + sys.version)



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOX_LENGTH = 78
MARGIN = 2
COLUMN_COUNT = int(SCREEN_WIDTH/(BOX_LENGTH+MARGIN))
ROW_COUNT = int(SCREEN_WIDTH/(BOX_LENGTH+MARGIN))
SCREEN_TITLE = "Cooperative Bots Design"
VIEWPORT_MARGIN = 200
MOVEMENT_SPEED = 5

#warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination

class gameWindow(arcade.Window):
  
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

  
  def on_draw(self):
    """Render the screen."""
    arcade.start_render()
    # Code to draw the screen goes here
    self.gridSpriteList.draw()

def main():
    """Main function"""
    window = gameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
  main()