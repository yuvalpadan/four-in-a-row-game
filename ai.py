##################################################
# FILE : ai.py
# AUTHORS : Yuval Padan , yuvalpadan , 313580912
#           Ran Inbar   , ran.inbar  , 313542409
# EXERCISE : Final project - "Four In A Row" game
##################################################

from random import choice
import game as g

ILLEGAL_AI_MOVE = "No possible AI moves."


class AI:
    """Class representing moves by a computer"""

    def __init__(self):
        pass

    def find_legal_move(self, game, func, timeout=None):
        """
        Recieves a Game object that describes the game's logic and checks
        for a legal move. If a legal move has been found the method activates
        "func", as a second-order function, on the move that was found.
        Otherwise, it raises an exception.
        """
        columns_list = list(range(g.COLUMNS))
        while columns_list:
            column = choice(columns_list)
            if game.get_board_object().is_free(column):
                func(column)
                return column
            else:
                columns_list.remove(column)
        raise Exception(ILLEGAL_AI_MOVE)
