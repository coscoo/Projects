import unittest
from colorama import Fore, Back, Style, init
import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

Player = None
if not Player:
    from Player import Player as Player 

CamelUp = None
if not CamelUp:
    from CamelUp import CamelUp as CamelUp 

class Test_CamelUp(unittest.TestCase):
    def setUp(self):
        """runs before each test"""
        self.camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
        }
        self.game = CamelUp(self.camel_styles, [Player("Dave", self.camel_styles), Player("Sasha", self.camel_styles)])
    
    def test_camelup_data_attributes(self):
        """CamelUp- Data Types"""
        self.assertIsInstance(self.game.board, object, "CamelUp.board should return an object")
        self.assertIsInstance(self.game.players, list, "CamelUp.players should return a list")
        self.assertIsInstance(self.game.players[0], object, "CamelUp.players[0] should return an object")
        self.assertIsInstance(self.game.STYLES, dict, "CamelUp.STYLES should return a dict")
        self.assertEqual(self.game.STYLES, self.camel_styles, "CamelUp.STYLES should be a dict of the camel styles")
        first, second = self.game.process_leg_payouts()
        self.assertIn(first, self.camel_styles.keys(), "process_leg_payouts should return a valid camel color for first place")
        self.assertIn(second, self.camel_styles.keys(), "process_leg_payouts should return a valid camel color for second place")
    
    def test_camelup_process_leg_payouts_with_bets(self):
        """CamelUp- process_leg_payouts with player bets"""
        self.game.board.track[0][4] = 'y'
        self.game.board.track[0][3] = 'b'
        self.game.players[0].add_bet(('y', 5))
        self.game.players[0].add_bet(('b', 3))
        self.game.players[1].add_bet(('g', 2))
        self.game.players[1].add_bet(('r', 3))
        self.game.players[1].add_bet(('b', 5))
        self.assertEqual(self.game.players[0].money, 3, "Player.money should start at 3")
        self.assertEqual(self.game.players[1].money, 3, "Player.money should start at 3")
        first, second = self.game.process_leg_payouts()
        self.assertEqual(first, 'y', "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(second, 'b', "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(self.game.players[0].money, 9, "Player.money should increase by the value of the ticket for first place and second place bets")
        self.assertEqual(self.game.players[1].money, 2, "Player.money should increase by the value of the ticket for first place and second place bets")


    def test_camelup_process_leg_payouts_with_no_bets(self):
        """CamelUp- process_leg_payouts with player bets"""
        first, second = self.game.process_leg_payouts()
        self.assertEqual(first, self.game.board.track[0][4], "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(second, self.game.board.track[0][3], "process_leg_payouts should return the top camel on space 0 as first place")

        self.assertEqual(self.game.players[0].money, 3, "Player.money should start at 3") #no bets
        self.assertEqual(self.game.players[1].money, 3, "Player.money should start at 3") #no bets

if __name__ == "__main__":
    unittest.main()