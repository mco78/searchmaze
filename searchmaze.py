# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Wed Jul 18 13:58:16 2018

@author: Marc Otten

Contributers:
    - "maze" by lvidarte (https://github.com/lvidarte/maze)
    
BUGS:
    - start cell acts as wall when moving back to that spot
    - exit cell acts as a wall and is not accessible

TODO:
    - implement game end
    - implement different controll modes (manual, 
      different agents)
    
"""

import random
import tkinter as tk
import sys


"""
MAIN CODE
"""

class Application(tk.Frame):
    
    def __init__(self, parent, width=21, height=21, size=10):
         tk.Frame.__init__(self, parent)
         self.maze = Maze(width, height)
         self.size = size
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
        self.status.config(text="This is a status Text")
    
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
        return self.maze.maze[y1][x1] == 0

    def get_cell_coords(self):
        position = self.canvas.coords(self.cell)
        x = int(position[0] / self.size)
        y = int(position[1] / self.size)
        return (x, y)
    
    def check_status(self):
        if self.maze.exit_cell == self.get_cell_coords():
            self.status.config(text="Finished in %d!" % self.steps)
    
    def get_color(self, x, y):
        if self.maze.start_cell == (x, y):
            return 'red'
        if self.maze.exit_cell == (x, y):
            return 'green'
        if self.maze.maze[y][x] == 1:
            return 'black'
       
         
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
        creates a random 2D-list. Borders are walls, the middle part 
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
    root = Tk()
    sys.setrecursionlimit(5000)
    app = Application(root, 10, 10, 30)
    app.master.title('Searchmaze')
    app.mainloop()
    