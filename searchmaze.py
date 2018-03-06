# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Wed Feb 28 17:45:57 2018

@author: Marc Otten
"""
"""
NEXT UP:
    Define new versions of agents (manual, search algorithm etc.)
"""

#LIBS
import time

#CUSTOM
from fixtures import *
import utils
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


class Agent(object):
    """Represents the agent that has to escape the maze
    REMINDER FOR LATER: MANY TYPES OF AGENTS COULD INHERIT FROM THIS CLASS AND
    POSSIBLY BE SEPERATED IN FILE AGENTS.PY"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_target_on_board(self, action):
        target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
        target = Tile(target_array[0], target_array[1])
        return target.is_on_board()
    
    def is_action_possible(self, action, state):
        if self.is_target_on_board(action):
            target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
            target_obj = state[target_array[0]][target_array[1]]
            if isinstance(target_obj, Goal):
                return True
            elif target_obj.wall == False:
                return True
        return False
    
    def act(self, state):
        """Function to make decisions and then move.
        This agent version simply goes east."""
        
        action = "e"
        print("action: {}".format(action))
        self.move(state, action)
        
    def move(self, state, action=False):
        # create east action if none provided
        if action:        
            if self.is_action_possible(action, state):
                target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
                self.x = target_array[0]
                self.y = target_array[1]

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
                    self.agent = Agent(x,y)
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
   

def main():
    """main() function for starting the game"""
    
    game = Game(MAZE)
    running = True
    gui.show(game, Tile, Goal)
    
    while running and game.round < MAX_ROUNDS:
        game.round += 1
        running = game.update_state()
        gui.show(game, Tile, Goal)
        time.sleep(GAME_SPEED)
    print("Game finished in Round {}!".format(game.round))        

if __name__ == '__main__':
    main()
    