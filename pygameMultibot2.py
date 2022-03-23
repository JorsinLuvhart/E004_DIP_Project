import sys
import numpy as np
import pygame
import random

print("Python version " + sys.version)

SCREEN_WIDTH = 880
SCREEN_HEIGHT = 880
GRID_SIZE = 80  # please only divide/multiply this by 2s
#MARGIN = 2
SCALE = GRID_SIZE / 80
#BOX_LENGTH = GRID_SIZE - MARGIN
COLUMN_COUNT = int(SCREEN_WIDTH / (GRID_SIZE))
ROW_COUNT = int(SCREEN_HEIGHT / (GRID_SIZE))
#SCREEN_TITLE = "Cooperative Bots Design"
ROBOT_COLLISION = True

# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, warehouseFloor, x, y,rbtCount):
        self.x = x
        self.y = y
        self.prevX = 0
        self.prevY = 0
        self.prev2X = 0
        self.prev2Y = 0
        self.loaded = 0
        self.prevLoad=0
        self.prev2Load=0
        self.image = pygame.image.load(r"Resources/Roomba-bot.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (int(GRID_SIZE*SCALE), int(GRID_SIZE*SCALE)))
        self.id = 1 + rbtCount*2
        warehouseFloor[self.x][self.y][1] = 1 + rbtCount*2 + self.loaded
        self.interval = 0

    def move_down(self, warehouseFloor):
        if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x][self.y + 1][0] not in [1]) and (warehouseFloor[self.x][self.y+1][1] == 0 or not ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0
            self.prev2X = self.prevX
            self.prev2Y = self.prevY
            self.prevX = self.x
            self.prevY = self.y
            self.y = self.y + 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_up(self, warehouseFloor):
        if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x][self.y-1][0] not in [1]) and (warehouseFloor[self.x][self.y-1][1] == 0 or not ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0
            self.prev2X = self.prevX
            self.prev2Y = self.prevY
            self.prevX = self.x
            self.prevY = self.y
            self.y = self.y - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_left(self, warehouseFloor):
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x-1][self.y][0] not in [1]) and (warehouseFloor[self.x - 1][self.y][1] == 0 or not ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0
            self.prev2X = self.prevX
            self.prev2Y = self.prevY
            self.prevX = self.x
            self.prevY = self.y
            self.x = self.x - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_right(self, warehouseFloor):
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [0.5,1.5] and (not self.loaded or warehouseFloor[self.x+1][self.y][0] not in [1]) and (warehouseFloor[self.x + 1][self.y][1] == 0 or not ROBOT_COLLISION)):
            warehouseFloor[self.x][self.y][1] = 0
            self.prev2X = self.prevX
            self.prev2Y = self.prevY
            self.prevX = self.x
            self.prevY = self.y
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
        self.image = pygame.transform.scale(self.image, (int(GRID_SIZE*SCALE), int(GRID_SIZE*SCALE)))
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
        self.image = pygame.image.load(r"Resources/desti.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (int(GRID_SIZE*SCALE), int(GRID_SIZE*SCALE)))
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
        self.image = pygame.transform.scale(self.image, (int(GRID_SIZE*SCALE), int(GRID_SIZE*SCALE)))
        warehouseFloor[self.x][self.y][0] = 0.5


class Human():
    def __init__(self, warehouseFloor, x, y):
        self.x = x
        self.y = y
        self.direction = 1 #1 is right side -1 is left
        self.image = pygame.image.load(r"Resources/person.png")
#        width, height = self.image.get_width(), self.image.get_height()  # get size of image
        self.image = pygame.transform.scale(self.image, (int(GRID_SIZE*SCALE), int(GRID_SIZE*SCALE)))
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

    def __init__(self, manualControl, parcelNum,loadFloor):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT,2], dtype=float)
        self.stepnum = 0
        self.collected = -1
        pygame.init()
        self.dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.loadFloor=loadFloor

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

        self.parcelCor = [[5,4],[6,4],[4,4],[7,4],[3,4]]
        for i in range(parcelNum):
            self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
            self.collected += 1

        self.boulderList = []
        boulderCor = [[5,5],[4,5],[6,5]]
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
                        self.printWHF()
                        print(self.evaluate())
                self.view1()

    def printWHF(self):
      print(self.warehouseFloor[:][:][:])
      # print(self.warehouseFloor[:][:][1])

    def parcelCol(self, parcel, robot):
        # need to eventually figure out which is the collected parcel\
        # print("Col")
        robot.loaded = 1
        self.warehouseFloor[parcel.x][parcel.y][0] = 0
        soundObj = pygame.mixer.Sound('Resources/parcelpickup.wav')
        soundObj.play()
        
        self.parcelList.remove(parcel)
        del parcel
        self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[self.collected % len(self.parcelCor)][0],
                                      self.parcelCor[self.collected % len(self.parcelCor)][1]))
        for parcel in self.parcelList:
            if robot.x == parcel.x and robot.y == parcel.y:
                self.warehouseFloor[parcel.x][parcel.y][0] = 1
                continue

    def parcelDep(self, robot):
        # print("Dep")
        robot.loaded = 0
        soundObj = pygame.mixer.Sound('Resources/movement.mp3')
        soundObj.play()

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

    def evaluate(self):
        self.reward = 0
        for robot in self.robotList:
            robot.prev2Load=robot.prevLoad
            robot.prevLoad=robot.loaded
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
                # if robot.x==robot.prev2X and robot.y==robot.prev2Y and robot.loaded==robot.prev2Load:
                if robot.y>robot.prevY and robot.loaded==0 and self.collected>2:
                    self.reward-=0.1
                if robot.y<robot.prevY and robot.loaded==1:
                    self.reward-=0.1
                # if robot.y<robot.prevY and robot.loaded==0 and self.collected>2:
                #     self.reward+=0.5
                # if robot.y>robot.prevY and robot.loaded==1:
                #     self.reward+=0.5
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
        # for i in range(len(self.robotList)):
        #     ret[self.robotList[i].x][self.robotList[i].y] = 4 + i * 2 + self.robotList[i].loaded
        return ret

    def view1(self):
        WHITE = (0,0,0)
        self.dis.fill((255, 255, 255))
        blockSize = GRID_SIZE #Set the size of the grid block
        # for x in range(SCREEN_WIDTH):
        #    for y in range(SCREEN_HEIGHT):
        #        rect = pygame.Rect(x*blockSize, y*blockSize,
        #                        blockSize, blockSize)
        #        pygame.draw.rect(self.dis, WHITE, rect, 1)
        if self.loadFloor:
            for i in range(11):
                for j in range(11):
                    self.dis.blit(pygame.image.load(r"Resources/floor.png"),(i * GRID_SIZE, j * GRID_SIZE))
            parcelPosition=[[5,4],[6,4],[4,4],[7,4],[3,4],[7,2],[6,2],[5,2],[4,2],[3,2]]
            for parcelPos in parcelPosition:
                self.dis.blit(pygame.image.load(r"Resources/parcel position.png"), (parcelPos[0] * GRID_SIZE, parcelPos[1] * GRID_SIZE))
        for desti in self.destiList:
            self.dis.blit(desti.image, (desti.x * GRID_SIZE, desti.y * GRID_SIZE))
        for parcel in self.parcelList:
            self.dis.blit(parcel.image, (parcel.x * GRID_SIZE, parcel.y * GRID_SIZE))
        for boulder in self.boulderList:
            self.dis.blit(boulder.image, (boulder.x * GRID_SIZE, boulder.y * GRID_SIZE))
        for human in self.humanList:
            self.dis.blit(human.image, (human.x * GRID_SIZE, human.y * GRID_SIZE))
        for robot in self.robotList:
            if robot.loaded == 1:
                robot.image = pygame.image.load(r"Resources/robot-with-load.png")
            else:
                robot.image = pygame.image.load(r"Resources/robot-without-load.png")
            self.dis.blit(robot.image, (robot.x * GRID_SIZE, robot.y * GRID_SIZE))
        pygame.display.update()

#GameWindow(1,2,1)
