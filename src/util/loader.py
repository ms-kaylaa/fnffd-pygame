import pygame
import pyvidplayer2
import xml.etree.ElementTree as et

from globals import IMG_DIRECTORY, SND_DIRECTORY, MUS_DIRECTORY, VID_DIRECTORY

# utility class for loading game assets

# cached filetypes
image_cache = {}
def load_image(filename) -> pygame.Surface:
    if not ".png" in filename:
        filename += ".png"
    if filename in image_cache:
        return image_cache[filename]
    
    try:
        image = pygame.image.load(IMG_DIRECTORY + filename)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Failed to load image: {IMG_DIRECTORY + filename}")
        pygame.quit()

    image_cache[filename] = image
    return image

video_cache = {}
def load_video(filename) -> pyvidplayer2.Video:
    if filename in video_cache:
        return video_cache[filename]

    try:
        video = pyvidplayer2.Video(VID_DIRECTORY + filename)
    except FileNotFoundError:
        print(f"Failed to load video: {VID_DIRECTORY +  filename}")

    video_cache[filename] = video
    return video

xml_cache = {}
def load_xml(filename) -> dict:
    if filename in xml_cache:
        return xml_cache[filename]
    
    root = et.parse(IMG_DIRECTORY + filename + ".xml").getroot()

    animations = {}

    parsing = None
    this_animation_data = {}

    """
    animations:
        {
        animation name:
            {
            0000:
                [x, y, width, height, frame_x, frame_y, frame_width, frame_height]
            0001:
                [x, y, width, height, frame_x, frame_y, frame_width, frame_height]
            }
        }
    """

    for frame in root:
        name = frame.get("name")
        
        x = int(frame.get("x"))
        y = int(frame.get("y"))

        width = int(frame.get("width"))
        height = int(frame.get("height"))

        frame_x = int(frame.get("frameX"))
        frame_y = int(frame.get("frameY"))

        frame_width = int(frame.get("frameWidth"))
        frame_height = int(frame.get("frameHeight"))

        # hope and pray that the input doesnt have an animation with a "0" in its name :pray:
        name_trimmed = name[0:name.index("0")] # get the actual animation name, e.g. "dude idle0000" -> "dude idle"
        id = name[name.index("0"):name.index("0")+4] # get the animation id,    e.g. "dude idle0000" -> "0000"

        if parsing != name_trimmed:
            # lock in (haha thats a funny term!) the already parsed animation data
            # but first make sure it's valid
            if parsing != None:
                animations[parsing] = this_animation_data
            this_animation_data = {}
            parsing = name_trimmed
            #print(f"Now parsing {name_trimmed}")

        this_data = [x, y, width, height, frame_x, frame_y, frame_width, frame_height]     
        this_animation_data[id] = this_data
        #print(f"Parsed frame {id} of animation {name_trimmed}")
    
    # add the last parsed data to the animation data if it doesnt already exist (weird issue idk why it does that)
    if not parsing in animations:
        animations[parsing] = this_animation_data

    xml_cache[filename] = animations
    return animations

# noncached filetypes