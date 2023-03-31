class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Controller(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}

    def reset_score(self) -> None:
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}


game_controller = Controller()
