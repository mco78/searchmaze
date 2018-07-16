# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Wed Feb 28 17:45:57 2018

@author: Marc Otten
"""
"""
STATE OF THE PROJECT (July 11 2018):
I cant figure out how to seperate the game logic from the gui. Also, I am not 
able to update the gui properly. With the text gui (set Text-gui in Fixtures)
the simple agents seem to work. Will abandon the project now to learn more 
about guis and their correspondencies with other game components.
"""

#LIBS
import time
from tkinter import *

#CUSTOM
from fixtures import *
from agents import *
#import utils
import gui

class Tile(object):
    """Represents a tile in the world"""
    
    def __init__(self, x, y, wall=False):
        self.x = x
        self.y = y
        self.wall = wall
        
    def is_on_board(self):
        if self.x < 0 or self.y < 0 or self.x >= MAZE_WIDTH or self.y >= MAZE_HEIGHT:
            return False
        else:
            return True


class Goal(Tile):
    """Represents the goal to escape the maze"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Game(object):
    """Class to create and update the game state."""
    
    def __init__(self, maze):
        self.round = 0
        self.state = []
        x = -1
        for row in maze:
            x += 1
            y = -1
            line = []
            for cell in row:
                y += 1
                if cell == 0:
                    line.append(Tile(x, y, False))
                elif cell == 1:
                    line.append(Tile(x, y, True))
                elif cell == 2:
                    line.append(Goal(x, y))
                elif cell == 3:
                    line.append(Tile(x, y, False))
                    self.agent = choose_agent(x,y) #OLD: Agent(x,y)
                else:
                    print("wrong Tile type.")
            self.state.append(line)  
        
    def get_object_at_position(self, x, y):
        return self.state[x][y]
    
    def set_object_at_position(self, obj, x, y):
        self.state[x][y] = obj
    
    def update_state(self):
        self.agent.act(self.state)
        if self.check_winning_conditions():
            
            return False
        else:
            return True
    
    def check_winning_conditions(self):
        obj_with_agent = self.get_object_at_position(self.agent.x, self.agent.y)
        if isinstance(obj_with_agent, Goal):
            return True
        else:   
            return False
   
def game_state_to_int(game):
    """function to transfer game state to 2D-List with INTs indicating objects
    on the board, which is given to gui"""
    result = []
    for row in game.state:
        line = []
        for cell in row:
            if isinstance(cell, Tile):
                if isinstance(cell, Goal):
                    line.append(2)
                elif cell.wall == False:
                    line.append(0)
                else:
                    line.append(1)
            else:
                line.append(9) # 9 means, Tile not detected.
        result.append(line)
    result[game.agent.x][game.agent.y] = 3
    return result

def main():
    """main() function for starting the game"""
    
    game = Game(MAZE)
    running = True
    
    #initialize GUI
    root = Tk()
    root.title("Searchmaze GUI")
    root.resizable(False,False)
    canvas = Canvas(root, width = MAZE_WIDTH * TILE_SIZE, height = MAZE_HEIGHT * TILE_SIZE)
    canvas.pack()
    
    game_gui = gui.create_gui(game_state_to_int(game), canvas)
    
    
    while running and game.round < MAX_ROUNDS:
        game.round += 1
        running = game.update_state()
        player_gui_tile = canvas.find_withtag("player")
        player_gui_tile.move_tile(CURRENT_ACTION)
        time.sleep(GAME_SPEED)
    print("Game finished in Round {}!".format(game.round))        
    root.mainloop()
    
if __name__ == '__main__':
    main()
    