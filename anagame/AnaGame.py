import time
import random
from valid_anagame_words import get_valid_word_list

try:
    from AnagramExplorer import AnagramExplorer
except ModuleNotFoundError:
    print("AnagramExplorer.py is not found.")
    pass

class AnaGame:
    def __init__(self, fun_factor:int, time_limit: int, corpus:list[str]):
        self.corpus = corpus
        self.explorer = AnagramExplorer(corpus)
        self.time_limit= time_limit
        self.letters= self.generate_letters(fun_factor, "SCRABBLE") #"UNIFORM", "SCRABBLE", "FREQUENCY"
        self.all_guesses= []
        self.stats= {}

    def generate_letters(self, fun_factor: int, distribution: str):
        '''Generates a list of 7 randomly-chosen lowercase letters which can form at least
            fun_factor unique anagramable words

            Args:
                fun_factor (int): minimum number of unique anagram words offered by the chosen letters
                distribution (str): The type of distribution to use in order to choose letters
                        "UNIFORM" - chooses letters based on a uniform distribution, with replacement
                        "SCRABBLE" - chooses letters based on a scrabble distribution, without replacement

            Returns:
                list: A list of 7 lowercase letters
        '''
        letters = []
        if distribution == "SCRABBLE":
            test_letters = []
            possible_letters = ("kjxqzbbccmmppffhhvvwwyygggddddllllssssuuuunnnnnnrrrrrrttttttooooooooaaaaaaaaaiiiiiiiiieeeeeeeeeeee")
            test_letters = random.sample(possible_letters, 7)
            while len(self.explorer.get_all_anagrams(test_letters)) < fun_factor:
                test_letters = random.sample(possible_letters, 7)

        elif distribution == "UNIFORM":
            test_letters = []
            possible_letters = list("qwertyuiopasdfghjklzxcvbnm")
            test_letters = random.sample(possible_letters, 7)
        while len(self.explorer.get_all_anagrams(test_letters)) < fun_factor:
                test_letters = random.sample(possible_letters, 7)
        letters = test_letters



        # Tip: Start with a predefined list of letters for testing
        #letters = ["p", "o", "t", "s", "r", "i", "a"]

        return letters

    def parse_guess(self, guess: str):
        '''Splits an entered guess into a two word tuple with all white space removed.

            Args:
                guess (str): A single string reprsenting the player guess

            Returns:
                tuple: A tuple of two words. ("", "") in case of invalid input.

            Examples
            --------
            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat, tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat , tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat,tea") == ("eat", "tea")
            True

            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.parse_guess("eat tea") == ("", "")
            True
        '''
        guess = list(guess)
        while " " in guess:
            guess.remove(" ")
        guess = "".join(guess)
        if len(tuple(guess.split(","))) < 3 and 1 < len(tuple(guess.split(","))):
            return tuple(guess.split(","))
        else:
            return tuple(["", ""])

    def play_game(self):
        '''Plays a single game of AnaGame'''

        print("\nWelcome to AnaGame!\n")
        print("Please enter your anagram guesses separated by a comma: eat,tea")
        print("Enter 'quit' to end the game early, or 'hint' to get a useful word\n")
        print(f"You have {time_limit} seconds to guess as many anagrams as possible!")
        print(f"{self.letters}")

        guesses = []
        quit = False

        start = time.perf_counter() #start the stopwatch (sec)
        stop = start + time_limit

        while time.perf_counter() < stop and not quit:
            guess = input('')
            if guess.strip().lower() == "quit":
                quit = True
            elif guess.strip().lower() == "hint":
                print(f"Try working with: {list(self.explorer.get_most_anagrams(self.letters))[0]}")
            else:
                tuple_guess = self.parse_guess(guess)
                if len(tuple_guess[0]) > 1:
                    self.all_guesses.append(tuple_guess)
                else:
                    print("Invalid input")

            print(f"{self.letters} {round(stop - time.perf_counter(), 2)} seconds left")

    def ch_to_prime(self, word):
        ch_to_prime= {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13,
            'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43,
            'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79,
            'w': 83, 'x': 89, 'y': 97, 'z': 101 }
        prime_keys = 1
        for y in word:
            prime_keys = ch_to_prime[y] * prime_keys
        return prime_keys

    def update_stats(self):
        '''Aggregates several statistics into a single dictionary with the following key-value pairs:
            "valid_guesses" - list of valid guesses
            "invalid_guesses" - list of invalid/duplicate guesses
            "unique_guessed" - set of unique words guessed from valid guesses
            "not_guessed" - list of unique words not guessed, sorted first by hashed keys then by anagrammability/alphabetically
            "score" - per the rules of the game
            "accuracy" -  truncated int percentage representing valid player guesses out of all player guesses
                    3 valid and 5 invalid guesses would result in an accuracy of 37 --> 3/8 = .375
            "skill" - truncated int percentage representing the total number of unique anagram words guessed out of all possible unique anagram words
                Guessing 66 out of 99 unique words would result in a skill of 66 --> 66/99 = .66666666
            Args:
            guesses (list): A list of tuples representing all word pairs guesses by the user
            letters (list): The list of valid letters from which user should create anagrams
            explorer (AnagramExplorer): helper object used to compute anagrams of letters.

            Returns:
            dict: Returns a dictionary with seven keys: "valid", "invalid", "score", "accuracy", "guessed", "not guessed", "skill"

            Example
            -------
            >>> letters = ["p", "t", "s", "a", "r"]
            >>> game = AnaGame(100, 60, get_valid_word_list())
            >>> game.letters = letters
            >>> game.all_guesses = [("star","tarts"),("far","rat"),("rat","art"),("rat","art"),("art","rat")]
            >>> game.update_stats()
            >>> game.stats["valid_guesses"] == [("rat", "art")]
            True
            >>> game.stats["invalid_guesses"] == [("star", "tarts"), ("far", "rat"), ("rat", "art"), ("art", "rat")]
            True
            >>> game.stats["score"]
            1
            >>> game.stats["accuracy"]
            20
            >>> game.stats["unique_guessed"] == {"rat", "art"}
            True
            >>> game.stats["not_guessed"] == ['par', 'rap', 'asp', 'sap', 'spa', 'apt', 'pat', 'tap', 'tar', 'raps', 'rasp', 'spar', 'part', 'prat', 'rapt', 'trap', 'past', 'pats', 'spat', 'taps', 'arts', 'rats', 'star', 'tars', 'parts', 'sprat', 'strap', 'traps']
            True
            >>> game.stats["skill"]
            6
            '''
        self.stats["valid_guesses"] = [] #[(rat, tar)]
        self.stats["invalid_guesses"] = [] #[(rat, tax)]
        self.stats["unique_guessed"] = set() #unique valid guessed words
        self.stats["not_guessed"] = [] #list... sorted by anagrammability
        self.stats["score"] = 0    #total score per the rules of the game
        self.stats["accuracy"] = 0 #int percentage- valid player guesses/all player guesses
        self.stats["skill"] = 0    #int percentage- unique guessed words/all possible unique anagram words
        seen = set()

        if self.all_guesses != None:
            self.stats["not_guessed"] = list(self.explorer.get_all_anagrams(self.letters)) #needs to be sorted by anagrammability
            for pairs in self.all_guesses:
                if self.explorer.is_valid_anagram_pair(pairs) == True and tuple(sorted(pairs)) not in seen: #checks if guesses are right
                    seen.add(tuple(sorted(pairs)))
                    for words in pairs:
                        self.stats["unique_guessed"].add(words) #will later be used as score keepre
                else:
                    self.stats["invalid_guesses"].append(pairs)#if wrong will add to invalid guesses
            for words in list(self.stats["unique_guessed"]):
                self.stats["not_guessed"].remove(words) #removes each word in list of anagrams not guesses yet
            for pairs in seen:
                self.stats["score"] += len(pairs[0]) - 2
            self.stats["valid_guesses"] = list(seen)
                    # for x in self.stats["valid_guesses"]:
                    #     if x[0] in seen:
                    #         self.stats["score"] -= ((len(pairs[0])) - 2)
            print(self.stats["unique_guessed"])

            if len(self.all_guesses) > 0:
                self.stats["accuracy"] =  int((len(self.stats["valid_guesses"]) / len(self.all_guesses))*100)
            self.stats["skill"] = int(len(self.stats["unique_guessed"]) / len(set(self.explorer.get_all_anagrams(self.letters))) * 100)
            self.stats["not_guessed"] = sorted(sorted(self.stats["not_guessed"]), key = self.ch_to_prime)

        else:
            return None



    def __str__(self):
        '''Returns a string representation of the game'''
        output = "------------\n"
        output+= f"Total Guesses: {len(self.all_guesses)}\n"
        for guess in self.all_guesses:
            output+=f"  {guess[0]},{guess[1]}"

        output += "\n------------\n"
        output+=f"Valid Guesses: {len(self.stats['valid_guesses'])}/{len(self.all_guesses)}\n"
        for guess in self.stats['valid_guesses']:
            output+=f"  {guess[0]},{guess[1]}"
        output+=f"\n\nInvalid Guesses: {len(self.stats['invalid_guesses'])}/{len(self.all_guesses)}\n"
        for guess in self.stats['invalid_guesses']:
            output+=f"  {guess[0]},{guess[1]}"

        output+="\n------------\n"
        output+=f"Unique Words Guessed: {len(self.stats['unique_guessed'])}\n"
        for guess in sorted(self.stats['unique_guessed']):
            output+=f"  {guess}"
        output+=f"\n\nWords you could have guessed: {len(self.stats['not_guessed'])}\n"
        for guess in self.stats['not_guessed']:
            output+=f"  {guess}"

        output+=f"\n------------\n"
        output+=f"Accuracy: {round(self.stats['accuracy'], 2)}%\n"
        output+=f"\nSkill: {self.stats['skill']}%\n"
        output+=f"\nScore: {self.stats['score']}\n"
        output+=f"------------\n"

        return output


if __name__ == "__main__":
    time_limit = 60
    fun_factor = 100
    game = AnaGame(fun_factor, time_limit, get_valid_word_list())
    game.play_game()
    game.update_stats()

    print("\nThanks for playing AnaGame!\n")
    print(game)
