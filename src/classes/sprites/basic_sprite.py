import pygame
import pygame_shaders

import globals
from globals import SHAD_DIRECTORY


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, x: float, y:  float, alpha=255, angle=0, scale=1):
        super().__init__()

        self.x, self.y = x, y

        self.angle = angle
        self.alpha = alpha
        self.scale = scale

        self.scroll_factor = pygame.math.Vector2(1, 1)

        self.color = (255, 255, 255, 255)
        self.colorignorelist = []

        self.shaders: list[str] = []
        self._last_shaders: list[str] = []
        self.shaders_uniforms = []

        self._shaders_objs: list[pygame_shaders.Shader] = []

        self._last_alpha = -1
        self._last_angle = -1
        self._last_scale = -1
        self._last_color = (255,255,255,255)

        self.parent: pygame.sprite.Group = None

        self.image = None

        self.should_draw = True
        self.should_update = True

        self.depth = 0

    def set_image(self, img: pygame.Surface):
        self.base_image = img
        self.rect = self.base_image.get_rect()
        self.image = None
        self.update_image()
        
    def update_image(self, force=False):
        # this could be HUGE for optimization but i need to figure it out some more
        this_sprite_offscreen = self.parent != None and not self.rect.colliderect(self.parent.internal_rect.scale_by(1.2,1.2).move(-self.parent.internal_rect.width*0.2,-self.parent.internal_rect.height*0.2))
        
        
        if force: print("im being forced to update! HEEELP!!!")

        frame_refresh = False
        if self.image == None or ((not this_sprite_offscreen) and (self._last_alpha != self.alpha or self._last_angle != self.angle or self._last_scale != self.scale or self._last_color != self.color)) or force:
            self.image = self.base_image.copy()
            frame_refresh = True

        if (frame_refresh and self._last_angle != self.angle) or force:
            self.image = pygame.transform.rotate(self.image, self.angle)
            self._last_angle = self.angle
        if (frame_refresh and (self.image.get_alpha() != self.alpha or self._last_alpha != self.alpha)) or force:
            self.image.set_alpha(self.alpha)
            self._last_alpha = self.alpha
        
        if (frame_refresh and (self.color != (255, 255, 255, 255) and self.color != (255,255,255))) or force:
            if len(self.colorignorelist) != 0:
                # MASK BECAUSE IM STUPID
                masksurf = self.image.copy()
                for color in self.colorignorelist:
                    masksurf.set_colorkey(color)
                mask = pygame.mask.from_surface(masksurf)
                color_surf = mask.to_surface(setcolor=self.color, unsetcolor=(255,255,255,255))
            
                self.image.blit(color_surf, special_flags=pygame.BLEND_MULT)
            else:
                self.image.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)
            self._last_color = self.color

        if frame_refresh and self.shaders != None and globals.options["shaders_enabled"]:
            if len(self.shaders) != len(self._last_shaders):
                if len(self.shaders) > len(self._last_shaders):
                    # new shaders have been added
                    for i in range(len(self.shaders) - len(self._last_shaders)):
                        self._shaders_objs.append(pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, SHAD_DIRECTORY + self.shaders[i+len(self._last_shaders)] + ".frag", self.image))
                self._last_shaders = self.shaders

            i = 0
            for obj in self._shaders_objs:
                obj.set_target_surface(self.image)
                
                # todo: this probably isnt very optimized
                if len(self.shaders_uniforms) > 0:
                    for uniform in self.shaders_uniforms[i]:
                        # check if param is a callable (used to do pixel measurements)
                        if not callable(self.shaders_uniforms[i][uniform]):
                            obj.send(uniform, self.shaders_uniforms[i][uniform])
                        else:
                            obj.send(uniform, self.shaders_uniforms[i][uniform]())

                self.image = obj.render()
                i += 1

        if (frame_refresh and self._last_scale != self.scale) or force:
            self.image = pygame.transform.scale_by(self.base_image, self.scale)
            self._last_scale = self.scale
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def update(self, dt):
        self.update_image()
        self.update_rect()