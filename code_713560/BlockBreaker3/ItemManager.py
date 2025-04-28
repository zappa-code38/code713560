import pygame as pg
from Define import *

df = Define

class ItemManager():
    def __init__(self,parent):
        self.parent = parent
        self.img_itemList = list()
        for i in range(5):
            self.img_itemList.append((pg.image.load(f'parts/capsule_{i:04d}.png'),-45)) # 0--4
        
        self.img_itemList.append((pg.image.load(f'parts/item_time.png'),0)) # 5
        self.img_itemList.append((pg.image.load(f'parts/item_pink.png'),0)) # 6
        self.img_itemList.append((pg.image.load(f'parts/item_gold_100.png'),0)) # 7
        self.img_itemList.append((pg.image.load(f'parts/item_gold_500.png'),0)) # 8
        self.img_itemList.append((pg.image.load(f'parts/item_gold_1000.png'),0)) # 9
        self.img_itemList.append((pg.image.load(f'parts/item_blue.png'),-90)) # 10

        self.itemList = dict()
    
    def itemEmpty(self):
        if len(self.itemList) == 0:
            return True
        return False

    def clearAll(self):
        self.itemList.clear()

    def addItem(self,key,type,x,y):
        item = Item(type,x,y)
        item.setImage(self.img_itemList[item.imgNo][0],self.img_itemList[item.imgNo][1])
        #self.itemList.append(item)
        self.itemList.setdefault(key,item)

    def itemDropStart(self,key):
        item = self.itemList.get(key)
        if item:
            item.dropStart()

    def update(self):
        for k,item in self.itemList.items():
            if item.status == 1:
                item.dropping()
            if item.status == -1:
                #self.itemList.remove(item)
                self.itemList.pop(k)
                break

    def paddleHitCheck(self,px,py):
        for k,item in self.itemList.items():
            dx = px - item.x
            dy = py - item.y

            if abs(dx) < (df.PADDLE_W / 2 + item.w/2) and abs(dy) < (df.PADDLE_H / 2 +item.h/2):

                item.broken()
                #self.itemList.remove(item)
                self.itemList.pop(k)

                # 得点加算
                self.parent.score += 10
                
                if item.type == 1:
                    self.parent.paddle.growStart()
                elif item.type == 2:
                    self.parent.ball.startSuper()
                elif item.type == 3:
                    self.parent.ball.startTriple(item.x,item.y,self.parent.levelSpeed)
                elif item.type == 4:
                    self.parent.ball.startSlow()
                elif item.type == 5:
                    self.parent.life += 1
                elif item.type == 6:
                    self.parent.score += 100                    
                elif item.type == 7:
                    self.parent.score += 500 
                elif item.type == 8:
                    self.parent.score += 1000 

                elif item.type == 9:    # パドル残像
                    self.parent.paddle.afterImageStart()

                # パドルヒット時の効果音
                self.parent.sound.getItemSound(item.type)   
                break

    def draw(self,screen,offset):
        for k,item in self.itemList.items():
            item.rotate_center_image(offset)
            screen.blit(item.rot_image,item.rect)

class Item():
    def __init__(self,type,x,y):
        self.type = type

        if type == 1:
            self.imgNo = 0
        elif type == 2:
            self.imgNo = 1
        elif type == 3:
            self.imgNo = 2
        elif type == 4:
            self.imgNo = 5     
        elif type == 5:
            self.imgNo = 6  
        elif type == 6:
            self.imgNo = 7
        elif type == 7:
            self.imgNo = 8
        elif type == 8:
            self.imgNo = 9
        elif type == 9:
            self.imgNo = 10
        else:
            self.imgNo = 0

        self.status = 0
        self.x = x
        self.y = y

    def setImage(self,img,angle):
        self.img = img
        self.rot_image = img
        self.w = self.img.get_width()
        self.h = self.img.get_height()

        self.image_angle = angle

    def rotate_center_image(self,offset):
        if self.status == 1:
            self.image_angle -= 10
            if self.image_angle <= -360:
                self.image_angle = 0

        self.rot_image = pg.transform.rotate(self.img, self.image_angle)
        rot_rect = self.rot_image.get_rect(center=self.rot_image.get_rect(center=(offset + self.x, self.y)).center)

        self.rect = rot_rect

    def dropStart(self):
        self.status = 1

    def dropping(self):
        self.y += 8
        if self.y > df.SCREEN_H:
            self.broken()

    def broken(self):
        self.status = -1        
