import pygame
from globals import WINDOW_WIDTH, WINDOW_HEIGHT
from util import awesome_util

class Camera(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(sprites)

        self.pos = pygame.math.Vector2(0, 0)
        self.zoom = 1
        self.angle = 0

        self.internal_surf_size_vector = pygame.math.Vector2(WINDOW_WIDTH * 0.75, WINDOW_HEIGHT * 0.75)
        self.internal_surf = pygame.Surface(self.internal_surf_size_vector).convert_alpha()
        self.internal_rect = self.internal_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        self.fade_surf = pygame.Surface(self.internal_surf_size_vector).convert_alpha()

        self.fade_color = (0, 0, 0)
        self.fade_speed = 0
        self.fade_alpha = 0

        self.alpha = 255

    def draw(self, surf: pygame.Surface):
        self.internal_surf.fill((0, 0, 0, 0))

        for sprite in self.sprites():
            if sprite.should_draw and sprite.image != None and self.internal_rect.move(self.pos[0], self.pos[1]).colliderect(sprite.rect):
                offset = pygame.math.Vector2(self.pos[0] * sprite.scroll_factor[0], self.pos[1] * sprite.scroll_factor[1])
                self.internal_surf.blit(sprite.image, sprite.rect.topleft - offset)
                #sprite.update_image()

        # fader
        if self.fade_alpha != 0 or self.fade_speed != 0:
            self.fade_surf.fill(self.fade_color)
            self.fade_surf.set_alpha(self.fade_alpha)
            self.internal_surf.blit(self.fade_surf, self.fade_surf.get_rect())

        scaled_surf = pygame.transform.scale_by(self.internal_surf, self.zoom + 1) if self.zoom != 0 else self.internal_surf
        if self.angle != 0:
            scaled_surf = pygame.transform.rotate(scaled_surf, self.angle)
        
        scaled_rect = scaled_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

        if self.alpha != 255:
            scaled_surf.set_alpha(self.alpha)

        surf.blit(scaled_surf, (scaled_rect.x, scaled_rect.y))

    def update(self, *args, **kwargs):
        self.fade_alpha = awesome_util.clamp(self.fade_alpha + self.fade_speed*args[0], 0, 255)
        for sprite in self.sprites():
            if sprite.should_update:
                sprite.update(*args)
