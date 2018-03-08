# -*- coding: utf-8 -*-
"""
Agents for searchmaze.py
Created on Thu Mar  8 14:49:13 2018

@author: Marc Otten
"""
import random
import utils
from fixtures import *
from searchmaze import Tile
from searchmaze import Goal

def choose_agent(x, y):
    if AGENT_TYPE == "default":
        return Agent(x, y)
    elif AGENT_TYPE == "random":
        return RandomAgent(x,y)

class Agent(object):
    """Represents the agent that has to escape the maze
    REMINDER FOR LATER: MANY TYPES OF AGENTS COULD INHERIT FROM THIS CLASS AND
    POSSIBLY BE SEPERATED IN FILE AGENTS.PY"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_target_on_board(self, action):
        target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
        target = Tile(target_array[0], target_array[1])
        return target.is_on_board()
    
    def is_action_possible(self, action, state):
        if self.is_target_on_board(action):
            target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
            target_obj = state[target_array[0]][target_array[1]]
            if isinstance(target_obj, Goal):
                return True
            elif target_obj.wall == False:
                return True
        return False
    
    def act(self, state):
        """Function to make decisions and then move.
        This agent version simply goes east."""
        
        action = "e"
        print("action: {}".format(action))
        self.move(state, action)
        
    def move(self, state, action=False):
        # create east action if none provided
        if action:        
            if self.is_action_possible(action, state):
                target_array = utils.array_addition([self.x, self.y], DIRECTIONS[action])
                self.x = target_array[0]
                self.y = target_array[1]


class RandomAgent(Agent):
    """This agent picks a random direction"""
    def act(self, state):
        actions = ["e", "s", "w", "n"]
        action = actions[random.randint(0,3)]
        print("action: {}".format(action))
        self.move(state, action)
        