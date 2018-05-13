"""

Coordinates for game determined from screenscreen once image is grabbed

"""


from PIL import ImageGrab
import os
import time
import win32api, win32con
from PIL import ImageOps
#from numpy import *
import numpy as np
import cv2
import math

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def enterPress():
    win32api.keybd_event(0x0D,0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x0D,0,win32con.KEYEVENTF_KEYUP,0)

def leftDown():
    rightUp()
    win32api.keybd_event(0x25,0,0,0)

def leftUp():
    win32api.keybd_event(0x25,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.01)
    
def rightDown():
    leftUp()
    win32api.keybd_event(0x27,0,0,0)

def rightUp():
    win32api.keybd_event(0x27,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.01)

def upPress():
    win32api.keybd_event(0x26,0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x26,0,win32con.KEYEVENTF_KEYUP,0)

def spacePress():

    win32api.keybd_event(0x20,0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)
    #print("Space hit")

def stopPlayer():
    win32api.keybd_event(0x27,0,0,0)
    win32api.keybd_event(0x25,0,0,0)    
    time.sleep(.01)
    #print("stopping")
    win32api.keybd_event(0x27,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(0x25,0,win32con.KEYEVENTF_KEYUP,0)

def stop():
    mousePos((204,19))
    leftClick()
    win32api.keybd_event(0x27,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.01)
    win32api.keybd_event(0x25,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(.01)

def reset():
    jumpTo(0)
    goTo((200,200))


def goTo(cord):

    player = getPlayer()
    if(player[0] < cord[0]):
        rightDown()
        direction = "right"
    elif (player[0] > cord[0]):
        leftDown()
        direction = "left"
    condition = True
    while condition:
        player = getPlayer()
        if player[0] >= (cord[0]-20) and direction == "right":
            rightUp()
            condition= False
        elif player[0] <= (cord[0]+20) and direction == "left":
            leftUp()
            condition= False
        elif player[0] > 740:
            stopPlayer()
            condition = False
        elif player[0] < 5:
            stopPlayer()
            condition = False
        
def jumpTo(platform):
    mousePos((347,390))
    leftClick()
    print("Jumping to: ", platform)
    if platform == 0:
        goTo((327,488))
        time.sleep(2)
    elif platform == 1:
        goTo((320,488))
        upPress()
        goTo((450,384))
    elif platform == 2 :
        goTo((440,384))
        upPress()
        goTo((215,234))
    elif platform == 3 :
        goTo((220,234))
        upPress()
        goTo((545,204))
        time.sleep(1)
    #If player hasnt made it to platform, reset.
    print("Finished jump")
    player = getPlayer()
    if getPlatform(player) != platform and platform != 0:
        print ("Resetting")
        reset()
     
def mousePos(cord):
    win32api.SetCursorPos(( cord[0], cord[1]+100))
     
def cords():
    x,y = win32api.GetCursorPos()
    print (x,y)

def startGame():
    #Click on game
    mousePos((347,390))
    leftClick()
    
    condition = True
    while condition:
        cont = getStar()
        if cont == "none":
            print("got all stars")
            time.sleep(2)


def closestStar():
    starArray = imageSearch('star.png')
    player = getPlayer() 
    closestStar=((1000,1000))
    distance = 1000
    for pt in zip(*starArray[::-1]):
        dis_x = (pt[0]-player[0]) **2
        dis_y = (pt[1]-player[1]) **2
        if math.sqrt(dis_x+dis_y) < distance:
            #Checking closest star to player
            distance = math.sqrt(dis_x+dis_y)
            closestStar = pt
    #print(closestStar[0], " ",closestStar[1])
    if closestStar[0] == 1000:
        stopPlayer()
    mousePos((closestStar[0],closestStar[1]))
    return closestStar


def getPlayer():
    precision = 0.8
    im = ImageGrab.grab(bbox = (0, 91, 799, 690))
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('dude.png',0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    player = max_loc
    return player

def getPlatform(item):
    if item[1] > 420:
        platform = 0
    elif item[1] > 280:
        platform = 1
    elif item[1] < 280 and item[0] < 350:
        platform = 2
    elif item[1] <280 and item [0] > 450:
        platform = 3

    #platform 1: 400,384 lowest
    #platform 2: 0, 234, corner 249,234
    #platform 3: 550, 204 highest
    #ground : x,546

    return platform

def imageSearch(image):
    im = ImageGrab.grab(bbox = (0, 91, 799, 690))
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    #check if array is empty
    if not loc:
        return [-1, -1]

    return loc           

def getStar():
    star = closestStar()
    if star[0] == 1000:
        return "none"
    platform = getPlatform(star)
    player = getPlayer()
    playerIsOn = getPlatform(player)
    print("Player: ",player[0]," ",player[1], "Platform: ", playerIsOn)
    print("Star: ",star[0]," ",star[1], "Star platform: ", platform)
    while playerIsOn != platform:
        if platform > playerIsOn:
            jumpTo(playerIsOn+1)
            playerIsOn = getPlatform(getPlayer())
        elif platform<playerIsOn:
            jumpTo(0)
            print("Jumping to the ground")
            playerIsOn = getPlatform(getPlayer())
    goTo(star)

def main():
    print("Hello World")

if __name__ == '__main__':
    main()

