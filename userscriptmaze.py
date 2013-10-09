import time
from pysprite import Sprite

sprites = {
            "moe" : Sprite("moe.png")
          }

def main():
    olddirection = None
    go = None
    directions = ["up", "down", "left", "right"]
    for i in range(100):
        for direction in directions:
            if direction != olddirection:
                go = sprites["moe"].traverseMaze(direction)
                if go:
                    olddirection = go
