import arcadeWindow
import arcade    
    

def main():
    """Main function"""
    window = arcadeWindow.GameWindow()
    # window.setup()
    arcade.run()
    # arcade.quick_run(10)

    window = arcade.get_window()
    if window:
        window.on_update(1 / 60)
        window.on_draw()

if __name__ == "__main__":
  main()
