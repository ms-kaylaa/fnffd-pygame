import pygame

import cProfile, pstats, os

import threading


import globals

from util.awesome_util import play_snd

from states import stage
from states import freeplay
from states import offseteditor


def get_module_from_state(state):
    match state:
        case "stage":
            return stage
        case "freeplay":
            return freeplay
        case "offseteditor":
            return offseteditor
        
def check_vol_binds():
    up_pressed, down_pressed = False, False
    while globals.gamestate != pygame.QUIT:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1] and not down_pressed:
            globals.volume = pygame.math.clamp(globals.volume - 0.1, 0, 1)
            
            play_snd("snd_ribbit2")

            down_pressed = True
        elif not keys[pygame.K_1]:
            down_pressed = False

        if keys[pygame.K_2] and not up_pressed:
            globalvollast = globals.volume
            globals.volume = pygame.math.clamp(globals.volume + 0.1, 0, 1)

            if globals.volume != 1 or globalvollast != 1:
                play_snd("snd_ribbit1")

            up_pressed = True
        elif not keys[pygame.K_2]:
            up_pressed = False

        pygame.mixer.music.set_volume(globals.volume)

def run_state_machine():
    last_gamestate = ""

    threading.Thread(target=check_vol_binds).start()
    
    while globals.gamestate != pygame.QUIT:
        state = get_module_from_state(globals.gamestate)

        if last_gamestate != globals.gamestate:
            state.init()
            last_gamestate = globals.gamestate
        
        #try:
        state.run()
        #except Exception as e:
        #    print(e)
        #    import sys
        #    sys.exit(1)

    pygame.quit()

if __name__ == "__main__":
    profile = True
    if profile:
        cProfile.run('run_state_machine()', 'debug/output.prof')

        with open("debug/profile_results.txt", "w") as f:
            stats = pstats.Stats('debug/output.prof', stream=f)
            stats.strip_dirs().sort_stats("cumulative").print_stats()
            os.remove('debug/output.prof')
    else:
        run_state_machine()