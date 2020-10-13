##################################################
# FILE : board.py
# AUTHORS : Yuval Padan , yuvalpadan , 313580912
#           Ran Inbar   , ran.inbar  , 313542409
# EXERCISE : Final project - "Four in a row" game
##################################################

# Constants
ROWS = 6
COLUMNS = 7
FREE_SPACE = "*"
FOUR_IN_A_ROW = 4


class Board:
    """Class representing the board of connect 4 game"""

    def __init__(self):
        """Instructor of Board object"""
        self._board = self.create_board()

    def get_board(self):
        """returns the board"""
        return self._board

    def create_board(self):
        """returns a new board (a list of lists) according to constants-
        ROWS, COLUMNS"""
        board = []
        for i in range(ROWS):
            row = []
            for j in range(COLUMNS):
                row.append(FREE_SPACE)
            board.append(row)
        return board

    def add_disk(self, column, player):
        """receives a column and a player and adds a player (1/0) to column"""
        for row in range(ROWS - 1, -1, -1):
            if self._board[row][column] == FREE_SPACE:
                self._board[row][column] = player
                break

    def is_free(self, column):
        """receives a column and returns True if it's free. Otherwise,
        return False. If something went wrong during the process an exception
        is raised."""
        if column > COLUMNS - 1 or column < 0:
            raise Exception
        if self._board[0][column] != FREE_SPACE:
            return False
        return True

    def board_is_full(self):
        """returns True if board is full. Otherwise, return False"""
        for row in self._board:
            if not row.count(FREE_SPACE):
                continue
            return False
        return True

    def is_four_in_a_row(self):
        """checks if there is a winning sequence of four in a row. if a
        sequence was found, the method returns True, a list of the sequence
        coordinates of the original board and the winning player. Otherwise,
        returns False, None"""
        horizontal_check = self.main_check(self._board)
        if horizontal_check[0]:
            return True, self.convert_i_horizontal(horizontal_check[1]), \
                   horizontal_check[2]

        vertical_check = self.main_check(self.board_down())
        if vertical_check[0]:
            return True, self.convert_i_vertical(vertical_check[1]), \
                   vertical_check[2]

        down_left_check = self.main_check(self.board_down_left())
        if down_left_check[0]:
            return True, self.convert_i_down_left(down_left_check[1]), \
                   down_left_check[2]

        right_left_check = self.main_check(self.board_right_left())
        if right_left_check[0]:
            return True, self.convert_i_right_left(right_left_check[1]), \
                   right_left_check[2]

        return False, None

    def convert_i_down_left(self, down_left_check):
        """receives a coordinate of the last disc in the winning sequence in
        down-left board and returns a list of the winning sequence coordinates
        which will match the original board"""

        # the following numbers in this method mustn't change and they might
        # not work perfectly for a different-sized board.

        row_i, col_i = down_left_check
        nex_x, nex_y = None, None
        if 0 <= row_i <= FOUR_IN_A_ROW - 1:
            nex_x, nex_y = col_i, FOUR_IN_A_ROW - (col_i - row_i) - 1
        if row_i == FOUR_IN_A_ROW and col_i == FOUR_IN_A_ROW - 1:
            nex_x, nex_y = (4, 3)
        if row_i == FOUR_IN_A_ROW and col_i == FOUR_IN_A_ROW:
            nex_x, nex_y = (5, 2)
        if row_i == FOUR_IN_A_ROW + 1 and col_i == FOUR_IN_A_ROW - 1:
            nex_x, nex_y = (row_i, col_i)
        return [(nex_x, nex_y), (nex_x - 1, nex_y + 1),
                (nex_x - 2, nex_y + 2),
                (nex_x - 3, nex_y + 3)]

    def convert_i_right_left(self, right_left_check):
        """receives a coordinate of the last disc in the winning sequence in
        right-left board and returns a list of the winning sequence coordinates
        which will match the original board"""

        # the following numbers in this method mustn't change and they might
        # not work perfectly for a different-sized board.

        row_i, col_i = right_left_check
        nex_x, nex_y = None, None
        if 0 <= row_i <= FOUR_IN_A_ROW - 2:
            nex_x, nex_y = FOUR_IN_A_ROW - (col_i - row_i) - 1, \
                           FOUR_IN_A_ROW + 2 - col_i
        if row_i == FOUR_IN_A_ROW - 1:
            nex_x = FOUR_IN_A_ROW - 2 - (col_i - row_i)
            nex_y = nex_x
        if row_i == FOUR_IN_A_ROW and col_i == FOUR_IN_A_ROW - 1:
            nex_x, nex_y = (2, 1)
        if row_i == FOUR_IN_A_ROW and col_i == FOUR_IN_A_ROW:
            nex_x, nex_y = (1, 0)
        if row_i == FOUR_IN_A_ROW + 1 and col_i == FOUR_IN_A_ROW - 1:
            nex_x, nex_y = (2, 0)
        return [(nex_x, nex_y), (nex_x + 1, nex_y + 1),
                (nex_x + 2, nex_y + 2),
                (nex_x + 3, nex_y + 3)]

    def convert_i_horizontal(self, horizontel_check):
        """receives a coordinate of the last disc in the winning and returns a
        list of the winning sequence coordinates"""
        row_i, col_i = horizontel_check
        return [(row_i, col_i), (row_i, col_i - 1), (row_i, col_i - 2),
                (row_i, col_i - 3)]

    def convert_i_vertical(self, vertical_check):
        """receives a coordinate of the last disc in the winning sequence in
        vertical board and returns a list of the winning sequence coordinates
        which will match the original board"""
        row_i, col_i = vertical_check
        return [(col_i, row_i), (col_i - 1, row_i), (col_i - 2, row_i),
                (col_i - 3, row_i)]

    def main_check(self, board):
        """this is the main check of four in a row. This method receives a
        converted board and check's it's rows for a winning sequence. if a
        sequence was found, it returns True, a tuple of coordinates (of the
        converted board) and the winning disc (1/0). Otherwise, returns
        False, None, None"""
        for i, row in enumerate(board):
            counter = 1
            for j in range(len(row) - 1):
                if board[i][j] == FREE_SPACE:
                    continue
                if board[i][j] == board[i][j + 1]:
                    counter += 1
                else:
                    counter = 1
                if counter == FOUR_IN_A_ROW:
                    return True, (i, j + 1), board[i][j + 1]
        return False, None, None

    def board_down(self):
        """returns a converted board - columns become rows"""
        new_board = []
        for i in range(len(self._board[0])):
            new_row = []
            for g in range(len(self._board)):
                new_row.append(self._board[g][i])
            new_board.append(new_row)
        return new_board

    def board_down_left(self):
        """returns a converted board - down-left diagonals become rows.
        Diagonals that their length is less than FOUR_IN_A_ROW are ignored"""
        max_diagonal_length = len(self._board[0]) + len(
            self._board) - FOUR_IN_A_ROW
        new_board = []
        for diagonal_size in range(FOUR_IN_A_ROW - 1, max_diagonal_length):
            new_row = []
            for i in range(len(self._board)):
                j = diagonal_size - i
                if len(self._board[0]) > j >= 0:
                    new_row.append(self._board[i][j])
            new_board.append(new_row)
        return new_board

    def board_right_left(self):
        """returns a converted board - right-left diagonals become rows.
        Diagonals that their length is less than FOUR_IN_A_ROW are ignored"""
        new_board = []
        for i in range(FOUR_IN_A_ROW - 1, len(self._board)):
            t, k, new_row = i, len(self._board[0]) - 1, []
            while k >= 0 and t >= 0:
                new_row.append(self._board[t][k])
                k, t = k - 1, t - 1
            new_board.append(new_row)
        for i in range(len(self._board[0]) - 2, FOUR_IN_A_ROW - 2, -1):
            t, k, new_row = i, len(self._board) - 1, []
            while t >= 0:
                new_row.append(self._board[k][t])
                k, t = k - 1, t - 1
            new_board.append(new_row)
        return new_board
