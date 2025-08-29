import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
grandparent_dir = os.path.join(parent_dir, '..')
sys.path.append(grandparent_dir)
AnaGame= None
if not AnaGame:
    from AnaGame import AnaGame

from valid_anagame_words import get_valid_word_list


class Test_parse_guess(unittest.TestCase):
  def setUp(self):
      #Runs before every test
      self.game = AnaGame(100, 60, get_valid_word_list())

  def test_parse_guess_1(self):
      """parse_guess -  Basic Correct"""
      guess = "eat,tea"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("eat", "tea"))

  def test_parse_guess_2(self):
      """parse_guess - Correct, 1 space after comma"""
      guess = "eat, tea"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("eat", "tea"))

  def test_parse_guess_3(self):
      """parse_guess - Correct, Many spaces"""
      guess = " eat , tea "
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("eat", "tea"))

  def test_parse_guess_4(self):
       """parse_guess - Incorrect, no comma"""
       guess = "eat tea"
       actual = self.game.parse_guess(guess)
       self.assertEqual(actual, ("", ""))

  def test_parse_guess_5(self):
      """parse_guess - Incorrect, multiple commas"""
      guess = "eat, tea,"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("", ""))

  def test_parse_guess_6(self):
      """parse_guess - Incorrect, one word"""
      guess = "eattea"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("", ""))

  def test_parse_guess_7(self):
      """parse_guess - Incorrect, three words"""
      guess = "eat, tea, ate"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("", ""))

  def test_parse_guess_8(self):
      """parse_guess - Basic Correct 2"""
      guess = "stop, pots"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("stop", "pots"))

  def test_parse_guess_9(self):
      """parse_guess - Mystery Correct 1"""
      guess = " stop ,pots"
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("stop", "pots"))

  def test_parse_guess_10(self):
      """parse_guess - Mystery Correct 2"""
      guess = "stop    ,pots   "
      actual = self.game.parse_guess(guess)
      self.assertEqual(actual, ("stop", "pots"))

if __name__ == '__main__':
    unittest.main() 