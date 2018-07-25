# -*- coding: utf-8 -*-
"""
Agent Classes for Searchmaze Application

Created on Wed Jul 25 16:52:16 2018

@author: Marc Otten
"""

import random

"""
FIXTURES
"""

DIRECTIONS = {"u": [0, -1],
              "r": [1, 0],
              "d": [0, 1],
              "l": [-1, 0]}

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