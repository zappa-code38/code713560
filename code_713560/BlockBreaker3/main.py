import os
import argparse
import pygame as pg
from BlockBreaker import BlockBreaker

execFilePath = os.path.dirname(__file__)
os.chdir(execFilePath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fullScreen", action='store_true', help="full screen")
    args = parser.parse_args()

    game = BlockBreaker(args)
    game.main()
    
    pg.quit()