import itertools
from valid_anagame_words import get_valid_word_list

class AnagramExplorer:
    def __init__(self, valid_words: list[str]):
        """
        Initializes the AnagramExplorer with a list of valid words.

        Args:
            valid_words (list[str]): A list of valid words to use for anagram exploration.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones"])
        >>> explorer.corpus
        ['listen', 'silent', 'enlist', 'inlets', 'stone', 'tones']
        """

        self.__corpus = valid_words
        #first step is to take all the valid words in and store it in our corpus,
        self.__lookup_dict = self.build_lookup_dict() #only calculated once, when the object is created
        #the second is to call the build loop up dictionary
        #to look up dict in the future u should call "loop_dict"
    @property
    def corpus(self):
        return self.__corpus

    @property
    def lookup_dict(self):
        return self.__lookup_dict

    def generate_hash(self, word: str) -> tuple[str]:
        """
        Generates a hash for the given word by sorting its letters and returning a tuple.

        Args:
            word (str): The word to generate a hash for.

        Returns:
            tuple[str]: A tuple representing the sorted letters of the word.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent"])
        >>> explorer.generate_hash("listen")
        ('e', 'i', 'l', 'n', 's', 't')
        """
        return tuple(sorted(word))


    def build_lookup_dict(self) -> dict[str, set[str]]:
        """
        Builds a lookup dictionary where keys are sorted tuples of lowercase letters,
        and values are sets of lowercase words from self.__corpus with the same letters.
        Facilitates quick retrieval of anagram families based on their sorted letter representation.

        Returns:
            dict: A dictionary mapping sorted letter tuples to sets of words.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets"])
        >>> lookup = explorer.build_lookup_dict()
        >>> lookup[('e', 'i', 'l', 'n', 's', 't')] ==  {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> lookup.get(('s', 't', 'o', 'n', 'e'), set())
        set()
        >>> lookup.get(('a', 'p', 'p', 'l', 'e'), set())
        set()
        """
        lookup = dict()
        hash_word = ()
        for x in self.__corpus:
            hash_word = tuple(sorted(x))
            if hash_word in lookup:
                lookup[hash_word].add (x)
            else:
                lookup[hash_word] = {x}
        return lookup
    def is_valid_anagram_pair(self, pair: tuple[str, str], letters: list[str] = None) -> bool:
        """
        Valid anagram pairs must exist in the corpus.
        If letters are provided, both words must match the letters in the list (without replacement).
        Words must be at least 3 characters long and not identical.

        Args:
            pair (tuple[str, str]): A tuple containing two words to check.
            letters (list[str]): A list of letters available for forming anagrams.

        Returns:
            bool: True if the pair forms a valid anagram, False otherwise.
        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets"])
        >>> explorer.is_valid_anagram_pair(("listen", "silent"), ["l", "i", "s", "t", "e", "n"])
        True
        >>> explorer.is_valid_anagram_pair(("stone", "tones"), ["s", "t", "o", "n", "e"])
        False
        >>> explorer.is_valid_anagram_pair(("apple", "pale"), ["a", "p", "p", "l", "e"])
        False
        """
        word1,word2 = pair[0],pair[1]
        word1 = list(word1.lower())
        word2 = list(word2.lower())
        if len(word1) < 3 and len(word2) < 3:
            return False
        if pair[0].lower() not in self.corpus or pair[1].lower() not in self.corpus:
            return False
        if word1 == word2 or len(word1) != len(word2):
            return False
        for y in word1:
            if y in word2:
                word2.remove(y)
        if letters != None:
            letters2 = sorted(letters)
            for y in word1:
                if y in letters2:
                    letters2.remove(y)
                else:
                    return False
        if len(word2) == 0:
            return True
        return False

    def get_all_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Finds all anagrams that can be formed using the given letters. If no letters are provided
        or if the letters list is empty, returns all words from the corpus that can form an anagram pair.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of all valid anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_all_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_all_anagrams() == {'listen', 'silent', 'enlist', 'inlets', 'stone', 'tones'}
        True
        >>> explorer.get_all_anagrams(["a", "p", "p", "l", "e"])
        set()
        """
        valid_anagram_pairs = set()
        if letters == None:
            for total_words in self.lookup_dict.values():
                if len(set(total_words)) > 1:
                    valid_anagram_pairs.update(set(total_words))
        else:
            letters = sorted(letters)
            valid_anagram_pairs = set()
            for len_of_combos in range(3, len(letters)+1):
                combos = itertools.combinations(letters,len_of_combos)
                for x in combos:
                    if x in self.lookup_dict.keys():
                        if len(self.lookup_dict[x])>1:
                            for y in self.lookup_dict[x]:
                                valid_anagram_pairs.add(y)
        return valid_anagram_pairs

    def get_most_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Generates a set of words which forms the largest number of anagram combinations within self.__corpus
        The returned set contains all words for each anagram group that produces the maximum number of anagrams.
        If a list of letters is provided, the search is restricted to anagrams that can be formed from those letters.

        Args:
            letters (list[str], optional): A list of letters to form anagrams. Defaults to None.

        Returns:
            set[str]: A set of words that form the most anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_most_anagrams(["l", "i", "s", "t", "e", "n"]) == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_most_anagrams() == {'listen', 'silent', 'enlist', 'inlets'}
        True
        >>> explorer.get_most_anagrams(["a", "p", "p", "l", "e"])
        set()
        """
        amnt_anagrams = 2
        longest_anagrams = set()
        if letters == None:
            for sets in self.lookup_dict.values():
                if len(sets) > amnt_anagrams:
                    amnt_anagrams = len(sets)
                    longest_anagrams = sets
                elif len(sets) == amnt_anagrams:
                    longest_anagrams = sets.union(longest_anagrams)
        else:
            letters = sorted(letters)
            for len_of_combos in range (3, len(letters)+1):
                combos = itertools.combinations(letters,len_of_combos)
                for x in combos:
                    if x in self.lookup_dict.keys():
                        if len(self.lookup_dict[x]) > amnt_anagrams:
                            amnt_anagrams = len(self.lookup_dict[x])
                            longest_anagrams = self.lookup_dict[x]
                        if len(self.lookup_dict[x]) == amnt_anagrams:
                            longest_anagrams = self.lookup_dict[x].union(longest_anagrams)
        return longest_anagrams




    def get_words_with_no_anagrams(self, letters: list[str] = None) -> set[str]:
        """
        Finds all words in the corpus that do not form any anagram pairs with any other word.

        Returns:
            set[str]: A set of words from the corpus that have no anagrams.

        Examples:
        >>> explorer = AnagramExplorer(["listen", "silent", "enlist", "inlets", "stone", "tones", "unique"])
        >>> explorer.get_words_with_no_anagrams() == {'unique'}
        True
        >>> explorer = AnagramExplorer(["rat", "tar", "art", "stop", "tops", "pots", "spot", "post"])
        >>> explorer.get_words_with_no_anagrams()
        set()
        >>> explorer = AnagramExplorer(["apple", "banana", "carrot"])
        >>> explorer.get_words_with_no_anagrams() == {'apple', 'banana', 'carrot'}
        True
        """
        """
        no_anagram = set()
        if letters == None:
            for total_words in self.lookup_dict.values():
                if len(set(total_words)) < 2 :
                    no_anagram.update(set(total_words))
        else:
            letters = sorted(letters)
            no_anagram = set()
            for len_of_combos in range(3, len(letters)+1):
                combos = itertools.combinations(letters,len_of_combos)
                for x in combos:
                    if x in self.lookup_dict.keys():
                        if len(self.lookup_dict[x]) < 2:
                            for y in self.lookup_dict[x]:
                                no_anagram.add(y)"""
        if not letters:
            all_anagrams = self.get_all_anagrams()
            no_anagram = all_anagrams.symmetric_difference(set(self.corpus))
        else:
            all_anagrams = self.get_all_anagrams(letters)
            no_anagram = all_anagrams.symmetric_difference(set(self.corpus))

        return no_anagram
        ## YOUR CODE GOES HERE

if __name__ == "__main__":
    print("Demonstrating AnagramExplorer functionality")

    simple_corpus = [
        "listen", "silent", "enlist", "inlets", "stone", "tones", "note", "tone", "rat", "tar", "art",
        "stop", "pots", "tops", "opt", "spot", "post", "unique", "apple", "banana", "carrot"
    ]

    # explorer = AnagramExplorer(simple_corpus)
    explorer = AnagramExplorer((simple_corpus))
    print(explorer.get_most_anagrams())
    # letters = ["l", "i", "s", "t", "e", "n"]
    #
    # print("\nGet all anagrams for a particular collection of letters:", letters)
    # print("Anagrams:", explorer.get_all_anagrams(letters))
    #
    # print("\nGet all words from the corpus that can form an anagram pair:")
    # print("Anagrams:", explorer.get_all_anagrams())
    #
    # print("\nFind the words that form the most anagrams for a particular collection of letters::", letters)
    # print("Most anagrams:", explorer.get_most_anagrams(letters))
    #
    # print("\nFind the words that form the most anagrams in the entire corpus:", letters)
    # print("Most anagrams:", explorer.get_most_anagrams())
    #
    # word_pair = ("listen", "silent")
    # print("\nCheck if two words form a valid anagram pair:", word_pair)
    # print("Is valid anagram pair:", explorer.is_valid_anagram_pair(word_pair, letters))
    #
    # letters = ["p", "i", "s", "t", "e", "n"]
    # print("\nWords with no anagrams in the corpus for a particular collection of letters:", letters)
    # print(explorer.get_words_with_no_anagrams(letters))
    #
    # print("\nWords with no anagrams in the corpus:")
    # print(explorer.get_words_with_no_anagrams())
