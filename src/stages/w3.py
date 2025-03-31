from stages.base_stage import BaseStage

import pygame
import math

from util import loader
from classes.sprites.static_sprite import StaticSprite

class W3Stage(BaseStage):
    def __init__(self):
        super().__init__()

        self.wd = "stage_assets/buddy/"
        self.scarysin2 = round(2*(math.sin((pygame.time.get_ticks()-300)/350)))

        self.back = None
        self.tvs = None
        self.tvmask = None
        self.masked_tvsurf = None
        self.tvback = None
        self.tvshade = None
        self.fore = None


    def make_bg_sprites(self):
        # budy
        
        self.back = StaticSprite(40, self.scarysin2, loader.load_image(f"{self.wd}buddyback_3"))
        self.back.scroll_factor = (0.33, 0.33)

        self.tvs = StaticSprite(50, self.scarysin2-60, loader.load_image(f"{self.wd}buddyback_2"))
        self.tvs.scroll_factor = (0.25, 1)

        self.tvmask = pygame.mask.from_surface(loader.load_image(f"{self.wd}tvmask"))

        self.tvmask.invert()
        self.masked_tvsurf = self.tvmask.to_surface(setsurface=loader.load_image(f"{self.wd}doodle dip"), unsetcolor=(0,0,0,0))
        self.masked_tvsurf.convert_alpha()

        self.tvback = StaticSprite(50, self.scarysin2-60, self.masked_tvsurf, 25)
        self.tvback.scroll_factor = self.tvs.scroll_factor
        self.tvback.alpha = 25

        self.tvshade = StaticSprite(self.tvs.x, self.tvs.y, loader.load_image(f"{self.wd}buddyback_2"))
        self.tvshade.scroll_factor = self.tvs.scroll_factor
        self.tvshade.color = (0,0,0,255)
        self.tvshade.alpha = 128
        self.tvshade.update_image()

        self.fore = StaticSprite(100, -40, loader.load_image(f"{self.wd}buddyback"))

        return [self.back, self.tvback, self.tvs, self.tvshade, self.fore]

    def make_fg_sprites(self):

        return []

    def update(self):
        self.scarysin2 = round(2*(math.sin((pygame.time.get_ticks()-300)/350)))

        self.tvs.y = self.scarysin2-60
        self.tvback.y = self.tvs.y
        self.tvshade.y = self.tvs.y

        self.tvback.alpha = (math.sin(pygame.time.get_ticks()/350)*128+128)
        self.tvback.update_image()