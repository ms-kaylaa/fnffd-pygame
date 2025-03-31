import pygame
from pygame.draw import * # no more top ramen in the crib we will be feasting
import pygame_shaders

import math


from classes.sprites.basic_sprite import BasicSprite

from globals import WINDOW_WIDTH, WINDOW_HEIGHT, IMG_DIRECTORY, FPS
import globals

from util.loader import load_image

class HealthBar(BasicSprite):
    def __init__(self):
        super().__init__(0, 0)

        self.skill = 50
        self.flow = 0.5

        self._last_skill = 0
        self._last_flow = 0
        
        self.coolscore = 0
        self.misses = 0

        self._last_score = 0
        self._last_misses = 0

        self.base_image = pygame.Surface((WINDOW_WIDTH//2, WINDOW_HEIGHT//4), pygame.SRCALPHA).convert_alpha() # TODO: base_image = bar frame, moving stuff is drawn/blitted on top
        self.rect = self.base_image.get_rect()

        self.outline_color = pygame.Color(0, 0, 0)
        self.player_color = pygame.Color(255, 255, 0)
        self.baddie_color = pygame.Color(128, 0, 128)

        self.player_icons = [load_image("ui/dude_neu.png"), load_image("ui/dude_lose.png"), load_image("ui/mcdonalds.png")]
        self.baddie_icons = [load_image("ui/strad_neu.png"), load_image("ui/strad_neu.png")]

        self.f_outline = pygame.Color(0, 0, 0)
        self.f_back = pygame.Color(18, 72, 75)
        self.f_full = pygame.Color(83, 206, 213)

        self.image =self.base_image

        self.sinny = round(math.sin(pygame.time.get_ticks()/200))
        self._last_sinny = 0
        
        self.shader = "fancysilhouette"
        self.shader_uniforms = {"shadowOffset": (-2/400, 2/200), "shadowColor": (0, 0, 0, 1)}

        self.y = 200
        self.make_bar()

    def make_bar(self):
        self.base_image = pygame.surface.Surface(self.base_image.get_size(), pygame.SRCALPHA).convert_alpha()
        #self.image.fill((0, 0, 0, 0))

        # healthbar
        rect(self.base_image, self.outline_color, pygame.Rect((59, 356-200), (282, 19)))
        rect(self.base_image, self.player_color, pygame.Rect((61, 358-200), (278, 15)))
        rect(self.base_image, self.baddie_color, ((61, 358-200), (self.skill*0.01*278, 15)))

        # flow
        """
        var sinnny=sin(current_time/200)
        draw_sprite_ext(spr_whitepixel,0,200-(80)-2,sinnny+((340-minus))-2,82*2,12,0,foutline,1)
        draw_sprite_ext(spr_whitepixel,0,200-(80),sinnny+(340-minus),80*2,8,0,fback,1)
        draw_sprite_ext(spr_whitepixel,0,200+(80),sinnny+(340-minus),(-80*2*flow),8,0,ffull,1) 
        """

        rect(self.base_image, self.f_outline, ((200-(80)-2, self.sinny+(340-200)-2), (82*2, 12)))
        rect(self.base_image, self.f_back, ((200-80, self.sinny+(340-200)), (80*2, 8)))
        rect(self.base_image, self.f_full, (((200+80)-(80*2*self.flow), self.sinny+(340-200)), (80*2*self.flow, 8))) # TODO: fix flicker

        eviltext = globals.small_font.render(f"score: {self.coolscore} | misses: {self.misses}", False, pygame.Color(0, 0, 0))
        evil_rect = eviltext.get_rect(center=(200,388-200))

        # scoretext
        for i in range(3): # as tyler intended
            for ii in range(3):
                self.base_image.blit(eviltext,evil_rect.move(i-1,ii-1))

        scoretext = globals.small_font.render(f"score: {self.coolscore} | misses: {self.misses}", False, pygame.Color(255,255,255))
        self.base_image.blit(scoretext,evil_rect)

        bh = 0
        dh = 0
        if self.skill > 65:
            bh = 1
        elif False: # mcdonald
            bh = 2
        

        if self.skill < 35:
            dh = 1

        #draw_sprite_ext(baddieicon,bh,((61-23)+obj_song.skill*0.01*278),(360+6-minus),1,1,0,c_white,1)
        #draw_sprite_ext(playericon,dh,((61+20)+obj_song.skill*0.01*278),(360+6-minus),1,1,0,c_white,1)
        baddie_icon = self.baddie_icons[dh]
        self.base_image.blit(baddie_icon, pygame.Rect((((61-23)+self.skill*0.01*278)-23, (360+6-200)-25), (baddie_icon.get_width(), baddie_icon.get_height())))
        player_icon = self.player_icons[bh]
        self.base_image.blit(player_icon, pygame.Rect((((61+20)+self.skill*0.01*278)-(20), (360+6-200)-(23)), (player_icon.get_width(), player_icon.get_height())))

    def update(self, dt):
        self.sinny = round(math.sin(pygame.time.get_ticks()/200))

        sin_diff = self.sinny != self._last_sinny
        skill_diff = self.skill != self._last_skill
        flow_diff = self.flow != self._last_flow

        miss_diff = self.misses != self._last_misses
        score_diff = self.coolscore != self._last_score

        if sin_diff or skill_diff or flow_diff or miss_diff or score_diff:
            self.make_bar()
            self.update_image(True)

        self._last_sinny = self.sinny
        self._last_skill = self.skill
        self._last_flow = self.flow
        self._last_misses = self.misses