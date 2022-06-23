import numpy as np
import numpy.random as rd
import pygame
import colors
import pyautogui
#regler ici les paramètres initiaux à la création d'un caractere


width, height= pyautogui.size()

MS_PER_FRAME=10

XSIZE=width-100
YSIZE=height-200

GREEN_NUMBER=15
RED_NUMBER=8
SMALLNESS=3
VISION_DISTANCE=200
SIZE=max(min(XSIZE,YSIZE)//(SMALLNESS*100),1)

class green():

    def __init__(self):

        self.name="GREEN"
        self.image=pygame.image.load("static/Green.png")
        self.color=colors.green

        self.position=(XSIZE/2,YSIZE/2)
        self.direction=0
        self.radius=SIZE*5
        self.energy=100
        self.speed=(SIZE*MS_PER_FRAME)//6
        self.vision_distance=VISION_DISTANCE*SIZE//2
        self.vision_angle=0.80

class red():

    def __init__(self):

        self.name="RED"
        self.image=pygame.image.load("static/Red.png")
        self.color=colors.red

        self.position=(XSIZE/2,YSIZE/2)
        self.direction=0
        self.radius=SIZE*5
        self.energy=100
        self.speed=(SIZE*MS_PER_FRAME)//5
        self.vision_distance=SIZE*VISION_DISTANCE
        self.vision_angle=0.20

if __name__=="__main__":
    print(XSIZE,YSIZE)
        