import sys
import pygame as pg
from Define import *

df = Define

# 数値の符号を判別する関数
def sgn(a):
    return 1 if a > 0 else -1

# TITLE -----------------------
def should_titleStart(self, evt):
    return (evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE) or \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topStart.collidepoint(evt.pos[0],evt.pos[1]))

def should_titleExit(self,evt):
    return evt.type == pg.QUIT or (evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE) or \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topQuit.collidepoint(evt.pos[0],evt.pos[1]))

def should_titleReturn(self, evt):
    return self.returnFlag == True and \
    (evt.type == pg.MOUSEBUTTONDOWN and self.btn_topReturn.collidepoint(evt.pos[0],evt.pos[1]))

# PLAY ------------------------
def should_exit(evt):
    return evt.type == pg.QUIT

def should_exitTop(evt):
    return evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE

def should_gotoTop(self,evt):
    return  evt.type == pg.MOUSEBUTTONDOWN and self.btn_exit.collidepoint(evt.pos[0],evt.pos[1])

def should_restart(self, evt):
    return  ((evt.type == pg.KEYDOWN and evt.key == pg.K_RETURN)  or  
      (evt.type == pg.MOUSEBUTTONDOWN and self.btn_start.collidepoint(evt.pos[0],evt.pos[1])))

def should_start(self, evt):
    if self.startFlag == True: return False
    return evt.type == pg.MOUSEBUTTONDOWN or (evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE)

def should_pause(self, evt):
    return self.gameOver == False and evt.type == pg.KEYDOWN and evt.key == pg.K_F12

def checkPaddleMove(self, evt):

    xpos = self.paddle.rect.centerx

    if evt.type == pg.MOUSEMOTION:

        mouse_x, mouse_y = evt.pos
        xpos = mouse_x-self.canvasLeft

    result = False
    if xpos != self.paddle.rect.centerx:
        result = True

    return result,xpos

def changeScreenSize(self,evt):
    if evt.type == pg.KEYDOWN and evt.key == pg.K_F2:

        if self.fullScreen == False:
            self.fullScreen = True
        else:
            self.fullScreen = False

        self.changeFullScreen()

# ------------------------------------------------------------
def title(self):
    for evt in pg.event.get():
        if should_titleExit(self,evt):sys.exit()

        if should_titleStart(self,evt):
            self.resetGame()
            self.sound.playSound("title_start")
            self.returnFlag = False
            return
        if should_titleReturn(self,evt):
            self.status = 'PLAY'
            self.returnFlag = False
            # マウスカーソル表示
            pg.mouse.set_visible(False)

        changeScreenSize(self,evt)


def over(self):
    for evt in pg.event.get():
        if should_exit(evt):sys.exit()

        if should_exitTop(evt):
            self.resetGame()
            self.status = 'TITLE'
        
        if should_gotoTop(self,evt):
            self.resetGame()
            self.status = 'TITLE'

        if should_restart(self,evt):
            self.resetGame()
            return


def play(self):

    keyPress = pg.key.get_pressed()

    paddleMoveFlag = False
    paddleMoveX = 0

    previousPaddleX = self.paddle.rect.centerx
    for evt in pg.event.get():

        if should_exit(evt):sys.exit()
        
        if should_exitTop(evt):
            self.status = 'TITLE'
            # マウスカーソル表示
            pg.mouse.set_visible(True)
            self.returnFlag = True

        if should_start(self,evt):
            self.startFlag = True

            self.ball.setSpeed(self.levelSpeed)            
            self.sound.playSound("start")
            return

        if should_pause(self,evt):
            if self.pause == False:
                self.pause = True
            else:
                self.pause = False

        paddleMoveFlag,paddleMoveX = checkPaddleMove(self,evt)

        changeScreenSize(self,evt)

    if self.pause == True: return

    if paddleMoveFlag == True:
        xpos = paddleMoveX
    else:
        xpos = self.paddle.rect.centerx
    # 移動キー押下でパドル位置を移動
    if(keyPress[pg.K_LEFT]): xpos -= 8
    elif(keyPress[pg.K_RIGHT]): xpos += 8
    elif(keyPress[pg.K_a]): xpos -= 8
    elif(keyPress[pg.K_d]): xpos += 8

    # パドル位置が画面にはみ出さないか確認
    # 画面の左右内にいる
    if xpos >= (self.paddle.width / 2) and xpos <= (df.WIDTH - (self.paddle.width / 2)):
        #self.paddle.centerx = xpos
        pass
    # 画面左からはみ出ていたら、画面左ジャストの位置に補正
    elif xpos < (self.paddle.width /2): xpos = self.paddle.width / 2
    # 画面右からはみ出ていたら、画面右ジャストの位置に補正
    elif xpos > (df.WIDTH - (self.paddle.width / 2)): xpos = (df.WIDTH - (self.paddle.width / 2))

    self.paddle.rect.centerx = xpos

    moveValue = previousPaddleX - xpos

    if self.paddle.afterImage == True:
        if self.paddle.statusAfterImage == 0:
            self.paddle.afterShift += moveValue
            if abs(self.paddle.afterShift) > df.PADDLE_W*0.9:
                self.paddle.afterShift = df.PADDLE_W*0.9 * sgn(self.paddle.afterShift)
    else:
        self.paddle.afterShift = 0

    count = len(self.ball.ballList)

    while count:
        count -= 1
        i = count

        ball = self.ball.ballList[i]

        # ボール移動方向
        x,y = self.ball.nextPos(i)

        # 画面枠に対するボールの反射
        soundFlag = False
        if x < self.ball.radius or x > (df.WIDTH - self.ball.radius): 
            ball[3] = -ball[3]
            soundFlag = True
        if y < df.PLAY_TOP + self.ball.radius: 
            ball[4] = -ball[4]
            soundFlag = True 
        #if y >df.HEIGHT: 
        if y >df.SCREEN_H:

            if len(self.ball.ballList) == 1:
                self.overCount += 1
                soundFlag = False
            else:
                self.ball.remove(i)

        
        if soundFlag == True:
            self.sound.playSound("hit_etc")

        # パドルに対するボールの反射
        paddleW = self.paddle.width
        paddleCenterX = self.paddle.rect.centerx

        if self.paddle.afterImage == True:
            if self.paddle.afterShift != 0:
                paddleW += abs(self.paddle.afterShift)
                paddleCenterX += self.paddle.afterShift/2

        dx = paddleCenterX - x
        dy = self.paddle.rect.centery - y

        if dy == 0: dy = 1
        if abs(dx) < (paddleW / 2 + self.ball.radius) and abs(dy) < (self.paddle.height / 2 +self.ball.radius):
            if abs(dx / dy) > (paddleW / self.paddle.height):
                ball[3] = -ball[3]
                ball[1] = paddleCenterX - sgn(dx) * (paddleW/2 + self.ball.radius)

                # 壁のハマリ対策
                if ball[1] < 0 or ball[1] > df.WIDTH: 
                    ball[3] = -ball[3]
            else:
                ball[3] = -dx / 10
                ball[4] = -ball[4]
                ball[2] = self.paddle.rect.centery - sgn(dy) * (self.paddle.height/2 + self.ball.radius)

            self.ball.checkReturnType()
            # パドルヒット時の効果音
            self.sound.playSound("hit_paddle")

        debugFlag = False
        # ブロックに対するボールの反射
        blockW = self.blockManager.block_w
        blockH = self.blockManager.block_h
        for block in self.blockManager.blocks:
            dx = block.centerX - x
            dy = block.centerY - y

            if self.ball.superFlag == False or i != 0:
                if dy == 0: dy = 1
                if abs(dx) < (blockW / 2 + self.ball.radius) and abs(dy) < (blockH / 2 + self.ball.radius):
                    # ブロックヒット！
                    if abs(dx / dy) > (blockW / blockH):
                        ball[3] = -ball[3]
                        ball[1] = block.centerX - sgn(dx) * (blockW / 2 +self.ball.radius)
                    else:
                        ball[4] = -ball[4]
                        ball[2] = block.centerY - sgn(dy) * (blockH / 2 + self.ball.radius)

                    block.damageCount -= 1
                    if block.damageCount == 0:
                        if block.type > 0:
                            self.itemManager.itemDropStart(block.key)

                        # ブロックを消して、得点加算
                        yy = block.top - (64 + df.PLAY_TOP)
                        self.score += 10 * (5 - int(yy / df.BLOCK_H)) * self.level
                        self.blockManager.blocks.remove(block)
                        
                        debugFlag = True

                    # ブロックヒット時の効果音
                    self.sound.playSound("hit_block")
                        
                    break
            else:
                if abs(dx) < (blockW / 2 + self.ball.radius) and abs(dy) < (blockH / 2 + self.ball.radius):
                    block.damageCount -= 1
                    if block.damageCount == 0:
                        if block.type > 0:
                            self.itemManager.itemDropStart(block.key)
                        yy = block.top - (64 + df.PLAY_TOP)
                        self.score += 10 * (5 - int(yy / df.BLOCK_H)) * self.level
                        self.blockManager.blocks.remove(block)                        

    # アイテム処理
    self.itemManager.update()

    # パドルとアイテムの当り判定
    self.itemManager.paddleHitCheck(self.paddle.rect.centerx,self.paddle.rect.centery)

    self.paddle.update()
    self.ball.update()

    if self.startFlag == False:
        x = self.paddle.rect.centerx
        y = self.paddle.rect.centery - (self.paddle.height / 2 + self.ball.radius)
        self.ball.resetPos(x,y)


    pg.mouse.set_pos((self.canvasLeft+self.paddle.rect.centerx,self.paddle.rect.centery)) # = (x,y)

    if self.overCount > 0:

        # ゲームオーバー時の効果音
        if self.overCount == 10:
            self.sound.playSound("game_over")
            # マウスカーソル表示
            pg.mouse.set_visible(True)


        if self.overCount > 100:
            self.ball.remove(0)

            self.ball.resetCounter()
            self.paddle.resetCounter()

            self.life -= 1

            if self.life < 0:    
                self.gameOver = True
                self.status = 'GAME_OVER'

            else:
                self.status = 'START_STAGE'

    # 全ブロッククリアしたか？
    #if debugFlag == True:
    if len(self.blockManager.blocks) == 0 and self.itemManager.itemEmpty():       
        self.stage += 1
        self.stage_display_no += 1
        if self.stage_display_no >= len(self.blockManager.block_layout): 
            self.stage_display_no = 0
            #   全ステージパターンクリア毎にライフ加算
            self.life += 1

        # レベルは２ステージクリア毎に１つアップする
        self.level = 1 + int(self.stage/2)
        self.levelSpeed = self.level
        if self.levelSpeed > 12:
            self.levelSpeed = 12

        # ステージクリア時の効果音
        self.sound.playSound("clear_stage")

        self.status = 'START_STAGE'