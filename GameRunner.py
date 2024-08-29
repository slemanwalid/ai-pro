import argparse
import numpy
import os

import Heuristics
import graphics_display
import multiagents
from game import Game
from Gamestate import GameState

# from graphics_display import GabrieleCirulli2048GraphicsDisplay
# from keyboard_agent import KeyboardAgent

NUM_OF_INITIAL_TILES = 2
class KeyboardAgent(multiagents.Agent):
    """
    An agent controlled by the keyboard.
    """
    LEFT_KEY = 'a'
    RIGHT_KEY = 'd'
    UP_KEY = 'w'
    DOWN_KEY = 's'

    def __init__(self, tk_window):
        super().__init__()
        self.keys = []
        tk_window.subscribe_to_mouse_click(self.listener)
        self.tk_window = tk_window
        self._should_stop = False
        self._move = None
    def get_action(self, state):
        self._should_stop = False
        move = self._move
        while move is None and not self._should_stop:
            self.tk_window.mainloop_iteration()
            move = self._move
        self._move = None
        return move

    def stop_running(self):
        self._should_stop = True


    def listener(self, tk_event=None, *args, **kw):
        col = tk_event.x//100
        print(col, tk_event.x)
        self._move = col


class GameRunner(object):
    def __init__(self, display=None, agent1=None,agent2=None,
                 sleep_between_actions=False):
        super(GameRunner, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.human_agent = agent1 is None

        if display is None:
            display = graphics_display.GabrieleCirulli2048GraphicsDisplay(self.new_game, self.quit_game, self.human_agent)

        if agent1 is None:
            agent1 = KeyboardAgent(display)
        if agent2 is None:
            agent2= KeyboardAgent(display)
        self.display = display
        self._agent1 = agent1
        self._agent2 = agent2
        self.current_game = None

    def new_game(self, initial_state=None, *args, **kw):
        self.quit_game()
        if initial_state is None:
            initial_state = GameState()
        game = Game(self._agent1, self._agent2, self.display, sleep_between_actions=self.sleep_between_actions)
        self.current_game = game
        return game.run(initial_state)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(agent_name, evaluation_function, depth):
    agent = {
        "MinmaxAgent":multiagents.MinmaxAgent,
        "ExpectimaxAgent":multiagents.ExpectimaxAgent,
        "AlphaBetaAgent":multiagents.AlphaBetaAgent,
    }
    agent_name = agent[agent_name](depth=depth, evaluation_function=Heuristics.evaluation_function)
    return agent_name


def main():
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'ReflexAgent', 'MinmaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default="GUI", type=str)
    parser.add_argument('--agent1', choices=agents, help='The agent.', default='KeyboardAgent', type=str)
    parser.add_argument('--agent2', choices=agents, help='The agent.', default='MinmaxAgent', type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='better', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    # if args.display != displays[0]:
    #     display = util.lookup('displays.' + args.display, globals())()
    # else:
    #     display = None
    #
    display = None
    if args.agent1 != agents[0]:
        agent1 = create_agent(args.agent1,args.evaluation_function,args.depth)
    else:
        agent1 = None
    if args.agent2 != agents[0]:
        agent2 = create_agent(args.agent2,args.evaluation_function,args.depth)

    else:
        agent2 = None
    game_runner = GameRunner(display=display, agent1=agent1,agent2=agent2,
                             sleep_between_actions=args.sleep_between_actions)
    # scores = []
    for i in range(args.num_of_games):
        score = game_runner.new_game(initial_state=None)
        # scores.append(score)
    if display is not None:
        display.print_stats()
    # return scores

if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
