import numpy as np


def evaluate_depth(board, player):
    """
    Evaluate the board based on the depth of pieces.

    Parameters:
    - board: 2D list representing the Connect Four board
    - player: int (1 for AI player, -1 for opponent)

    Returns:
    - int: The score based on depth
    """
    score = 0
    opponent_player = 1 if player == 2 else 2
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row, col] == player:
                # Deeper rows (closer to the bottom) are more valuable
                # Assign a higher score to lower rows
                score += (len(board) - row)
            elif board[row, col] == opponent_player:
                # Penalize for opponent's pieces in the same way
                score -= (len(board) - row)
    return score


def evaluate_center_control(board, player):
    """
    Evaluate the board based on control of the center columns.

    Parameters:
    - board: 2D list representing the Connect Four board
    - player: int (1 for AI player, -1 for opponent)

    Returns:
    - int: The score based on center control
    """
    score = 0
    center_column = (board.shape[1]) // 2
    opponent_player = 1 if player == 2 else 2

    for row in range(board.shape[0]):
        if board[row, center_column] == player:
            score += 3  # Assign higher score for controlling the center column
        elif board[row, center_column] == opponent_player:
            score -= 3  # Penalize for opponent's control

    return score
def evaluate_four_connected(game_state, player):
    """
    four connected -> inf
    three connected with open end -> high score
    two connected with two open ends -> medium score
    one connected with mulltiple open spaces -> low score
    :param game_state:
    :param player:
    :return:
    """
    pass
def evaluate_opponent_moves(game_state, player):
    """
    -1 * evaluate_four_connected(game_state, opponent_player)
    :param game_state:
    :param opponent_player:
    :return:
    """
    pass
def evaluation_function_1(game_state, player):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """
    

    depth = evaluate_depth(game_state.board, player)
    center_control = evaluate_center_control(game_state.board, player)

    depth_weight = 0.5
    center_control_weight = 1.5

    return depth * depth_weight + center_control * center_control_weight


easy_evaluation_function = evaluation_function_1
medium_evaluation_function = None
hard_evaluation_function = None
