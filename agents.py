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

DIRECTIONS = {"u": (0, -1),
              "r": (1, 0),
              "d": (0, 1),
              "l": (-1, 0)}

"""
AGENT CLASSES
"""

class Agent(object):
    
    def get_possible_directions(self, game, position):
        """get all possible free positions next to position"""
        poss_actions = []
        for d in DIRECTIONS:
            if game.check_move_from_position(position.position, DIRECTIONS[d][0], DIRECTIONS[d][1]):
                poss_actions.append(DIRECTIONS[d])
                
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
    
    def __init__(self):
        self.plan = None
    
    def think(self, game):
        if not self.plan:
            self.get_plan(game)
            return None
        else:
            action = self.plan[0]
            del self.plan[0]
            return action
    
    def get_plan(self, game):
        exit_found = False        
        start = Position(game.get_cell_coords(), None)
        visited = [] #virtually visited positions (as tuple) while thinking
        visited.append(start.position)
        next_to_eval = []
        next_to_eval.append(start)
        evaluated = 0
        
        while exit_found == False:
            current = next_to_eval[0]
            evaluated += 1
            print("Evaluating %s" %str(current.position))
            if current.position == game.maze.exit_cell:
                exit_found = True
                #translate path to plan for directions
                plan = []
                for i in range(len(current.ancestors)):
                    x1 = current.ancestors[i].position[0]-current.ancestors[i-1].position[0]
                    y1 = current.ancestors[i].position[1]-current.ancestors[i-1].position[1]
                    for ac, pos in DIRECTIONS.items():
                        if pos == (x1, y1):
                            plan.append(ac)
                #last step        
                x1 = current.position[0] - current.ancestors[-1].position[0]
                y1 = current.position[1] - current.ancestors[-1].position[1]
                for ac, pos in DIRECTIONS.items():
                        if pos == (x1, y1):
                            plan.append(ac)    
                print("%i positions evaluated." % evaluated)
                print("submitting plan with %i steps." %len(plan))
                self.plan = plan
            
            else:
                #get possible directions
                poss_dir = self.get_possible_directions(game, current)    
                #translate directions to list of Position objects with ancestors
                poss_pos = []
                for d in poss_dir:
                    ancestors = []
                    if current.ancestors:
                        for a in current.ancestors:
                            ancestors.append(a)
                    ancestors.append(current)
                    new_x = current.position[0] + d[0]
                    new_y = current.position[1] + d[1]
                    poss_pos.append(
                            Position((new_x, new_y), ancestors)
                            )
                #remove already visited positions
                eval_pos = []
                for pos in poss_pos:
                    if pos.position not in visited: 
                        eval_pos.append(pos)
                for ev in eval_pos:
                    visited.append(ev.position)
                    next_to_eval.append(ev)
                next_to_eval.remove(current)             
  

class Position(object):
    """Data object for positions for path saving
        position = x,y Tuple of actual position
        ancestors = list of positions that where on the path to this position
        successors = list of possible positions (without already visited)
    """
    def __init__(self, position, ancestors):
        self.position = position
        self.ancestors = ancestors 
        self.successors = []             


def get_positions_list_string(p_list):
    """utility to strigify a list of Positions"""
    pos_str = ""
    for p in p_list:
        pos_str += str(p.position)
    return pos_str
    
    
        
    