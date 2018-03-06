# -*- coding: utf-8 -*-
"""
GUI for searchmaze.py
Created on Mon Mar  5 16:46:41 2018

@author: Marc Otten
"""
import numpy as np

from fixtures import GUI_STYLE

"""First try will be a textbased GUI with a very low framerate, so one can
read everything in the console. The object is to design everything so that 
the textbased GUI can be replaced with another later"""

def show(game, Tile, Goal):
    if GUI_STYLE == "text":
        text_show(game, Tile, Goal)


def text_show(game, Tile, Goal):
    """Text based version of show(). Needs Tile and Goal Class to compare 
    objects."""
    print("_______________")
    print("Round {}".format(game.round))
    
    output_strings = []
    for row in game.state:
        row_string = []
        for cell in row:
            if isinstance(cell, Tile):
                if isinstance(cell, Goal):
                    row_string.append("O")
                elif cell.wall == False:
                    row_string.append("_")
                else:
                    row_string.append("X")
            else:
                row_string.append("F") # 'F' means, Tile not detected.
        output_strings.append(row_string)
    #add agent to display
    output_strings[game.agent.x][game.agent.y] = "A"
    
    #rotate for display reasons
    output = np.array(output_strings).transpose().tolist()   
    for row in output:
        print("".join(row))
