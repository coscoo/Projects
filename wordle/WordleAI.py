import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from wordle_secret_words import get_secret_words
from valid_wordle_guesses import get_valid_wordle_guesses

class WordleAI:
    def __init__(self, all_valid_words: list[str], valid_wordle_answers: list[str]):
        self.valid_guesses = all_valid_words
        self.possible_answers = valid_wordle_answers
        # Add additional data attributes as needed
        pass

    def get_feedback(self, guess: str, secret_word: str) -> str:
        '''Generates a feedback string based on comparing a 5-letter guess with the secret word.
            The feedback string uses the following schema:
                - Correct letter, correct spot: uppercase letter ('A'-'Z')
                - Correct letter, wrong spot: lowercase letter ('a'-'z')
                - Letter not in the word: '-'

            Args:
                guess (str): The guessed word
                secret_word (str): The secret word

            Returns:
                str: Feedback string, based on comparing guess with the secret word

            Examples
            >>> AI = WordleAI(get_valid_wordle_guesses(), get_secret_words())
            >>> AI.get_feedback("lever", "EATEN") == "-e-E-"
            True
            >>> AI.get_feedback("LEVER", "LOWER") == "L--ER"
            True
            >>> AI.get_feedback("MOMMY", "MADAM") == "M-m--"
            True
            >>> AI.get_feedback("ARGUE", "MOTTO") == "-----"
            True
        '''

        feedback_string = ["-","-","-","-","-"]
        letter_counter = {}
        guess = guess.upper()
        secret_word = secret_word.upper()
        for letter in secret_word:
            if letter in letter_counter.keys():
                letter_counter[letter.upper()] += 1
            else:
                letter_counter[letter.upper()] = 1

        for i in range(len(guess)): #iterate thru all the first ones first because it takes priority for which is correct
            if guess[i] == secret_word[i]:
                feedback_string[i] = guess[i].upper()
                letter_counter[guess[i]] -= 1

        for i in range(len(guess)):
            if guess[i] in secret_word and letter_counter[guess[i]] > 0: # also include a counter and create a second for loop
                if feedback_string[i] == "-":
                    letter_counter[guess[i]] -= 1
                    feedback_string[i] = guess[i].lower()
        return "".join(feedback_string)

        pass


    def guess(self, guesses: list[str], feedback: list[str]) -> str:
        '''Analyzes feedback from previous guesses/feedback (if any) to make a new guess

        Args:
            guesses (list): A list of string guesses, which could be empt
            "guess","gAins"
            feedback (list): A list of feedback strings, which could be empty
            ""
        Returns:
            str: a valid guess that is exactly 5 uppercase letters
        '''
        #make dict of most recent feed back and each char should be a Key and the value should be the INDEX
        # where u used each character in the feedback_string
        total_answers = list(self.possible_answers)
        possible_answers = []
        possible_letters = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
        correct_word_placement = {}
        incorrect_word_placement = {}
        final_guess = []
        #None in feedback and None in guesses and
        if not feedback and not guesses and None in feedback and None in guesses:
            return str(random.choice(possible_answers))
        else:
            for i, word in enumerate(feedback):
                for j,letter in enumerate(word):
                    if letter == '-':
                        if guesses[i][j] in possible_letters:
                            if guesses[i][j] not in correct_word_placement.keys():
                                if guesses[i][j] not in incorrect_word_placement.keys():
                                    possible_letters.remove(guesses[i][j])

                    elif letter.isupper():
                        correct_word_placement[letter] = j
                        if letter not in possible_letters:
                            possible_letters.append(letter)

                    elif letter.islower():
                        incorrect_word_placement[letter] = j
                        if letter not in possible_letters:
                            possible_letters.append(letter)

            for answers in total_answers: #so b4 we had n^2 with two nester for loops, now its n^4.. but we were thinking in this case, we eliminate
            #options because the first if statement will elimated a bunch of words (thus it will skip the for loops under). will this be more complex
            # or less complex?
                if set(correct_word_placement.keys()) in set(answers) and set(incorrect_word_placement.keys()) in set(answers):
                    for def_letters in correct_word_placement.keys():
                        if answers[correct_word_placement[def_letters]] == def_letters:
                            for in_letters in incorrect_word_placement.keys():
                                if in_letters in answers and answers[incorrect_word_placement[in_letters]] != in_letters:
                                    for i in range(len(answers)):
                                        if answers[i] not in possible_letters:
                                            break
                                        else:
                                            continue
                                        possible_answers.append(answers)
        if possible_answers:
            letter_counter = {}
            most_appeared_word = str()
            current_len = 0
            longest_len = 0
            for word in possible_answers:
                for letter in word:
                    if letter in letter_counter.keys():
                        letter_counter[letter] += 1
                    else:
                        letter_counter[letter] = 1
            for key in letter_counter.keys():
                current_len = letter_counter[key]
                if current_len > longest_len:
                    longest_len = current_len
                    most_appeared_letter = key
            for answer in possible_answers:
                if most_appeared_letter not in answer:
                    possible_answers.remove(answer)

            return possible_answers[0]
        else:
            print(possible_answers)
        pass

if __name__ == "__main__":
    AI = WordleAI(get_valid_wordle_guesses(), get_secret_words())
    #print(AI.get_feedback("LEVER", "LOWER")) #"L--ER"
    guesses = ["CRANE", "CATER"]
    feedback = ["cra-e", "cater"]
    print("look here")
    print(AI.guess(guesses, feedback)) #ee--- REACT
