import pygame

import io
import json
import requests

import globals

from util import loader

def lerp(a, b, f):
    '''
    "LERP IT!" -gunk, probably\n
    just use pygame.math.lerp
    '''
    return pygame.math.lerp(a, b, f)

def clamp(val, low, high):
    '''
    just use pygame.math.clamp
    '''
    return pygame.math.clamp(val, low, high)

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

# should this be in loader?
# maybe...

# this functions cool because the load speed for the video game actively depends on your internet speed!
def get_discord_pfp(id:int, imagesize = "") -> pygame.Surface:
    try:
        r = requests.get(f"http://avatar-cyan.vercel.app/api/pfp/{id}/{imagesize + "image"}")
        return pygame.image.load(io.BytesIO(r.content))
    except requests.ConnectionError as e:
        print("couldnt get pfp for some reason: " + str(e))
        return loader.load_image(f"backuppfps/bk{imagesize}")