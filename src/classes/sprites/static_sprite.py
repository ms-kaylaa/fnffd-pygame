import pygame

from typing import overload

from util.loader import load_image
from classes.sprites.basic_sprite import BasicSprite

# TODO: when u update a value, it should refresh image and rect (if its not just alpha)
class StaticSprite(BasicSprite):
    @overload
    def __init__(self, x: float, y:  float, img: pygame.Surface, alpha=255, angle=0, scale=1):
        super().__init__(x, y, alpha, angle, scale)

        self.set_image(load_image(img))
        self.update_image()

    def __init__(self, x: float, y: float, img: pygame.Surface, alpha=255, angle=0, scale=1):
        super().__init__(x, y, alpha, angle, scale)

        self.set_image(img)

        self.update_image()

    def update(self, dt):
        self.update_rect()
        pass