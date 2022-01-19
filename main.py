import sys
import arcade

print("Python version " + sys.version)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Cooperative Bots Design"
VIEWPORT_MARGIN = 200
MOVEMENT_SPEED = 5

class gameWindow(arcade.Window):
  
  def __init__(self):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    arcade.set_background_color(arcade.color.BLACK)

  def setup(self):
    """ Set up the game here. Call this function to restart the game. """
    pass
  
  def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        # Code to draw the screen goes here

def main():
    """Main function"""
    window = gameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
  main()