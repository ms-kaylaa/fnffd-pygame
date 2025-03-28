import pygame
import pyvidplayer2

import globals

from classes.sprites.basic_sprite import BasicSprite

class VideoSprite(BasicSprite):
    def __init__(self, video: pyvidplayer2.Video):
        super().__init__(0, 0)

        self.video = video
        self.base_image = pygame.Surface(self.video.current_size)
        self.image = pygame.Surface(self.video.current_size)
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.base_rect = self.base_image.get_rect()
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.base_image = pygame.Surface(self.video.current_size)
        try:
            self.video.draw(self.base_image, (0, 0))
        except pyvidplayer2.error.FFmpegNotFoundError:
            print("oops i couldnt find ffmpeg!!")
            globals.HAS_FFMPEG = False
            return
        self.base_rect = self.base_image.get_rect()

        self.image = pygame.transform.scale_by(self.base_image, self.scale)
        self.rect = self.base_rect.scale_by(self.scale)
        self.rect.topleft = (self.x, self.y)