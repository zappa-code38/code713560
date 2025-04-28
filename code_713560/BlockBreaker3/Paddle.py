import pygame as pg
from Define import *

df = Define

class Paddle():
    def __init__(self,parent):
        self.parent = parent

        self.growth = False
        self.statusGrow = 0
        self.counterGrowth = 0

        self.afterImage = False
        self.statusAfterImage = 0
        self.counterAfterImage = 0
        self.afterShift = 0

        self.rect:pg.Rect

        self.imgList = list()
        for i in range(1):
            self.imgList.append(pg.image.load(f'parts/paddle_{i:04d}.png').convert_alpha())

        ww = self.imgList[0].get_width()

        temp = pg.Surface((10, df.PADDLE_H),pg.SRCALPHA)
        temp.blit(self.imgList[0], (0, 0), (0, 0, 10, df.PADDLE_H))
        self.imageLeft = temp

        temp = pg.Surface((10, df.PADDLE_H),pg.SRCALPHA)
        temp.blit(self.imgList[0], (0, 0), (ww-10, 0, 10, df.PADDLE_H))
        self.imageRight = temp

        temp = pg.Surface((ww-20, df.PADDLE_H),pg.SRCALPHA)
        temp.blit(self.imgList[0], (0, 0), (10, 0, ww-20, df.PADDLE_H))
        self.imageCenter = temp

        self.resetPos()
    
    def paddleImage(self):
        image = self.imgList[0]

        temp = pg.Surface((df.PADDLE_W-20, df.PADDLE_H),pg.SRCALPHA)
        temp.blit(image, (0, 0), (10, 0, df.PADDLE_W-20, df.PADDLE_H))
        temp = pg.transform.scale(temp, (self.width-20, self.height))
        self.imageCenter = temp
    
    def resetCounter(self):
        self.growth = False
        self.statusGrow = 0
        self.counterGrowth = 0

        self.afterImage = False
        self.statusAfterImage = 0        
        self.counterAfterImage = 0
        self.afterShift = 0

    def resetPos(self):
        self.width = df.PADDLE_W
        self.height = df.PADDLE_H
        x = df.WIDTH / 2
        y = df.SCREEN_H - 64
        # パドル表示位置は、(x,y)座標が中央になるように設定
        self.rect = pg.Rect(x - (self.width / 2),y - (self.height / 2), self.width,self.height)

    def setRect(self):
        x = self.rect.centerx
        y = self.rect.centery
        self.rect = pg.Rect(x - (self.width / 2),y - (self.height / 2), self.width,self.height)

    def update(self):
        if self.growth == True:
            if self.statusGrow == 0:
                self.growIn()
            elif self.statusGrow == 1:
                self.counterGrowth -= 1
                if self.counterGrowth <= 0:
                    self.counterGrowth = 0
                    self.statusGrow = 2
                    self.parent.sound.playSound('get item 2')
            elif self.statusGrow == 2:
                self.growOut()

        if self.afterImage == True:
            if self.statusAfterImage == 0:
                self.counterAfterImage -= 1
                if self.counterAfterImage <= 0:
                    self.counterAfterImage = 0   
                    self.parent.sound.playSound('get item 9')
                    if self.afterShift != 0:
                        self.statusAfterImage = 1
                    else:
                        self.afterImageEnd()

            if self.afterShift != 0:
                if self.afterShift < 0:
                    self.afterShift+=1
                    if self.afterShift > 0:
                        self.afterShift = 0
                else:
                    self.afterShift-=1
                    if self.afterShift < 0:
                       self.afterShift = 0         

                if self.statusAfterImage == 1:
                    if self.afterShift == 0:
                        self.afterImageEnd()

    def draw(self,screen,offset):

        self.paddleImage()
        if self.afterImage == True:
            self.imageLeft.set_alpha(96)
            screen.blit(self.imageLeft,(offset + self.afterShift + self.rect.x,self.rect.y))
            self.imageRight.set_alpha(96)
            screen.blit(self.imageRight,(offset + self.afterShift + self.rect.x + self.width-10,self.rect.y))
            self.imageCenter.set_alpha(96)
            screen.blit(self.imageCenter,(offset + self.afterShift + self.rect.x + 10,self.rect.y))            

        self.imageLeft.set_alpha(255)
        screen.blit(self.imageLeft,(offset + self.rect.x,self.rect.y))
        self.imageRight.set_alpha(255)
        screen.blit(self.imageRight,(offset + self.rect.x + self.width-10,self.rect.y))
        self.imageCenter.set_alpha(255)
        screen.blit(self.imageCenter,(offset + self.rect.x + 10,self.rect.y))

    # 伸びる処理---------------------------------------------
    def growStart(self):
        self.growth = True
        self.statusGrow = 0

    def growEnd(self):
        self.growth = True
        self.statusGrow = 2

    def growIn(self):
        self.width += 2
        if self.width >= df.PADDLE_MAX_W:
            self.width = df.PADDLE_MAX_W
            self.statusGrow = 1
            self.counterGrowth +=  60 * 5  # 5秒間
        self.setRect()
    
    def growOut(self):
        self.width -= 2
        if self.width <= df.PADDLE_W:
            self.width = df.PADDLE_W
            self.statusGrow = 0
            self.growth = False

        self.setRect()

    # 残像処理----------------------------------------------
    def afterImageStart(self):
        self.afterImage = True
        self.statusAfterImage = 0
        self.counterAfterImage +=  60 * 10  # 10秒間

    def afterImageEnd(self):
        self.afterImage = False
        self.statusAfterImage = 0
        self.counterAfterImage = 0

