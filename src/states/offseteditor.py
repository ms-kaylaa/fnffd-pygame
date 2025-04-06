import pygame, pyautogui, os, shutil

import globals
from globals import clock, screen, FPS

from classes.stage.character import Character
from classes.upscale_group import UpscaleGroup
from classes.sprites.static_sprite import StaticSprite
from classes.camera import Camera

from util.loader import load_image
from util.awesome_util import lerp
from util.awesome_util import play_snd
from util.awesome_util import clamp # i cant live without it!

import json

grp:Camera = None
char:Character = None
ghostchar:Character = None
backsprite:StaticSprite = None
cross:StaticSprite = None
tutorialtext:pygame.Surface = None

curanim = None
anims = None

charname = "dude"

cam_x,cam_y = -200,-400

def init():
    global grp,backsprite,char,cross,curanim,anims,ghostchar,tutorialtext,charname

    charname = pyautogui.prompt(text="gimme character name",title="")
    if not os.path.exists(globals.CHR_DIRECTORY+charname+".json"):
        pyautogui.alert("character doesnt exist! creating it now")
        shutil.copy2(globals.CHR_DIRECTORY+"default.json",globals.CHR_DIRECTORY+charname+".json")

    grp = Camera()

    char = Character.load_from_json(charname)
    char.x, char.y = 0, 0
    char.xx, char.yy = 0, 0
    char.play_animation("idle")   

    ghostchar = Character.load_from_json(charname)
    ghostchar.x, ghostchar.y = 0, 0
    ghostchar.xx, ghostchar.yy = 0, 0
    ghostchar.play_animation("idle")   
    ghostchar.alpha = 0.5*255 # fuck you john pygame

    curanim = 0
    anims = list(char.animations.keys())

    backsprite = StaticSprite(50,50,load_image("menus/back_blue"),255,0,2)

    cross = StaticSprite(-13/2,-13/2,load_image("menus/offset/crosshair"))

    # i needed the symbols
    tutorialtext = globals.default_font.render(f"""OFFSETTER 2000 (tm)
A and D switch through animations
arrow keys move around the camera
IJKL moves around the character's offset
hold ctrl and or shift to go faster! they both stack
ctrl+s to save! will immediately overwrite the original json LMAO
crosshair shows where (0,0) is! probably not useful just align everything to the idle anim""", False, pygame.Color(255,255,255))
    

    grp.add(backsprite)
    grp.add(ghostchar)
    grp.add(char)
    grp.add(cross)


    pygame.mixer.music.stop()

def update_ofs():
    ofsx = char.animations[anims[curanim]]["offsets"][0]
    ofsy = char.animations[anims[curanim]]["offsets"][1]
    return ofsx,ofsy

def run():
    global cam_x,cam_y,backsprite,char,curanim,anims,ghostchar,tutorialtext
    print("we workign")
    space_pressed,left_pressed,right_pressed = False,False,False
    ofs_left_pressed,ofs_right_pressed,ofs_up_pressed,ofs_down_pressed = False,False,False,False
    while True:
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.gamestate = pygame.QUIT
                return
            
        keys = pygame.key.get_pressed()

        # og

        if keys[pygame.K_ESCAPE]:
            globals.gamestate = "freeplay"
            return
        
        if keys[pygame.K_LCTRL] and keys[pygame.K_s] and not save_pressed:
            save_pressed = True
            json_name = globals.CHR_DIRECTORY + charname + ".json"
            faker = { # i found you
                "spritesheet" : charname,

                "animations" : char.animations,

                "scale": char.scale

            }
            json.dump(faker,open(json_name,"w"),indent=4) # blindly overwrite and call it a day
            play_snd("snd_ribbit1")
        elif not keys[pygame.K_LCTRL] and not keys[pygame.K_s]:
            save_pressed = False

        if keys[pygame.K_LEFT]:
            cam_x -= 5*dt
        if keys[pygame.K_DOWN] and not save_pressed:
            cam_y += 5*dt
        if keys[pygame.K_UP]:
            cam_y -= 5*dt
        if keys[pygame.K_RIGHT]:
            cam_x += 5*dt

        if keys[pygame.K_SPACE] and not space_pressed:
            space_pressed = True
            char.play_animation(anims[curanim])
        elif not keys[pygame.K_SPACE]:
            space_pressed = False

        if keys[pygame.K_a] and not left_pressed:
            left_pressed = True
            curanim-=1
            curanim=clamp(curanim,0,len(anims)-1)
            char.play_animation(anims[curanim])
        elif not keys[pygame.K_a]:
            left_pressed = False

        if keys[pygame.K_d] and not right_pressed:
            right_pressed = True
            curanim+=1
            curanim=clamp(curanim,0,len(anims)-1)
            char.play_animation(anims[curanim])
        elif not keys[pygame.K_d]:
            right_pressed = False

        speed = 1
        if keys[pygame.K_LSHIFT]:
            speed+=3
        if keys[pygame.K_LCTRL]:
            speed+=3

        ofsx, ofsy = update_ofs()

        if keys[pygame.K_j] and not ofs_left_pressed:
            ofs_left_pressed = True
            char.animations[anims[curanim]]["offsets"] = [ofsx-speed,ofsy]
            ofsx, ofsy = update_ofs()
        elif not keys[pygame.K_j]:
            ofs_left_pressed = False

        if keys[pygame.K_l] and not ofs_right_pressed:
            ofs_right_pressed = True
            char.animations[anims[curanim]]["offsets"] = [ofsx+speed,ofsy]
            ofsx, ofsy = update_ofs()
        elif not keys[pygame.K_l]:
            ofs_right_pressed = False

        if keys[pygame.K_i] and not ofs_up_pressed:
            ofs_up_pressed = True
            char.animations[anims[curanim]]["offsets"] = [ofsx,ofsy-speed]
            ofsx, ofsy = update_ofs()
        elif not keys[pygame.K_i]:
            ofs_up_pressed = False

        if keys[pygame.K_k] and not ofs_down_pressed:
            ofs_down_pressed = True
            char.animations[anims[curanim]]["offsets"] = [ofsx,ofsy+speed]
            ofsx, ofsy = update_ofs()
        elif not keys[pygame.K_k]:
            ofs_down_pressed = False


        ghostchar.animations["idle"]["offsets"] = char.animations["idle"]["offsets"]
        #ghostchar.update_rect()

        backsprite.scroll_factor = [0,0]
        backsprite.update_image()

        grp.pos = pygame.math.Vector2(cam_x,cam_y)

        grp.draw(screen)
        grp.update(dt)
        screen.blit(tutorialtext,(10,10))

        globals.screen_shader.render()
        pygame.display.flip()