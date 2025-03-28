import math

# most of this has not been tested

class Conductor():
    def __init__(self):
        self.bpm = 60.0

        self._time = 0.0
        self._last_time = 0.0

    # time
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, new):
        self._last_time = self._time
        self._time = new


    # crochet
    def get_crochet(self):
        return 60 / self.bpm

    def get_crochet_sec(self):
        return self.get_crochet() * 2


    # beat
    @property
    def beat_float(self):
        return self._time / self.get_crochet()

    @property
    def beat(self):
        return math.floor(self.beat_float)


    # step
    @property
    def step_float(self):
        return self.beat_float * 4

    @property
    def step(self):
        return math.floor(self.step_float)

    @property
    def section_float(self):
        return self.beat_float / 4

    @property
    def section(self):
        return math.floor(self.section_float)