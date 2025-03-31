import pygame
import pygame_shaders

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

        self.shader: str = None
        self._last_shader: str = None
        self.shader_uniforms = {}

        self._shader_obj: pygame_shaders.Shader = None

        self._last_alpha = -1
        self._last_angle = -1
        self._last_scale = -1

        self.parent: pygame.sprite.Group = None

        self.image = None

        self.should_draw = True
        self.should_update = True

    def set_image(self, img: pygame.Surface):
        self.base_image = img
        self.rect = self.base_image.get_rect()
        self.update_image(True)
        
    def update_image(self, force=False):
        if self.parent != None and not self.rect.colliderect(self.parent.internal_rect):
            return
        frame_refresh = False

        if self.image == None or (self._last_alpha != self.alpha or self._last_angle != self.angle or self._last_scale != self.scale) or force:
            self.image = self.base_image.copy()
            frame_refresh = True

        if (frame_refresh and self._last_scale != self.scale) or force:
            self.image = pygame.transform.scale_by(self.base_image, self.scale)
        if (frame_refresh and self._last_angle != self.angle) or force:
            self.image = pygame.transform.rotate(self.image, self.angle)
        if (frame_refresh and (self.image.get_alpha() != self.alpha or self._last_alpha != self.alpha)) or force:
            self.image.set_alpha(self.alpha)
        
        if (self.color != (255, 255, 255, 255) and frame_refresh) or force:
            self.image.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)

        if self.shader != None and frame_refresh:
            # todo: this probably isnt very optimized
            self._shader_obj = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, SHAD_DIRECTORY + self.shader + ".frag", self.image)
            if len(self.shader_uniforms) > 0:
                for uniform in self.shader_uniforms:
                    # check if param is a callable (used to do pixel measurements)
                    if not callable(self.shader_uniforms[uniform]):
                        self._shader_obj.send(uniform, self.shader_uniforms[uniform])
                    else:
                        self._shader_obj.send(uniform, self.shader_uniforms[uniform]())

            self.image = self._shader_obj.render()

        self._last_alpha = self.alpha
        self._last_angle = self.angle
        self._last_scale = self.scale

        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

    def update(self, dt):
        self.update_image()
        self.update_rect()