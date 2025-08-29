import random
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

try:
    from WordleAI import WordleAI as WordleAI
except ModuleNotFoundError:
    print("WordleAI.py is not found.")

from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses

class Wordle:
    def __init__(self, STYLES: dict[str, str], wordleAI:WordleAI, secret_words:get_secret_words):
        self.STYLES = STYLES
        self.secret_word = get_secret_words()
        target_word = random.choice(self.secret_word)
        guess = input("yo tell us your guess: ")
        print(Back.WHITE+Style.DIM + "       ")
        print(Back.WHITE+Style.DIM + " " + Back.BLACK+Style.DIM + secret_word + Back.WHITE+Style.DIM + " ")


    pass

if __name__ == "__main__":
    STYLES= {
            "yellow": Back.YELLOW+Style.BRIGHT,
            "green": Back.GREEN+Style.BRIGHT,
            "gray": Back.BLACK+Style.BRIGHT,
            "border": Back.WHITE+Style.BRIGHT
    }
    wordle = Wordle(STYLES)
    print(str(Wordle)+"\n")

    pass
