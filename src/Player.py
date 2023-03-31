"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Player.
"""
from typing import TypeVar

import settings
from src.GameEntity import GameEntity
from src.states.entities import player_states
from src.GameObject import GameObject

class Player(GameEntity):
    def __init__(self, x: int, y: int, game_level: TypeVar("GameLevel")) -> None:
        super().__init__(
            x,
            y,
            16,
            20,
            "martian",
            game_level,
            states={
                "idle": lambda sm: player_states.IdleState(self, sm),
                "walk": lambda sm: player_states.WalkState(self, sm),
                "jump": lambda sm: player_states.JumpState(self, sm),
                "fall": lambda sm: player_states.FallState(self, sm),
            },
            animation_defs={
                "idle": {"frames": [0]},
                "walk": {"frames": [9, 10], "interval": 0.15},
                "jump": {"frames": [2]},
            },
        )

    def handle_tilemap_collision_on_top(self) -> bool:
        collision_rect = self.get_collision_rect()

        # Row for the center of the player
        i = self.tilemap.to_i(collision_rect.centery)

        # Left and right columns
        left = self.tilemap.to_j(collision_rect.left)
        right = self.tilemap.to_j(collision_rect.right)

        collide_left = self.tilemap.collides_tile_on(i - 1, left, self, GameObject.BOTTOM)

        collide_right = self.tilemap.collides_tile_on(i - 1, right, self, GameObject.BOTTOM)

        if collide_left or collide_right:
            # Fix the entity position
            self.y = self.tilemap.to_y(i)

            # Check collision with key spawner
            if collide_left:
                ci, cj, clayer = collide_left
                tile = clayer[ci][cj]
                
                if tile.frame_index == settings.KEY_SPAWNER_FRAME_INDEX:
                    self.game_level.add_item({
                        "item_name": "keys",
                        "frame_index": 68,
                        "x": tile.x,
                        "y": tile.y - 16,
                        "width": 16,
                        "height": 16,
                    })
        
            return True

        return False
