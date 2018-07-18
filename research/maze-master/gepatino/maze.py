#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import Tkinter as tk


class Application(tk.Frame):

    def __init__(self, width=21, height=21, size=10):
        tk.Frame.__init__(self)
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

        self.canvas.tag_raise(self.cell) # bring to front
        self.status.config(text='Movidas mínimas: %d' % self.maze.steps)

    def create_events(self):
        self.canvas.bind_all('<KeyPress-Up>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Down>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Left>', self.move_cell)
        self.canvas.bind_all('<KeyPress-Right>', self.move_cell)

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

        args = (self.steps, self.maze.steps)
        self.status.config(text='Movidas: %d/%d' % args)
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
            args = (self.steps, self.maze.steps)
            self.status.config(text='Resuelto en %d/%d movidas!' % args)

    def get_color(self, x, y):
        if self.maze.start_cell == (x, y):
            return 'red'
        if self.maze.exit_cell == (x, y):
            return 'green'
        if self.maze.maze[y][x] == 1:
            return 'black'


class StackList(object):
    def __init__(self):
        self._data = []

    def add(self, level):
        if len(level):
            self._data.insert(0, level)

    def pop(self):
        if not self._data:
            return None
        item = self._data[0].pop()
        if len(self._data[0]) == 0:
            self._data.pop(0)
        return item


class Maze(object):
    """

    ## MAZE GENERATOR ##

    Based on Depth-first search algorithm:
    http://en.wikipedia.org/wiki/Maze_generation_algorithm#Depth-first_search

      1. Start at a particular cell and call it the "exit."
      2. Mark the current cell as visited, and get a list of its neighbors.
         For each neighbor, starting with a randomly selected neighbor:
           1. If that neighbor hasn't been visited, remove the wall between
              this cell and that neighbor, and then recurse with that neighbor as
              the current cell.

    __author__ = "Leonardo Vidarte"


    """

    def __init__(self, width=21, height=21, exit_cell=(1, 1)):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        self.width = width
        self.height = height
        self.start_cell = None
        self.exit_cell = exit_cell
        self.steps = 0
        self.maze = None
        self.create()

    def create(self):
        self.maze = [[1, ] * self.width  for _ in range(self.height)] # full of walls

        visited = []
        stack = StackList()
        item = (None, self.exit_cell)
        while item is not None:
            prev, cell = item
            if cell not in visited:
                x, y = cell
                self.maze[y][x] = 0
                if prev and cell:
                    self._remove_wall(prev, cell)
                neighbors = [x for x in self._get_neighbors(cell) if x not in visited]
                random.shuffle(neighbors)
                stack.add([(cell, x) for x in neighbors])
                visited.append(cell)
            item = stack.pop()

    def __str__(self):
        res = ''
        for row in self.maze:
            for col in row:
                res += col and '##' or '  '
            res += '\n'
        return res

    def _get_neighbors(self, cell):
        """
        Get the cells next to the cell

        Example:
          Given the following mazes
          The a neighbor's are b

          # # # # # # #     # # # # # # #
          # # # b # # #     # a # b # # #
          # # # # # # #     # # # # # # #
          # b # a # b #     # b # # # # #
          # # # # # # #     # # # # # # #
          # # # b # # #     # # # # # # #
          # # # # # # #     # # # # # # #

        """
        x, y = cell
        neighbors = []

        # Left
        if x - 2 > 0:
            neighbors.append((x-2, y))
        # Right
        if x + 2 < self.width:
            neighbors.append((x+2, y))
        # Up
        if y - 2 > 0:
            neighbors.append((x, y-2))
        # Down
        if y + 2 < self.height:
            neighbors.append((x, y+2))

        return neighbors

    def _remove_wall(self, cell, neighbor):
        """
        Remove the wall between two cells

        Example:
          Given the cells a and b
          The wall between them is w

          # # # # #
          # # # # #
          # a w b #
          # # # # #
          # # # # #

        """
        x0, y0 = cell
        x1, y1 = neighbor
        # Vertical
        if x0 == x1:
            x = x0
            y = (y0 + y1) / 2
        # Horizontal
        if y0 == y1:
            x = (x0 + x1) / 2
            y = y0

        # remove walls
        self.maze[y][x] = 0 

        self.start_cell = neighbor
        self.steps += 2

    def _update_start_cell(self, cell, depth):
        if depth > self.recursion_depth:
            self.start_cell = cell
            self.steps = depth * 2 # wall + cell

    def show(self, verbose=False):
        MAP = {0: ' ', # path
               1: '#', # wall
               2: 'B', # exit
               3: 'A', # start
              }
        x0, y0 = self.exit_cell
        self.maze[y0][x0] = 2
        x1, y1 = self.start_cell
        self.maze[y1][x1] = 3
        for row in self.maze:
            print ' '.join([MAP[col] for col in row])
        if verbose:
            print "Steps from A to B:", self.steps


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Maze game")
    parser.add_argument('--width', type=int, default=21, help="maze width (must be odd)")
    parser.add_argument('--height', type=int, default=21, help="maze height (must be odd)")
    parser.add_argument('--size', type=int, default=10, help="cells size")
    args = parser.parse_args()

    ##app = Application(101, 101, args.size)
    ##app.master.title('Maze game')
    ##app.mainloop()

    m = Maze(12, 12)
    print m

