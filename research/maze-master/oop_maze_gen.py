#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

## MAZE GENERATOR ##

Author: Leo Vidarte <http://nerdlabs.com.ar>

This is free software,
you can redistribute it and/or modify it
under the terms of the GPL version 3
as published by the Free Software Foundation.

Based on Depth-first search algorithm:
http://en.wikipedia.org/wiki/Maze_generation_algorithm#Depth-first_search

  1. Start at a particular cell and call it the "exit."
  2. Mark the current cell as visited, and get a list of its neighbors.
     For each neighbor, starting with a randomly selected neighbor:
       1. If that neighbor hasn't been visited, remove the wall between
          this cell and that neighbor, and then recurse with that neighbor as
          the current cell.

"""


import random


class Maze(object):

    def __init__(self, width=21, height=21, exit_cell=(1, 1)):
        self.width = width
        self.height = height
        self.exit_cell = exit_cell
        self.create()

    def create(self):
        self.maze = [[1] * self.width for _ in range(self.height)] # full of walls
        self.start_cell = None
        self.steps = None
        self.recursion_depth = None
        self._visited_cells = []
        self._visit_cell(self.exit_cell)

    def _visit_cell(self, cell, depth=0):
        x, y = cell
        self.maze[y][x] = 0 # remove wall
        self._visited_cells.append(cell)
        neighbors = self._get_neighbors(cell)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if not neighbor in self._visited_cells:
                self._remove_wall(cell, neighbor)
                self._visit_cell(neighbor, depth+1)
        self._update_start_cell(cell, depth)

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
        self.maze[y][x] = 0 # remove wall

    def _update_start_cell(self, cell, depth):
        if depth > self.recursion_depth:
            self.recursion_depth = depth
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

    from optparse import OptionParser
    parser = OptionParser(description="Maze random generator")
    parser.add_option('-W', '--width', type=int, default=21,
                      help="maze width (must be odd)")
    parser.add_option('-H', '--height', type=int, default=21,
                      help="maze height (must be odd)")
    parser.add_option('-v', '--verbose', action='store_true',
                      help="show steps from start to exit")
    args, _ = parser.parse_args()

    for arg in ('width', 'height'):
        if getattr(args, arg) % 2 == 0:
            setattr(args, arg, getattr(args, arg) + 1)
            print "Warning: %s must be odd, using %d instead" % (arg, getattr(args, arg))

    exit_cell = (args.width-2, args.height-2)
    maze = Maze(args.width, args.height, exit_cell)
    maze.show(args.verbose)

