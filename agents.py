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
    
    def get_possible_directions(self, game, position):
        """get all possible free positions next to position"""
        poss_actions = []
        for d in DIRECTIONS:
            if game.check_move_from_position(position, DIRECTIONS[d][0], DIRECTIONS[d][1]):
                poss_actions.append(DIRECTIONS[d])
        print("possible directions: %s" %str(poss_actions))
        return poss_actions


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
                
class BFSAgent(Agent):
    """
    Agent with "Breadth First Search" orientated on Berkley AI Course
    """
    def think(self, game):
        #possible steps (say 3)
            #take 1st possible step
                #finish?
            #take 2nd possible step
                #finish?
            #take 3rd possible step
                #finish?
        #maybe with anytree?
        exit_found = False
        
        start = game.get_cell_coords()
        visited = [] #virtually visited positions while thinking
        visited.append(start)
        next_to_eval = []
        next_to_eval.append(start)
        
        while exit_found == False:
            current = next_to_eval[0]
            print("Evaluating %s" %str(current))
            if current == game.maze.exit_cell:
                print("Position %s is the exit!" % str(current))
                exit_found = True
            else:
                poss_dir = self.get_possible_directions(game, current)
                poss_pos = []
                for d in poss_dir:
                    poss_pos.append((current[0] + d[0], current[1] + d[1]))
                print("possible positions: %s" %str(poss_pos))
                eval_pos = []
                for pos in poss_pos:
                    if pos not in visited:
                        eval_pos.append(pos) #positions to evaluate
                print("positions to evaluate: %s" %str(eval_pos))
                for ev in eval_pos:
                    print("Adding %s" %str(ev))
                    visited.append(ev)
                    next_to_eval.append(ev)
                next_to_eval.remove(current)
                print("Eval Queue %s:" %str(next_to_eval))
                print("Visited %s: " %str(visited))
                
        """
        TODO: 
            - Create a Dir with all the successors to each position, so when
              solution is found, agent has a path to walk
            - draw small dot or something on the canvas for evaluated positions
            - apply actual move with the plan
        """
            
        
    
    
        
    