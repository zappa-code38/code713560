import pygame as pg
from Define import *

df = Define

class Ball():

    def __init__(self):

        self.superFlag = False
        self.slowFlag = False

        self.counterSuper = 0
        self.counterSlow = 0

        self.returnTypeSuper = False

        self.radius = df.BALL_RADIUS

        self.ballList = [[2,0,0,0,0,2]]

        self.img_List = list()
        for i in range(9):
            self.img_List.append(pg.image.load(f'parts/ball_{i:04d}.png').convert_alpha())        

    def createTopBall(self):
        self.ballList = [[2,0,0,0,0,2]]

    def resetCounter(self):
        self.superFlag = False
        self.slowFlag = False
        self.counterSuper = 0
        self.counterSlow = 0
        self.returnTypeSuper = False

    def resetPos(self,x,y):
        self.ballList[0][1] = x
        self.ballList[0][2] = y
        self.checkReturnType()

    def checkReturnType(self):
        if self.returnTypeSuper == True:
            self.superFlag = False
            self.returnTypeSuper = False    
            self.ballList[0][0] = self.ballList[0][5]

    def resetSpeed(self):
        self.ballList[0][3] = 0.0
        self.ballList[0][4] = 0.0

    def setSpeed(self,level):

        if level <= 1:
            level = 2
        sx = 2.0 + level*0.4
        sy = -2.5 - level*0.4
        self.ballList[0][3] = sx
        self.ballList[0][4] = sy

    def nextPos(self,index):
        x = self.ballList[index][1] + self.ballList[index][3]
        y = self.ballList[index][2] + self.ballList[index][4]
        return x,y    

    def draw(self,screen,offset):
        for ball in self.ballList:
            screen.blit(self.img_List[ball[0]],
                (offset + int(ball[1])-self.radius, int(ball[2])-self.radius))

    def update(self): 
        for ball in self.ballList:
            if self.slowFlag == True:
                ball[1] += ball[3]*0.5
                ball[2] += ball[4]*0.5
            else:
                ball[1] += ball[3]
                ball[2] += ball[4]  

        if self.superFlag == True and self.returnTypeSuper == False:
            self.counterSuper -= 1
            if self.counterSuper <= 0:
                self.counterSuper = 0
                self.returnTypeSuper = True

        if self.slowFlag == True:
            self.counterSlow -= 1
            if self.counterSlow <= 0:
                self.counterSlow = 0
                self.slowFlag = False
                #self.ballList[0][0] = self.ballList[0][5]


    # スーパーボールの処理---------------------------------------------        
    def startSuper(self):
        self.superFlag = True
        self.returnTypeSuper = False
        self.counterSuper += 60 * 5   # 5秒間
        self.ballList[0][0] = 8
        

    # トリプルボールの処理---------------------------------------------        
    def startTriple(self,x,y,level):

        sx = 2.0 + level
        sy = -2.5 - level
        self.ballList.append([4,x,y,sx,sy,4])

        sx = 0.0
        sy = -2.5 - level
        self.ballList.append([5,x,y,sx,sy,5])

        sx = -2.0 + level
        sy = -2.5 - level
        self.ballList.append([6,x,y,sx,sy,6])

    def remove(self,index):
        self.ballList.pop(index)

    # スローボールの処理---------------------------------------------        
    def startSlow(self):
        self.slowFlag = True
        self.counterSlow += 60 * 10   # 10秒間
        #self.ballList[0][0] = 1

