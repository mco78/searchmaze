# -*- coding: utf-8 -*-
"""
SearchMaze - a maze game for testing AI
Created on Wed Jul 18 13:58:16 2018

@author: Marc Otten

Contributers:
    - "maze" by lvidarte (https://github.com/lvidarte/maze)

    
TODO:
    - implement DFS agent
    - implement flexible maze size
    - implement maze file selection    
    - restart option with new option selection
    - implement exception handling
    - document all classes and methods

BUGS:
    - AI agent keeps on running after restart dialogue anwered with no (combine with new restart options!)
    - radom maze doesn't work anymore -> OS ERROR
"""


from functools import reduce
import tkinter as tk
from tkinter import messagebox
import sys
from math import floor

from agents import *


AI_MOVEMENT_SPEED = 150

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
        
        root.geometry("520x340+400+400")
        
        self.options_frame = tk.Frame(self, width=150, height=300)
        self.options_frame.grid(row = 0, column = 0)
        self.game_frame = tk.Frame(self, bg = "white", width=300, height=300)
        self.game_frame.grid(row = 0, column = 1)
    
        self.get_options()
    
    """
    OPTIONS DIALOGUE
    """
    def get_options(self):
        """
        shows a radiobutton option to choose the type of agent for the game
        """

        agents = [
                 ("manual", 1),
                 ("go right", 2),
                 ("random", 3),
                 ("BFS", 4)
                 ]
        agent_option = tk.IntVar()
        agent_option.set(1)
        
        mazes = [
                ("Maze 1", 1),
                ("Maze 2", 2),
                ("random", 3)
                ]
        maze_option = tk.IntVar()
        maze_option.set(2)
        
        agent_label = tk.Label(self.options_frame, 
                               text="Choose the type of agent:",
                               padx = 20)
        agent_label.grid(row=0)
        
        r = 0
        self.radio_buttons = []
        for txt, val in agents:
            r += 1
            button = tk.Radiobutton(self.options_frame, 
                                    text=txt,
                                    padx = 20, 
                                    variable=agent_option,
                                    value=val)
            button.grid(row=r)
            self.radio_buttons.append(button)
            
        tk.Label(self.options_frame,
                 text="Choose a maze:",
                 padx = 20
                 ).grid(row=r+1)
        r = r + 1 #skip one row for label
        for txt, val in mazes:
            r += 1
            button = tk.Radiobutton(self.options_frame,
                                    text=txt,
                                    padx=20,
                                    variable=maze_option,
                                    value=val)
            button.grid(row=r)
            self.radio_buttons.append(button)


        self.start_button = tk.Button(self.options_frame,
                  text="Start",
                  padx = 20, 
                  command=lambda : self.clear_options(self.options_frame,
                                                      agent_option.get(), 
                                                      maze_option.get())
                  )
        self.start_button.grid(row=r+1)
    
    def clear_options(self, options_frame, agent_option, maze_option):
        """
        disables the option menu and starts the main game
        """
        self.agent_type = agent_option
        self.maze_type = maze_option
        if self.maze_type == 1:
            self.maze_file = "maze1.maze"
        if self.maze_type == 2:
            self.maze_file = "maze2.maze"
        
        self.start_button['state'] = 'disabled'
        for button in self.radio_buttons:
            button['state'] = 'disabled'
        self.start()
         
    """
    SET UP MAZE
    """
    def start(self):
        if self.maze_type == 3: #Could be needed to update after more mazes added!
            self.maze = Maze(self.width, self.height)
        else:
            self.maze = Maze(self.maze_file)
        
        self.steps = 0
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
        self.canvas = tk.Canvas(self.game_frame, width=width, height=height)
        self.canvas.grid()
        self.status = tk.Label(self)
        self.status.grid(row=1, column=1)

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
    
    def draw_eval_dot(self, action):
        #TODO
        x0 = action[0] * self.size + floor(0.4 * self.size)
        x1 = x0 + floor(0.2 * self.size)
        y0 = action[1] * self.size + floor(0.4 * self.size)
        y1 = y0 + floor(0.2 * self.size)
        self.canvas.create_oval(x0, y0, x1, y1, fill="gray82")
        
    
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
        elif self.agent_type == 4:
            self.agent = BFSAgent(self)
        else:
            print("agent type not available...")
                
    def create_AI_loop(self):
        self.AI_move()
        root.after(AI_MOVEMENT_SPEED, self.create_AI_loop)
        
    def AI_move(self):
        action = self.agent.think(self)
        if type(action) == tuple: #no actual move, just evaluating a position
            self.draw_eval_dot(action)
        else:
            self.move_cell(action)
    
    """
    CLASS UTILS
    """
    def check_move(self, x, y):
        position = self.get_cell_coords()
        return self.check_move_from_position(position, x, y)
            
    def check_move_from_position(self, position, x, y):
        x0, y0 = position
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
    def __init__(self, filename=None, width=21, height=21, exit_cell=(1,1)):
        if filename:
            self.maze = self.parse_file(filename)
            self.width = len(self.maze[0])
            self.height = len(self.maze)
            self.exit_cell = self.find_cell(2)
            self.start_cell = self.find_cell(3) 
        else:
            self.width = width
            self.height = height
            self.exit_cell = exit_cell
            self.create_random()
    
    
    def create_random(self):
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
    
    
    def parse_file(self, filename):
        board = []
        with open(filename, 'r') as f:
            content = f.readlines()
            for line in content:
                row = []
                strip_line = line.rstrip()
                for c in strip_line:
                    row.append(int(c))
                board.append(row)
        # basic validation of file - could be handled with exceptions
        all_elements = reduce(lambda x,y :x+y, board)
        if len(board) != 10 or len(board[1]) != 10:
            print("ERORR: File dimensions do not fit!")
            return None
        elif max(all_elements) > 3 or min(all_elements) < 0:
            print("ERROR: File contains invalid characters")
            return None
        elif all_elements.count(2) != 1:
            print("ERROR: File has not one exit")
            return None
        elif all_elements.count(3) != 1:
            print("ERROR: File has not one start")
            return None
        else:
            return board
        
    def find_cell(self, element):
        y = -1
        for row in self.maze:
            y += 1
            x = -1
            for pos in row:
                x += 1
                if pos == element:
                    return (x, y)
    

"""
MAIN FUNCTION
"""
if __name__ == '__main__':
    root = tk.Tk()
    sys.setrecursionlimit(5000)
    app = Application(root, 10, 10, 30)
    app.master.title('Searchmaze')
    app.mainloop()
    