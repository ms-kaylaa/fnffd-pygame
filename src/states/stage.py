import pygame
import pygame_shaders

import math


import globals

from util import awesome_util
from util import loader
from util.conductor import Conductor
from util.spritesheet import Spritesheet

from globals import screen, clock, FPS, MUS_DIRECTORY, SWS_DIRECTORY

from classes.sprites.static_sprite import StaticSprite
from classes.sprites.animated_sprite import AnimatedSprite
from classes.sprites.video_sprite import VideoSprite

from classes.stage.character import Character

from classes.stage.ui.ui_note import UINote
from classes.stage.ui.note import Note

from classes.stage.ui.health_bar import HealthBar

from classes.upscale_group import UpscaleGroup
from classes.camera import Camera

from stages.base_stage import BaseStage

# per-init vars

# cam an ui
grp:Camera = None

cam_targ_x = 0
cam_targ_y = 0

ui_group:UpscaleGroup = None

# characters and stage
dude:Character = None
badguy:Character = None
lady:Character = None

stage:BaseStage = None

# ui stuff
bar:HealthBar = None

last_fps_str = ""
fps_surf: pygame.Surface = None
evil_fps_surf: pygame.Surface = None

# STUPID
vidsprite:VideoSprite = None

prebuffer_window = 2.0  # seconds
video_buffer_start = -1

# beat stuff
conductor:Conductor = None
last_beat = -1
beat_hit_zoom_interval, beat_hit_zoom_amount, beat_hit_character_idle_interval = 0, 0, 0

songlength = None
songlong = None
songbeat = None

# game stuff
paused = False

player_ui_notes = []
badguy_ui_notes = []

player_notes = []
badguy_notes = []

notes: list[list[Note]] = []

# input
pressed_keys = [False, False, False, False]

enter_pressed = False
b_pressed = False # shader debug

def check_note(id, anim):
    global note_xoff, note_yoff
    hit_note = False
    for note in player_notes:
        if note.rect.colliderect(player_ui_notes[id].rect) and note.solid:
            #print(note.note_type)
            note.kill()
            player_notes.remove(note)

            if note.note_type != 1 and note.note_type != 8 and note.note_type != 2 and note.note_type != 7 and note.note_type != 4 and note.note_type != 5 and note.note_type != 6:
                print("dude hit special note: " + str(note.note_type))

            hit_note = True
            bar.flow = awesome_util.clamp(bar.flow + 0.01, 0, 1)
            bar.skill = awesome_util.clamp(bar.skill - 1, 0, 100)

            bar.coolscore += 100

            if note.note_type == 2:
                anim += "-alt"

            dude.play_animation(anim)
            break

    if not hit_note: # you tried to hit a note when there were no notes to hit
        bar.flow = 0
        bar.skill = awesome_util.clamp(bar.skill + 5, 0, 100)
        bar.misses+=1

def check_hold_note(id, anim):
    for note in player_notes:
        if note.rect.colliderect(player_ui_notes[id].rect.scale_by(1, 0.2)) and (note.note_type == 8 or note.note_type == 9):
            note.kill()
            player_notes.remove(note)
            hit_note = True
            bar.flow = awesome_util.clamp(bar.flow + 0.01, 0, 1)
            bar.skill = awesome_util.clamp(bar.skill - 1, 0, 100)

            bar.coolscore+=25

            dude.play_animation(anim)
            break

def execute_special_note(note_type, player_note):
    global cam_targ_x, cam_targ_y, event_hit, event_num, targ_cam_zoom, grp, video_start_time, note_xoff, note_yoff, vidsprite
    char_hit = dude if player_note else badguy
    #print ("execcing " + str(note_type))
    match note_type:
        case 4:
            # dudecam
            cam_targ_x = dude.x-350
            cam_targ_y = dude.y-400
        case 6:
            # badguy cam
            cam_targ_x = badguy.x-150
            cam_targ_y = badguy.y-400
        case 7:
            char_hit.play_animation(char_hit.ayy_anim)
            # todo: ayy sound

        case 10:
            # todo: scalability
            global beat_hit_zoom_amount, beat_hit_zoom_interval
            print(f"this is event num {event_num}!")
            match event_num:
                case 0:
                    targ_cam_zoom = 1.4
                    stage.colorto = (75,46,112,255)
                case 1:
                    targ_cam_zoom = 1.15
                    grp.fade_color = (255, 255, 255)
                    grp.fade_alpha = 128
                    grp.fade_speed = -15

                    #stage.colorto = (0, 0, 255)

                    beat_hit_zoom_amount = .03
                    beat_hit_zoom_interval = 4
                case 2:
                    grp.fade_alpha = 0
                    grp.fade_speed = 15
                case 3:
                    grp.fade_alpha = 255
                    grp.fade_speed = -10
                    beat_hit_zoom_amount = .06
                    beat_hit_zoom_interval = 1
                case 4:
                    grp.fade_alpha = 0
                    grp.fade_color = (0,0,0)
                    grp.fade_speed = 7
                case 5:
                    grp.fade_alpha = 255
                    grp.fade_speed = -7

            event_num += 1

        # custom video notetype (thanks for custom notetypes hexose)
        # no problem - hexose
        case 13:
            print("starting video")
            video_start_time = pygame.mixer.music.get_pos() / 1000
            
            vidsprite.video.toggle_pause()
            event_hit = True


def init():
    global dude, badguy, lady, songlong, songbeat, notes, vidsprite, songlength, video_buffer_start
    dude = Character.load_from_json("dude")
    dude.x, dude.y = 525, 290
    dude.xx, dude.yy = 525, 290
    dude.play_animation("idle")

    badguy = Character.load_from_json("cdhack")
    badguy.x, badguy.y = 280, 290
    badguy.xx, badguy.yy = badguy.x, badguy.y
    badguy.play_animation("idle")

    dude.shaders.append("silhouette")
    dude.shaders.append("shadow")
    dude.shaders.append("shadow")
    #dude.color = (128, 255, 128, 255)
    def getDOffset():
        return [-(1/dude.image.get_width())*4, (1/dude.image.get_height())*4]
    colorgo2 = (75/70/255, 46/70/255, 112/70/255, 0.41)
    dude.shaders_uniforms.append({"colorreplace": [75/255, 46/255, 112/255, 0.14], "ignoreRGB": [32/255,30/255,40/255]})
    dude.shaders_uniforms.append({"shadowColor": colorgo2, "shadowOffset": getDOffset, "ignoreRGB": [32/255,30/255,40/255]})
    dude.shaders_uniforms.append({"shadowColor": (0,0,0,0.34), "shadowOffset": getDOffset, "ignoreRGB": [32/255,30/255,40/255]})

    badguy.shaders = dude.shaders.copy()
    badguy.colorignorelist.append((255,255,255,255))
    #badguy.color = dude.color
    def getBOffset():
        return [(1/badguy.image.get_width())*4, (1/badguy.image.get_height())*4]
    badguy.shaders_uniforms.append({"colorreplace": [75/255, 46/255, 112/255, 0.14], "ignoreRGB": [1,1,1]})
    badguy.shaders_uniforms.append({"shadowColor": dude.shaders_uniforms[1]["shadowColor"], "shadowOffset": getBOffset, "ignoreRGB": [1,1,1]})
    badguy.shaders_uniforms.append({"shadowColor": dude.shaders_uniforms[2]["shadowColor"], "shadowOffset": getBOffset, "ignoreRGB": [1,1,1]})

    lady = StaticSprite(340, 275, loader.load_image("stage_assets/ladycutout.png")) # thanks avery
    lady.y -= lady.base_image.get_height()

    lady.shaders = dude.shaders.copy()
    lady.color = dude.color
    def getLOffset():
        return [0, (1/lady.image.get_height())*7]
    lady.shaders_uniforms.append({"colorreplace": [75/255, 46/255, 112/255, 0.14], "ignoreRGB": [1,1,1]})
    lady.shaders_uniforms.append({"shadowColor": dude.shaders_uniforms[1]["shadowColor"], "shadowOffset": getLOffset, "ignoreRGB": [1,1,1]})
    lady.shaders_uniforms.append({"shadowColor": dude.shaders_uniforms[2]["shadowColor"], "shadowOffset": getLOffset, "ignoreRGB": [1,1,1]})
    lady.update_image(True)

    dude.shaders.append("highlight")
    dude.shaders_uniforms.append({"toHighlight": [32/255, 30/255, 40/255], "highlightWith": [1,1,1]})

    global bar
    bar = HealthBar()

    global player_notes, player_ui_notes, badguy_notes, badguy_ui_notes, pressed_keys, notes, last_beat

    last_beat = 0

    player_ui_notes = []
    badguy_ui_notes = []

    player_notes = []
    badguy_notes = []

    notes = []

    # input
    pressed_keys = [False, False, False, False]

    song = "mus_w3s2-old"

    global conductor
    conductor = Conductor()

    file = open(SWS_DIRECTORY + song + ".swows")
    file.readline()
    bpm = int(file.readline())
    conductor.bpm = bpm
    notespeed = float(file.readline())
    file.readline()

    print(f"{bpm} {notespeed}")

    pygame.mixer.music.load(MUS_DIRECTORY + song + ".ogg")
    song_sound = pygame.mixer.Sound(MUS_DIRECTORY + song + ".ogg")

    songlength = song_sound.get_length()

    # var songlong=round(((audio_sound_length(obj_song.song)/60)*obj_song.bpm*4));
    songlong = round((song_sound.get_length()/60)*bpm*4)
    songbeat=((songlong/60*bpm*4)*(48*notespeed))

    global cam_targ_x, cam_targ_y
    cam_targ_x = 0
    cam_targ_y = 0

    global ui_group
    ui_group = UpscaleGroup()

    for bb in range(8):
        if bb < 4:
            myx = 16+(44*bb)
        else:
            myx = (234-20)+(44*(bb-4))
        
        downscroll_y = 352
        norm_y = 48

        sucker = UINote(myx, norm_y-20, bb%4)
        if bb >= 4:
            player_ui_notes.append(sucker)
        else:
            badguy_ui_notes.append(sucker)
        
        ui_group.add(sucker)
        #sucker.update_image()

        for b in range(songlong):
            type = int(file.readline())
            # 4 5 6 7 10
            if type != 0:
                prefix = "notes_"
                postfix = "funny"
                if type == 3 and bb > 3:
                    prefix = "tsu_notes_"
                    postfix = "funny"
                dingus = Note(myx, norm_y+(b*48*notespeed), bb%4, type, postfix, prefix)
                dingus.should_draw = False
                dingus.should_update = False
                if type == 3 and bb > 3:
                    dingus.solid = False
                if (type == 3 and bb <= 3) or type == 4 or type == 5 or type == 6 or type == 7 or type == 10:
                    dingus.alpha = 128
                    #dingus.update_image()
                if type == 11 or type == 12:
                    if type == 11:
                        dingus.alpha = 128//2

                    #dingus.update_image()
                    dingus.image.fill((0, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)

                if bb < 4:
                    badguy_notes.append(dingus)
                else:
                    player_notes.append(dingus)

                dingus.update_rect()
                if dingus.y < 400 and dingus.rect.bottom > 0:
                    dingus.should_draw = True
                    dingus.should_update = True

    notes = [player_notes, badguy_notes]
    

    file.close()

    ui_group.add(notes)
    ui_group.add(bar)

    # vidtest
    vid = loader.load_video("tsu-old.mp4")
    vidsprite = VideoSprite(vid)
    vidsprite.scroll_factor = pygame.math.Vector2(0, 0)
    vidsprite.rect.topleft = (0, 0)
    vidsprite.scale = 800/vidsprite.video.current_size[0]
    vidsprite.video.play()
    video_buffer_start = pygame.time.get_ticks() / 1000  # real time, not music time


    # stagehand LITE!
    global beat_hit_zoom_interval, beat_hit_zoom_amount, beat_hit_character_idle_interval
    beat_hit_zoom_interval = 10000000
    beat_hit_zoom_amount = .03
    beat_hit_character_idle_interval = 2

    bg_group = []
    fg_group = [] # idk if ill use this

    from stages.w3 import W3Stage
    global stage
    stage = W3Stage()
    match song:
        case 'mus_w3s2-old':
            badguy.x = 185
            badguy.y = 320 + dude.base_image.get_height()

            dude.x = 425
            dude.y = 320 + dude.base_image.get_height()
            
            bg_group = stage.make_bg_sprites()
            fg_group = stage.make_fg_sprites()

            #beat_hit_character_idle_interval = 1

    global grp
    grp = Camera(bg_group, lady, badguy, dude, fg_group)
    grp.pos = pygame.math.Vector2(200, 0)

    global note_xoff, note_yoff
    note_xoff = 0
    note_yoff = 0

    global targ_cam_zoom
    targ_cam_zoom = 1

    paused = False

    pygame.mixer.music.play()
    
    global event_hit
    event_hit = False
    global event_num
    event_num = 0
    global video_start_time
    video_start_time = -1

def run():
    global enter_pressed, b_pressed, paused, last_beat, last_fps_str, fps_surf, evil_fps_surf, notes, badguy_notes, badguy_ui_notes, player_notes, player_ui_notes, conductor
    while True:
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.gamestate = pygame.QUIT
                return
            #if event.type == pygame.MOUSEWHEEL:
            #    targ_cam_zoom += event.y * 0.03
            
        screen.fill((145, 207, 221))

        stage.update()

        keys = pygame.key.get_pressed()

        """
        if keys[pygame.K_LEFT]:
            cam_targ_x -= 5*dt
        if keys[pygame.K_DOWN]:
            cam_targ_y += 5*dt
        if keys[pygame.K_UP]:
            cam_targ_y -= 5*dt
        if keys[pygame.K_RIGHT]:
            cam_targ_x += 5*dt

        if keys[pygame.K_q]:
            grp.angle = -3
        if keys[pygame.K_e]:
            grp.angle = 3
        """

        if keys[pygame.K_9] and not b_pressed:
            globals.options["shaders_enabled"] = not globals.options["shaders_enabled"]
            b_pressed = True
        elif not keys[pygame.K_9]:
            b_pressed = False

        if keys[globals.options["bind_left"]] and not pressed_keys[0]:
            player_ui_notes[0].ui_press()
            pressed_keys[0] = True
            check_note(0, "singLEFT")
        elif not keys[globals.options["bind_left"]]:
            pressed_keys[0] = False
        elif pressed_keys[0]:
            check_hold_note(0, "singLEFT")

        if keys[globals.options["bind_down"]] and not pressed_keys[1]:
            player_ui_notes[1].ui_press()
            pressed_keys[1] = True
            check_note(1, "singDOWN")
        elif not keys[globals.options["bind_down"]]:
            pressed_keys[1] = False
        elif pressed_keys[1]:
            check_hold_note(1, "singDOWN")

        if keys[globals.options["bind_up"]] and not pressed_keys[2]:
            player_ui_notes[2].ui_press()
            pressed_keys[2] = True
            check_note(2, "singUP")
        elif not keys[globals.options["bind_up"]]:
            pressed_keys[2] = False
        elif pressed_keys[2]:
            check_hold_note(2, "singUP")
            
        if keys[globals.options["bind_right"]] and not pressed_keys[3]:
            player_ui_notes[3].ui_press()
            pressed_keys[3] = True
            check_note(3, "singRIGHT")
        elif not keys[globals.options["bind_right"]]:
            pressed_keys[3] = False
        elif pressed_keys[3]:
            check_hold_note(3, "singRIGHT")

        if keys[globals.options["bind_select"]] and not enter_pressed:
            enter_pressed = True
        elif not keys[globals.options["bind_select"]] and enter_pressed:
            enter_pressed = False
            paused = not paused
            if event_hit:
                vidsprite.video.toggle_pause()
            if paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()


        cam_lerp_amt = 0.075/2*dt

        if not paused and not event_hit:
            x_lerp = cam_targ_x
            if grp.pos[0] != cam_targ_x and abs(grp.pos[0] - cam_targ_x) > .7:
                x_lerp = awesome_util.lerp(grp.pos[0], x_lerp, cam_lerp_amt)
            y_lerp = cam_targ_y
            if grp.pos[1] != cam_targ_y and abs(grp.pos[1] - cam_targ_y) > .7:
                y_lerp = awesome_util.lerp(grp.pos[1], y_lerp, cam_lerp_amt)
            grp.pos = pygame.math.Vector2(x_lerp, y_lerp)
            #print(x_lerp,y_lerp)

            if grp.angle != 0:
                grp.angle = awesome_util.lerp(grp.angle, 0, 0.2)
                if grp.angle != 0 and (grp.angle < 0.05 != grp.angle > -0.05):
                    grp.angle = 0
                    print("snapped cam angle")

            if grp.zoom != targ_cam_zoom:
                grp.zoom = awesome_util.lerp(grp.zoom, targ_cam_zoom, 0.04)
                if grp.zoom != targ_cam_zoom and (grp.zoom < targ_cam_zoom + .005 != grp.zoom > targ_cam_zoom - .005):
                    grp.zoom = targ_cam_zoom  

            #dude.color = stage.colorfrom.lerp(stage.colorfrom.grayscale() // pygame.Color(3, 3, 3, 1), 0.8)
            #badguy.color = dude.color
            #lady.color = dude.color

            grp.update(dt)
        
        if not event_hit: grp.draw(screen)

        if globals.HAS_FFMPEG and event_hit:
            vidsprite.update(dt)
            # make sure we still have ffmpeg (itll be invalidated in update if we dont) before going any further
            if globals.HAS_FFMPEG and not vidsprite.video.buffering:
                relative_time = (pygame.mixer.music.get_pos() / 1000 - video_start_time)
                if abs(vidsprite.video.get_pos() - relative_time) > 0.15:
                    vidsprite.video.seek(relative_time, False)
                    print("im seeking... ahhh!!!!")
                screen.blit(vidsprite.image, vidsprite.rect) 
        elif globals.HAS_FFMPEG and not vidsprite.video.paused:
            current_real_time = pygame.time.get_ticks() / 1000
            if current_real_time - video_buffer_start >= prebuffer_window:
                vidsprite.video.toggle_pause()
                print("stopped prebuffer")

        

        ui_group.draw(screen)
        if not paused:
            for note in player_ui_notes + badguy_ui_notes:
                if note.rect.colliderect(ui_group.internal_rect): note.update(dt)
        bar.update(dt)

        if paused:
            pause_surf = pygame.Surface((800, 800), flags=pygame.SRCALPHA).convert_alpha()
            pause_surf.fill((0,0,0,128))
            screen.blit(pause_surf, (0,0))

        conductor.time = (pygame.mixer.music.get_pos() + 0.01) / 1000

        if last_beat < conductor.beat:
            if conductor.beat % beat_hit_character_idle_interval == 0:
                if not dude.animating or dude.cur_named_anim == "idle":
                    dude.play_animation("idle")
                if not badguy.animating or badguy.cur_named_anim == "idle":
                    badguy.play_animation("idle")

            if conductor.beat % beat_hit_zoom_interval == 0:
                grp.zoom += beat_hit_zoom_amount

            last_beat = conductor.beat

        dumb_song_progress = pygame.mixer.music.get_pos()/songlong
        #print(dumb_song_progress)
        ymod = (48+(dumb_song_progress/1000*songbeat))
        #print(ymod)

        # BIG NOTE HANDLER LOOP
        for note_list in notes:
            for note in note_list:
                note.y = note.yy - ymod
                if note.y < 400 and note.rect.bottom > -60: # cull offscreen notes
                    # re-enable drawing if it's offscreen
                    if not note.should_draw:
                        note.should_draw = True
                        note.should_update = True
                        note.update_image()

                    note.update_rect()
                    
                    # only do autohit checks if it's close enough
                    if note.y < 100:
                        # check special note autohit
                        if not note.solid:
                            player_autohit_con = note_list == player_notes and note.rect.move(0, note.rect.height/2).scale_by(1, 0.05).colliderect(player_ui_notes[note.dir_int].rect)
                            badguy_autohit_con = note.rect.move(0, note.rect.height/2).scale_by(1, 0.05).colliderect(badguy_ui_notes[note.dir_int].rect)

                            if player_autohit_con or badguy_autohit_con:
                                note.kill()
                                note_list.remove(note)
                                execute_special_note(note.note_type, note_list == player_notes)
                                continue

                        # check badguy autohit
                        if note_list == badguy_notes and note.solid:
                            badguy_autohit_con = note.rect.move(0, note.rect.height/2).scale_by(1, 0.05).colliderect(badguy_ui_notes[note.dir_int].rect)
                            if badguy_autohit_con:
                                badguy_notes.remove(note)
                                note.kill()

                                anim = ""
                                match note.dir_int:
                                    case 0:
                                        anim="singLEFT"
                                    case 1:
                                        anim="singDOWN"
                                    case 2:
                                        anim="singUP"
                                    case 3:
                                        anim="singRIGHT"

                                if note.note_type == 2:
                                    anim += "-alt"

                                badguy.play_animation(anim)
                                continue
                elif note.rect.bottom < -60 and note.solid:
                    note.kill()
                    note_list.remove(note)
                    if note_list == player_notes: # make sure you dont get dinged for the opponent missing
                        bar.misses += 1

        fps_str = f"FPS: {int(clock.get_fps())}"
        
        if fps_str != last_fps_str:
            fps_surf = globals.small_font.render(fps_str, False, pygame.Color(255,255,255))
            evil_fps_surf = globals.small_font.render(fps_str, False, pygame.Color(0,0,0,128))
        screen.blit(evil_fps_surf, (17, 17))
        screen.blit(fps_surf, (15, 15))
        last_fps_str = fps_str

        globals.screen_shader.render()

        pygame.display.flip()

        if not (pygame.mixer.music.get_busy() or paused):
            pygame.mixer.music.stop()
            globals.gamestate = "freeplay"
            return