import pygame

import cProfile, pstats, os

import threading
import importlib

import globals

from util.awesome_util import play_snd

from states import stage
from states import freeplay
from states import offseteditor
from states import bwords

states_dict = {}
def load_states(): # adapted from party phil!
    states_dict.clear()
    base_path = "src/states"
    base_prefix = len(base_path) + 1  # get the index where stuff we care about shows up
    
    for root, _, files in os.walk(base_path):
        relative_root = root[base_prefix:].replace(os.sep, ".")  # convert to module path
        if relative_root.startswith("_") or relative_root.endswith("_"):
            continue  # skip backend stuff
        
        for file in files:
            if not file.endswith(".py") or file.startswith("_"):
                continue  # skip backend stuff
            
            name = file[:-3]  # remove extension
            module_path = f"states.{relative_root + '.' if relative_root else ''}{name}"
            states_dict[name] = importlib.import_module(module_path)

    print("finished loading states")

def get_module_from_state(state):
    return states_dict[state]
        
def check_vol_binds():
    up_pressed, down_pressed = False, False
    while globals.gamestate != pygame.QUIT:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_MINUS] and not down_pressed:
            globals.volume = pygame.math.clamp(globals.volume - 0.1, 0, 1)
            
            play_snd("snd_ribbit2")

            down_pressed = True
        elif not keys[pygame.K_MINUS]:
            down_pressed = False

        if keys[pygame.K_EQUALS] and not up_pressed:
            globalvollast = globals.volume
            globals.volume = pygame.math.clamp(globals.volume + 0.1, 0, 1)

            if globals.volume != 1 or globalvollast != 1:
                play_snd("snd_ribbit1")

            up_pressed = True
        elif not keys[pygame.K_EQUALS]:
            up_pressed = False

        pygame.mixer.music.set_volume(globals.volume)

def run_state_machine():
    last_gamestate = ""

    threading.Thread(target=check_vol_binds).start()
    load_states()
    
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