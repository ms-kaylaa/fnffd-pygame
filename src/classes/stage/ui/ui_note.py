from classes.sprites.animated_sprite import AnimatedSprite

class UINote(AnimatedSprite):
    def __init__(self, x, y, dir, noteskin_postfix = "funny"):
        super().__init__(x, y, "ui/notes/notes_" + noteskin_postfix, 255, 0, 1)

        match (dir):
            case 0:
                self.dir = "left"
            case 1:
                self.dir = "down"
            case 2:
                self.dir = "up"
            case 3:
                self.dir = "right"

        self.show_frame("ui " + self.dir, 0)

        self.alpha_timer = 0

    def ui_press(self):
        self.alpha_timer = 6
        self.alpha = 128
        self.color = (128,128,128,255)
        self.update_image(True)

    def update(self, dt):
        if self.alpha_timer > 0:
            self.alpha_timer -= dt
            if self.alpha_timer <= 0:
                self.alpha_timer = 0
                self.alpha = 255
                self.color = (255,255,255,255)
                self.update_image()