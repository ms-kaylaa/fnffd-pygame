import json

from globals import CHR_DIRECTORY
from classes.sprites.animated_sprite import AnimatedSprite

class Character(AnimatedSprite):

    @staticmethod
    def load_from_json(json_name):
        json_name = CHR_DIRECTORY + json_name + ".json"
        read_json = json.load(open(json_name))

        made_char = Character(0,0, read_json['spritesheet'])

        made_char.animations = read_json['animations']
        made_char.scale = read_json['scale']
        if 'ayy_sound' in read_json:
            made_char.ayy_sound = read_json['ayy_sound']

        return made_char

    def __init__(self, x: float, y:  float, img: str):
        super().__init__(x, y, "characters/" + img, 255, 0, 1)

        self.xx = self.x
        self.yy = self.y
        self.cur_named_anim = "idle"

        self.ayy_anim = "ayy"

        self.animations = {}
    def update_rect(self):
        offsets = self.animations[self.cur_named_anim]["offsets"]
        self.x = self.xx + offsets[0]
        self.y = self.yy + offsets[1]

        self.rect.topleft = (self.x, self.y)

        self.rect.bottom -= self.spritesheet.get_frame(self.animations["idle"]['xml_name']).get_height()

    def play_animation(self, name):
        if name == "ayy": name = self.ayy_anim
        super().play_animation(self.animations[name]['xml_name'], self.animations[name]["indices"])
        self.cur_named_anim = name
        self.update_rect()