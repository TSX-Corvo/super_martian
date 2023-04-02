"""
ISPPJ1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PauseState.
"""
from typing import Dict, Any

import pygame

from gale.input_handler import InputHandler, InputData
from gale.state_machine import BaseState
from gale.timer import Timer
from gale.text import render_text

import settings
from src.Controller import game_controller
from src.Veil import Veil
from src.GameLevel import GameLevel
from src.Player import Player

class TransitionState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level")
        self.game_level = enter_params.get("game_level")
        self.camera = enter_params.get("camera")

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            self.player = Player(0, settings.VIRTUAL_HEIGHT - 66, self.game_level)
            self.player.change_state("idle")

        self.veil = Veil()

        pygame.mixer.music.pause()

        def after_level_change() -> None:
            game_controller.scoregoal = game_controller.get_score_goal(self.level + 1)
            self.state_machine.change(
                "play", 
                level=self.level + 1,
            )

        Timer.tween(
            settings.LEVEL_CHANGE_DELAY,
            [
                (self.veil, {"alpha": 255})
            ],
            on_finish=after_level_change
        )

    def exit(self) -> None:
        # InputHandler.unregister_listener(self)
        # InputHandler.register_listener(self.player.state_machine.current)
        pygame.mixer.music.unpause()

    def render(self, surface: pygame.Surface) -> None:
        world_surface = pygame.Surface((self.tilemap.width, self.tilemap.height))
        self.game_level.render(world_surface)
        self.player.render(world_surface)
        surface.blit(world_surface, (-self.camera.x, -self.camera.y))

        render_text(
            surface,
            f"Score: {game_controller.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        self.veil.render(surface)


   