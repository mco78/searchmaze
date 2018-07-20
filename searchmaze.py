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

CONTINUE: cant clear options menu and start the game properly

"""

import random
import tkinter as tk
from tkinter import messagebox
import sys


"""
MAIN CODE
"""

class Application(tk.Frame):
    
    def __init__(self, parent, width=21, height=21, size=10):
        self.frame = tk.Frame.__init__(self, parent)
        self.width = width
        self.height = height
        self.size = size
        self.get_options()
        
    def get_options(self):
        """
        shows an radiobutton option to choose the type of agent for the game
        """
        agent_option = None
        agents = [
                 ("manual", 1),
                 ("go right", 2),
                 ("random", 3)
                 ]
        tk.Label(self.frame, 
               text="Choose an agent type:",
               padx = 20
               ).grid()
        for txt, val in agents:
            tk.Radiobutton(self.frame, 
            text=txt,
            padx = 20, 
            variable=agents, 
            value=val).grid()
        
        tk.Button(self.frame,
                  text="Start",
                  padx = 20, 
                  command=lambda : self.clear_options(agent_option)
                  ).grid()
    
    def clear_options(self, agent_option):
        """clears the option menu and starts the main game"""
        self.agent_type = agent_option
        for widget in self.winfo_children():
            widget.destroy() #does not work!
        self.start()
         
    def start(self):
        self.game_frame = tk.Frame(self, self.frame)
        self.maze = Maze(self.width, self.height)
        self.steps = 0
        self.grid()
        self.create_widgets() 
        self.draw_maze()
        self.create_events()
        
         
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
    
    def create_events(self):
        self.canvas.bind_all("<KeyPress-Up>", self.move_cell)
        self.canvas.bind_all("<KeyPress-Down>", self.move_cell)
        self.canvas.bind_all("<KeyPress-Left>", self.move_cell)
        self.canvas.bind_all("<KeyPress-Right>", self.move_cell)
    
    def move_cell(self, event):
        if event.keysym == 'Up':
            if self.check_move(0, -1):
                self.canvas.move(self.cell, 0, -self.size)
                self.steps += 1
        if event.keysym == 'Down':
            if self.check_move(0, 1):
                self.canvas.move(self.cell, 0, self.size)
                self.steps += 1
        if event.keysym == 'Left':
            if self.check_move(-1, 0):
                self.canvas.move(self.cell, -self.size, 0)
                self.steps += 1
        if event.keysym == 'Right':
            if self.check_move(1, 0):
                self.canvas.move(self.cell, self.size, 0)
                self.steps += 1
        
        self.status.config(text="Moves: %d" % self.steps)
        self.check_status()
    
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
    
    def check_status(self):
        if self.maze.exit_cell == self.get_cell_coords():
            self.status.config(text="Finished in %d moves!" % self.steps)
            self.restart_dialogue()
            
    
    def get_color(self, x, y):
        if self.maze.start_cell == (x, y):
            return 'red'
        if self.maze.exit_cell == (x, y):
            return 'green'
        if self.maze.maze[y][x] == 1:
            return 'black'
    
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
        
        #place exit_cell
        self.maze[self.exit_cell[1]][self.exit_cell[0]] = 2
        
        #create random starting cell 
        rand_x = random.randint(1, self.width-2)
        rand_y = random.randint(1, self.height-2)
        self.start_cell = (rand_x, rand_y)
        self.maze[rand_y][rand_x] = 3

if __name__ == '__main__':
    root = tk.Tk()
    sys.setrecursionlimit(5000)
    app = Application(root, 10, 10, 30)
    app.master.title('Searchmaze')
    app.mainloop()
    