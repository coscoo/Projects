import unittest
import statistics
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

class Test_generate_letters(unittest.TestCase):

  def check_if_fun_factor_is_met(self, letters, factor):
    return len(self.game.explorer.get_all_anagrams(letters)) >= factor
  
  def setUp(self):
      #Runs before every test
      self.game = AnaGame(100, 60, get_valid_word_list())
      self.game.letters = ["p", "o", "t", "s", "r", "i", "a"]
      self.all_anagrams = ["air", "ira", "par", "rap", "asp", "sap", "spa", "apt", "pat", "tap", "art", "rat", "tar", "pit",  
                          "tip", "its", "sit", "opt", "pot", "top", "airs", "sari", "oars", "soar", "rota", "taro", "raps",  
                          "rasp", "spar", "oats", "taos", "part", "prat", "rapt", "trap", "past", "pats", "spat", "taps",  
                          "arts", "rats", "star", "tars", "riot", "trio", "pris", "rips", "pits", "spit", "tips", "pairs",  
                          "paris", "opts", "post", "pots", "spot", "stop", "tops", "astir", "stair", "rots", "sort", "parts",  
                          "sprat", "strap", "traps", "riots", "trios", "strip", "trips", "patios", "patois", "ports",  
                          "sport", "strop"]
    
  def test_generate_letters_1(self):
      """generate_letters - Data Types, Produces 7 Letters"""
      letters = self.game.generate_letters(1, 'SCRABBLE')
      self.assertIsInstance(letters, list)      
      self.assertTrue(len(letters) == 7, "A scrabble distribution should produce 7 letters")
      letters = self.game.generate_letters(1, 'UNIFORM')
      self.assertTrue(len(letters) == 7, "A uniform distribution should produce 7 letters")
  
  def test_generate_letters_2(self):
      """generate_letters - Scrabble Fun Factor of 50"""
      fun_factor = 50
      for _ in range(10):
        letters = self.game.generate_letters(fun_factor, 'SCRABBLE')
        result = self.check_if_fun_factor_is_met(letters, fun_factor)
        self.assertTrue(result)
  
  def test_generate_letters_3(self):
      """generate_letters - Uniform Fun Factor of 50"""
      fun_factor = 50
      for _ in range(10):
        letters = self.game.generate_letters(fun_factor, 'UNIFORM')
        result = self.check_if_fun_factor_is_met(letters, fun_factor)
        self.assertTrue(result)
  
  def test_generate_letters_4(self):
    """generate_letters - Scrabble Letters Generated Randomly"""
    # Run generate_letters 25 times and check that not all 25 sets of letters are the same.
    seen_letters = set()
    for _ in range(25):
        letters = self.game.generate_letters(5, 'SCRABBLE')
        seen_letters.add(tuple(letters))
    # Make sure we did not only see 1 set of letters generated.  
    self.assertTrue(len(seen_letters) > 1)

  def test_generate_letters_5(self):
    """generate_letters - Uniform Letters Generated Randomly"""
    # Run generate_letters 25 times and check that not all 25 sets of letters are the same.
    seen_letters = set()
    for _ in range(25):
        letters = self.game.generate_letters(5, 'UNIFORM')
        seen_letters.add(tuple(letters))
    # Make sure we did not only see 1 set of letters generated.  
    self.assertTrue(len(seen_letters) > 1)

  def test_generate_letters_6(self):
    """generate_letters - Scrabble vs Uniform letter count distributions for fun_factor of -1 """
    # Run generate_letters 500 times and count all the letters that are generated
    # Fun factor of -1 to avoid the selected sample of anagrammable words since all random choices are valid
    fun_factor = -1
    letter_count = {}
    for i in range(97, 123):
       letter_count[chr(i)] = 0

    for _ in range(500):
        letters = self.game.generate_letters(fun_factor, 'SCRABBLE')
        for letter in letters:
           letter_count[letter.lower()]+=1
    
    print("Scrabble:",letter_count)
    scrabble_std_dev = statistics.stdev(letter_count.values())
    print("Scrabble Std Dev:", scrabble_std_dev)

    letter_count = {}
    for i in range(97, 123):
       letter_count[chr(i)] = 0

    for _ in range(500):
        letters = self.game.generate_letters(fun_factor, 'UNIFORM')
        for letter in letters:
           letter_count[letter.lower()]+=1
    
    print("Uniform:",letter_count)
    uniform_std_dev = statistics.stdev(letter_count.values())
    print("Uniform Std Dev:", uniform_std_dev)

    self.assertTrue(scrabble_std_dev - uniform_std_dev>30, "The average standard deviation of uniform and scrabble generations should be significantly different. We've chosen a test threshold difference of 30, but uniform should ballpark around 10s and scrabble should ballpark the 100s.")
    
  def test_generate_letters_7(self):
    """generate_letters - Valid Scrabble letter limits re: picking w/out replacement """
    # max of 3 g's, 1 j,  etc

    fun_factor = -1
    freq = {
       "e":12,
        "a":9,
        "i":9,
        "o":8,
        "n":6,
        "r":6,
        "t":6,
        "d":4,
        "l":4,
        "s":4,
        "u":4,
        "g":3,
        "b":2,
        "c":2,
        "f":2,
        "h":2,
        "m":2,
        "p":2,
        "v":2,
        "w":2,
        "y":2,
        "j":1,
        "k":1,
        "q":1,
        "x":1,
        "z":1

    }

    for _ in range(50):
      letters = self.game.generate_letters(fun_factor, 'SCRABBLE')
      letter_count = {}

      for letter in letters:
          letter_count[letter.lower()] = letter_count.get(letter.lower(), 0) + 1

      for letter in letter_count:
          self.assertTrue(letter_count[letter] <= freq[letter], "Letter count exceeded for letter during a generation: " + letter)

if __name__ == '__main__':
    unittest.main() 