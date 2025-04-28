import pygame as pg
from Define import *
import Play
import Draw
from BlockManager import *
from ItemManager import *
from Sound import *
from Paddle import *
from Ball import *

df = Define

class BlockBreaker():
    def __init__(self,args):
        self.fullScreen = args.fullScreen

        pg.init()
        self.sysInit()
        self.setButtonLayout()
    
    @staticmethod
    def getWindowCenterShift(screenW,screenH):
        xx = (screenW - df.WIDTH) // 2
        yy = (screenH - df.HEIGHT) // 2
        return xx,yy

    def setButtonLayout(self):
        # システムパーツ　ボタンなど
        self.btn_W = 160
        self.btn_H = 40
        self.btn_Ws = 100
        self.btnFont = pg.font.SysFont(None, 42)
        # タイトル画面
        self.btnText_topStart = self.btnFont.render("START", True, df.GREEN)
        self.btnText_topReturn = self.btnFont.render("RETURN", True, df.YELLOW)
        self.btnText_topReturnDisabled = self.btnFont.render("RETURN", True, df.MIDGLAY)
        self.btnText_topQuit = self.btnFont.render("QUIT", True, df.BLACK)
        # プレイ画面
        self.btnText_start = self.btnFont.render("START", True, df.GREEN)
        self.btnText_exit = self.btnFont.render("EXIT", True, df.YELLOW)

        self.buttonLayout()

    def buttonLayout(self):
        self.btn_topStart = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-100,self.btn_W,self.btn_H)
        self.btn_topReturn = pg.Rect(self.canvasLeft + df.WIDTH - (140 + self.btn_W) , df.HEIGHT-100,self.btn_W,self.btn_H)
        self.btn_topQuit = pg.Rect(self.canvasLeft + 140, df.HEIGHT-100,self.btn_Ws,self.btn_H)

        self.btn_start = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-150,self.btn_W,self.btn_H)
        self.btn_exit = pg.Rect(self.canvasLeft + df.WIDTH/2 - self.btn_W/2, df.HEIGHT-80,self.btn_W,self.btn_H)

    def changeFullScreen(self):
        if self.fullScreen == True:
            self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((df.SCREEN_W,df.SCREEN_H))

    def loadResources(self):
        self.img_title = pg.image.load('parts/title.png').convert_alpha()

        self.img_backList = list()
        for i in range(6):
            self.img_backList.append(pg.image.load(f'parts/back_{i:04d}.png').convert_alpha())

        self.img_heartList = list()
        for i in range(1):
            self.img_heartList.append(pg.image.load(f'parts/heart_{i:04d}.png').convert_alpha())  

        self.img_numList = list()
        for i in range(10):
            self.img_numList.append(pg.image.load(f'parts/num_{i:02d}.png').convert_alpha())  

        self.img_fontList = list()
        s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in s:
            self.img_fontList.append(pg.image.load(f'parts/{i}.png').convert_alpha())
        self.fontW = self.img_fontList[0].get_width()
        self.fontH = self.img_fontList[0].get_height()
        
    def sysInit(self):

        self.clock = pg.time.Clock()
        self.caption = pg.display.set_caption("Block Breaker")
   
        self.changeFullScreen()

        self.canvasLeft:int
        self.canvasTop:int
        window_width, window_height = pg.display.get_window_size()
        self.canvasLeft,self.canvasTop = self.getWindowCenterShift(window_width,window_height)

        self.font = pg.font.Font(None, 64)

        self.status = 'TITLE'

        self.returnFlag = False

        self.stageNo = 0
        self.startFlag:bool

        self.gameOver = False

        self.pause = False

        self.level = 1
        self.levelSpeed = 1
        self.stage = 0
        self.score = 0
        self.life = 3
        self.stage_display_no = 0

        # スコアエリア
        self.topRect = pg.Rect(0, 0, df.WIDTH, df.PLAY_TOP)

        self.loadResources()

        self.ball = Ball()
        self.paddle = Paddle(self)
        self.sound = Sound()
        self.blockManager = BlockManager(self)
        self.itemManager = ItemManager(self)

    def stageInit(self):

        if df.DEBUG == True:
            if self.level < 12:
                self.level = 12
                self.levelSpeed = 12
                self.stage = 22
                self.stage_display_no = 2
                self.score = 33000


        # マウスカーソル非表示
        pg.mouse.set_visible(False)


        if len(self.ball.ballList) == 0:
            self.ball.createTopBall()


        if len(self.ball.ballList) == 1:

            self.startFlag = False
            self.paddle.resetPos()

            # ボールの座標
            # パドルの上面中央の位置にセット
            x = self.paddle.rect.centerx
            y = self.paddle.rect.centery - self.paddle.height / 2
            self.ball.resetPos(x,y)
            self.ball.resetSpeed()

            # マウスカーソル初期位置
            # パドル座標に合わせる
            pg.mouse.set_pos((self.canvasLeft+self.paddle.rect.centerx,self.paddle.rect.centery)) # = (x,y)
        else:
            self.ball.setSpeed(self.levelSpeed)

        self.blockManager.setStage()
                
        self.status = 'PLAY'
        self.overCount = 0

    def resetGame(self):
        self.blockManager.blocks.clear()
        self.level = 1
        self.levelSpeed = 1
        self.stage = 0
        self.score = 0
        self.life = 3
        self.stage_display_no = 0
        self.gameOver = False
        self.overCount = 0
        self.status = 'START_STAGE'

    def main(self):
        while True:
            if self.status == 'TITLE':
                Play.title(self)
                Draw.title(self)

            elif self.status == 'START_STAGE':
                self.stageInit()

            elif self.status == 'PLAY':
                Play.play(self)
                Draw.play(self)

            elif self.status == 'GAME_OVER':
                Play.over(self)
                Draw.play(self)

            pg.display.update()
            self.clock.tick(60)
