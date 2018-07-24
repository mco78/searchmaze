# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Wed Jul 18 13:58:16 2018

@author: Marc Otten

Contributers:
    - "maze" by lvidarte (https://github.com/lvidarte/maze)
    
TODO:
    - implement different controll modes (manual, 
      different agents)
    - implement options for maze: take maze file or random maze

BUGS:
    - size of options frame should be the same size than maze later
    - AI agents should move without keyboard input!

"""

import random
import time
import tkinter as tk
from tkinter import messagebox
import sys

"""
FIXTURES
"""
DIRECTIONS = {"u": [0, -1],
              "r": [1, 0],
              "d": [0, 1],
              "l": [-1, 0]}

AI_MOVEMENT_SPEED = 200

"""
MAIN CODE
"""

class Application(tk.Frame):
    
    def __init__(self, parent, width=21, height=21, size=10):
        tk.Frame.__init__(self, parent)
        self.grid()
        self.width = width
        self.height = height
        self.size = size
        self.get_options()
    
    """
    OPTIONS DIALOGUE
    """
    def get_options(self):
        """
        shows an radiobutton option to choose the type of agent for the game
        """
        options_frame = tk.Frame(self, 
                                 width=self.width * self.size, 
                                 height=self.height * self.size)
        agents = [
                 ("manual", 1),
                 ("go right", 2),
                 ("random", 3)
                 ]
        agent_option = tk.IntVar()
        agent_option.set(1)
        
        tk.Label(options_frame, 
               text="Choose the type of Agent:",
               padx = 20
               ).grid()
        r = -1
        for txt, val in agents:
            r += 1
            tk.Radiobutton(options_frame, 
                           text=txt,
#                           indicatoron = 0,
                           padx = 20, 
                           variable=agent_option,
                           value=val).grid()
        
        tk.Button(options_frame,
                  text="Start",
                  padx = 20, 
                  command=lambda : self.clear_options(options_frame, agent_option.get())
                  ).grid()
        
        options_frame.grid()
    
    def clear_options(self, options_frame, agent_option):
        """clears the option menu and starts the main game"""
        self.agent_type = agent_option
        options_frame.destroy()
        self.start()
         
    """
    SET UP MAZE
    """
    def start(self):
        self.maze = Maze(self.width, self.height)
        self.steps = 0
        self.grid()
        self.create_widgets() 
        self.draw_maze()
        if self.agent_type == 1:
            self.create_events()
        else:
            self.create_AI_agent()
            self.create_AI_loop()
            
    def create_widgets(self):
        width = self.maze.width * self.size
        height = self.maze.height * self.size
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.grid()
        self.status = tk.Label(self)
        self.status.grid()

    def draw_maze(self):
        for i, row in enumerate(self.maze.maze):
            for j, col in enumerate(row):
                x0 = j * self.size
                y0 = i * self.size
                x1 = x0 + self.size
                y1 = y0 + self.size
                color = self.get_color(x=j, y=i)
                id = self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=color)
                if self.maze.start_cell == (j, i):
                    self.cell = id
        self.canvas.tag_raise(self.cell) #bring to front
        self.status.config(text="Let's go!")
    
    """
    MOVING CELL
    """
    def move_cell(self, action):
        if action == "u":
            self.canvas.move(self.cell, 0, -self.size)
        elif action == "d":
            self.canvas.move(self.cell, 0, self.size)
        elif action == "l":
            self.canvas.move(self.cell, -self.size, 0)
        elif action == "r":
            self.canvas.move(self.cell, self.size, 0)
        self.steps += 1
        self.canvas.update()
        self.status.config(text="Moves: %d" % self.steps)
        self.check_status()
    
    """ 
    MANUAL MODE
    """
    def create_events(self):
        self.canvas.bind_all("<KeyPress-Up>", self.manual_move)
        self.canvas.bind_all("<KeyPress-Down>", self.manual_move)
        self.canvas.bind_all("<KeyPress-Left>", self.manual_move)
        self.canvas.bind_all("<KeyPress-Right>", self.manual_move)
    
    def manual_move(self, event):
        if event.keysym == 'Up':
            if self.check_move(0, -1):
                self.move_cell("u")
        if event.keysym == 'Down':
            if self.check_move(0, 1):
                self.move_cell("d")
        if event.keysym == 'Left':
            if self.check_move(-1, 0):
                self.move_cell("l")
        if event.keysym == 'Right':
            if self.check_move(1, 0):
                self.move_cell("r")
    
    """
    AI MODE
    """
    def create_AI_agent(self):
        if self.agent_type == 2:
            self.agent = GoRightAgent()
        elif self.agent_type == 3:
            self.agent = RandomAgent()
        else:
            print("agent type not available...")
                
    def create_AI_loop(self):
        self.AI_move()
        root.after(AI_MOVEMENT_SPEED, self.create_AI_loop)
        
    def AI_move(self):
        action = self.agent.think(self)
        self.move_cell(action)
    
    """
    CLASS UTILS
    """
    def check_move(self, x, y):
        x0, y0 = self.get_cell_coords()
        x1 = x0 + x
        y1 = y0 + y
        return self.maze.maze[y1][x1] != 1

    def get_cell_coords(self):
        position = self.canvas.coords(self.cell)
        x = int(position[0] / self.size)
        y = int(position[1] / self.size)
        return (x, y)
    
    def get_color(self, x, y):
        if self.maze.start_cell == (x, y):
            return 'red'
        if self.maze.exit_cell == (x, y):
            return 'green'
        if self.maze.maze[y][x] == 1:
            return 'black'
    
    """
    GAME END
    """
    def check_status(self):
        if self.maze.exit_cell == self.get_cell_coords():
            self.status.config(text="Finished in %d moves!" % self.steps)
            self.restart_dialogue()
    
    def restart_dialogue(self):
        """Unbinds all events, if game finishes. Shows a message with 
        instructions to restart application
        """
        self.canvas.unbind_all("<KeyPress-Up>")
        self.canvas.unbind_all("<KeyPress-Down>")
        self.canvas.unbind_all("<KeyPress-Left>")
        self.canvas.unbind_all("<KeyPress-Right>")
        
        msg = "Finished in %d moves. Do you want to restart?" % self.steps
        if messagebox.askyesno("Restart", msg):
            self.restart()
    
    def restart(self):
        self.canvas.destroy()
        self.status.destroy()
        self.steps = 0
        self.create_widgets() 
        self.draw_maze()
        self.create_events()


"""
MAZE CLASS
"""
         
class Maze(object):
    """
    A class that generates the maze. The maze is defined by a 
    2D-list. INTs in the 2D list represent the following:
        0: path
        1: wall
        2: exit
        3: start
    """
    def __init__(self, width=21, height=21, exit_cell=(1,1)):
        self.width = width
        self.height = height
        self.exit_cell = exit_cell
        self.create()
        
    def create(self):
        """
        Creates a random 2D-list. Borders are walls, the middle part 
        consists of 80% paths and 20% walls
        """
        self.maze = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    row.append(1)
                else:
                    r = random.random()
                    if r < 0.8:
                        row.append(0)
                    else:
                        row.append(1)
            self.maze.append(row)
        
        self.maze[self.exit_cell[1]][self.exit_cell[0]] = 2
        
        rand_x = random.randint(1, self.width-2)
        rand_y = random.randint(1, self.height-2)
        self.start_cell = (rand_x, rand_y)
        self.maze[rand_y][rand_x] = 3


"""
AGENT CLASSES
"""

class Agent(object):
    pass

class GoRightAgent(Agent):
    """
    Very basic version of an agent, always tries to move right
    """
    def think(self, game):
        if game.check_move(1, 0):
            return "r"
        else:
            print("No possible moves...")

class RandomAgent(Agent):
    """
    Basic agent that chooses a random direction, that is possible
    """
    def think(self, game):
        actions = ["u", "d", "l", "r"]
        for i in range(len(actions)):
            r = random.randint(0, (len(actions)-1))
            action = DIRECTIONS[actions[r]]
            if game.check_move(action[0], action[1]):
                return actions[r]
            else:
                del actions[r]

"""
MAIN FUNCTION
"""
if __name__ == '__main__':
    root = tk.Tk()
    sys.setrecursionlimit(5000)
    app = Application(root, 10, 10, 30)
    app.master.title('Searchmaze')
    app.mainloop()
    