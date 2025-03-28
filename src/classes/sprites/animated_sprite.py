from classes.sprites.static_sprite import BasicSprite
from util.spritesheet import Spritesheet
import globals

class AnimatedSprite(BasicSprite):
    def __init__(self, x: float, y:  float, img: str, alpha=255, angle=0, scale=1):
        super().__init__(x, y, alpha, angle, scale)

        self.spritesheet = Spritesheet(img)

        self.frame_time = 0
        self.anim_time = 0
        self.fps = 12

        self.cur_anim = ""
        self.frames = []
        self.cur_frame = 0

        self.animating = False

    def _update_animation(self, dt):
        if self.frame_time >= (globals.FPS/self.fps):
            
            if self.cur_frame >= len(self.frames)-1:
                self.animating = False
            else:
                self.frame_time = 0
                self.cur_frame += 1
            
                self.set_image(self.frames[self.cur_frame])

        self.update_image()

    

    # frame stuff
    def show_frame(self, name, idx):
        self.set_image(self.spritesheet.get_frame(name, idx))
        self.animating = False

    def play_animation(self, name, indices=[]):
        # reset animation variables
        self.frame_time = 0
        self.anim_time = 0

        self.cur_frame = 0

        self.animating = True

        if name != self.cur_anim:
            self.frames = self.spritesheet.get_animation(name, indices)
        self.set_image(self.frames[0])

        self.cur_anim = name



    def update(self, dt):
        self.frame_time += dt
        self.anim_time += dt

        if self.animating:
            self._update_animation(dt)
