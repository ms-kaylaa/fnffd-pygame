import pygame

from globals import WINDOW_WIDTH, WINDOW_HEIGHT

class UpscaleGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(sprites)

        self.internal_surf = pygame.Surface((400, 400)).convert_alpha()
        self.internal_rect = self.internal_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)).scale_by(1.4,1.4).move(-100,-100)

        self.alpha = 255
        

    def draw(self, surf: pygame.Surface):
        self.internal_surf.fill((0, 0, 0, 0))

        def bydepth(spr): return spr.depth
        for sprite in sorted(self.sprites(), key=bydepth):
            if sprite.should_draw and sprite.rect.colliderect(self.internal_rect) and sprite.image != None:
                self.internal_surf.blit(sprite.image, sprite.rect.topleft)
                sprite.update_image()

        # 2x upscale like free download does
        scaled_surf = pygame.transform.scale_by(self.internal_surf, 2)
        scaled_rect = scaled_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

        if self.alpha != 255:
            scaled_surf.set_alpha(self.alpha)

        surf.blit(scaled_surf, (0, 0))

    def update(self, *args, **kwargs):
        for sprite in self.sprites():
            if sprite.should_update and sprite.rect.colliderect(self.internal_rect):
                sprite.update(*args)
                
