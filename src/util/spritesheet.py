import pygame

from util.loader import load_image, load_xml

class Spritesheet():
    def __init__(self, filename):
        self.name = filename
        self.sheet: pygame.Surface = load_image(filename + ".png")

        self.frame_data = load_xml(filename)

        self.cached_frames = {}



    def get_frame(self, name, frame_num = "0000"):
        frame_num = str(frame_num)

        # pad out to fit the "0000" format
        while len(frame_num) < 4:
            frame_num = "0" + frame_num
        #print(self.frame_data)
        if name + frame_num in self.cached_frames:
            return self.cached_frames[name + frame_num]
        #print("getting data " + name)
        data = self.frame_data[name][frame_num]

        # index legend: 0 = x, 1 = y, 2 = width, 3 = height
        frame_raw = self.sheet.subsurface(data[0], data[1], data[2], data[3])
        #frame = pygame.transform.scale2x(frame)

        # make it as big as its meant to be (and put it where its meant to be)
        # index legend: 0 = frameX, 1 = frameY, 2 = frameWidth, 3 = frameHeight
        framing_data = []
        for i in range(4):
            ii = i + 4
            framing_data.append(self.frame_data[name][frame_num][ii])

        frame_surf = pygame.Surface((framing_data[2], framing_data[3]), pygame.SRCALPHA).convert_alpha()
        frame_surf.blit(frame_raw, (-framing_data[0],-framing_data[1]))  # frameX, frameY


        self.cached_frames[name + frame_num] = frame_surf
        return frame_surf


    def get_animation(self, name, indices = []):
        ret = []
        #print(self.frame_data)
        if len(indices) == 0:
            for index in self.frame_data[name]:
                #print(index)
                ret.append(self.get_frame(name, index))
        else:
            for index in indices:
                ret.append(self.get_frame(name, index))

        return ret