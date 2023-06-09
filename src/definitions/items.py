"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for items.
"""
from typing import Dict, Any

import random

from gale.timer import Timer

import settings
from src.GameItem import GameItem
from src.Player import Player
from src.Camera import Camera
from src.Controller import game_controller


def pickup_coin(
    coin: GameItem, player: Player, points: int, color: int, time: float
) -> None:
    settings.SOUNDS["pickup_coin"].stop()
    settings.SOUNDS["pickup_coin"].play()
    game_controller.add_score(points, color)
    Timer.after(time, lambda: coin.respawn())


def pickup_green_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 1, 62, random.uniform(2, 4))


def pickup_blue_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 5, 61, random.uniform(5, 8))


def pickup_red_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 20, 55, random.uniform(10, 18))


def pickup_yellow_coin(coin: GameItem, player: Player):
    pickup_coin(coin, player, 50, 54, random.uniform(20, 25))


def pickup_key(key: GameItem, player: Player):
    # Go to next level
    game_controller.go_next_level(player)
   

ITEMS: Dict[str, Dict[int, Dict[str, Any]]] = {
    "coins": {
        62: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_green_coin,
        },
        61: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_blue_coin,
        },
        55: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_red_coin,
        },
        54: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": True,
            "collidable": True,
            "on_consume": pickup_yellow_coin,
        },
    },
    "keys": {
        68: {
            "texture_id": "tiles",
            "solidness": dict(top=False, right=False, bottom=False, left=False),
            "consumable": False,
            "collidable": False,
            "on_consume": pickup_key,
        }
    }
}
