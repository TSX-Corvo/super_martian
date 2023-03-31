import settings

from src.Player import Player

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
        self.level = 1

    def reset_score(self) -> None:
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}

    def go_next_level(self, player: Player) -> None:
        # Update current state
        self.level += 1
        gamelevel = player.game_level
        gamelevel.change_level(self.level)
        
        # Update player state
        player.tilemap = gamelevel.tilemap
        player.x = 0
        player.y = settings.VIRTUAL_HEIGHT - 66

game_controller = Controller()
