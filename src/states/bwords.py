import pygame

import random

import globals
from globals import screen, FPS, small_font, MUS_DIRECTORY, clock

from classes.upscale_group import UpscaleGroup

from util.awesome_util import get_discord_pfp
from util.conductor import Conductor

texts:list[pygame.Surface] = []

kayla_pfp:pygame.Surface = None
hex_pfp:pygame.Surface = None

conductor:Conductor = None
last_beat = -1

introtexts = []
chosentext = []

def init():
    global last_beat, conductor, texts, kayla_pfp,hex_pfp, introtexts, chosentext
    last_beat = -1

    conductor = Conductor()
    conductor.bpm = 115

    kayla_pfp = pygame.transform.smoothscale_by(get_discord_pfp(1135951334651207701), 0.5)
    hex_pfp = get_discord_pfp(587298000439869463, "small") # little image for little contributions!

    pygame.mixer.music.load(MUS_DIRECTORY + "mus_game.ogg")
    pygame.mixer.music.play(-1)

    with open(globals.DATA_DIRECTORY + "introtexts.txt") as f:
        for line in f.readlines():
            introtexts.append(line.split("--"))

    chosentext = random.choice(introtexts)

def run():
    global last_beat, conductor,texts
    while globals.gamestate == "bwords":
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.gamestate = pygame.QUIT
                return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pygame.mixer.music.set_pos(8.35)
            globals.gamestate = "freeplay"

        conductor.time = pygame.mixer.music.get_pos()/1000
        if conductor.beat > last_beat:
            last_beat = conductor.beat
            handle_beatstep()

        for text in texts:
            screen.blit(text[0],text[1])

        if conductor.beat == 7 and (kayla_pfp != None and hex_pfp != None):
            screen.blit(kayla_pfp, kayla_pfp.get_rect(center=(400,550)))
            screen.blit(hex_pfp, (10, 800-hex_pfp.height-10))

        globals.screen_shader.render()
        pygame.display.flip()

def handle_beatstep():
    match conductor.beat:
        case 0:
            draw_text("FREE DOWNLOAD  BY")
        case 2:
            draw_text("TYLER_MON  &  FUNNE",1)
        case 4:
            texts.clear()
            draw_text("PORTED  TO", -1)
        case 6:
            draw_text("PYGAME  BY",)
        case 7:
            draw_text("KAYLA",1)
            # i'm not making a function for this
            newtext = small_font.render("with  contributions  from  hexose  :]", False, (255,255,255))
            newtext = pygame.transform.scale_by(newtext, 2)
            rect = newtext.get_rect(bottomleft=(150,790))
            texts.append([newtext,rect])
        case 8:
            texts.clear()
            draw_text(chosentext[0])
        case 10:
            draw_text(chosentext[1],1)
        case 12:
            texts.clear()
            draw_text("FNF")
        case 13:
            draw_text("FREE",1)
        case 14:
            draw_text("DOWNLOAD",2)
        case 15:
            draw_text("PYGAME  PORT",3)
        case 16:
            globals.gamestate = "freeplay"
        
def draw_text(txt = "I ERRORS...",y=0):
    # i dont know if this is better or worse!
    global texts
    newtext = small_font.render(txt, False, (255,255,255))
    newtext = pygame.transform.scale_by(newtext, 4)
    rect = newtext.get_rect(center=(400,280+70*y))
    texts.append([newtext,rect])