import time
from pysprite import Sprite

canvas = "tavern.jpg"
sprites = {
            "moe" : Sprite("moe.png")
          }

def main():
    for i in range(100):
        sprites["moe"].move(3)
        sprites["moe"].rotate(3)
    
