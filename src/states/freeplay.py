import pygame

# why so many tween
import tween
import tween.tween

import math


import globals
from globals import clock, screen, FPS, MUS_DIRECTORY

from classes.upscale_group import UpscaleGroup
from classes.sprites.static_sprite import StaticSprite

from util.loader import load_image
from util.awesome_util import lerp

grp:UpscaleGroup = None

# background
backsprite:StaticSprite = None

layersurf:pygame.Surface = None
layersprite:StaticSprite = None

hueinterval = 0
targcolor = None

fader:StaticSprite = None # this should be built into upscalegroup... oh well!

# infocard
infocard:StaticSprite = None
infocard_tween:tween.tween.Tween = None

#poscard:StaticSprite = None
basepossurf:pygame.Surface = None
possurf:pygame.Surface = None

# icon stuff
iconlist:list[pygame.Surface] = None
iconsprites:list[StaticSprite] = None

discsprite:StaticSprite = None

iconxstarts:list[int] = None

iconymods:list[int] = None
iconstart_y = 0

# song list stuff
weekndlist = [
    "weeknd 7 billion", # yolo man

    "BONUS | weeknd 4",
    "BONUS | weeknd 3",
    "BONUS | weeknd 2",
    "BONUS | weeknd 1",

    "tutorial",
    "weeknd 1",
    "weeknd 2",
    "weeknd 3",
    "weeknd 4",

    "BONUS" # generic in case i add bonus songs! unlikely
]

# STRUCTURE:[weekndid:int (index in weeknds list - 5) title:str, iconoffset:int = 0]
songlist = [
    [-5, "misplaced"],

    [-4, "cinemassacre"], # i havent added these yet.. i might never!
    [-3, "break it down triangle man"],
    [-2, "channelsurfing and nermal"],
    [-1, "infographic"],

    [0, "i robot"],
    
    [1, "summer"],
    [1, "stars"],

    [2, "girl next door"],
    [2, "gamejack", 1],

    [3, "twinkle"],
    [3, "tsunami"],

    [4, "satellite"],
    [4, "starfire"],

    [5, "tsunami old", -1]
]
layout=".....|.........|."
cursel = 0
selected = False

iconxshift = None
targxshift = None

def load_icons():
    global iconlist, iconsprites, iconymods, iconstart_y, iconxstarts, discsprite

    def _changeicon(icon):
        return pygame.transform.scale_by(icon, 2)

    for i in range(11):
        iconlist.append(_changeicon(load_image(f"menus/freeplay/icons/{i}")))
    iconlist.append(_changeicon(load_image("menus/freeplay/icons/L"))) # methinks i will never use this

    # space between icons is 230!!
    curxmod = 200 - iconlist[0].width/2
    iconstart_y = curxmod + 40
    
    i = 0
    totalshift = 0
    for song in songlist:
        if len(song) > 2:
            totalshift = song[2]
        songicon = StaticSprite(curxmod, iconstart_y, iconlist[song[0]+5+totalshift])
        iconxstarts.append(songicon.x)
        songicon.depth += i

        if i != cursel:
            songicon.color = (128, 128, 128)
            iconymods.append(0)
            songicon.alpha = 164
        else:
            iconchangey = 65
            iconymods.append(-iconchangey)
            songicon.y -= iconchangey
            songicon.depth += 100

        curxmod += 230

        iconsprites.append(songicon)

        i += 1

def init():
    global grp, backsprite, layersprite, infocard, iconsprites, discsprite, hueinterval, targcolor, fader, iconxshift, basepossurf, iconlist, selected
    global iconxstarts, iconymods, iconxshift, targxshift

    selected = False

    iconlist = []
    iconsprites = []
    iconxstarts = []
    iconymods = []

    iconxshift = -230*cursel
    targxshift = -230*cursel

    load_icons()
    
    grp = UpscaleGroup()

    backsprite = StaticSprite(0,0,load_image("menus/back_gray"))

    layersurf = pygame.Surface((400, 400))
    layersurf.fill(backsprite.color)

    layersprite = StaticSprite(0,0,layersurf)
    layersprite.alpha = 65
    
    infocard = StaticSprite(200-225/2, 330, make_infocard(weekndlist[songlist[cursel][0]+5], songlist[cursel][1], "hiscore:21200 | least misses:2"))
    infocard.x = 200 - infocard.image.width/2
    infocard.depth = 9999999

    del discsprite
    discsprite = StaticSprite(200, 250, load_image("menus/freeplay/disc"))
    discsprite.x -= discsprite.image.width/2
    discsprite.y -= discsprite.image.height/2
    #discsprite.alpha = 0
    discsprite.depth = len(songlist)+1

    hueinterval = 360/len(songlist)

    backsprite.color = pygame.Color.from_hsva(hueinterval*cursel, 60, 75, 100)
    layersprite.color = backsprite.color
    targcolor = backsprite.color

    fadersurf = pygame.Surface((400,400))
    fadersurf.fill((0,0,0))
    fader = StaticSprite(0,0,fadersurf)
    fader.depth = 99999999999
    fader.alpha = 0

    grp.add(backsprite)
    grp.add(layersprite)
    grp.add(discsprite)
    grp.add(iconsprites)
    grp.add(infocard)
    #grp.add(poscard)
    grp.add(fader)

    basepossurf = make_poscard()
    change_selection(5 if cursel == 0 else 0)
    iconxshift = targxshift

    pygame.mixer.music.load(MUS_DIRECTORY + "mus_game.ogg")
    pygame.mixer.music.play(-1)

def run():
    global iconsprites, iconxshift, selected, infocard, discsprite, fader, backsprite, layersprite, possurf
    discstarts = [discsprite.x, discsprite.y]

    left_pressed, right_pressed, enter_pressed = False, False, False

    global moveon
    moveon = False # should be true. im looking at you free download community

    while True:
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        tween.update(dt/FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.gamestate = pygame.QUIT
                return
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not left_pressed:
            change_selection(-1)
            left_pressed = True
        elif not keys[pygame.K_LEFT]:
            left_pressed = False

        if keys[pygame.K_RIGHT] and not right_pressed:
            change_selection(1)
            right_pressed = True
        elif not keys[pygame.K_RIGHT]:
            right_pressed = False

        if keys[pygame.K_RETURN] and not enter_pressed and not selected:
            iconsprites[cursel].y += 20
            iconymods[cursel] = -65
            enter_pressed = True
            selected = True
            pygame.mixer.music.stop()
            
            def upd():
                global possurf
                possurf.set_alpha(infocard.alpha)
            tween.to(infocard, "alpha", -50, 0.1).on_update(upd)

            twn2 = tween.to(discsprite, "y", discstarts[1]-10,0.4, "easeOutQuad")
            def fade():
                def trans():
                    global moveon
                    globals.gamestate = "stage"
                    moveon = True
                twn3 = tween.to(fader, "alpha", 255, 0.25, "linear", 0.2)
                twn3.on_complete(trans)
            twn2.on_complete(fade)
        elif not keys[pygame.K_RETURN]:
            enter_pressed = False

        if not selected: iconymods[cursel] = (-65)+math.sin(pygame.time.get_ticks()/700)*6

        iconxshift = lerp(iconxshift, targxshift, 0.15)
        for i in range(len(iconsprites)):
            sprite = iconsprites[i]
            startx = iconxstarts[i]
            targy = iconymods[i] + iconstart_y

            sprite.x = startx + iconxshift
            sprite.y = lerp(sprite.y, targy, 0.2 if not selected else 0.1)
            sprite.update_rect()
        
        discsprite.x = discstarts[0]+iconxshift+230*cursel
        if not selected:discsprite.y = discstarts[1]-iconstart_y+iconsprites[cursel].y
        discsprite.update_rect()

        backsprite.color = backsprite.color.lerp(targcolor, 0.2)
        layersprite.color = backsprite.color
        backsprite.update_image()
        layersprite.update_image()
            
        grp.draw(screen)
        grp.update(dt)

        screen.blit(possurf, (400-possurf.width/2,2))

        globals.screen_shader.render()
        pygame.display.flip()

        if moveon:
            return


def make_infocard(toptext:str, songname:str, scoretext:str):
    shadow_dist = 1

    # make and blit songname, adjust infocard size accordingly
    songnamerender = globals.small_font.render(f"{songname}", False, (255,255,255))
    songnamerender = pygame.transform.scale_by(songnamerender, 2)

    infocard_surf = pygame.Surface((min(songnamerender.width*2, 375), 62), flags=pygame.SRCALPHA)
    infocard_surf.fill((0,0,0,128))

    # make and blit toptext
    toptextrender = globals.small_font.render(toptext, False, (255,255,255))
    
    # FIXME
    #eviltoptextrender = toptextrender.copy()
    #eviltoptextrender.fill((0,0,0, 255), special_flags=pygame.BLEND_RGBA_MULT)

    #infocard_surf.blit(eviltoptextrender, (225/2-eviltoptextrender.width/2+shadow_dist, 5+shadow_dist))
    infocard_surf.blit(toptextrender, (infocard_surf.width/2-toptextrender.width/2, 2))
    infocard_surf.blit(songnamerender, (infocard_surf.width/2-songnamerender.width/2, 62/2-songnamerender.height/2))

    # make and blit songname
    scoretextrender = globals.small_font.render(scoretext, False, (255,255,255))

    infocard_surf.blit(scoretextrender, (infocard_surf.width/2-scoretextrender.width/2, 62-scoretextrender.height))

    return infocard_surf

def update_and_push_infocard():
    global infocard, infocard_tween

    infocard.set_image(make_infocard(weekndlist[songlist[cursel][0]+5], songlist[cursel][1], "placed holder"))
    infocard.x = 200 - infocard.image.width/2
    infocard_tween = tween.to(infocard, "y", 330, 0.1, "easeOutQuad")

def change_selection(amt = 0):
    global infocard, infocard_tween, iconsprites, cursel, targxshift, discsprite, targcolor, possurf
    if cursel + amt > len(songlist)-1 or cursel + amt < 0:
        return

    infocard_tween = tween.to(infocard, "y", 400+infocard.image.height, 0.1, "easeOutQuad")

    iconsprites[cursel].depth -= 100
    iconsprites[cursel].alpha = 164
    iconsprites[cursel].color = (128, 128, 128)
    iconymods[cursel] = 0

    cursel += amt
    targxshift -= 230*amt
    targcolor = pygame.Color.from_hsva(hueinterval*cursel, 60, 75, 100)

    possurf = pygame.transform.scale_by(make_updated_poscard(basepossurf), 4)

    iconsprites[cursel].depth += 100
    iconsprites[cursel].alpha = 255
    iconsprites[cursel].color = (255, 255, 255)
    iconymods[cursel] = -65

    infocard_tween.on_complete(update_and_push_infocard)

def make_poscard():
    lenlay = len(layout)+2
    #print(lenlay)
    stupidsurf = pygame.Surface((4*lenlay+5+4, 9), flags=pygame.SRCALPHA)
    stupidsurf.fill((0,0,0,128))


    for i in range(5):
        stupidsurf.set_at((i+2,4-i), (255,255,255))
        stupidsurf.set_at((i+2,4+i), (255,255,255))
    for i in range(10, (lenlay)*4, 4):
        fundex = (i-8)//4  # its fun!

        fundexadj = fundex - len(layout[:-(len(layout)-(fundex+1))].replace(".", "")) # this is less fun.

        char = layout[fundex]
        #print(char)
        if char == "|":
            for j in range(3):
                stupidsurf.set_at((i,4-j), (255,255,255))
                stupidsurf.set_at((i,4+j), (255,255,255))
        elif char == ".":
            stupidsurf.set_at((i, 4), (255,255,255))


    jj = 4
    for i in range(lenlay*4, lenlay*4+5):
        stupidsurf.set_at((i,4-jj), (255,255,255))
        stupidsurf.set_at((i,4+jj), (255,255,255))
        jj-=1
    return stupidsurf

def make_updated_poscard(stupidsurf:pygame.Surface):
    stupidsurf = stupidsurf.copy()
    lenlay = len(layout)+2

    for i in range(10, (lenlay)*4, 4):
        fundex = (i-8)//4  # its fun!

        fundexadj = fundex - len(layout[:-(len(layout)-(fundex+1))].replace(".", "")) # this is less fun.

        char = layout[fundex]
        #print(char)
        if char == "." and (fundexadj == cursel or (cursel == len(songlist)-1 and i == lenlay*4-2)): # WHY DOES IT DO THIS
            for j in range(3):
                for k in range(3):
                    stupidsurf.set_at((i+(j-1), 4+(k-1)), (255,255,255))

    return stupidsurf