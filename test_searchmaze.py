# -*- coding: utf-8 -*-
"""
Test Suite for searchmaze.py
Created on Thu Mar  1 21:52:10 2018

@author: Marc Otten
"""

import unittest
import searchmaze
import utils
from fixtures import TEST_MAZE
from fixtures import TEST_MAZE_HEIGHT
from fixtures import TEST_MAZE_WIDTH


class TestTile(unittest.TestCase):
    
    def setUp(self):
        self.tile = searchmaze.Tile(3,0,False)
        self.east_of_board_tile = searchmaze.Tile(0,TEST_MAZE_WIDTH)
        self.south_of_board_tile = searchmaze.Tile(TEST_MAZE_WIDTH, TEST_MAZE_HEIGHT)
        
    def test_tile_creation(self):
        self.assertEqual(self.tile.x, 3, "Tile position not set")
    
    def test_is_on_board(self):
        self.assertTrue(self.tile.is_on_board(), "Tile should be on board")
        self.assertFalse(self.east_of_board_tile.is_on_board(), "Tile east of board should not be on board")
        self.assertFalse(self.south_of_board_tile.is_on_board(), "Tile south of board should not be on board")
           
    def tearDown(self):
        del self.tile
        del self.east_of_board_tile
        del self.south_of_board_tile
        
class TestAgent(unittest.TestCase):
    
    def setUp(self):
        self.game = searchmaze.Game(TEST_MAZE)
        
    def test_is_target_on_board(self):
        self.assertFalse(self.game.agent.is_target_on_board("n"), "Target north should not be on board")
        self.assertTrue(self.game.agent.is_target_on_board("e"), "Target east should be on board")
        self.assertTrue(self.game.agent.is_target_on_board("s"), "Target south should be on board")
        self.assertFalse(self.game.agent.is_target_on_board("w"), "Target west should not be on board")
    
    def test_is_action_possible(self):
        self.assertTrue(self.game.agent.is_action_possible("e", self.game.state), "Action east should be possible")
        self.assertFalse(self.game.agent.is_action_possible("s", self.game.state), "Action south should not be possible")
        self.assertFalse(self.game.agent.is_action_possible("w", self.game.state), "Action west should not be possible")
        
    def test_move(self):
        self.assertEqual([self.game.agent.x, self.game.agent.y], [0, 0], "Before moving, agent should be on 0/0.")
        self.game.agent.move(self.game.state, "e")
        self.assertEqual([self.game.agent.x, self.game.agent.y], [1, 0], "After moving, agent should be on 1/0.")

    def tearDown(self):
        del self.game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = searchmaze.Game(TEST_MAZE)
    
    def test_game_creation(self):
        self.assertEqual(type(self.game.get_object_at_position(2, 3)), type(searchmaze.Tile(0,0)), 
                         "Object 'Tile' should be set at position 2,3.")
    
    def test_set_object_at_position(self):
        obj = searchmaze.Tile(0,0)
        self.game.set_object_at_position(obj, 2,3)
        self.assertEqual(type(self.game.get_object_at_position(2, 3)), type(searchmaze.Tile(0,0)), 
                         "Object 'Tile' should be set at position 2,3.")

    def tearDown(self):
        del self.game

class TestUtitlities(unittest.TestCase):
    def test_array_addition(self):
        self.assertEqual(utils.array_addition([2,2], searchmaze.DIRECTIONS["e"]), [3, 2])
        self.assertEqual(utils.array_addition([2,2], searchmaze.DIRECTIONS["n"]), [2, 1])
        self.assertEqual(utils.array_addition([2,2], searchmaze.DIRECTIONS["w"]), [1, 2])
        self.assertEqual(utils.array_addition([2,2], searchmaze.DIRECTIONS["s"]), [2, 3])
        

if __name__ == '__main__':
    unittest.main()
