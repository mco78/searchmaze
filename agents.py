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

              
class BFSAgent(Agent):
    
    """
    Agent with "Breadth First Search" orientated on Berkley AI Course
    
    """
    
    def __init__(self, game):
        self.plan = None
        self.exit_found = False
        self.visited = []
        self.start = Position(game.get_cell_coords(), None)
        self.visited.append(self.start.position)
        self.next_to_eval = []
        self.next_to_eval.append(self.start)
        self.evaluated = 0
    
    def think(self, game):
        """
        If agent has a plan, it follows it and returns an action. If there is
        not plan it evaluates next position in self.next_to_eval and returns 
        evaluated position (for drawing a dot in GUI)
        """
        if not self.plan:
            eval_pos = self.get_plan(game)
            return eval_pos
        else:
            action = self.plan[0]
            del self.plan[0]
            return action
    
    def get_plan(self, game):
        """
        evaluate neighboured positions if there is the exit. if exit is reached
        submit plan. save new positions to be evaluated in self.next_to_eval.
        In any case return evaluated position.
        """
        if self.exit_found == False:
            current = self.next_to_eval[0]
            self.evaluated += 1
            print("Evaluating %s" %str(current.position))
            if current.position == game.maze.exit_cell:
                self.exit_found = True
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
                print("%i positions evaluated." % self.evaluated)
                print("submitting plan with %i steps." %len(plan))
                self.plan = plan
                return current.position
            
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
                    if pos.position not in self.visited: 
                        eval_pos.append(pos)
                for ev in eval_pos:
                    self.visited.append(ev.position)
                    self.next_to_eval.append(ev)
                self.next_to_eval.remove(current)
                return current.position
  

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
    
    
        
    