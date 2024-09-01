import argparse

import numpy
import os

import Heuristics
from Displays.SummaryDisplay import SummaryDisplay
from Displays.GUIDisplay import FourInARow
from Agents.AlphaBetaAgent import  AlphaBetaAgent
from Agents.KeyboardAgent import  KeyboardAgent
from Agents.ExpictimaxAgent import ExpectimaxAgent
from Agents.MinmaxAgent import MinmaxAgent
from  GameRunner import GameRunner






def create_display(display_name):
    if display_name == "GUI":
        return FourInARow()
    elif display_name == "SummaryDisplay":
        return SummaryDisplay()
    raise Exception("Invalid summary display type.")

def create_agent(agent_name,player , evaluation_function, depth, display):
    if agent_name == "MinmaxAgent":
        return MinmaxAgent(depth=depth, evaluation_function=Heuristics.easy_evaluation_function, player=player)
    elif agent_name == "ExpictimaxAgent":
        return ExpectimaxAgent(depth=depth, evaluation_function=Heuristics.easy_evaluation_function, player=player)
    elif agent_name == "AlphaBetaAgent":
        return AlphaBetaAgent(depth=depth, evaluation_function=Heuristics.easy_evaluation_function, player=player)
    elif agent_name == "KeyboardAgent":
        return KeyboardAgent(display)
    raise Exception("Invalid agent name.")


def main():
    parser = argparse.ArgumentParser(description='2048 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.', default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'ReflexAgent', 'MinmaxAgent', 'AlphaBetaAgent', 'ExpectimaxAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default="GUI", type=str)
    parser.add_argument('--agent1', choices=agents, help='The agent.', default='MinmaxAgent', type=str)
    parser.add_argument('--agent2', choices=agents, help='The agent.', default='MinmaxAgent'
                                                                               , type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2, type=int)
    parser.add_argument('--sleep_between_actions', help='Should sleep between actions.', default=False, type=bool)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--evaluation_function', help='The evaluation function for ai agent.',
                        default='better', type=str)
    args = parser.parse_args()
    numpy.random.seed(args.random_seed)
    display = create_display(args.display)
    agent1 = create_agent(args.agent1,1,args.evaluation_function,args.depth,display)
    agent2 = create_agent(args.agent2,2,args.evaluation_function,args.depth, display)

    game_runner = GameRunner(display=display, agent1=agent1,agent2=agent2,
                             sleep_between_actions=args.sleep_between_actions)
    for i in range(args.num_of_games):
        score = game_runner.new_game(initial_state=None)
    # if display is not None:
    #     display.print_stats()
    # return scores

if __name__ == '__main__':
    main()
    input("Press Enter to continue...")
