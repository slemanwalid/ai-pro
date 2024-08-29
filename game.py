import abc
from collections import namedtuple
from enum import Enum

import numpy as np
import time


class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5


OpponentAction = namedtuple('OpponentAction', ['row', 'column', 'value'])






class Game(object):
    def __init__(self, agent, opponent_agent, display, sleep_between_actions=False):
        super(Game, self).__init__()
        self.sleep_between_actions = sleep_between_actions
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = None
        self._should_quit = False

    def run(self, initial_state):
        self._should_quit = False
        self._state = initial_state
        self.display.initialize(initial_state)
        return self._game_loop()

    def quit(self):
        self._should_quit = True
        self.agent.stop_running()
        self.opponent_agent.stop_running()

    def _game_loop(self):
        #TODO : connect X button to game.quit()
        while not self._state.done and not self._should_quit:
            if self.sleep_between_actions:
                time.sleep(1)

            self.display.mainloop_iteration()

            action = self.agent.get_action(self._state)
            cor1 = self._state.move(action, 1)
            self.display.update_state(cor1, 1)

            # self.display.mainloop_iteration()
            opponent_action = self.opponent_agent.get_action(self._state)
            cor2 = self._state.move(opponent_action, 2)
            self.display.update_state(cor2, 2)
        # return self._state.score, self._state.max_tile
