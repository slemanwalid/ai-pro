import abc


class Agent:
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass
