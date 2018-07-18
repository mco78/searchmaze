# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Mon Jul 16 11:08:36 2018

@author: Marc Otten

TODO: 17.07.18: Agent not moving, UI shows up, when all moves are done. Try to update 
game on button -> bind button event, then update

"""

# IMPORTS
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import numpy as np
import time
import utils
from random import randint


# GLOBALS

GAME_SPEED = 0.5 # seconds between rounds
MAX_ROUNDS = 10 # max rounds until game interrups 
TILE_SIZE = 50

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

# ERROR HANDLING

class SearchmazeError(Exception):
    """An application specific error."""
    pass

# MAIN CODE

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
    """Represents the agent that has to escape the maze"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    

    def act(self, board):
        """Function to make decisions and then move.
        This agent version simply goes east."""
        
        action = "e"
        print("action: {}".format(action))
        move = DIRECTIONS[action]
        return move
        


class MazeBoard(object):
    """Maze Board to hold the structure of the board"""
    def __init__(self, maze):
        self.state = self.__create_board(maze)
    
    def __create_board(self, maze):
        board = []
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
                    # create normal tile on which the agent object will sit
                    line.append(Tile(x, y, False))
                else:
                    raise SearchmazeError(
                            "Wrong tile type!"
                            )
            board.append(line)
        return board
    
    def __get_object_at_position(self, x, y):
        return self.state[x][y]
    
    def __set_object_at_position(self, obj, x, y):
        self.state[x][y] = obj
    

class MazeGame(object):
    """ The Seachmaze game, in charge of coordinating the actions of the agent
    and to check the winning conditions
    """
    def __init__(self, maze):
        self.board = MazeBoard(maze)
        agent_x, agent_y = self.__get_agent_position(maze)
        self.agent = Agent(agent_x, agent_y)
    
    def start(self):
        self.game_over = False
        
    def update(self):
        agent_move = self.agent.act(self.board)
        print(agent_move)
        if self.move_possible(agent_move):
            self.agent.x += agent_move[0]
            self.agent.y += agent_move[1]
            print("new agent position:" + str(self.agent.x) + "/" + str(self.agent.y))
        else:
            raise SearchmazeError(
                        "Agent move not valid!"
                        )        
        return agent_move
    
    def target_on_board(self, move):
        target_array = utils.array_addition([self.agent.x, self.agent.y], move)
        target = Tile(target_array[0], target_array[1])
        return target.is_on_board()
    
    def move_possible(self, move):
        if self.target_on_board(move):
            target_array = utils.array_addition([self.agent.x, self.agent.y], move)
            target_obj = self.board.state[target_array[0]][target_array[1]]
            if isinstance(target_obj, Goal):
                return True
            elif target_obj.wall == False:
                return True
        return False
    
    
    def check_win(self):
        #TODO for now just return False
        return False
    
    def __get_agent_position(self, maze):
        x = -1
        for row in maze:
            x += 1
            y = -1
            for cell in row:
                y += 1
                if cell == 3:
                    return x, y
    
        
class MazeUI(Frame):
    """
    The Tkinter UI, responsible for drawing the maze
    """
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent)
                
        self.__initUI()
    
    
    def __initUI(self):
        self.parent.title("Seachmaze")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self,
                             width = MAZE_WIDTH * TILE_SIZE,
                             height = MAZE_HEIGHT * TILE_SIZE)
        
        self.canvas.pack(fill=BOTH, side=TOP)
        self.__draw_maze()
#        for i in range(3):
#            move = self.game.update()
#            self.updateUI(move)
#            time.sleep(1)
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.__key_pressed)
        
    def __draw_maze(self):
        current_state = self.game_state_to_int()
        x = -1
        for row in current_state:
            x += 1
            y = -1
            for cell in row:
                y += 1
                if cell == 1:
                    color = "#476042"
                    self.__draw_tile(x, y, color, "tile")
                elif cell == 2:
                    color = "yellow"
                    self.__draw_tile(x, y, color, "tile")
                elif cell == 0:
                    color = "grey"
                    self.__draw_tile(x, y, color,"tile")
        
        agent_x, agent_y = self.game.agent.x, self.game.agent.x
        """
        Hier weitermachen. Problem ist, dass die agent position hier in der UI 
        eine andere ist als im game object und im game.board. Die Architektur
        muss vermutlich umgestellt werden und die Positionen über Funktionen
        aus dem Game Objekt abgefragt werden...
        """
        print(str(agent_x) + str(agent_y))
        self.__draw_tile(agent_x, agent_y, "red", "agent")
        
    def __draw_tile(self, x, y, color, tag):
        self.canvas.create_rectangle(TILE_SIZE*x, TILE_SIZE*y, 
                                TILE_SIZE*(x+1), TILE_SIZE*(y+1), fill=color, tags=tag)
    
    
    def updateUI(self, move):
        UI_agent = self.canvas.find_withtag("agent")
        deltax = move[0] * TILE_SIZE
        deltay = move[1] * TILE_SIZE
        self.canvas.move(UI_agent, deltax, deltay)
        self.__draw_maze()

    
    
    def game_state_to_int(self):
        """function to transfer game board to 2D-List with INTs indicating objects
        on the board"""
        result = []
        for row in self.game.board.state:
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
        result[self.game.agent.x][self.game.agent.y] = 3
        return result
    
    
    def __key_pressed(self, event):
        move = self.game.update()
        self.updateUI(move)

"""
Main Function
"""
if __name__ == '__main__':
    game = MazeGame(MAZE)
    game.start()
    
    root = Tk()
    MazeUI(root, game)
    root.mainloop()