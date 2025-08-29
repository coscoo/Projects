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

class Test_update_stats(unittest.TestCase):
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
    
  def test_update_stats_0(self):
       """game.update_stats - Data Types"""
       self.game.all_guesses.append(("star","tarts"))
       self.game.all_guesses.append(("far","rat"))
       self.game.all_guesses.append(("top","tip"))
       print(f"Guesses: {self.game.all_guesses}")

       self.game.update_stats()
       scoreDict = self.game.stats
       self.assertIn("score", scoreDict, "The dictionary should have a 'score' key.")
       self.assertIsInstance(scoreDict["score"], int, "The score key should map to an integer value.")
       self.assertIn("accuracy", scoreDict, "The dictionary should have an 'accuracy' key.")
       self.assertIsInstance(scoreDict["accuracy"], int, "The 'accuracy' key should map to an integer value.")
       self.assertIn("skill", scoreDict, "The dictionary should have a 'skill' key.")
       self.assertIsInstance(scoreDict["skill"], int, "The 'skill' key should map to an integer value.")
       self.assertIn("valid_guesses", scoreDict, "The dictionary should have a 'valid_guesses' key.")
       self.assertIsInstance(scoreDict["valid_guesses"], list, "The 'valid' key should map to a list value.")
       self.assertIn("invalid_guesses", scoreDict, "The dictionary should have an 'invalid_guesses' key.")
       self.assertIsInstance(scoreDict["invalid_guesses"], list, "The 'invalid' key should map to a list value.")
       self.assertIn("unique_guessed", scoreDict, "The dictionary should have an 'unique_guessed' key.")
       self.assertIsInstance(scoreDict["unique_guessed"], set, "The 'guessed' key should map to a set value.")
       self.assertIn("not_guessed", scoreDict, "The dictionary should have a 'not_guessed' key.")
       self.assertIsInstance(scoreDict["not_guessed"], list, "The 'not guessed' key should map to a set value.")

  def test_update_stats_1(self):
       """game.update_stats - No valid guesses out of 3 guesses"""
       self.game.all_guesses.append(("star","tarts"))
       self.game.all_guesses.append(("far","rat"))
       self.game.all_guesses.append(("top","tip"))
       print(f"Guesses: {self.game.all_guesses}")

       self.game.update_stats()
       scoreDict = self.game.stats
       self.assertEqual(scoreDict["score"], 0)
       self.assertEqual(len(scoreDict["valid_guesses"]), 0)
       self.assertEqual(len(scoreDict["invalid_guesses"]), 3)
       self.assertEqual(scoreDict["accuracy"], 0)
       self.assertEqual(scoreDict["skill"], 0)
       self.assertEqual(len(scoreDict["unique_guessed"]), 0)
       self.assertEqual(scoreDict["not_guessed"], self.all_anagrams)

  def test_update_stats_2(self):
      """game.update_stats - All valid guesses with one duplicate anagram stem"""
      self.game.all_guesses.append(("art","rat")) 
      self.game.all_guesses.append(("rats","arts"))
      self.game.all_guesses.append(("spit","pits"))
      self.game.all_guesses.append(("spit","tips"))
      self.game.all_guesses.append(("stop","pots"))
      self.game.all_guesses.append(("tip","pit"))
      self.game.all_guesses.append(("top","pot"))
      
      self.game.update_stats()
      scoreDict = self.game.stats      
      self.assertEqual(scoreDict["score"], 11)
      self.assertEqual(len(scoreDict["valid_guesses"]), 7 )
      self.assertEqual(len(scoreDict["invalid_guesses"]), 0)
      self.assertEqual(scoreDict["accuracy"], 100)

      guessed = ["art","rat","rats","arts","spit","pits","tips","stop","pots","tip","pit","top","pot"]
      expectedSkill = 17
      self.assertEqual(scoreDict["skill"], expectedSkill)
      self.assertEqual(len(scoreDict["unique_guessed"]), len(guessed))
      self.assertEqual(len(scoreDict["not_guessed"]), len(self.all_anagrams)-len(guessed))
      self.assertEqual(len(scoreDict["unique_guessed"].union(guessed)), len(guessed))

      not_guessed = self.all_anagrams.copy()
      for guessed_word in guessed:
          not_guessed.remove(guessed_word)  
      self.assertEqual(scoreDict["not_guessed"], not_guessed)

  def test_update_stats_3(self):
      """game.update_stats - Some valid and some invalid guesses"""
      self.game.all_guesses.append(("star","pair"))
      self.game.all_guesses.append(("fun","rat"))
      self.game.all_guesses.append(("top","tip"))
      self.game.all_guesses.append(("art","rat")) #1
      self.game.all_guesses.append(("rats","arts")) #2
      self.game.all_guesses.append(("spit","pits")) #2
      self.game.all_guesses.append(("pits","tips")) #2
      self.game.all_guesses.append(("stop","pots")) #2
      self.game.all_guesses.append(("tip","pit")) #1
      self.game.all_guesses.append(("top","pot")) #1
      self.game.all_guesses.append(("ports","sport")) #3
      self.game.all_guesses.append(("spot", "spit")) 
      self.game.all_guesses.append(("sot", "spit"))
      self.game.all_guesses.append(("hiss", "cat"))
      self.game.all_guesses.append(("mouse", "rat"))
      self.game.all_guesses.append(("cat", "dog"))
      print(f"Guesses: {self.game.all_guesses}")

      self.game.update_stats()
      scoreDict = self.game.stats
      print(f"Testing score... expecting 14..")
      self.assertEqual(scoreDict["score"], 14)
      print(f"Testing valid words... expecting 8 pairs of valid words")
      self.assertEqual(len(scoreDict["valid_guesses"]), 8)
      print(f"Testing invalid words... expecting 8 pairs of iinvalid words")
      self.assertEqual(len(scoreDict["invalid_guesses"]), 8)
      print(f"Testing accuracy... expecting an accuracy of 50")
      self.assertEqual(scoreDict["accuracy"], 50)

      guessed = {"art","rat","rats","arts","spit","pits","tips","stop","pots","tip","pit","top","pot", "ports","sport"}
      print(f"Testing unique words guessed... expecting {guessed}")
      self.assertEqual(scoreDict["unique_guessed"], guessed)
      all_anagrams2=self.all_anagrams.copy()
      for word in guessed:
           all_anagrams2.remove(word)
      print(f"Testing unique words not guessed... expecting {all_anagrams2}")  
      self.assertEqual(scoreDict["not_guessed"], all_anagrams2)
      expectedSkill = 20
      print(f"Testing skill... expecting a skill of 20")
      self.assertEqual(scoreDict["skill"], expectedSkill)

  def test_update_stats_4(self):
     """game.update_stats - No guesses"""
     self.game.all_guesses=[]
     print(f"Guesses: {self.game.all_guesses}")

     self.game.update_stats()
     scoreDict = self.game.stats
     self.assertEqual(scoreDict["score"], 0)
     self.assertEqual(len(scoreDict["valid_guesses"]), 0)
     self.assertEqual(len(scoreDict["invalid_guesses"]), 0)
     self.assertEqual(scoreDict["accuracy"], 0)
     self.assertEqual(scoreDict["skill"], 0)
     self.assertEqual(len(scoreDict["unique_guessed"]), 0)
     self.assertEqual(len(scoreDict["not_guessed"]), len(self.all_anagrams))

  def test_update_stats_5(self):
       """game.update_stats - Scoring with duplicate and invalid guesses"""
       self.game.all_guesses.append(("star","tarts")) #INVALID
       self.game.all_guesses.append(("far","rat")) #INVALID
       self.game.all_guesses.append(("rat","art"))
       self.game.all_guesses.append(("rat","art")) #INVALID
       self.game.all_guesses.append(("art","rat")) #INVALID
       #letters = ["p", "o", "t", "s", "r", "i", "a"]

       print(f"Guesses: {self.game.all_guesses}")

       self.game.update_stats()
       scoreDict = self.game.stats
       print(f"Testing score... expecting 1")
       self.assertEqual(scoreDict["score"], 1, "Score is incorrect!")
       print(f"Testing valid words... expecting 1 pair of valid words")
       self.assertEqual(len(scoreDict["valid_guesses"]), 1, "Number of valid words is incorrect!")
       print(f"Testing invalid words... expecting 4 pairs of invalid words")
       self.assertEqual(len(scoreDict["invalid_guesses"]), 4, "Number of invalid words is incorrect!")
       print(f"Testing accuracy... expecting an accuracy of 20")
       self.assertEqual(scoreDict["accuracy"], 20, "Accuracy is incorrect")
       guessed={"art", "rat"}
       print(f"Testing unique words guessed... expecting {self.game.all_guesses}")
       self.assertEqual(len(scoreDict["unique_guessed"]), 2, "Number of unique words guessed is incorrect!")
       print(f"Testing unique words not guessed... expecting {len(self.all_anagrams)-2} words not guessed")  
       self.assertEqual(len(scoreDict["not_guessed"]), len(self.all_anagrams)-2, "Number of unique words not guessed is incorrect!")
       print(f"Testing skill... expecting a skill of 2")
       self.assertEqual(scoreDict["skill"], 2, "Skill is incorrect!")

if __name__ == '__main__':
    unittest.main() 

