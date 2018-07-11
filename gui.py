# -*- coding: utf-8 -*-
"""
GUI for searchmaze.py
Created on Mon Mar  5 16:46:41 2018

@author: Marc Otten
"""
import numpy as np
import tkinter as tk

from fixtures import GUI_STYLE
from fixtures import MAZE_WIDTH
from fixtures import MAZE_HEIGHT
from fixtures import TILE_SIZE

"""First try will be a textbased GUI with a very low framerate, so one can
read everything in the console. The object is to design everything so that 
the textbased GUI can be replaced with another later"""

def show(state, game_round):
    
        
    
    """Desides which gui to use and calls gui show function. Takes game state in 
    2D list of ints is passes it to specified gui"""
    if GUI_STYLE == "text":
        text_show(state, game_round)
    if GUI_STYLE == "tk":
        if game_round == 0:
            tk_init(state) #HIER WEITERMACHEN: GUI INITIAILIEREN UND DANN UPDATEN
        else:
            tk_update(state, game_round)


def text_show(state, game_round):
    """Text based version of show(). Needs Tile and Goal Class to compare 
    objects."""
    print("_______________")
    print("Round {}".format(game_round))
    
    output_strings = []
    for row in state:
        row_string = []
        for cell in row:
            if cell == 0:
                row_string.append("_")
            elif cell == 1:
                row_string.append("X")
            elif cell == 2:
                row_string.append("O")
            elif cell == 3:
                row_string.append("A")
            else:
                row_string.append("F") # 'F' means, Tile not detected.
        output_strings.append(row_string)
    
    #rotate for display reasons
    output = np.array(output_strings).transpose().tolist()   
    for row in output:
        print("".join(row))

def tk_init(state, game_round):
    """displays game state using tkinter gui"""
        
    def checkered(canvas, line_distance):
       """create grid fitting in canvas"""
       # vertical lines at an interval of "line_distance" pixel
       for x in range(line_distance,canvas_width,line_distance):
          canvas.create_line(x, 0, x, canvas_height, fill="#476042")
       # horizontal lines at an interval of "line_distance" pixel
       for y in range(line_distance,canvas_height,line_distance):
          canvas.create_line(0, y, canvas_width, y, fill="#476042")
    
    def display_objects():
        color = ""
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if state[x][y] == 1:
                    color = "#476042"
                elif state[x][y] == 2:
                    color = "yellow"
                elif state[x][y] == 3:
                    color = "red"
                else:
                    color = "grey"
                w.create_rectangle(TILE_SIZE*x, TILE_SIZE*y, 
                               TILE_SIZE*(x+1), TILE_SIZE*(y+1), fill=color) 
    
    
    master = tk.Tk()
    canvas_width = MAZE_WIDTH * TILE_SIZE
    canvas_height = MAZE_HEIGHT * TILE_SIZE 
    w = tk.Canvas(master, 
               width=canvas_width,
               height=canvas_height)
    w.pack()
    
    checkered(w,TILE_SIZE)
    display_objects()
    
    tk.mainloop()
    """Does work in displaying one state. How to update state and redraw canvas? 
    mainloop has to go to searchmaze? Further investigations with tkinter 
    needed. start here: 
        https://stackoverflow.com/questions/25430786/moving-balls-in-tkinter-canvas/25431690#25431690
    """
