import pygame as pg
from Define import *
from ItemManager import *
from Stages import *

df = Define

class BlockManager():
    def __init__(self,parent):
        self.parent = parent

        # ブロックのサイズ
        self.block_w = df.BLOCK_W        # 幅
        self.block_h = df.BLOCK_H        # 高さ
        self.block_layout = Stages.stage
        self.blocks = list()

        self.img_blockList = list()
        for i in range(7):
            loadImage = pg.image.load(f'parts/block_{i:04d}.png').convert_alpha()
            scaled_image = pg.transform.scale(loadImage, (self.block_w, self.block_h))
            self.img_blockList.append(scaled_image)

    def setStage(self):
        self.blocks.clear()
        self.parent.itemManager.clearAll()
        # ステージブロック作成　（横１０ブロック構成）
        max = len(self.block_layout[self.parent.stage_display_no])
        for cc in range(max):
            if isinstance(self.block_layout[self.parent.stage_display_no][cc],tuple) == False:continue

            x = (cc % 10) * (self.block_w+4) + 58
            y = int(cc / 10) * (self.block_h+4) + 64 + df.PLAY_TOP
            type = self.block_layout[self.parent.stage_display_no][cc][0]
            imgNo = self.block_layout[self.parent.stage_display_no][cc][1]
            # Blockクラス
            key = cc
            block = Block(self.parent.level,key, type, imgNo)
            block.setRect(x,y,self.block_w,self.block_h)
            self.blocks.append(block)

            if block.type > 0:
                x,y = block.getCenter()
                self.parent.itemManager.addItem(key,block.type,x,y)        


    def draw(self,screen,offset):
        for block in self.blocks:

            image_ = self.img_blockList[block.imgNo]
            image_.set_alpha(255)
            if block.hardness > block.damageCount:
                image_.set_alpha(255 - (block.hardness - block.damageCount) * block.alphaStep)

            screen.blit(image_,(offset+block.left,block.top))        

class Block():
    def __init__(self,level,key,type=0,imgNo=0):

        # アイテム出現開始レベル
        adaptLevel = (0,2,4,1,10,12,2,6,10,2)
        if df.DEBUG == False:
            if level < adaptLevel[type]:
                type = 0

        self.key = key
        self.type = type
        self.imgNo = imgNo

        # ブロックの固さ（破壊までのアタック回数）
        adapthardness = (1,2,3,3,2,4,2,3,4,4)
        self.hardness = adapthardness[type]

        self.damageCount = self.hardness
        self.alphaStep = (255-64) // self.hardness

        self.status = 0
    
    def getCenter(self):
        x = self.left + self.width/2
        y = self.top + self.height/2
        return x,y
    
    def setRect(self,left,top,width,height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.centerX = left + width//2
        self.centerY = top + height//2
        self.right = left + width-1
        self.bottom = top + height-1
