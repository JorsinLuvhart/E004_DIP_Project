import sys
import numpy as np
import pygame
import random

print("Python version " + sys.version)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
GRID_SIZE = 80  # please only divide/multiply this by 2s
MARGIN = 2
SCALE = GRID_SIZE / 80
BOX_LENGTH = GRID_SIZE - MARGIN
COLUMN_COUNT = int(SCREEN_WIDTH / (GRID_SIZE))
ROW_COUNT = int(SCREEN_HEIGHT / (GRID_SIZE))
SCREEN_TITLE = "Cooperative Bots Design"
MOVEMENT_SPEED = 1
NUM_BOTS = 1
NUM_DESTI = 1
NUM_PARCEL = 1


# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, warehouseFloor, x, y):
        self.x = x
        self.y = y
        self.loaded = 0
        self.image = pygame.image.load(r"Resources/loader.png")
        # warehouseFloor[self.x][self.y] = 1 + self.loaded

    def move_up(self, warehouseFloor):
        if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1] not in [3]):
            if not (self.loaded == 1 and warehouseFloor[self.x][self.y + 1] == 1):
                self.y = self.y + 1

    def move_down(self, warehouseFloor):
        if (self.y > 0 and warehouseFloor[self.x][self.y - 1] not in [3]):
            if not (self.loaded == 1 and warehouseFloor[self.x][self.y - 1] == 1):
                self.y = self.y - 1

    def move_left(self, warehouseFloor):
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y] not in [3]):
            if not (self.loaded == 1 and warehouseFloor[self.x - 1][self.y] == 1):
                self.x = self.x - 1

    def move_right(self, warehouseFloor):
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y] not in [3]):
            if not (self.loaded == 1 and warehouseFloor[self.x + 1][self.y] == 1):
                self.x = self.x + 1


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
        warehouseFloor[self.x][self.y] = 1


class Destination():
    def __init__(self, warehouseFloor, x, y):
        # self.x = random.randint(0, COLUMN_COUNT-1)
        # self.y = random.randint(0, ROW_COUNT-1)
        # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
        #   self.x = random.randint(0, COLUMN_COUNT-1)
        #   self.y = random.randint(0, ROW_COUNT-1)
        self.x = x
        self.y = y
        self.image = pygame.image.load(r"Resources/warehouse.png")
        warehouseFloor[self.x][self.y] = 2


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
        self.image = pygame.image.load(r"Resources/boulder.png")
        warehouseFloor[self.x][self.y] = 3


class GameWindow():

    def __init__(self, manualControl, parcelNum):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT], dtype=int)
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
        self.robotCor = [[0, 0], [8, 0]]
        for robot in self.robotCor:
            self.robotList.append(Robot(self.warehouseFloor, robot[0], robot[1]))

        # destination sprite
        self.destiList = []
        # self.destiCor=[[8,8]]
        self.destiCor = [[8, 8], [0, 8]]
        for desti in self.destiCor:
            self.destiList.append(Destination(self.warehouseFloor, desti[0], desti[1]))

        self.parcelList = []
        # self.parcelCor = [[6,2],[8,4]]
        # self.parcelCor = [[5, 3], [7, 7], [6, 3], [5, 6], [8, 4], [7, 3], [6, 3], [5, 7],
        #                   [8, 2], [7, 5], [7, 7], [6, 3], [5, 6], [8, 4], [7, 7],[5, 3], [6, 2], [6, 4], [7, 3], [6, 3],
        #                   [5, 7], [8, 2], [7, 5]]
        # self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5]]
        self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3]]
        for i in range(parcelNum):
            self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
            self.collected += 1

        self.boulderList = []
        # boulderCor=[]
        boulderCor = [[4, 6], [4, 5],[4, 4]]
        for boulder in boulderCor:
            self.boulderList.append(Boulder(self.warehouseFloor, boulder[0], boulder[1]))

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

    def parcelCol(self, parcel, robot):
        # need to eventually figure out which is the collected parcel\
        # print("Col")
        robot.loaded = 1
        self.warehouseFloor[parcel.x][parcel.y] = 0
        self.parcelList.remove(parcel)
        del parcel
        self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[self.collected % len(self.parcelCor)][0],
                                      self.parcelCor[self.collected % len(self.parcelCor)][1]))

    def parcelDep(self, robot):
        # print("Dep")
        robot.loaded = 0

    def action(self, action):
        self.stepnum += 1

        if action // 5 == 0:
            pass
        if action // 5 == 1:
            self.robotList[0].move_up(self.warehouseFloor)
        if action // 5 == 2:
            self.robotList[0].move_down(self.warehouseFloor)
        if action // 5 == 3:
            self.robotList[0].move_left(self.warehouseFloor)
        if action // 5 == 4:
            self.robotList[0].move_right(self.warehouseFloor)
        if action % 5 == 0:
            pass
        if action % 5 == 1:
            self.robotList[1].move_up(self.warehouseFloor)
        if action % 5 == 2:
            self.robotList[1].move_down(self.warehouseFloor)
        if action % 5 == 3:
            self.robotList[1].move_left(self.warehouseFloor)
        if action % 5 == 4:
            self.robotList[1].move_right(self.warehouseFloor)

    def evaluate(self):
        self.reward = 0
        for robot in self.robotList:
            if (self.warehouseFloor[robot.x][robot.y] == 1 and robot.loaded != 1):
                self.collected += 1
                for parcel in self.parcelList:
                    if robot.x == parcel.x and robot.y == parcel.y:
                        self.parcelCol(parcel, robot)
                        continue
                self.reward += 1
            elif (self.warehouseFloor[robot.x][robot.y] == 2 and robot.loaded == 1):
                self.parcelDep(robot)
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
        for i in range(len(self.robotList)):
            ret[self.robotList[i].x][self.robotList[i].y] = 4 + i * 2 + self.robotList[i].loaded
        return ret

    def view1(self):

        self.dis.fill((255, 255, 255))
        for robot in self.robotList:
            self.dis.blit(robot.image, (robot.x * 80, robot.y * 80))
        for desti in self.destiList:
            self.dis.blit(desti.image, (desti.x * 80, desti.y * 80))
        for parcel in self.parcelList:
            self.dis.blit(parcel.image, (parcel.x * 80, parcel.y * 80))
        for boulder in self.boulderList:
            self.dis.blit(boulder.image, (boulder.x * 80, boulder.y * 80))
        pygame.display.update()

a=GameWindow(1,2)
