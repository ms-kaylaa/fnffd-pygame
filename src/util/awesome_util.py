import pygame

import globals

def lerp(a, b, f):
    '''
    "LERP IT!" -gunk, probably
    '''
    return pygame.math.lerp(a, b, f)

def clamp(val, low, high):
    return max(low, min(val, high))

def play_snd(file:str):
    """
    plays a sound located in `globals.SND_DIRECTORY`, taking into account the current game volume

    returns the pygame.Channel instance in case you wanna do something with it
    """
    if not file.endswith(".ogg"):
        file += ".ogg"
    snd = pygame.Sound(f"{globals.SND_DIRECTORY}{file}")
    snd.set_volume(globals.volume)

    return snd.play()