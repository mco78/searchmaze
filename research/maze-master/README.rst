====
maze
====

A little maze game in Tkinter::

    $ ./maze.py --width=31 --height=21 --size=10

Madness::

    $ ./maze.py -W 200 -H 200 --size 3


procedural_maze_gen.py and oop_maze_gen.py
------------------------------------------

Scripts to generate random mazes based on `Depth-first search algorithm`_

.. _Depth-first search algorithm: http://en.wikipedia.org/wiki/Maze_generation_algorithm#Depth-first_search

Example::

    $ python procedural_maze_gen.py -W 21 -H 21 --verbose
    # # # # # # # # # # # # # # # # # # # # # 
    #   #               #               #   # 
    #   #   #   # # #   # # # # #   #   #   # 
    #       #       #               #       # 
    #   # # # # #   # # # # # # # # # # #   # 
    #   #       #           #           #   # 
    #   #   # # # # # # #   # # #   #   #   # 
    #       #               #       #   #   # 
    # # # # #   # # # # # # #   # # # # #   # 
    #           #           #       #       # 
    #   # # # # #   # # #   #   #   #   # # # 
    #   #       #       # A #   #   #       # 
    #   # # #   #   #   # # #   #   # # #   # 
    #       #       #   #       #           # 
    #   #   # # # # #   #   # # # # # # #   # 
    #   #           #           #       #   # 
    #   # # # # #   #   # # # # #   #   # # # 
    #   #       #   #       #       #       # 
    #   #   #   #   # # # # #   # # # # #   # 
    #       #   #                       # B # 
    # # # # # # # # # # # # # # # # # # # # # 
    Steps from A to B: 128

    $ python oop_maze_gen.py -v -W 41 -H 11
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #   #                       #                           #           #           #
    #   #   #   # # # # # # # # #   # # # # #   # # # # #   #   # # # # #   # # #   #
    #   #   #   #           #       #           #       #       #       #   #       #
    #   #   #   #   # # #   #   # # #   #   # # #   #   # # #   #   #   #   #   # # #
    #       #   #   #       #   #       #   #       #       #   #   #       #       #
    #   # # #   #   #   # # #   #   # # #   #   # # # # #   #   #   # # # # # # #   #
    #   #       #   #           #       #   #   #       #   #   #           #   #   #
    #   #   # # #   # # # # # # # # #   # # #   #   #   #   # # # # # # #   #   #   #
    # A #                           #               #   #                       # B #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    Steps from A to B: 142


