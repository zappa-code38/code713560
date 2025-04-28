import pygame as pg

class Sound():
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 4096)

        self.sound_fx = {
            # key          # value : サウンドファイル,ボリューム
            'hit_paddle' :('sound/hit_paddle.mp3',0.2),     # パドルヒット
            'hit_block'  :('sound/hit_block.mp3',1.0),      # ブロックヒット
            'clear_stage':('sound/clear_stage.mp3',1.0),    # ステージヒット
            'game_over'  :('sound/game_over.mp3',0.4),      # ゲームオーバー
            'hit_etc'    :('sound/hit_etc.mp3',0.3),        # 壁ヒット
            'title_start':('sound/title_start.mp3',0.5),    # ゲームスタート時
            'start'      :('sound/start.mp3',0.5),          # ステージスタート時

            'get item 0' :('sound/item_0000.mp3',0.5),                      # ダミー
            'get item 1' :('sound/item_paddle_grow.mp3',0.5),               # パドル長く
            'get item 2' :('sound/item_paddle_end.mp3',0.5),                # パドル短く
            'get item 3' :('sound/item_super_ball.mp3',0.3),                # スーパーボール
            'get item 4' :('sound/item_three_ball.mp3',0.6),                # ３つ玉
            'get item 5' :('sound/item_slow.mp3',0.6),                      # スローモード
            'get item 6' :('sound/item_life.mp3',0.5),                      # ライフ加算
            'get item 7' :('sound/item_gold.mp3',0.3),                      # 得点加算
            'get item 8' :('sound/item_paddle_afterImage_start.mp3',0.5),   # パドル残像スタート
            'get item 9' :('sound/item_paddle_afterImage_end.mp3',0.5)      # パドル残像エンド            
        }

    # 効果音の再生
    def playSound(self, sname):
        sound = pg.mixer.Sound(self.sound_fx[sname][0])
        sound.set_volume(self.sound_fx[sname][1])
        sound.play()    

    def getItemSound(self, type):
        sname = ('get item 0','get item 1','get item 3','get item 4','get item 5',
                 'get item 6','get item 7','get item 7','get item 7','get item 8')
        self.playSound(sname[type])