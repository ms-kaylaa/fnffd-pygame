import pygame

import globals
from globals import screen, FPS, small_font, MUS_DIRECTORY, clock

from classes.upscale_group import UpscaleGroup

from util.conductor import Conductor

texts:list[pygame.Surface] = []

conductor:Conductor = None
last_beat = -1

def init():
    global last_beat, conductor, texts
    last_beat = -1

    conductor = Conductor()
    conductor.bpm = 115

    pygame.mixer.music.load(MUS_DIRECTORY + "mus_game.ogg")
    pygame.mixer.music.play(-1)
    pass

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
            print("beat hit")

        for text in texts:
            screen.blit(text[0],text[1])

        globals.screen_shader.render()
        pygame.display.flip()

def handle_beatstep():
    match conductor.beat:
        case 0:
            draw_text("FREE DOWNLOAD BY")
        case 2:
            draw_text("TYLER_MON & FUNNE",1)
        case 4:
            texts.clear()
            draw_text("PORTED TO")
        case 6:
            draw_text("PYGAME BY",1)
        case 7:
            draw_text("KAYLA",2)
            # i'm not making a function for this
            newtext = small_font.render("with contributions from hexose :]", False, (255,255,255))
            newtext = pygame.transform.scale_by(newtext, 2)
            rect = newtext.get_rect(center=(400,600))
            texts.append([newtext,rect])
        case 8:
            texts.clear()
            draw_text("like this")
        case 10:
            draw_text("like this",1)
        case 12:
            texts.clear()
            draw_text("FNF")
        case 13:
            draw_text("FREE",1)
        case 14:
            draw_text("DOWNLOAD",2)
        case 15:
            draw_text("PYGAME PORT",3)
        case 16:
            globals.gamestate = "freeplay"
        
def draw_text(txt = "I ERRORS...",y=0):
    # i dont know if this is better or worse!
    global texts
    newtext = small_font.render(txt, False, (255,255,255))
    newtext = pygame.transform.scale_by(newtext, 4)
    rect = newtext.get_rect(center=(400,280+70*y))
    texts.append([newtext,rect])