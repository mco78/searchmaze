# -*- coding: utf-8 -*-
"""
Fixtures and Constants for searchmaze.py
Created on Fri Mar  2 13:19:18 2018

@author: Marc Otten
"""
#LIBS
import numpy as np

"""Global Game Variables
"""
GAME_SPEED = 0.5 # seconds between rounds
MAX_ROUNDS = 10 # max rounds until game interrups 
GUI_STYLE = "text" # options "text", ...

"""
MAZE
holds the structure for the world:
    0=empty
    1=wall
    2=goal
    3=agent
For better human reading, MAZE_GRID is created in y,x-format and 
then transposed, so that MAZE[x][y] can be accessed properly
"""
MAZE_GRID = [[0,0,0,0,0,2],
             [0,0,1,0,0,0],
             [0,0,1,1,1,0],
             [3,0,0,0,1,0],
             [0,1,0,0,0,0]]

MAZE = np.array(MAZE_GRID).transpose().tolist()
MAZE_WIDTH = len(MAZE)
MAZE_HEIGHT = len(MAZE[1])

DIRECTIONS = {"n": [0, -1],
              "e": [1, 0],
              "s": [0, 1],
              "w": [-1, 0]}


# TEST MAZE 

TEST_MAZE_GRID = [[3,0,0,0,0,2],
                  [1,0,0,0,0,0],
                  [0,0,1,1,1,0],
                  [0,0,0,0,1,0],
                  [0,1,0,0,0,0]]

TEST_MAZE = np.array(TEST_MAZE_GRID).transpose().tolist()
TEST_MAZE_WIDTH = len(TEST_MAZE)
TEST_MAZE_HEIGHT = len(TEST_MAZE[1])

"""Other testing mazes"""

#MAZE_GRID = [[3,0,0,0,0,2],
#             [0,0,0,0,0,0],
#             [0,0,0,0,0,0],
#             [0,0,0,0,0,0],
#             [0,0,0,0,0,0]]
