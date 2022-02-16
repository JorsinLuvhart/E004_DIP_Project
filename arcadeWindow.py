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
    self.sprite = arcade.Sprite("Resources/robot-without-load.png")
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
    self.sprite = arcade.Sprite("Resources/brick.png")
    self.sprite.center_x = self.x * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
    self.sprite.center_y = self.y * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
    self.sprite.scale = SCALE

class Sound():
    """ This class represents a sound you can play."""

    def __init__(self, file_name: Union[str, Path], streaming: bool = False):
        self.file_name: str = ""
        file_name = resolve_resource_path(file_name)

        if not Path(file_name).is_file():
            raise FileNotFoundError(
                f"The sound file '{file_name}' is not a file or can't be read."
            )
        self.file_name = str(file_name)

        self.source: Union[media.StaticSource, media.StreamingSource] = media.load(self.file_name, streaming=streaming)

        self.min_distance = 100000000  # setting the players to this allows for 2D panning with 3D audio

    def play(self, volume: float = 1.0, pan: float = 0.0, loop: bool = False) -> media.Player:
        """
        Play the sound.

        :param float volume: Volume, from 0=quiet to 1=loud
        :param float pan: Pan, from -1=left to 0=centered to 1=right
        :param bool loop: Loop, false to play once, true to loop continously
        """
        if isinstance(self.source, media.StreamingSource) \
                and self.source.is_player_source:
            raise RuntimeError("Tried to play a streaming source more than once."
                               " Streaming sources should only be played in one instance."
                               " If you need more use a Static source.")

        player: media.Player = media.Player()
        player.volume = volume
        player.position = (pan, 0.0, math.sqrt(1 - math.pow(pan, 2)))  # used to mimic panning with 3D audio
        player.loop = loop
        player.queue(self.source)
        player.play()
        media.Source._players.append(player)

        def _on_player_eos():
            media.Source._players.remove(player)
            # There is a closure on player. To get the refcount to 0,
            # we need to delete this function.
            player.on_player_eos = None

        player.on_player_eos = _on_player_eos
        return player


    def stop(self, player: media.Player) -> None:
        """
        Stop a currently playing sound.
        """
        player.pause()
        player.delete()
        if player in media.Source._players:
            media.Source._players.remove(player)


    def get_length(self) -> float:
        """ Get length of audio in seconds """
        return self.source.duration


    def is_complete(self, player: media.Player) -> bool:
        """ Return true if the sound is done playing. """
        if player.time >= self.source.duration:
            return True
        else:
            return False


    def is_playing(self, player: media.Player) -> bool:
        """
        Return if the sound is currently playing or not

        :param pyglet.media.Player player: Player returned from :func:`play_sound`.
        :returns: A boolean, ``True`` if the sound is playing.
        :rtype: bool

        """
        return player.playing


    def get_volume(self, player: media.Player) -> float:
        """
        Get the current volume.

        :param pyglet.media.Player player: Player returned from :func:`play_sound`.
        :returns: A float, 0 for volume off, 1 for full volume.
        :rtype: float
        """
        return player.volume


    def set_volume(self, volume, player: media.Player) -> None:
        """
        Set the volume of a sound as it is playing.

        :param float volume: Floating point volume. 0 is silent, 1 is full.
        :param pyglet.media.Player player: Player returned from :func:`play_sound`.
        """
        player.volume = volume


    def get_stream_position(self, player: media.Player) -> float:
        """
        Return where we are in the stream. This will reset back to
        zero when it is done playing.

        :param pyglet.media.Player player: Player returned from :func:`play_sound`.

        """
        return player.time



def load_sound(path: Union[str, Path], streaming: bool = False) -> Optional[Sound]:
    """
    Load a sound.

    :param Path path: Name of the sound file to load.
    :param bool streaming: Boolean for determining if we stream the sound
                           or load it all into memory. Set to ``True`` for long sounds to save
                           memory, ``False`` for short sounds to speed playback.
    :returns: Sound object which can be used by the  :func:`play_sound` function.
    :rtype: Sound
    """

    file_name = str(path)
    try:
        sound = Sound(file_name, streaming)
        return sound
    except Exception as ex:
        raise FileNotFoundError(f'Unable to load sound file: "{file_name}". Exception: {ex}')



def play_sound(
        sound: Sound, volume: float = 1.0, pan: float = 0.0, looping: bool = False
) -> media.Player:
    """
    Play a sound.

    :param Sound sound: Sound loaded by :func:`load_sound`. Do NOT use a string here for the filename.
    :param float volume: Volume, from 0=quiet to 1=loud
    :param float pan: Pan, from -1=left to 0=centered to 1=right
    :param bool looping: Should we loop the sound over and over?
    """
    if sound is None:
        print("Unable to play sound, no data passed in.")
        return None
    elif isinstance(sound, str):
        msg = (
            "Error, passed in a string as a sound. "
            "Make sure to use load_sound first, and use that result in play_sound."
        )
        raise Exception(msg)
    try:
        return sound.play(volume, pan, looping)
    except Exception as ex:
        print("Error playing sound.", ex)



def stop_sound(player: media.Player):
    """
    Stop a sound that is currently playing.

    :param pyglet.media.Player player: Player returned from :func:`play_sound`.
    """
    if isinstance(player, Sound):
        raise ValueError("stop_sound takes the media player object returned from the play() command, "
                         "not the loaded Sound object.")

    if not isinstance(player, media.Player):
        raise ValueError("stop_sound takes a media player object returned from the play() command.")

    player.pause()
    player.delete()
    if player in media.Source._players:
        media.Source._players.remove(player)

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
    k = 0
    for k in range(2):
      print("warehouse ", k)  
      self.desti = Destination(self.warehouseFloor)
      self.destinationList.append(self.desti.sprite)
      k = k + 1

    j = 0
    for j in range(1):
      print("Parcel ", j)
      self.parcel = Parcel(self.warehouseFloor)
      self.parcelList.append(self.parcel.sprite)
      j = j + 1

    i = 0
    for i in range(5):
      print("Object ", i)
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
    audio = arcade.load_sound("Resources/parcelpickup.wav", False)
    arcade.play_sound(audio, 2.0, -1, False)
    audio.play()
    print("Sound is playing")

  def parcelDep(self):
    print("Dep")
    self.robot.loaded = 0			  
				
						 
													   
