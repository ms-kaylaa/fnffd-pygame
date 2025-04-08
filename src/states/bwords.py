import pygame

import globals
from globals import screen, FPS, small_font, MUS_DIRECTORY, clock

from classes.upscale_group import UpscaleGroup
from classes.sprites.static_sprite import StaticSprite

from util.conductor import Conductor

textsprites:list[StaticSprite] = []
textspriteyshift = 0
grp:UpscaleGroup = None

conductor:Conductor = None
last_beat = -1


def init():
    global last_beat, conductor, textsprites, grp
    last_beat = -1

    grp = UpscaleGroup()

    conductor = Conductor()
    conductor.bpm = 115

    textsprites = []
    grp.add(textsprites)

    pygame.mixer.music.load(MUS_DIRECTORY + "mus_game.ogg")
    pygame.mixer.music.play(-1)
    pass

def run():
    global last_beat, conductor, grp
    while globals.gamestate == "bwords":
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.gamestate = pygame.QUIT
                return
        keys = pygame.key.get_pressed()

        conductor.time = pygame.mixer.music.get_pos()/1000
        if conductor.beat > last_beat:
            last_beat = conductor.beat
            handle_beatstep()
            print("beat hit")

        grp.update(dt)
        grp.draw(screen)

        globals.screen_shader.render()
        pygame.display.flip()

def handle_beatstep():
    # bad function name but whatever
    # this entire function fucking sucks
    global grp, textsprites, textspriteyshift
    changed_textsprites = True
    match conductor.beat:
        case 0:
            make_textsprite(["FREE DOWNLOAD BY"])
        case 2:
            make_textsprite(["TYLER_MON & FUNNE"])

        case 4:
            textsprites.clear()
            textspriteyshift = -50
            make_textsprite(["PORTED TO"])
        case 6:
            make_textsprite(["PYGAME BY"])
        case 7:
            make_textsprite(["KAYLA"])
        case 8:
            textsprites.clear()
            textspriteyshift = 0
            make_textsprite(["like this"])
        case 10:
            make_textsprite(["like this"])
        case 12:
            textsprites.clear()
            textspriteyshift = -50
            make_textsprite(["FNF"])
        case 13:
            make_textsprite(["FREE"])
        case 14:
            make_textsprite(["DOWNLOAD"])
        case 15:
            make_textsprite(["PYGAME PORT"])
        case 16:
            globals.gamestate = "freeplay"
        
        case _:
            changed_textsprites = False

    if changed_textsprites:
        grp.empty()
        grp.add(textsprites)

    

def make_textsprite(lines = ["I ERRORS..."]):
    global textsprites, grp

    fontheight = small_font.get_height()*2
    linebuf = 30*2
    # int totalHeight = fm.getHeight() * lines.length + (lineBufferHeight*lines.length-1);
    totalheight = fontheight*(len(lines)+len(textsprites))+(linebuf*(len(lines)+len(textsprites)))
    for i in range(len(textsprites), len(lines)+len(textsprites)):
        line = lines[i-len(textsprites)]

        textsurf = pygame.transform.scale_by(small_font.render(line, False, (255,255,255)), 2)
        # this fucking sucks
        textsprite = StaticSprite(200-textsurf.width/2, 200-(((totalheight/2)/(len(lines)+len(textsprites)))*((len(lines))-(i)))-fontheight/2+textspriteyshift, textsurf)
        print(textsprite.x, textsprite.y)

        textsprites.append(textsprite)
        #print("made textsprite")