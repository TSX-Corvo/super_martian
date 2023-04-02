import pygame
from gale.timer import Timer

import settings


class Veil:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.alpha = 0
   
    def render(self, surface: pygame.Surface) -> None:
        image = pygame.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
        image.fill((0, 0, 0, self.alpha))

        surface.blit(image, (self.x, self.y))
