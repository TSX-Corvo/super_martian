from typing import Dict, Any
import settings

from gale.timer import Timer

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
        self.score: int = 0
        self.coins_counter: Dict[int, int] = {54: 0, 55: 0, 61: 0, 62: 0}
        self.scoregoal = 1
        self.level: int = 1
        self.play_state: Any = None

    def reset_score(self) -> None:
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}

    def add_score(self, value: int, color: int, amount: int = 1) -> None:
        self.score += value
        self.coins_counter[color] += amount
        if self.score >= self.scoregoal:
            # Level cleared
            Timer.clear()
            layers = self.play_state.game_level.tilemap.layers
            spawner = list(filter(lambda tile: tile.frame_index == settings.KEY_SPAWNER_FRAME_INDEX, 
                [item for sublist in layers[-1] for item in sublist]
            ))

            if not spawner:
                return

            spawner[0].solidness = {k: True for k in spawner[0].solidness.keys()}
            spawner[0].visible = True

    def go_next_level(self, player: Player) -> None:
        # Update current state
        self.level += 1
        gamelevel = player.game_level
        gamelevel.change_level(self.level)
        self.scoregoal = self.level * 5
        
        # Update player state
        player.tilemap = gamelevel.tilemap
        player.x = 0
        player.y = settings.VIRTUAL_HEIGHT - 66

        # Update play state
        self.play_state.timer = 30

game_controller = Controller()
