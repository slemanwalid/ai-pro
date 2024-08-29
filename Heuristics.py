
import numpy as np
def evaluation_function(game_state):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """
    board = game_state.board


    return   np.count_nonzero(board)

def get_smoothness(game_state):
    """
    Calculate the smoothness of the board.
    Smoothness measures how similar adjacent tiles are in value.
    """
    board = game_state.board

    row_diff = np.abs(board[:, :-1] - board[:, 1:])
    col_diff = np.abs(board[:-1, :] - board[1:, :])

    diff = np.sum(row_diff) + np.sum(col_diff)

    return diff


def get_corner_score(game_state):
    """
    Calculate a score based on the values in the corners.
    """
    board = game_state.board
    # return np.sum(board[0, :] )+ np.sum(board[:, -1]) + np.sum(board[-1, :]) + np.sum(board[:, 0])
    return board[0,0] + board[0,-1] + board[-1,0] + board[-1,-1]
# Abbreviation
heuristic = evaluation_function
