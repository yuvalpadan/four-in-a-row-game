##################################################
# FILE : four_in_a_row.py
# AUTHORS : Yuval Padan , yuvalpadan , 313580912
#           Ran Inbar   , ran.inbar  , 313542409
# EXERCISE : Final project - "Four In A Row" game
##################################################

from tkinter import *
import game
from game import Game
from communicator import Communicator
from ai import AI

# Massages_constants
AI_PLAYER = "ai"
HUMAN_PLAYER = "human"
SERVER_TITLE = "Player One"
CLIENT_TITLE = "Player Two"
ERROR = "This column is full"
ILLEGAL_MOVE_MSG = "Try another column"
ILLEGAL_PROGRAM_MSG = "Illegal program arguments."

# Images_constants
PLAYER_TWO_DISK = "images/red.png"
PLAYER_ONE_DISK = "images/blue.png"
WIN_DISC = "images/win-disc.png"
DRAW_SCREEN = "images/draw.png"
BOARD = "images/board.png"
PLAYER_ONE_TURN = "images/player_1_turn.png"
PLAYER_TWO_TURN = "images/player_2_turn.png"
PLAYER_ONE_WIN_SCREEN = "images/player 1 win.png"
PLAYER_TWO_WIN_SCREEN = "images/player 2 win.png"

# Numbers_constants
BACKGROUND_HEIGHT = 475
BACKGROUND_WIDTH = 637
MAX_PORT = 65535
MIN_PORT = 1000


class FourInARow:
    """Class representing a game of connect-4 with graphics"""

    def __init__(self, parent, player, port, ip=None):
        """Instructor of FourInARow object"""
        self._end_game = False
        self.__init_graphics__()
        self._game = Game()
        self._root = parent
        self._status = None
        self._player = player
        self.__init__ai_or_human()
        self.__init__ip_distinguisher(ip)
        self.__communicator = Communicator(self._root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.__handle_message)

    def __init_graphics__(self):
        """initiates the graphic of the game"""
        self._player1_disc = PhotoImage(file=PLAYER_ONE_DISK)
        self._player2_disc = PhotoImage(file=PLAYER_TWO_DISK)
        self._player1_turn = PhotoImage(file=PLAYER_ONE_TURN)
        self._player2_turn = PhotoImage(file=PLAYER_TWO_TURN)
        self._win_disc = PhotoImage(file=WIN_DISC)
        self._player1_won = PhotoImage(file=PLAYER_ONE_WIN_SCREEN)
        self._player2_won = PhotoImage(file=PLAYER_TWO_WIN_SCREEN)
        self._draw_screen = PhotoImage(file=DRAW_SCREEN)

    def __init__ai_or_human(self):
        """initiates the type of player"""
        if self._player == HUMAN_PLAYER:
            self.__init__new_canvas(BOARD)
            self._canvas.bind("<Button-1>", self.game_screen_callback)
        if self._player == AI_PLAYER:
            self.__init__new_canvas(BOARD)
            self._ai = AI()
            self._root.after(1, self.make_ai_move)

    def __init__ip_distinguisher(self, ip):
        """initiates the player num whether ip is None or not"""
        if ip is not None:
            self._player_num = self._game.PLAYER_TWO
        else:
            self._player_num = self._game.PLAYER_ONE

    def __init__new_canvas(self, img):
        """this method receives an image initiates a new canvas with it."""
        self._background = PhotoImage(file=img)
        self._canvas = Canvas(self._root, height=BACKGROUND_HEIGHT,
                              width=BACKGROUND_WIDTH)
        self._canvas.create_image(3, 3, image=self._background, anchor=NW)
        self._canvas.pack()

    def make_ai_move(self):
        """makes a move for an ai player"""
        if not self._end_game:
            if self._game.get_current_player() == self._player_num:
                col = self._ai.find_legal_move(self._game, self.general_move)
                self.__communicator.send_message(str(col))
            self._root.after(1, self.make_ai_move)

    def __handle_message(self, text=None):
        """this method receives text that represent a column-index and
        operates general_move with this column."""
        if text:
            column = int(text)
            self.general_move(column)

    def game_screen_callback(self, event):
        """the callback method for the game-screen.
        The method receives an event and operates other func whether the
        event was under certain conditions or not"""

        # numbers in this function represent coordinates on the screen only!

        # if self._game.get_current_player() != self._player_num:
        #     return
        x = event.x
        y = event.y
        for col in range(game.COLUMNS):
            if x in range(39 + col * 63, 86 + col * 63) and 26 < y < 447:
                if self.general_move(col):
                    self.__communicator.send_message(str(col))

    def general_move(self, column):
        """this is the general method for making moves in the game.
        It receives a column-index and inserts the current player's disc in
        this column (in the game's board and in the graphic screen as well).
        If something went wrong during the process an exception is raised."""
        self._game.make_move(column)
        row_counter = 0
        for i in range(len(self._game.get_board()) - 1, -1, -1):
            if self._game.get_board()[i][column] == game.board.FREE_SPACE:
                break
            row_counter += 1
        self.add_disc(column, game.ROWS - row_counter)
        return True

    def add_disc(self, col, row):
        """adds a current player's graphic disc to the screen."""

        # numbers in this function represent coordinates on the screen only!

        if self._game.get_current_player() == Game.PLAYER_ONE:
            self._canvas.create_image(64 + 64 * col, 70 + 56.5 * row,
                                      image=self._player1_disc)
            self._canvas.create_image(559, 211, image=self._player1_turn)
        else:
            self._canvas.create_image(64 + 64 * col, 70 + 56.5 * row,
                                      image=self._player2_disc)
            self._canvas.create_image(559, 211, image=self._player2_turn)
        self.game_status()

    def game_status(self):
        """checks for the game status. Whether one of the players won or its a
        draw, and operates other methods according to the status."""
        self._status = self._game.get_winner()
        if self._status[0] in [self._game.PLAYER_ONE, self._game.PLAYER_TWO]:
            self.show_winner(self._status[0], self._status[1])
            self._canvas.bind("<Button-1>", self.exit_game)
            self._end_game = True
        if self._status[0] == self._game.DRAW:
            self._canvas.create_image(3, 3, image=self._draw_screen, anchor=NW)
            self._canvas.bind("<Button-1>", self.exit_game)
            self._end_game = True

    def show_winner(self, winner, win_discs_list):
        """if a winner was found in the game status method, this method
        show's the winner's discs that made a sequence and the winner player
        himself."""

        # numbers in this function represent coordinates on the screen only!

        for disc in win_discs_list:
            row, col = disc
            self._canvas.create_image(64 + 64 * col, 70 + 56.5 * row,
                                      image=self._win_disc)
        if winner == self._game.PLAYER_ONE:
            self._canvas.create_image(3, 3, image=self._player1_won, anchor=NW)
        else:
            self._canvas.create_image(3, 3, image=self._player2_won, anchor=NW)

    def exit_game(self, event):
        """this method ends the game (including graphics)."""
        if event:
            self._root.quit()
            self._root.destroy()


if __name__ == '__main__':
    root = Tk()
    argument = sys.argv
    try:
        if len(argument) in [3, 4] and MIN_PORT <= int(argument[2]) <= \
                MAX_PORT and argument[1] in [HUMAN_PLAYER, AI_PLAYER]:
            if len(argument) == 3:
                FourInARow(root, argument[1], int(argument[2]))
                root.title(SERVER_TITLE)
            else:
                FourInARow(root, argument[1], int(argument[2]),
                           argument[3])
                root.title(CLIENT_TITLE)
            root.mainloop()
        else:
            print(ILLEGAL_PROGRAM_MSG)
    except ValueError:
        print(ILLEGAL_PROGRAM_MSG)
