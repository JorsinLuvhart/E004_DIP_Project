# import sys
# import numpy as np
# import pygame
# import random
#
# print("Python version " + sys.version)
#
# SCREEN_WIDTH = 720
# SCREEN_HEIGHT = 720
# GRID_SIZE = 80  # please only divide/multiply this by 2s
# MARGIN = 2
# SCALE = GRID_SIZE / 80
# BOX_LENGTH = GRID_SIZE - MARGIN
# COLUMN_COUNT = int(SCREEN_WIDTH / (GRID_SIZE))
# ROW_COUNT = int(SCREEN_HEIGHT / (GRID_SIZE))
# SCREEN_TITLE = "Cooperative Bots Design"
#
#
# # warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
# class Robot():
#     def __init__(self, warehouseFloor, x, y, rbtCount):
#         self.x = x
#         self.y = y
#         self.loaded = 0
#         self.image = pygame.image.load(r"Resources/loader.png")
#         self.id = 1 + rbtCount * 2
#         warehouseFloor[self.x][self.y][1] = 1 + rbtCount * 2 + self.loaded
#
#     def move_up(self, warehouseFloor):
#         if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [3]):
#             warehouseFloor[self.x][self.y][1] = 0
#             self.y = self.y + 1
#             warehouseFloor[self.x][self.y][1] = self.id + self.loaded
#
#     def move_down(self, warehouseFloor):
#         if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [3]):
#             warehouseFloor[self.x][self.y][1] = 0
#             self.y = self.y - 1
#             warehouseFloor[self.x][self.yz][1] = self.id + self.loaded
#
#     def move_left(self, warehouseFloor):
#         if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [3]):
#             warehouseFloor[self.x][self.y][1] = 0
#             self.x = self.x - 1
#             warehouseFloor[self.x - 1][self.y][1] = self.id + self.loaded
#
#     def move_right(self, warehouseFloor):
#         if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [3]):
#             warehouseFloor[self.x][self.y][1] = 0
#             self.x = self.x + 1
#             warehouseFloor[self.x + 1][self.y][1] = self.id + self.loaded
#
#
# class Parcel():
#     def __init__(self, warehouseFloor, x, y):
#         self.x = x
#         self.y = y
#         # self.x = random.randint(0, COLUMN_COUNT-1)
#         # self.y = random.randint(0, ROW_COUNT-1)
#         # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
#         #   self.x = random.randint(0, COLUMN_COUNT-1)
#         #   self.y = random.randint(0, ROW_COUNT-1)
#         self.image = pygame.image.load(r"Resources/package.png")
#         warehouseFloor[self.x][self.y][0] = 1
#
#
# class Destination():
#     def __init__(self, warehouseFloor, x, y):
#         # self.x = random.randint(0, COLUMN_COUNT-1)
#         # self.y = random.randint(0, ROW_COUNT-1)
#         # while(warehouseFloor[self.x][self.y]):  #if there is already an object there, rerandomise the location of the parcel
#         #   self.x = random.randint(0, COLUMN_COUNT-1)
#         #   self.y = random.randint(0, ROW_COUNT-1)
#         self.x = x
#         self.y = y
#         self.image = pygame.image.load(r"Resources/warehouse.png")
#         warehouseFloor[self.x][self.y][0] = 2
#
#
# class Boulder():
#     def __init__(self, warehouseFloor, x, y):
#         # self.x = random.randint(0, COLUMN_COUNT - 1)
#         # self.y = random.randint(0, ROW_COUNT - 1)
#         # while (
#         # warehouseFloor[self.x][self.y]):  # if there is already an object there, rerandomise the location of the boulder
#         #   self.x = random.randint(0, COLUMN_COUNT - 1)
#         #   self.y = random.randint(0, ROW_COUNT - 1)
#         self.x = x
#         self.y = y
#         self.image = pygame.image.load(r"Resources/boulder.png")
#         warehouseFloor[self.x][self.y][0] = 3
#
#
# class GameWindow():
#
#     def __init__(self, manualControl, parcelNum):
#         """ Initialise object here"""
#
#         self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT, 2], dtype=int)
#         self.stepnum = 0
#         self.collected = -1
#         pygame.init()
#         self.dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#
#         # self.gridSprites = []
#         # for row in range(ROW_COUNT):
#         #     self.gridSprites.append([])
#         #     for column in range(COLUMN_COUNT):
#         #         x = column * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
#         #         y = row * (BOX_LENGTH + MARGIN) + (BOX_LENGTH + MARGIN) / 2
#         #         sprite = arcade.SpriteSolidColor(BOX_LENGTH, BOX_LENGTH, arcade.color.WHITE)
#         #         sprite.center_x = x
#         #         sprite.center_y = y
#         #         self.gridSpriteList.append(sprite)
#         #         self.gridSprites[row].append(sprite)
#
#         # robot sprite
#         self.robotList = []
#         self.robotCor = [[0, 0], [8, 0]]
#         for robot in self.robotCor:
#             self.robotList.append(Robot(self.warehouseFloor, robot[0], robot[1], len(self.robotList)))
#
#         # destination sprite
#         self.destiList = []
#         # self.destiCor=[[8,8]]
#         self.destiCor = [[8, 8], [0, 8]]
#         for desti in self.destiCor:
#             self.destiList.append(Destination(self.warehouseFloor, desti[0], desti[1]))
#
#         self.parcelList = []
#         # self.parcelCor = [[6,2],[8,4]]
#         # self.parcelCor = [[5, 3], [7, 7], [6, 3], [5, 6], [8, 4], [7, 3], [6, 3], [5, 7],
#         #                   [8, 2], [7, 5], [7, 7], [6, 3], [5, 6], [8, 4], [7, 7],[5, 3], [6, 2], [6, 4], [7, 3], [6, 3],
#         #                   [5, 7], [8, 2], [7, 5]]
#         # self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5]]
#         self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3]]
#         for i in range(parcelNum):
#             self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
#             self.collected += 1
#
#         self.boulderList = []
#         # boulderCor=[]
#         boulderCor = [[4, 6], [4, 5], [4, 4]]
#         for boulder in boulderCor:
#             self.boulderList.append(Boulder(self.warehouseFloor, boulder[0], boulder[1]))
#
#         if manualControl:
#             while True:
#                 for event in pygame.event.get():
#                     if event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_LEFT:
#                             self.action(3)
#                         if event.key == pygame.K_RIGHT:
#                             self.action(4)
#                         if event.key == pygame.K_UP:
#                             self.action(2)
#                         if event.key == pygame.K_DOWN:
#                             self.action(1)
#                         if event.key == pygame.K_SPACE:
#                             self.action(0)
#                         print(self.evaluate())
#                 self.view1()
#
#     def printWHF(self):
#         print(self.warehouseFloor[:][:][0])
#         print(self.warehouseFloor[:][:][1])
#
#     def parcelCol(self, parcel, robot):
#         # need to eventually figure out which is the collected parcel\
#         # print("Col")
#         robot.loaded = 1
#         self.warehouseFloor[parcel.x][parcel.y][0] = 0
#         self.parcelList.remove(parcel)
#         del parcel
#         while(self.warehouseFloor[self.parcelCor[self.collected % len(self.parcelCor)][0]][self.parcelCor[self.collected % len(self.parcelCor)][1]][0]):  #if there is already an object there, rerandomise the location of the parcel
#             self.collected+=1
#         self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[self.collected % len(self.parcelCor)][0],
#                                       self.parcelCor[self.collected % len(self.parcelCor)][1]))
#
#     def parcelDep(self, robot):
#         # print("Dep")
#         robot.loaded = 0
#
#     def action(self, action):
#         self.stepnum += 1
#
#         for robot in self.robotList:
#             if action % 5 == 0:
#                 pass
#             elif action % 5 == 1:
#                 robot.move_up(self.warehouseFloor)
#             elif action % 5 == 2:
#                 robot.move_down(self.warehouseFloor)
#             elif action % 5 == 3:
#                 robot.move_left(self.warehouseFloor)
#             elif action % 5 == 4:
#                 robot.move_right(self.warehouseFloor)
#             action = action // 5
#
#     def evaluate(self):
#         self.reward = 0
#         for robot in self.robotList:
#             if (self.warehouseFloor[robot.x][robot.y][0] == 1 and robot.loaded != 1):
#                 self.collected += 1
#                 for parcel in self.parcelList:
#                     if robot.x == parcel.x and robot.y == parcel.y:
#                         self.parcelCol(parcel, robot)
#                         continue
#                 self.reward += 1
#             elif (self.warehouseFloor[robot.x][robot.y][0] == 2 and robot.loaded == 1):
#                 self.parcelDep(robot)
#                 self.reward += 1
#             else:
#                 self.reward -= 0.1
#
#         return self.reward
#
#     def is_done(self):
#         if self.stepnum == 1000:
#             return True
#         return False
#
#     def observe(self):
#         ret = self.warehouseFloor.copy()
#         for i in range(len(self.robotList)):
#             ret[self.robotList[i].x][self.robotList[i].y] = 4 + i * 2 + self.robotList[i].loaded
#         return ret
#
#     def view1(self):
#
#         self.dis.fill((255, 255, 255))
#         for robot in self.robotList:
#             self.dis.blit(robot.image, (robot.x * 80, robot.y * 80))
#         for desti in self.destiList:
#             self.dis.blit(desti.image, (desti.x * 80, desti.y * 80))
#         for parcel in self.parcelList:
#             self.dis.blit(parcel.image, (parcel.x * 80, parcel.y * 80))
#         for boulder in self.boulderList:
#             self.dis.blit(boulder.image, (boulder.x * 80, boulder.y * 80))
#         pygame.display.update()
#
# a=GameWindow(1,2)

import sys
import numpy as np
import pygame
import random

print("Python version " + sys.version)

SCREEN_WIDTH = 880
SCREEN_HEIGHT = 880
GRID_SIZE = 80  # please only divide/multiply this by 2s
MARGIN = 2
SCALE = GRID_SIZE / 80
BOX_LENGTH = GRID_SIZE - MARGIN
COLUMN_COUNT = int(SCREEN_WIDTH / (GRID_SIZE))
ROW_COUNT = int(SCREEN_HEIGHT / (GRID_SIZE))
SCREEN_TITLE = "Cooperative Bots Design"


# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, warehouseFloor, x, y, rbtCount):
        self.x = x
        self.y = y
        self.loaded = 0
        self.image = pygame.image.load(r"Resources/loader.png")
        self.id = 1 + rbtCount * 2
        warehouseFloor[self.x][self.y][1] = 1 + rbtCount * 2 + self.loaded
        self.interval=0

    def move_down(self, warehouseFloor):
        # if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [3] and warehouseFloor[self.x][self.y + 1][1] not in [1,2,3,4,5,6] and (not self.loaded or warehouseFloor[self.x][self.y + 1][0] not in [1])):
        if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [0.5] and (not self.loaded or warehouseFloor[self.x][self.y + 1][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0
            self.y = self.y + 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_up(self, warehouseFloor):
        if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [0.5]  and (not self.loaded or warehouseFloor[self.x][self.y-1][0] not in [1])):
        # if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [3] and warehouseFloor[self.x][self.y - 1][1] not in [1,2,3,4,5,6] and (not self.loaded or warehouseFloor[self.x][self.y-1][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0
            self.y = self.y - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_left(self, warehouseFloor):
        # if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [3] and warehouseFloor[self.x-1][self.y][1] not in [1,2,3,4,5,6] and (not self.loaded or warehouseFloor[self.x-1][self.y][0] not in [1])):
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [0.5]  and (not self.loaded or warehouseFloor[self.x-1][self.y][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0
            self.x = self.x - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_right(self, warehouseFloor):
        # if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [3] and warehouseFloor[self.x+1][self.y][1] not in [1,2,3,4,5,6] and (not self.loaded or warehouseFloor[self.x+1][self.y][0] not in [1])):
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [0.5] and (not self.loaded or warehouseFloor[self.x+1][self.y][0] not in [1])):
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
        self.image = pygame.image.load(r"Resources/warehouse.png")
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
        self.image = pygame.image.load(r"Resources/boulder.png")
        warehouseFloor[self.x][self.y][0] = 0.5


class GameWindow():

    def __init__(self, manualControl, parcelNum):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT, 2], dtype=float)
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
        # self.robotCor = [[0, 0], [10, 0],[5,0]]
        self.robotCor = [[4, 0], [5, 0],[6,0]]
        for robot in self.robotCor:
            self.robotList.append(Robot(self.warehouseFloor, robot[0], robot[1], len(self.robotList)))

        # destination sprite
        self.destiList = []
        # self.destiCor=[[8,8]]
        # self.destiCor = [[8, 8],[4,8], [0, 8]]
        self.destiCor = [[3,10],[4,10],[5,10],[6,10],[7,10]]
        for desti in self.destiCor:
            self.destiList.append(Destination(self.warehouseFloor, desti[0], desti[1]))

        self.parcelList = []
        # self.parcelCor = [[6,2],[8,4]]
        # self.parcelCor = [[5, 3], [7, 7], [6, 3], [5, 6], [8, 4], [7, 3], [6, 3], [5, 7],
        #                   [8, 2], [7, 5], [7, 7], [6, 3], [5, 6], [8, 4], [7, 7],[5, 3], [6, 2], [6, 4], [7, 3], [6, 3],
        #                   [5, 7], [8, 2], [7, 5]]
        # self.parcelCor = [[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5],[7,7],[6,3],[5,6],[8,4],[7,3],[6,3],[5,7],[8,2],[7,5]]
        # self.parcelCor = [[2, 5], [6, 5],[4,7],[6, 4], [3, 3],[2, 2], [5, 3], [2, 5], [6, 2], [6, 4], [3, 3], [2, 1], [1, 6],[7,7],]
        # self.parcelCor = [[3,1],[4,1],[5,1],[6,1],[7,1],[3,3],[4,3],[5,3],[6,3],[7,3]]
        # self.parcelCor = [[4,3],[5,3],[6,3],[9,6],[1,6],[5,5],[2,2],[8,2],[6, 5],[4,7],[6, 4]]
        # self.parcelCor = [[5,6],[5,6],[6,4],[5,6],[5,4],[5,6],[4,4],[3,4],[7,4],[5,2],[4,2],[5,6],[5,6],[6,4],[5,6],[5,4],[5,6],[4,4],[3,4],[7,4],[5,2],[6,2]]
        self.parcelCor = [[5,4],[6,4],[4,4],[7,4],[3,4]]
        for i in range(parcelNum):
            self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[i][0], self.parcelCor[i][1]))
            self.collected += 1

        self.boulderList = []
        # boulderCor=[[0,10],[1,10],[2,10],[8,10],[9,10],[10,10],[0,9],[1,9],[2,9],[8,9],[9,9],[10,9],[0,8],[1,8],[2,8],[8,8],[9,8],[10,8]]
        boulderCor=[]
        # boulderCor=[[5,5],[4,5],[6,5]]
        # boulderCor=[[1,i]for i in range(11)]+[[9,i]for i in range(11)]
        # boulderCor = [[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5]]
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
                        # self.printWHF()
                        print(self.evaluate())

                self.view1()


    def printWHF(self):
        print(self.warehouseFloor)
        # print(self.warehouseFloor[:][:][1])

    def parcelCol(self, parcel, robot):
        # need to eventually figure out which is the collected parcel\
        # print("Col")
        robot.loaded = 1
        self.warehouseFloor[parcel.x][parcel.y][0] = 0
        self.parcelList.remove(parcel)
        del parcel
        # while (self.warehouseFloor[self.parcelCor[self.collected % len(self.parcelCor)][0]][self.parcelCor[self.collected % len(self.parcelCor)][1]][0]):  # if there is already an object there, rerandomise the location of the parcel
        #     self.collected += 1
        for parcel in self.parcelList:
            if robot.x == parcel.x and robot.y == parcel.y:
                self.warehouseFloor[parcel.x][parcel.y][0] = 1
                continue
        self.parcelList.append(Parcel(self.warehouseFloor, self.parcelCor[self.collected % len(self.parcelCor)][0],
                                      self.parcelCor[self.collected % len(self.parcelCor)][1]))

    def parcelDep(self, robot):
        # print("Dep")
        robot.loaded = 0

    def action(self, action):
        self.stepnum += 1

        for robot in self.robotList:

            if action % 4 == 0:
                robot.move_up(self.warehouseFloor)
            elif action % 4 == 1:
                robot.move_down(self.warehouseFloor)
            elif action % 4 == 2:
                robot.move_left(self.warehouseFloor)
            elif action % 4 == 3:
                robot.move_right(self.warehouseFloor)
            action = action // 4
            # if action % 5 == 0:
            #     pass
            # elif action % 5 == 1:
            #     robot.move_up(self.warehouseFloor)
            # elif action % 5 == 2:
            #     robot.move_down(self.warehouseFloor)
            # elif action % 5 == 3:
            #     robot.move_left(self.warehouseFloor)
            # elif action % 5 == 4:
            #     robot.move_right(self.warehouseFloor)
            # action = action // 5

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

# a=GameWindow(1,1)