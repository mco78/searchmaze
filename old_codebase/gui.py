# -*- coding: utf-8 -*-
"""
GUI for searchmaze.py
Created on Mon Mar  5 16:46:41 2018

@author: Marc Otten


"""
import numpy as np


from fixtures import GUI_STYLE
from fixtures import MAZE_WIDTH
from fixtures import MAZE_HEIGHT
from fixtures import TILE_SIZE

class guiTile(object):
    def __init__(self, canvas, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.canvas = canvas
        self.tile = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color)
        if self.color == "red":
            canvas.itemconfig(self.tile, tags="player")
            
        

    def move_tile(self, action):
        x, y = DIRECTIONS[action]
        deltax = x * TILE_SIZE
        deltay = y * TILE_SIZE
        self.canvas.move(self.tile, deltax, deltay)
        self.canvas.after(500, self.move_tile) #was soll diese Zeile?? Aus TKinter_test4.py übernommen
        
def create_gui(state, canvas):
    tiles = []
    x = -1
    for row in state:
        x += 1
        y = -1
        for cell in row:
            y += 1
            if cell == 1:
                color = "#476042"
            elif cell == 2:
                color = "yellow"
            elif cell == 3:
                color = "grey"
                player_x = x
                player_y = y
            elif cell == 0:
                color = "grey"
            tiles.append(guiTile(canvas, TILE_SIZE*x, TILE_SIZE*y, TILE_SIZE*(x+1), TILE_SIZE*(y+1), color))
    player = guiTile(canvas, TILE_SIZE*player_x, TILE_SIZE*player_y, TILE_SIZE*(player_x+1), TILE_SIZE*(player_y+1), "red")
    tiles.append(player)
    canvas.tag_raise("player")
    return tiles