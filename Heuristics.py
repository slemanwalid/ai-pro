import numpy as np


def evaluate_depth(board,last_added, player):
    """
    Evaluate the board based on the depth of pieces.

    Parameters:
    - board: 2D list representing the Connect Four board
    - player: int (1 for AI player, -1 for opponent)

    Returns:
    - int: The score based on depth
    """
    # print(last_added)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(board)
    col_weights = [1,2,4,8,4,2,1]
    score = 0
    # opponent_player = 1 if player == 2 else 2
    # for row in range(board.shape[0]):
    #     for col in range(board.shape[1]):
    #         if board[row, col] == player:
    #             # Deeper rows (closer to the bottom) are more valuable
    #             # Assign a higher score to lower rows
    #             score += row * col_weights[col]
    #         elif board[row, col] == opponent_player:
    #             # Penalize for opponent's pieces in the same way
    #             score -= row * col_weights[col]
    # return score

    for col in range(len(last_added)):
        score += (6-last_added[col])*col_weights[col]
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
    
    def check_sequences(board, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # vertical, horizontal, diagonal down-right, diagonal down-left
        counts = {2: 0, 3: 0, 4: 0}  # Counts for the given player

        def count_in_direction(row, col, d_row, d_col):
            count = 0
            r, c = row, col
            # Check in one direction
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r += d_row
                c += d_col

            r, c = row - d_row, col - d_col
            # Check in the opposite direction
            while 0 <= r < board.shape[0] and 0 <= c < board.shape[1] and board[r, c] == player:
                count += 1
                r -= d_row
                c -= d_col

            return count

        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] == player:  # Only check spots occupied by the player
                    for d_row, d_col in directions:
                        sequence_length = count_in_direction(row, col, d_row, d_col)
                        for seq in [2, 3, 4]:
                            if sequence_length == seq:
                                counts[seq] += 1

        return counts

    score = check_sequences(game_state.board,player)
    # print(game_state.board)
    # print("------------------------")
    # print("######",score)
    if score[4] != 0:
        print("helllooooooo")
        return float("inf")
    return score[2] + score[3]*10 
    
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
    

    depth = evaluate_depth(game_state.board,game_state.last_added, player)
    center_control = evaluate_center_control(game_state.board, player)

    depth_weight = 0.5
    center_control_weight = 1.5


    return evaluate_four_connected(game_state,player) + 10 * depth


easy_evaluation_function = evaluation_function_1
medium_evaluation_function = None
hard_evaluation_function = None
