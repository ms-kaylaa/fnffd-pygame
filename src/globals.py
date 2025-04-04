import pygame, pygame.mixer, pygame.freetype
import pygame_shaders

# -= PYGAME SETUP =- #

# window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

FPS = 60

# pygame init stuff

pygame.init()
pygame.mixer.init()
pygame.freetype.init()

opengl_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("FNF FREE DOWNLOAD")
screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
screen_shader = pygame_shaders.DefaultScreenShader(screen)
clock = pygame.time.Clock()

# -= default options =- #
options = {
    # visual options
    "shaders_enabled": True,

    # binds
    "bind_left": pygame.K_d,
    "bind_down": pygame.K_f,
    "bind_up": pygame.K_j,
    "bind_right": pygame.K_k,

    "bind_select": pygame.K_RETURN,
    "bind_back": pygame.K_ESCAPE
}
scores = {
    "mus_w3s2_old": [-50, 2]
}

# -= game vars -= #
small_font = pygame.font.Font("assets/fnt/fnt-comic1.ttf", 14)
default_font = pygame.font.Font(None, 25)
gamestate = "freeplay"
volume = 1

# -= DIRECTORIES =- #

# general assets (assets that dont fit a (sub)category)
ASSETS_DIRECTORY = "assets/"

IMG_DIRECTORY = ASSETS_DIRECTORY + "img/" # images
SND_DIRECTORY = ASSETS_DIRECTORY + "snd/" # sounds
MUS_DIRECTORY = ASSETS_DIRECTORY + "mus/" # music
VID_DIRECTORY = ASSETS_DIRECTORY + "vid/" # videos
FNT_DIRECTORY = ASSETS_DIRECTORY + "fnt/" # fonts

# data directories (plaintext files/data structures)
DATA_DIRECTORY = ASSETS_DIRECTORY + "data/"

CHR_DIRECTORY = DATA_DIRECTORY + "chr/" # characters
SWS_DIRECTORY = DATA_DIRECTORY + "sws/" # charts
SHAD_DIRECTORY= DATA_DIRECTORY + "shad/"# shaders

# in case ffmpeg doesnt exist (meaning videos cant play)
HAS_FFMPEG = True # assume it exists until proven wrong