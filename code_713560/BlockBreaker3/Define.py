import dataclasses

@dataclasses.dataclass

class Define:

        #DEBUG:bool = True
        DEBUG:bool = False

        # カラー値
        WHITE:tuple = (255,255,255)
        RED:tuple = (255,0,0)
        YELLOW:tuple = (255,255,0)
        GREEN:tuple = (0,255,0)
        BLUE:tuple = (0,0,255)
        GLAY:tuple = (128,128,128)
        DARKGLAY:tuple = (64,64,64)
        MIDGLAY:tuple = (96,96,96)
        BLACK:tuple = (0,0,0)

        # コンテンツサイズ
        PLAY_TOP:int = 60
        WIDTH:int = 853
        HEIGHT:int = 720 - PLAY_TOP

        # 画面サイズ
        SCREEN_W:int = 1280
        SCREEN_H:int = 720

        # 各パーツサイズ
        PADDLE_W:int = 96
        PADDLE_H:int = 16
        PADDLE_MAX_W:int = 192
        BLOCK_W:int = 70
        BLOCK_H:int = 32
        BALL_RADIUS:int = 10
