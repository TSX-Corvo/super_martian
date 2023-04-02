import pygame
from typing import Dict, Any
from gale.timer import Timer

import settings
from src.Player import Player
from src.Veil import Veil

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
        self.scoregoal = 5
        self.level: int = 1
        self.play_state: Any = None
        self.timers = []

    def reset_score(self) -> None:
        self.score = 0
        self.coins_counter = {54: 0, 55: 0, 61: 0, 62: 0}

    def add_score(self, value: int, color: int, amount: int = 1) -> None:
        self.score += value
        self.coins_counter[color] += amount
        if self.score >= self.scoregoal:
            # Level cleared

            # Stop countdown
            self.timers = Timer.items
            Timer.clear()

            # Make goal visible and collidable
            layers = self.play_state.game_level.tilemap.layers
            spawner = list(filter(lambda tile: tile.frame_index == settings.KEY_SPAWNER_FRAME_INDEX, 
                [item for sublist in layers[-1] for item in sublist]
            ))

            if not spawner:
                return

            spawner[0].solidness = {k: True for k in spawner[0].solidness.keys()}
            spawner[0].visible = True

            # Make remaining items not collidable
            for item in self.play_state.game_level.items:
                item.collidable = False
                item.consumable = False

            settings.SOUNDS["level_clear"].play()

    def get_score_goal(self, level: int) -> int:
        return level * 50

    def go_next_level(self, player: Player) -> None:
        
        self.play_state.state_machine.change(
            "transition", 
            level=self.level,
            game_level=self.play_state.game_level,
            camera=self.play_state.camera,
        )

      

game_controller = Controller()
