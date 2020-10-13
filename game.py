##################################################
# FILE : game.py
# AUTHORS : Yuval Padan , yuvalpadan , 313580912
#           Ran Inbar   , ran.inbar  , 313542409
# EXERCISE : Final project - "Four In A Row" game
##################################################

from board import Board
import board

ILLEGAL_MOVE_EXCEPTION = "Illegal move."
COLUMNS = board.COLUMNS
ROWS = board.ROWS


class Game:
    """Class representing a game of connect-4"""

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2

    def __init__(self):
        """Instructor of Game object"""
        self._board = Board()
        self._cur_player = Game.PLAYER_ONE

    def make_move(self, column):
        """receives a column and adds a player (1/0) in this column in the
        game's board. If something went wrong during the process an exception
        is raised."""
        if self._board.is_free(column):
            if self.get_current_player() == Game.PLAYER_ONE:
                self._board.add_disk(column, Game.PLAYER_ONE)
                self._cur_player = Game.PLAYER_TWO
            else:
                self._board.add_disk(column, Game.PLAYER_TWO)
                self._cur_player = Game.PLAYER_ONE
        else:
            raise Exception(ILLEGAL_MOVE_EXCEPTION)

    def get_winner(self):
        """this method checks for the game status. if there is winner,
        it returns the player and the a list of coordinates of the winning
        sequence. If it's a draw. it return a Draw, None. Otherwise, returns
        None, None"""
        status = self._board.is_four_in_a_row()
        if status[0]:
            if status[2] == Game.PLAYER_ONE:
                return Game.PLAYER_ONE, status[1]
            if status[2] == Game.PLAYER_TWO:
                return Game.PLAYER_TWO, status[1]
        if self._board.board_is_full():
            return Game.DRAW, None
        return None, None

    def get_player_at(self, row, col):
        """receives a row and a columns and returns the shown player in this
        place in the board (1/0)."""
        if self._board.get_board()[row][col] == Game.PLAYER_ONE:
            return Game.PLAYER_ONE
        if self._board.get_board()[row][col] == Game.PLAYER_TWO:
            return Game.PLAYER_TWO
        return None

    def get_current_player(self):
        """returns the player whose his turn"""
        return self._cur_player

    def get_board(self):
        """returns the board of the game (list of lists)"""
        return self._board.get_board()

    def get_board_object(self):
        """returns the board attribute"""
        return self._board

    def set_new_game(self):
        """this method resets the board and sets the first player to be
        PLAYER_ONE"""
        self._board = Board()
        self._cur_player = Game.PLAYER_ONE
