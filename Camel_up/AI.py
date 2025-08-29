from colorama import Fore, Back, Style, init
import copy
from itertools import permutations, product
import math

try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass

class AI:
    def __init__(self, board:Board):
        self.STYLES = board.STYLES
        self.board = board #reference to actual game board... updates as game is played
        pass

    def get_all_roll_sequences(self) -> set[tuple[tuple[str, int]]]:
        '''
            Constructs a set of all possible roll sequences for the dice currently in the pyramid
            Note: Use itertools product function

            Return
                A set of tuples representing all the ordered dice seqences that could result from shaking all dice from the pyramid
        '''
        itertools.permutations()
        pass

    def run_enumerative_analysis(self) -> dict[str, tuple[float, float]]:
        '''Conducts an enumerative analysis of the probability that each camel will win either 1st or
           2nd place in this leg of the race. The enumerative analysis counts 1st/2nd place finishes
           via calculating the entire state space tree of possible outcomes given the current state of
           the game.

           General Steps:
                1) Precalculate all possible dice sequences for the dice currently in the pyramid
                2) Move through each sequence of possible dice rolls to count the number of 1st/2nd places
                   finishes for each camel
                3) Calculates the probability that each camel will come in 1st or 2nd based on the total
                   number of 1st/2nd finishes out of the total number of dice sequences

           Returns:
               A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        pass

    def run_experimental_analysis(self, trials:int) -> dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimenta analysis counts
            1st/2nd place finishes bycounting outcomes from randomly shaking the pyramid over a given
            number of trials.

           General Steps:
                1) Shake the pyramid enough times to randomly generate a dice sequence to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total
                   number of 1st/2nd finishes out of the total number of trials

           Args
              trials (int): The number of random simulations to conduct

           Returns:
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an experimental analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        pass

    def get_ticket_EV(self, ticket_value:int, prob_first:float, prob_second:float)->float:
        '''Caclulates the Expected Value of a ticket

            Args:
                ticket_value (int): The value of a betting ticket if a camel comes in first place for a leg
                prob_first (float): The probability (0.0 - 1.0) that a camel will come in fist place
                prob_second (float): The probability (0.0 - 1.0) that a camel will come in second place

            Return:
                float: The expected value of the ticket
        '''
        pass

    def run_analysis(self, trials:int)-> tuple[dict[str, tuple[float, float]], dict[str, tuple[float, float]]]:
        '''Conducts both an enumerative and experimental analysis based on the current board state
           Uses deepcopy to preserve the current game state.

           Args:
                trials: an integer indicating the number of trials to run for the experimental analysis

           Returns:
                enumerative_analysis: -A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an enumerative analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }

                experimental_analysis: - A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an experimental analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        pass

    def __str__(self) -> str:
        enum, exper = self.run_analysis(5000)

        stats_str="  Enumerative\tExperimental\n"
        analysis = [(self.STYLES[c]+c+Style.RESET_ALL, enum[c][0],enum[c][1], exper[c][0], exper[c][1])  for c in enum ]
        stats_str+="   1st   2nd\t 1st   2nd\n"
        for row in analysis:
            stats_str+="{: >1} {: >5.2f} {: >5.2f} \t{: >5.2f} {: >5.2f}".format(*row)+"\n"

        advice_str="Available bets: "
        best_ev = -10
        best_camel = "x"
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value=tickets_left[0]
                ev = self.get_ticket_EV(top_ticket_value, enum[color][0], enum[color][1])
                if ev>best_ev:
                    best_ev=ev
                    best_camel=color
                advice_str += f"({color})"+self.STYLES[color]+str(top_ticket_value)+Style.RESET_ALL+f" EV:{ev:.2f} "
            else:
                advice_str += f"({color})"+self.STYLES[color]+"X"+Style.RESET_ALL+" "

        advice_str += "\nAI Advice: "
        if best_ev>1:
            advice_str+=f"  Bet on {self.STYLES[best_camel]+best_camel+Style.RESET_ALL} with an expected value of {best_ev:.2f}\n"
        else:
            advice_str+="  No camel has an EV > 1. You should roll instead of bet.\n"

        return stats_str + advice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    game_board = Board(STYLES)
    ai = AI(game_board)
    print(game_board)
    for _ in range(3):
        rolled_die=game_board.roll_die()
        game_board.move_camel(rolled_die)
    print(game_board)
    print(ai)
    print(game_board) #game state hasn't changed

    all_possible_roll_outcomes = ai.get_all_roll_sequences()
    print(f"There are {len(all_possible_roll_outcomes)} possible outcomes for the next two dice rolls:")
    for dice_sequence in all_possible_roll_outcomes:
        print(dice_sequence)
