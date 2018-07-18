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


def get_neighbors(cell, maze):
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
    maze_width = len(maze[0])
    maze_height = len(maze)

    # Left
    if x - 2 > 0:
        neighbors.append((x-2, y))
    # Right
    if x + 2 < maze_width:
        neighbors.append((x+2, y))
    # Up
    if y - 2 > 0:
        neighbors.append((x, y-2))
    # Down
    if y + 2 < maze_height:
        neighbors.append((x, y+2))

    return neighbors

def remove_wall(maze, cell, neighbor):
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
    maze[y][x] = 0

def update_start_cell(cell, depth, _={'start_cell': None, 'recursion_depth': None}):
    if depth > _['recursion_depth']:
        _['start_cell'] = cell
        _['recursion_depth'] = depth
    start_cell = _['start_cell']
    steps = _['recursion_depth'] * 2 # wall + cell
    return (start_cell, steps)

def visit_cell(maze, cell, cells_visited, depth=0):
    x, y = cell
    maze[y][x] = 0 
    cells_visited.append(cell)
    neighbors = get_neighbors(cell, maze)
    random.shuffle(neighbors)
    for neighbor in neighbors:
        if not neighbor in cells_visited:
            remove_wall(maze, cell, neighbor)
            visit_cell(maze, neighbor, cells_visited, depth+1)
    start_cell, steps = update_start_cell(cell, depth)
    return (maze, start_cell, steps)

def create_maze(width=21, height=21, exit_cell=(1,1)):
    maze = [[1] * width for _ in range(height)] # full of walls
    maze, start_cell, steps = visit_cell(maze, exit_cell, cells_visited=[])
    return (maze, start_cell, steps)

def show_maze(maze, exit_cell, start_cell, verbose=False):
    MAP = {0: ' ', # path
           1: '#', # wall
           2: 'B', # exit
           3: 'A', # start
          }
    x0, y0 = exit_cell
    maze[y0][x0] = 2
    x1, y1 = start_cell
    maze[y1][x1] = 3
    for row in maze:
        print ' '.join([MAP[col] for col in row])
    if args.verbose:
        print "Steps from A to B:", steps


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
    maze, start_cell, steps = create_maze(args.width, args.height, exit_cell)
    show_maze(maze, exit_cell, start_cell, args.verbose)

