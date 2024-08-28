import argparse
import numpy
import os
import util
from game import Game, RandomOpponentAgent
from Gamestate import GameState
# from graphics_display import GabrieleCirulli2048GraphicsDisplay
# from keyboard_agent import KeyboardAgent

NUM_OF_INITIAL_TILES = 2


class GameRunner(object):
    def __init__(self, display=None, agent1=None,agent2=None,
                 sleep_between_actions=False):
        super(GameRunner, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        # if display is None:
        #     display = GabrieleCirulli2048GraphicsDisplay(self.new_game, self.quit_game, self.human_agent)

        # if agent is None:
        #     agent = KeyboardAgent(display)

        self.display = display
        self._agent1 = agent1
        self._agent2 = agent2
        self.current_game = None

    def new_game(self, initial_state=None, *args, **kw):
        self.quit_game()
        if initial_state is None:
            initial_state = GameState()
        opponent_agent = RandomOpponentAgent()
        game = Game(self._agent, opponent_agent, self.display, sleep_between_actions=self.sleep_between_actions)
        for i in range(self.num_of_initial_tiles):
            initial_state.apply_opponent_action(opponent_agent.get_action(initial_state))
        self.current_game = game
        return game.run(initial_state)

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


def create_agent(agent,evaluation_function,depth):
    agent = util.lookup('multi_agents.' + agent, globals())(depth=depth,
                                                                 evaluation_function=evaluation_function)
    return agent


def main():
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'ReflexAgent', 'MinmaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default="GUI", type=str)
    parser.add_argument('--agent', choices=agents, help='The agent.', default='KeyboardAgent', type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--num_of_initial_tiles', help='The number non empty tiles when the game started.', default=2,
                        type=int)
    parser.add_argument('--initial_board', help='Initial board for new games.', default=None, type=str)
    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='better', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    if args.display != displays[0]:
        display = util.lookup('displays.' + args.display, globals())()
    else:
        display = None

    agent1 = create_agent(args.agent1,args.evaluation_function,args.depth)
    agent2 = create_agent(args.agent2,args.evaluation_function,args.depth)

    initial_state = None
    if args.initial_board is not None:
        with open(os.path.join('layouts', args.initial_board), 'r') as f:
            lines = f.readlines()
            initial_board = numpy.array([list(map(lambda x: int(x), line.split(','))) for line in lines])
            initial_state = GameState(board=initial_board)
    game_runner = GameRunner(display=display, agent1=agent1,agent2=agent2,
                             sleep_between_actions=args.sleep_between_actions)
    # scores = []
    for i in range(args.num_of_games):
        score = game_runner.new_game(initial_state=initial_state)
        # scores.append(score)
    if display is not None:
        display.print_stats()
    # return scores

if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
