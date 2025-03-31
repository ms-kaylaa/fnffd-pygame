import pygame

def lerp(a, b, f):
    '''
    "LERP IT!" -gunk, probably
    '''
    return pygame.math.lerp(a, b, f)

def clamp(val, low, high):
    return max(low, min(val, high))