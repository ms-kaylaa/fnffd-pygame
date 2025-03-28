from classes.sprites.animated_sprite import AnimatedSprite

class Note(AnimatedSprite):
    def __init__(self, x, y, dir, note_type, noteskin_postfix, noteskin_prefix = "notes_"):
        super().__init__(x, y, "ui/notes/" + noteskin_prefix + noteskin_postfix, 255, 0, 1)
        self.yy = self.y

        self.note_type = note_type

        self.dir_int = dir
        match (dir):
            case 0:
                self.dir = "left"
            case 1:
                self.dir = "down"
            case 2:
                self.dir = "up"
            case 3:
                self.dir = "right"

        if self.note_type == 8 or self.note_type == 9:
            self.dir = "hold " + self.dir

        
        # type list:
        # 0 = none
        # 1 = normal
        # 2 = alt anim
        # 3 = bomb
        # 4 = dudecam
        # 5 = bothcam
        # 6 = badguy cam
        # 7 = ayy
        # 8 = hold
        # 9 = alt hold
        # 10 = event

        # anyway assign solid/autohits
        solid_notetypes = [1, 2, 3, 8, 9, 12]
        self.solid = True if self.note_type in solid_notetypes else False

        self.show_frame(self.dir, 0)