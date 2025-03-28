def lerp(a, b, f):
    '''
    "LERP IT!" -gunk, probably
    '''
    return (a * (1.0 - f)) + (b * f)

def clamp(val, low, high):
    return max(low, min(val, high))