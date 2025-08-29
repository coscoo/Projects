import random
from colorama import Fore, Back, Style, init

class Pyramid:
    def __init__(self, camel_styles:dict[str, str]):
        '''Creates a pyramid of dice for the game Camel Up.'''
        self.STYLES = camel_styles
        self.DIE_VALUES = [1,2,3]
        self.DIE_COLORS = list(self.STYLES.keys()).copy()
        self.remaining_dice = list(self.STYLES.keys()).copy()


        pass

    def shake(self):
        '''Shakes the pyramid to remove a random color from the remaining dice.

            Return
                tuple[str, int] - A tuple representation of the rolled die
                                  If there are no dice remaining, return ("", 0)
        '''
        if len(self.remaining_dice) > 0:
            dice_chosen = random.choice(self.remaining_dice)
            numb_chosen = random.choice(self.DIE_VALUES)
            self.remaining_dice.remove(dice_chosen)
            return str(dice_chosen), (numb_chosen)

        else:
            return tuple(["", 0])

        pass

    def reset_leg(self):
        '''Ensures that all dice colors are returned to the pyramid
        '''
        self.DIE_VALUES = [1,2,3]
        self.DIE_COLORS = list(self.STYLES.keys()).copy()
        self.remaining_dice = list(self.STYLES.keys()).copy()

        pass

    def __str__(self):
        dice_str="Remaining dice: "
        for die in self.remaining_dice:
            dice_str+=self.STYLES[die[0]]+die[0]+Style.RESET_ALL+" "
        return dice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    pyramid = Pyramid(STYLES)
    print(pyramid)
    num_rolls=3
    for _ in range(num_rolls):
        rolled_die = pyramid.shake()
        print(f"{rolled_die} was shaken from the pyramid")
    print(pyramid)
