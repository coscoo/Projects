import random
from colorama import Fore, Back, Style, init

try:
    from Pyramid import Pyramid
except ModuleNotFoundError:
    print("Pyramid.py is not found.")
    pass

class Board:
    def __init__(self, STYLES: dict[str, str] ):
        self.TRACK_LENGTH = 16
        self.STYLES = STYLES
        self.track = []#list of lists
        for x in range(16):
            self.track.append([])
        self.pyramid = Pyramid(self.STYLES)
        self.ticket_tents = {"r":[5,3,2,2], "g": [5,3,2,2], "b": [5,3,2,2], "y": [5,3,2,2], "p": [5,3,2,2]}  # dict str -list of ints
        self.dice_tents = [] #list of tuples with first being str and second being in
        self.place_camels()
        self.reset_leg()

    def place_camels(self):
        '''Places stacked camels in a random order on the first position of the track.
        '''
        camel_removed = list()
        camel_available = list(self.STYLES.keys())
        if camel_removed == list():
            camel_removed.append(random.choice(camel_available))
            camel_available.remove(camel_removed[0])
        for i in range (4):
            camel_removed.append(random.choice(camel_available))
            camel_available.remove(camel_removed[-1])
        self.track[0] = camel_removed
        #print(self.track[0])
        pass

    def move_camel(self, die: tuple[str, int]):
        '''Moves the camel of the given color forward by the given number of spaces.
            If the camel is on a tile with other camels, it moves with all camels
            on top of it.

            If the camel reaches the end of the track, it ... TODO

            Args:
                die (tuple[str, int]): A tuple containing the color and value of the die.
                    The color is a string representing the camel's color.
                    The value is an integer representing the number of spaces to move.
        '''
        for tiles in self.track:
            if die[0] in tiles:
                self.track[self.track.index(tiles) + die[1]].extend(tiles[tiles.index(die[0]):])
                org_len = len(tiles) - tiles.index(die[0])
                for i in range (org_len):
                    tiles.remove(tiles[-1])
                return self.track
        pass

    def roll_die(self):
        '''Shakes the pyramid and places the rolled die on the next dice tent
            If the pyramid is empty, returns a die with color "" and value 0.

            Returns:
                tuple[str, int] - A tuple representation of the rolled die
        '''
        rolled_die = self.pyramid.shake()
        if rolled_die == ("", 0):
            return rolled_die
        else:
            self.dice_tents.append(rolled_die)
            return rolled_die
        pass

    def take_ticket(self, color:str):
        '''Removes the top ticket available from the ticket tent of the given color.
           Tickets are removed from the tent in the order of their values, with the highest value ticket being removed first.

            If no tickets are available, returns a ticket with value of 0.

            Returns:
                tuple[str, int] - A tuple representation of the ticket
        '''
        if self.ticket_tents[color] != []:
            ticket = (color, self.ticket_tents[color][0])
            self.ticket_tents[color].pop(0)
        else:
            ticket = (color,0)
        return ticket
        pass

    def is_leg_finished(self):
        ''' A leg is finished when all dice have been rolled. This is determined by checking dice tents
            as playing with crazy camels involves more than five dice.

            Returns:
                bool - True if all dice have been rolled, False otherwise
        '''
        return len(self.dice_tents) == 5

        pass

    def get_rankings(self):
        '''Returns the first and second place camels as a tuple of strings.

            Return
                tuple[str, str] - A tuple containing the first and second place camels
        '''
        first_place = ""
        second_place = ""
        for i in range (15,-1,-1):
            if self.track[i] != []:
                if len(self.track[i]) > 1:
                    if first_place != "":
                        second_place = self.track[i][-1]
                        break
                    else:
                        first_place = self.track[i][-1]
                        second_place = self.track[i][-2]
                        break
                else:
                    if first_place == "":
                        first_place = self.track[i][0]
                        continue
                    else:
                        second_place = self.track[i][0]
                        break
        return (first_place, second_place)

    def reset_leg(self):
        '''Resets the board for a new leg of the game.
            - Resets the pyramid
            - Resets the ticket tents
            - Empties the dice tents
            - Does not move camels
        '''
        self.pyramid.reset_leg()
        self.ticket_tents = {"r":[5,3,2,2], "g": [5,3,2,2], "b": [5,3,2,2], "y": [5,3,2,2], "p": [5,3,2,2]}  # dict str -list of ints
        self.dice_tents = [] #list of tuples with first being str and second being int
        pass

    def __str__(self):
        board_string = ""
         #Ticket Tents
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string+=self.STYLES[ticket_color]+next_ticket_value+Style.RESET_ALL+" "
        board_string += ticket_string +"\t\t"

        #Dice Tents
        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string+=self.STYLES[die[0]]+str(die[1])+Style.RESET_ALL+" "
        for i in range (5-len(self.dice_tents)):
            dice_string+=Back.WHITE+" "+Style.RESET_ALL+" "

        #Camels and Race Track
        board_string += dice_string +"\n"
        for row in range(4, -1, -1):
            row_str = [" "]*16
            for i in range(len(self.track)):
                for camel_place, camel in enumerate(self.track[i]):
                    if camel_place == row:
                        row_str[i]=self.STYLES[camel]+ camel +  Style.RESET_ALL
            board_string += "🌴 "+str("   ".join(row_str))+" |🏁\n"
        board_string += "   "+"".join([str(i)+"   " for i in range(1, 10)])
        board_string += "".join([str(i)+"  " for i in range(10, 17)])

        return board_string



if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    board = Board(STYLES)
    print(str(board)+"\n")

    num_rolls=2
    for _ in range(num_rolls):
        rolled_die=board.roll_die()
        board.move_camel(rolled_die)
        print(f"{rolled_die} was shaken from the pyramid")
    print(board.pyramid)
    ticket = board.take_ticket(rolled_die[0])
    print(f"Player took a {rolled_die[0]} ticket: {ticket}")
    print(board)

    first, second = board.get_rankings()
    print(f"First place: {first}, Second place: {second}")
    print("\nResetting leg...")
    board.reset_leg()
    print(board)
