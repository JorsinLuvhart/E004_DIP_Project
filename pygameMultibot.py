import sys
import numpy as np
import pygame
import random

print("Python version " + sys.version)

SCREEN_WIDTH = 880
SCREEN_HEIGHT = 880
GRID_SIZE = 80  # please only divide/multiply this by 2s
# MARGIN = 2 
SCALE = GRID_SIZE / 80
# BOX_LENGTH = GRID_SIZE - MARGIN
COLUMN_COUNT = int(SCREEN_WIDTH / (GRID_SIZE))
ROW_COUNT = int(SCREEN_HEIGHT / (GRID_SIZE))
ROBOT_COLLISION = True
# If False, no collision, if True, collision allowed
# SCREEN_TITLE = "Cooperative Bots Design"


# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, warehouseFloor, x, y,rbtCount):
        self.x = x
        self.y = y
        self.loaded = 0
        self.image = pygame.image.load(r"Resources/Roomba-bot.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (GRID_SIZE*SCALE, GRID_SIZE*SCALE))
        self.id = 1 + rbtCount*2
        warehouseFloor[self.x][self.y][1] = 1 + rbtCount*2 + self.loaded
        self.interval = 0

    def move_down(self, warehouseFloor):
        if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x][self.y + 1][0] not in [1]) and (warehouseFloor[self.x][self.y+1][1] == 0 or ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0  
            self.y = self.y + 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded  

    def move_up(self, warehouseFloor):
        if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x][self.y-1][0] not in [1]) and (warehouseFloor[self.x][self.y-1][1] == 0 or ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0  
            self.y = self.y - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_left(self, warehouseFloor):
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x-1][self.y][0] not in [1]) and (warehouseFloor[self.x - 1][self.y][1] == 0 or ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0  
            self.x = self.x - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_right(self, warehouseFloor):
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x+1][self.y][0] not in [1]) and (warehouseFloor[self.x + 1][self.y][1] == 0 or ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0  
            self.x = self.x + 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded



class Parcel():
    def __init__(self, warehouseFloor, x, y):
        self.x = x
        self.y = y
        # self.x = random.randint(0, COLUMN_COUNT-1)
        # self.y = random.randint(0, ROW_COUNT-1)
        # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        #   self.x = random.randint(0, COLUMN_COUNT-1)
        #   self.y = random.randint(0, ROW_COUNT-1)
        self.image = pygame.image.load(r"Resources/package.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (GRID_SIZE*SCALE, GRID_SIZE*SCALE))
        warehouseFloor[self.x][self.y][0] = 1


class Destination():
    def __init__(self, warehouseFloor, x, y):
        # self.x = random.randint(0, COLUMN_COUNT-1)
        # self.y = random.randint(0, ROW_COUNT-1)
        # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        #   self.x = random.randint(0, COLUMN_COUNT-1)
        #   self.y = random.randint(0, ROW_COUNT-1)
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"Resources/warehouse-new.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (GRID_SIZE*SCALE, GRID_SIZE*SCALE))
        warehouseFloor[self.x][self.y][0] = 2


class Boulder():
    def __init__(self, warehouseFloor, x, y):
        # self.x = random.randint(0, COLUMN_COUNT - 1)
        # self.y = random.randint(0, ROW_COUNT - 1)
        # while (
        # warehouseFloor[self.x][self.y]):  # if there is already an object there, rerandomise the location of the boulder
        #   self.x = random.randint(0, COLUMN_COUNT - 1)
        #   self.y = random.randint(0, ROW_COUNT - 1)
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"Resources/brick.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (GRID_SIZE*SCALE, GRID_SIZE*SCALE))
        warehouseFloor[self.x][self.y][0] = 0.5


class Human():
    def __init__(self, warehouseFloor, x, y):
        self.x = x
        self.y = y
        self.direction = 1 #1 is right side -1 is left
        self.image = pygame.image.load(r"Resources/person.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (GRID_SIZE*SCALE, GRID_SIZE*SCALE))
        warehouseFloor[self.x][self.y][0] = 1.5

    def randMov(self, warehouseFloor):
      choice = random.randint(0, 2)
      if choice%3 == 0: #move left
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] == 0 and warehouseFloor[self.x - 1][self.y][1] == 0):
            warehouseFloor[self.x][self.y][0] = 0  
            self.x = self.x - 1
            warehouseFloor[self.x][self.y][0] = 1.5 
      elif choice%3 == 1: #move right
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] == 0 and warehouseFloor[self.x + 1][self.y][1] == 0):
            warehouseFloor[self.x][self.y][0] = 0  
            self.x = self.x + 1
            warehouseFloor[self.x][self.y][0] = 1.5

    def movTilCol(self, warehouseFloor):
      if (self.x+self.direction >= 0 and self.x+self.direction < COLUMN_COUNT and warehouseFloor[self.x+self.direction][self.y][0] == 0 and warehouseFloor[self.x+self.direction][self.y][1] == 0):
        warehouseFloor[self.x][self.y][0] = 0
        self.x = self.x + self.direction
        warehouseFloor[self.x][self.y][0] = 1.5
      else:
        self.direction = self.direction * -1
        if (self.x+self.direction >= 0 and self.x+self.direction < COLUMN_COUNT and warehouseFloor[self.x+self.direction][self.y][0] == 0 and warehouseFloor[self.x+self.direction][self.y][1] == 0):
          warehouseFloor[self.x][self.y][0] = 0
          self.x = self.x + self.direction
          warehouseFloor[self.x][self.y][0] = 1.5
        

class GameWindow():

    def __init__(self, manualControl, parcelNum):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT,2], dtype=float)
        self.stepnum = 0
        self.collected = -1
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
        self.robotList = []
        self.robotCor = [[4, 0], [5, 0], [6, 0]]
        for robot in self.robotCor:
            self.robotList.append(Robot(self.warehouseFloor, robot[0], robot[1],len(self.robotList)))

        # destination sprite
        self.destiList = []
        # self.destiCor=[[8,8]]
        self.destiCor = [[3, 10], [4, 10], [5, 10], [6, 10], [7,10]]
        for desti in self.destiCor:
            self.destiList.append(Destination(self.warehouseFloor, desti[0], desti[1]))

        self.parcelList = []
        # self.parcelCor = [[6,2],[8,4]]
        # self.parcelCor = [[5, 3], [7, 7], [6, 3], [5, 6], [8, 4], [7, 3], [6, 3], [5, 7],
        #                   [8, 2], [7, 5], [7, 7], [6, 3], [5, 6], [8, 4], [7, 7],[5, 3], [6, 2], [6, 4], [7, 3], [6, 3],
        #                   [5, 7], [8, 2], [7, 5]]
        # self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5]]
        # self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3]]
        self.parcelCor = [[5,4],[6,4],[4,4],[7,4],[3,4]]
        for i in range(parcelNum):
            self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
            self.collected += 1

        self.boulderList = []
        # boulderCor=[]
        boulderCor = []
        for boulder in boulderCor:
            self.boulderList.append(Boulder(self.warehouseFloor, boulder[0], boulder[1]))

        self.humanList = []
        humanCor = []
        for human in humanCor:
            self.humanList.append(Human(self.warehouseFloor, human[0], human[1]))

        if manualControl:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.action(2)
                        elif event.key == pygame.K_RIGHT:
                            self.action(3)
                        elif event.key == pygame.K_DOWN:
                            self.action(1)
                        elif event.key == pygame.K_UP:
                            self.action(0)
                        print(self.evaluate())
                self.view1()

    def printWHF(self):
      print(self.warehouseFloor[:][:][0])
      print(self.warehouseFloor[:][:][1])

    def parcelCol(self, parcel, robot):
        # need to eventually figure out which is the collected parcel
        # print("Col")
        robot.loaded = 1
        self.warehouseFloor[parcel.x][parcel.y][0] = 0
        self.parcelList.remove(parcel)
        del parcel
        self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[self.collected % len(self.parcelCor)][0],
                                      self.parcelCor[self.collected % len(self.parcelCor)][1]))


    def parcelDep(self, robot):
        # print("Dep")
        robot.loaded = 0

    def action(self, action):
        self.stepnum += 1

        for human in self.humanList:
          human.movTilCol(self.warehouseFloor)
        
        for robot in self.robotList:
          if action % 4 == 0:
            robot.move_up(self.warehouseFloor)
          elif action % 4 == 1:
            robot.move_down(self.warehouseFloor)
          elif action % 4 == 2:
            robot.move_left(self.warehouseFloor)
          elif action % 4 == 3:
            robot.move_right(self.warehouseFloor)
          action = action//4

        for robot in self.robotList:
          self.warehouseFloor[robot.x][robot.y][1] = robot.id

        for parcel in self.parcelList:
          self.warehouseFloor[parcel.x][parcel.y][0] = 1

    def evaluate(self):
        self.reward = 0
        for robot in self.robotList:
            if (self.warehouseFloor[robot.x][robot.y][0] == 1 and robot.loaded != 1):
                self.collected += 1
                robot.interval=0
                # if robot==self.robotList[0]:
                #     self.reward+=6
                for parcel in self.parcelList:
                    if robot.x == parcel.x and robot.y == parcel.y:
                        self.parcelCol(parcel, robot)
                        continue
                self.reward += 1
            elif (self.warehouseFloor[robot.x][robot.y][0] == 2 and robot.loaded == 1):
                self.parcelDep(robot)
                robot.interval = 0
                # if robot==self.robotList[0]:
                #     self.reward+=6
                self.reward += 1
            else:
                if robot.interval<70:
                    robot.interval+=1
                self.reward -= 0.005*robot.interval

        return self.reward


    def is_done(self):
        if self.stepnum == 1000:
            return True
        return False

    def observe(self):
        ret = self.warehouseFloor.copy()
        for i in range(len(self.robotList)):
            ret[self.robotList[i].x][self.robotList[i].y] = 4 + i * 2 + self.robotList[i].loaded
        return ret

    def view1(self):
        WHITE = (0,0,0)
        self.dis.fill((0, 255, 255))
        blockSize = GRID_SIZE #Set the size of the grid block
        # for x in range(SCREEN_WIDTH):
        #    for y in range(SCREEN_HEIGHT):
        #        rect = pygame.Rect(x*blockSize, y*blockSize,
        #                        blockSize, blockSize)
        #        pygame.draw.rect(self.dis, WHITE, rect, 1)
        for robot in self.robotList:
            if robot.loaded == 1:
                robot.image = pygame.image.load(r"Resources/robot-with-load.png")
            else:
                robot.image = pygame.image.load(r"Resources/robot-without-load.png")
            self.dis.blit(robot.image, (robot.x * GRID_SIZE, robot.y * GRID_SIZE))
        for desti in self.destiList:
            self.dis.blit(desti.image, (desti.x * GRID_SIZE, desti.y * GRID_SIZE))
        for parcel in self.parcelList:
            self.dis.blit(parcel.image, (parcel.x * GRID_SIZE, parcel.y * GRID_SIZE))
        for boulder in self.boulderList:
            self.dis.blit(boulder.image, (boulder.x * GRID_SIZE, boulder.y * GRID_SIZE))
        for human in self.humanList:
            self.dis.blit(human.image, (human.x * GRID_SIZE, human.y * GRID_SIZE))
        pygame.display.update()

GameWindow(1,2)
