import numpy as np
import abc
import util
from enum import Enum


class Agent:
    def __init__(self):
        pass
    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        # print("**********************************")
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best
        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score
        if board[0][0] == max_tile:
            score += max_tile
            i = 1
            prev = board[0][0]
            while i < len(board[0]) and board[0][i] <= prev:
                score += board[0][i]
                prev = board[0][i]
                i+=1

        num_zeros = (board == 0).sum()
        score += num_zeros

        # if action == Action.LEFT:
        #     score += 10
        # if action == Action.DOWN:
        #     score = 0

        return score


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def helper(self, game_state, depth, turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if not legal_moves or depth == 0:
            return self.evaluation_function(game_state), None

        if turn % 2 == 0:
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score > max_score:
                    max_score = score
                    best_action = action
            return max_score, best_action
        else:
            min_score = float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score < min_score:
                    min_score = score
                    best_action = action
            return min_score, best_action

        # print(legal_moves)
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        """*** YOUR CODE HERE ***"""
        action =  self.helper(game_state, self.depth * 2)[1]
        # print(action)
        return action
        # util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def helper(self, game_state, depth, alpha=-float('inf'), beta=float('inf'), turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if not legal_moves or depth == 0:
            return self.evaluation_function(game_state), None

        if turn % 2 == 0:
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth - 1, alpha, beta, turn + 1)
                if score > max_score:
                    max_score = score
                    best_action = action
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_action
        else:
            min_score = float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth -1, alpha, beta, turn + 1)
                if score < min_score:
                    min_score = score
                    best_action = action
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_action

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        action =  self.helper(game_state, self.depth*2)[1]
        return action



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """
    def helper(self, game_state, depth, turn=0):
        legal_moves = game_state.get_legal_actions(turn % 2)
        if not legal_moves or depth == 0 :
            return self.evaluation_function(game_state) , None

        if turn % 2 == 0:  # Maximizing player
            max_score = -float('inf')
            best_action = None
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth - 1, turn + 1)
                if score > max_score:
                    max_score = score
                    best_action = action
            return max_score, best_action
        else:
            total_score = 0
            probability = 1 / len(legal_moves)
            for action in legal_moves:
                successor = game_state.generate_successor(turn % 2, action)
                score, _ = self.helper(successor, depth -1, turn + 1)
                total_score += probability * score
            return total_score, None

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        action =  self.helper(game_state, self.depth*2)[1]
        return action




def better_evaluation_function(game_state):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current GameState and returns a number, where higher numbers are better.
    """


    empty_cells_weight =0.1
    score_weight = 1.1
    smoothness_weight = -1.06
    corner_weight = 0.5

    empty_cells = (game_state.board == 0).sum()
    score = game_state.score
    smoothness = get_smoothness(game_state)
    corner_score = get_corner_score(game_state)
    evaluation = (
                    empty_cells_weight * empty_cells +
                   score_weight * score+
                  smoothness_weight * smoothness +
                  corner_weight * corner_score)
    return   evaluation

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
better = better_evaluation_function
