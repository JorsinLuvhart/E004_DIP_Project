import sys
import numpy as np
import pygame
import random
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import platform
import pygame
import PySimpleGUI as pg
import os
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


# warehouse floor, 0=blank space, 1=robot, 2=parcel, 3=destination
class Robot():
    def __init__(self, warehouseFloor, x, y,rbtCount):
        self.x = x
        self.y = y
        self.loaded = 0
        self.image = pygame.image.load(r"Resources/loader.png")
        self.id = 1 + rbtCount*2
        warehouseFloor[self.x][self.y][1] = 1 + rbtCount*2 + self.loaded

    def move_down(self, warehouseFloor):
        if (self.y < ROW_COUNT - 1 and warehouseFloor[self.x][self.y + 1][0] not in [3] and (not self.loaded or warehouseFloor[self.x][self.y + 1][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0  
            self.y = self.y + 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded  

    def move_up(self, warehouseFloor):
        if (self.y > 0 and warehouseFloor[self.x][self.y - 1][0] not in [3] and (not self.loaded or warehouseFloor[self.x][self.y-1][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0  
            self.y = self.y - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_left(self, warehouseFloor):
        if (self.x > 0 and warehouseFloor[self.x - 1][self.y][0] not in [3] and (not self.loaded or warehouseFloor[self.x-1][self.y][0] not in [1])):
            warehouseFloor[self.x][self.y][1] = 0  
            self.x = self.x - 1
            warehouseFloor[self.x][self.y][1] = self.id + self.loaded

    def move_right(self, warehouseFloor):
        if (self.x < COLUMN_COUNT - 1 and warehouseFloor[self.x + 1][self.y][0] not in [3] and (not self.loaded or warehouseFloor[self.x+1][self.y][0] not in [1])):
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
        warehouseFloor[self.x][self.y][0] = 3


class GameWindow():

    def __init__(self, manualControl, parcelNum):
        """ Initialise object here"""

        self.warehouseFloor = np.zeros([COLUMN_COUNT, ROW_COUNT,2], dtype=int)
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
            self.robotList.append(Robot(self.warehouseFloor, robot[0], robot[1],len(self.robotList)))

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
                        if event.key == pygame.K_DOWN:
                            self.action(2)
                        if event.key == pygame.K_UP:
                            self.action(1)
                        if event.key == pygame.K_SPACE:
                            self.action(0)
                        print(self.evaluate())
                self.view1()
                self.view2()

    def printWHF(self):
      print(self.warehouseFloor[:][:][0])
      print(self.warehouseFloor[:][:][1])

    def parcelCol(self, parcel, robot):
        # need to eventually figure out which is the collected parcel\
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

        for robot in self.robotList:
          if action % 5 == 0:
            pass
          elif action % 5 == 1:
            robot.move_up(self.warehouseFloor)
          elif action % 5 == 2:
            robot.move_down(self.warehouseFloor)
          elif action % 5 == 3:
            robot.move_left(self.warehouseFloor)
          elif action % 5 == 4:
            robot.move_right(self.warehouseFloor)
          action = action//5

    def evaluate(self):
        self.reward = 0
        for robot in self.robotList:
            if (self.warehouseFloor[robot.x][robot.y][0] == 1 and robot.loaded != 1):
                self.collected += 1
                for parcel in self.parcelList:
                    if robot.x == parcel.x and robot.y == parcel.y:
                        self.parcelCol(parcel, robot)
                        continue
                self.reward += 1
            elif (self.warehouseFloor[robot.x][robot.y][0] == 2 and robot.loaded == 1):
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

        #window = Tk()

        #window.title("Cooperative Bots Design")
        #window.geometry('1600x900')
        #combo = Combobox(window)
        #combo1 = Combobox(window)

        #def click():
            #lbl.configure(text="Parcel is at XXX")
        #def click1():
            #lbl.configure(text="Parcel delivered at XXX")

        #lbl = Label(window, text="Status: \n\n Robot 1: \n\n Robot 2: \n\n Robot 3: \n\n", font=("Arial Bold", 10))
        #lbl.grid(column=0, row=0)

        #lbl1 = Label(window, text="Parameters: \n No. of parcel:\n", font=("Arial Bold", 10))
        #lbl1.grid(column=1500, row=0)
        #btn = Button(window, text="Parcel details", command=click)
        #btn.grid(column=1500, row=2)
        #combo['values'] = (1, 2, 3, 4, 5)
        #combo.current(1)  # set the selected item
        #combo.grid(column=1500, row=1)

        #lbl1 = Label(window, text="No. of destination:.", font=("Arial Bold", 10))
        #lbl1.grid(column=1500, row=5)
        #btn1 = Button(window, text="Destination details", command=click1)
        #btn1.grid(column=1500, row=7)
        #combo1['values'] = (1, 2, 3, 4, 5)
        #combo1.current(1)  # set the selected item
        #combo1.grid(column=1500, row=6)


        WHITE = (0,0,0)
        self.dis.fill((0, 255, 255))
        blockSize = 80 #Set the size of the grid block
        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                rect = pygame.Rect(x*blockSize, y*blockSize,
                                blockSize, blockSize)
                pygame.draw.rect(self.dis, WHITE, rect, 1)
        for robot in self.robotList:
            self.dis.blit(robot.image, (robot.x * 80, robot.y * 80))
        for desti in self.destiList:
            self.dis.blit(desti.image, (desti.x * 80, desti.y * 80))
        for parcel in self.parcelList:
            self.dis.blit(parcel.image, (parcel.x * 80, parcel.y * 80))
        for boulder in self.boulderList:
            self.dis.blit(boulder.image, (boulder.x * 80, boulder.y * 80))
        pygame.display.update()
        #window.mainloop()

    def view2(self):
        # set theme
        pg.theme("default1")

        #create the layout
        layout = [
            [
                pg.Text("Status of Robot: ", size=(10, 10)),
                pg.OptionMenu(values = ("Robot 1", "Robot 2", "Robot 3"), size = (20,1)), pg.Text("1", size=(8,1))
                #pg.Checkbox("Robot 1", "1.00"),
                #pg.Checkbox("Robot 2", "2.00"),
                #pg.Checkbox("Robot 3", "3.00"),
                
            ],
            [
                pg.Text("Number of Parcels: ",  size = (10, 10)),
                pg.OptionMenu(values = ("1", "2", "3"), size = (20, 1)), pg.Text("1", size = (8, 1))
                #pg.Radio("1", "1"),
                #pg.Radio("2", "2"),
                #pg.Radio("3", "3"),
                
            ],
            [
                pg.Text("Number of destination: ", size = (10, 10)),
                pg.OptionMenu(values = ("1", "2", "3"), size = (20, 1)), pg.Text("1", size = (8, 1))
                #pg.Radio("1", "1.0"),
                #pg.Radio("2", "2.0"),
                #pg.Radio("3", "3.0"),
                
            ],
            [
                pg.Button('Start', button_color=('white', 'black'), key='Start'),      
                pg.Button('Stop', button_color=('white', 'black'), key='Stop'),      
                pg.Button('Reset', button_color=('white', 'firebrick3'), key='Reset'),      
                pg.Button('Submit', button_color=('white', 'springgreen4'), key='Submit')
            ]

        ]
        
        # Create Window
        # Blue = (0,0,200)
        window = pg.Window("Cooperative Bots Design", layout, default_element_size=(12,1), text_justification='r', auto_size_text=False, auto_size_buttons=False, default_button_element_size=(12,1), finalize=True)

        window['Stop'].update(disabled=True)      
        window['Reset'].update(disabled=True)      
        window['Submit'].update(disabled=True)      
        recording = have_data = False
        # Event Loop

        while True:      
            event, values = window.read()      
            print(event)      
            if event == pg.WIN_CLOSED:
                exit(69)      
            if event == 'Start':      
                window['Start'].update(disabled=True)      
                window['Stop'].update(disabled=False)      
                window['Reset'].update(disabled=False)      
                window['Submit'].update(disabled=True)      
                recording = True      
            elif event == 'Stop'  and recording:      
                window['Stop'].update(disabled=True)      
                window['Start'].update(disabled=False)      
                window['Submit'].update(disabled=False)      
                recording = False      
                have_data = True      
            elif event == 'Reset':      
                window['Stop'].update(disabled=True)      
                window['Start'].update(disabled=False)      
                window['Submit'].update(disabled=True)      
                window['Reset'].update(disabled=False)      
                recording = False      
                have_data = False      
            elif event == 'Submit'  and have_data:      
                window['Stop'].update(disabled=True)      
                window['Start'].update(disabled=False)      
                window['Submit'].update(disabled=True)      
                window['Reset'].update(disabled=False)      
                recording = False     


GameWindow(1,2)
