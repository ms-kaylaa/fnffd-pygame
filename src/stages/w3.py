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

        self.colorfrom = pygame.Color(0,0,0, 255)
        self.colorto = pygame.Color(255,255,255, 255)


    def make_bg_sprites(self):
        # budy
        
        self.back = StaticSprite(40, self.scarysin2, loader.load_image(f"{self.wd}buddyback_3"))
        self.back.scroll_factor = (0.33, 0.33)

        self.tvs = StaticSprite(50, self.scarysin2-60, loader.load_image(f"{self.wd}buddyback_2"))
        self.tvs.scroll_factor = (0.25, 1)

        self.tvmask = pygame.mask.from_surface(loader.load_image(f"{self.wd}tvmask"))

        self.tvmask.invert()
        #setsurface=loader.load_image(f"{self.wd}doodle dip")
        self.masked_tvsurf = self.tvmask.to_surface(setcolor=(255,255,255), unsetcolor=(0,0,0,0))
        self.masked_tvsurf.convert_alpha()

        self.tvback = StaticSprite(50, self.scarysin2-60, self.masked_tvsurf, 255)
        self.tvback.scroll_factor = self.tvs.scroll_factor
        #self.tvback.alpha = 25

        self.tvshade = StaticSprite(self.tvs.x, self.tvs.y+3, loader.load_image(f"{self.wd}buddyback_2"))
        self.tvshade.scroll_factor = self.tvs.scroll_factor
        self.tvshade.color = (0,0,0,128)
        self.tvshade.update_image()

        self.fore = StaticSprite(100, -40, loader.load_image(f"{self.wd}buddyback"))
        self.fore.shaders = ["silhouette"]
        self.fore.shaders_uniforms.append({"colorreplace": (75/70/255, 46/70/255, 112/70/255, 0.5), "ignoreRGB": (2,2,2)})
        self.fore.update_image(True)

        return [self.back, self.tvback, self.tvs, self.tvshade, self.fore]

    def make_fg_sprites(self):

        return []

    def update(self):
        self.scarysin2 = round(2*(math.sin((pygame.time.get_ticks()-300)/350)))

        self.tvs.y = self.scarysin2-60
        self.tvback.y = self.tvs.y
        self.tvshade.y = self.tvs.y

        #self.tvback.alpha = (math.sin(pygame.time.get_ticks()/350)*128+128)
        self.colorfrom = self.colorfrom.lerp(self.colorto, 0.1)
        self.tvback.color = self.colorfrom
        #print(self.colorfrom)
        self.tvback.update_image()