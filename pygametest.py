import sys
import numpy as np
import pygame
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
  def __init__(self, warehouseFloor,x,y):
    self.x = x
    self.y = y
    self.loaded = 0
    self.image = pygame.image.load(r"Resources/loader.png")
    # warehouseFloor[self.x][self.y] = 1 + self.loaded

  def move_up(self, warehouseFloor):
    if(self.y < ROW_COUNT-1 and warehouseFloor[self.x][self.y + 1] != 5):
      self.y = self.y + 1


  def move_down(self, warehouseFloor):
    if(self.y > 0 and warehouseFloor[self.x][self.y - 1] != 5):
      self.y = self.y - 1

  def move_left(self,warehouseFloor):
    if(self.x > 0 and warehouseFloor[self.x - 1][self.y] != 5):
      self.x = self.x - 1


  def move_right(self, warehouseFloor):
    if(self.x < COLUMN_COUNT-1 and warehouseFloor[self.x + 1][self.y] != 5):
      self.x = self.x + 1


class Parcel():
    def __init__(self, warehouseFloor,x,y):
      self.x = x
      self.y = y
      # self.x = random.randint(0, COLUMN_COUNT-1)
      # self.y = random.randint(0, ROW_COUNT-1)
      # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
      #   self.x = random.randint(0, COLUMN_COUNT-1)
      #   self.y = random.randint(0, ROW_COUNT-1)
      self.image = pygame.image.load(r"Resources/package.png")
      warehouseFloor[self.x][self.y] = 3


class Destination():
    def __init__(self, warehouseFloor,x,y):
      # self.x = random.randint(0, COLUMN_COUNT-1)
      # self.y = random.randint(0, ROW_COUNT-1)
      # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
      #   self.x = random.randint(0, COLUMN_COUNT-1)
      #   self.y = random.randint(0, ROW_COUNT-1)
      self.x = x
      self.y = y
      self.image = pygame.image.load(r"Resources/warehouse.png")
      warehouseFloor[self.x][self.y] = 4


class Boulder():
  def __init__(self, warehouseFloor,x,y):
    # self.x = random.randint(0, COLUMN_COUNT - 1)
    # self.y = random.randint(0, ROW_COUNT - 1)
    # while (
    # warehouseFloor[self.x][self.y]):  # if there is already an object there, rerandomise the location of the boulder
    #   self.x = random.randint(0, COLUMN_COUNT - 1)
    #   self.y = random.randint(0, ROW_COUNT - 1)
    self.x = x
    self.y = y
    self.image = pygame.image.load(r"Resources/boulder.png")
    warehouseFloor[self.x][self.y] = 5


class GameWindow():

    def __init__(self,manualControl,parcelNum):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT], dtype=int)
        self.stepnum = 0
        self.collected=-1
        pygame.init()
        self.dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # self.gridSprites = []
        # for row in range(ROW_COUNT):
        #     self.gridSprites.append([])
        #     for column in range(COLUMN_COUNT):
        #         x = column * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
        #         y = row * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
        #         sprite = arcade.SpriteSolidColor(BOX_LENGTH, BOX_LENGTH, arcade.color.WHITE)
        #         sprite.center_x = x
        #         sprite.center_y = y
        #         self.gridSpriteList.append(sprite)
        #         self.gridSprites[row].append(sprite)

        # robot sprite
        self.robot = Robot(self.warehouseFloor,0,0)

        # destination sprite
        self.desti = Destination(self.warehouseFloor,9,8)

        self.parcelList=[]
        # self.parcelCor = [[2, 2],[2, 5]]
        self.parcelCor = [[2, 2], [2, 3], [2, 5], [3, 2], [4, 3], [15,2], [2, 1], [1, 6]]
        for i in range (parcelNum):
            self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
            self.collected+=1

        # self.parcel = Parcel(self.warehouseFloor,2,2)


        self.boulderList=[]
        boulderCor=[[10,8],[10,7],[10,6],[10,5],[10,4],[10,3]]
        for boulder in boulderCor:
            self.boulderList.append(Boulder(self.warehouseFloor,boulder[0],boulder[1]))

        if manualControl:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.action(3)
                        if event.key == pygame.K_RIGHT:
                            self.action(4)
                        if event.key == pygame.K_UP:
                            self.action(2)
                        if event.key == pygame.K_DOWN:
                            self.action(1)
                        if event.key == pygame.K_SPACE:
                            self.action(0)
                        print(self.evaluate())
                self.view1()

    def printWHF(self):
        for i in range(COLUMN_COUNT):
            for j in range(ROW_COUNT):
                print(self.warehouseFloor[j][i] + " ")
            print("\n")

    def parcelCol(self,parcel):
        # need to eventually figure out which is the collected parcel\
        # print("Col")
        self.robot.loaded = 1
        self.warehouseFloor[parcel.x][parcel.y] = 0
        self.parcelList.remove(parcel)
        del parcel
        self.parcelList.append(Parcel(self.warehouseFloor,self.parcelCor[self.collected % len(self.parcelCor)][0],self.parcelCor[self.collected % len(self.parcelCor)][1]))

    def parcelDep(self):
        # print("Dep")
        self.robot.loaded = 0

    def action(self, action):
        self.stepnum += 1

        if action == 0:
            pass
        if action == 1:
            self.robot.move_up(self.warehouseFloor)
        if action == 2:
            self.robot.move_down(self.warehouseFloor)
        if action == 3:
            self.robot.move_left(self.warehouseFloor)
        if action == 4:
            self.robot.move_right(self.warehouseFloor)

    def evaluate(self):
        self.reward = 0

        if (self.warehouseFloor[self.robot.x][self.robot.y] == 3 and self.robot.loaded != 1):
            self.collected+=1
            for parcel in self.parcelList:
                if self.robot.x==parcel.x and self.robot.y==parcel.y:
                    self.parcelCol(parcel)
                    continue
            self.reward += 1
        elif (self.warehouseFloor[self.robot.x][self.robot.y] == 4 and self.robot.loaded == 1):
            self.parcelDep()
            self.reward += 1
        else:
            self.reward -= 0.1

        return self.reward

    def is_done(self):
        if self.stepnum == 1000:
            return True
        return False

    def observe(self):
        ret = self.warehouseFloor.copy()
        ret[self.robot.x][self.robot.y] = 1 + self.robot.loaded
        return ret

    def view1(self):

        self.dis.fill((255, 255, 255))
        self.dis.blit(self.robot.image, (self.robot.x*80, self.robot.y*80))
        self.dis.blit(self.desti.image, (self.desti.x*80, self.desti.y*80))
        for parcel in self.parcelList:
            self.dis.blit(parcel.image, (parcel.x*80, parcel.y*80))
        for boulder in self.boulderList:
            self.dis.blit(boulder.image, (boulder.x*80, boulder.y*80))
        pygame.display.update()

# a=GameWindow(1,3)