import pygame

import cProfile, pstats, os


import globals

from states import stage
from states import freeplay


def get_module_from_state(state):
    match state:
        case "stage":
            return stage
        case "freeplay":
            return freeplay
def run_state_machine():
    last_gamestate = ""
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