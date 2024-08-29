import numpy as np

DEFAULT_COLUMNS = 7
DEFAULT_ROWS = 6
DEFAULT_BOARD_SIZE = 6


class GameState:
    def __init__(self, rows=DEFAULT_ROWS, columns=DEFAULT_COLUMNS, board=None, done=False):
        self.__player = 0
        if  board is None:
            board = np.zeros((rows, columns))
        self.__board = board
        self.__turn = 0
        self.__done = done
        self.__rows = rows
        self.__cols = columns
        self.__last_added = [rows] * columns

    @property
    def done(self):
        """
        :return:
        """
        return self.__done

    @property
    def _is_full(self):
        return sum(self.__last_added) == 0

    @property
    def board(self):
        return self.__board

    def get_legal_actions(self, agent_index):
        return [col for col in range(len(self.__last_added)) if self.__last_added[col] != 0]

    def move(self, col,turn):
        row = self.__last_added[col] - 1
        # TODO: check invalid human case
        self.__board[row][col] = turn
        if self.check_win((row,col)):
            self.__done = True
            return row, col
        if self._is_full:
            self.__done = True
            return row, col
        self.__last_added[col] -= 1
        return row, col

    def generate_successor(self, col, turn):
        successor = GameState(rows=self.__rows, columns=self.__cols, board=self.__board.copy(),
                               done=self.__done)
        successor.move(col, turn)
        return successor

    def check_win(self, cor):
        """
        this function checks checks if there are four squares that have the same disc
        :return: True if there are four squares that have the same disc, False if there aren't
        """
        (row, col) = cor
        directions = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, -1)]
        for ind1, ind2 in directions:
            if self.valid_coordinate((row + 3 * ind1, col + 3 * ind2)):
                if self.__board[row, col] == self.__board[row + ind1, col + ind2] == \
                        self.__board[row + 2 * ind1, col + 2 * ind2] == self.__board[row + 3 * ind1, col + 3 * ind2]:
                    return True
        return False

    def valid_coordinate(self, cor):
        (row, col) = cor
        if (0 <= col <= self.__board.shape[1] - 1) and (0 <= row <= self.__board.shape[0] - 1):
            return True

        return False
