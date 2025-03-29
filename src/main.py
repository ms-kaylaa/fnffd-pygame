import pygame
import pygame_shaders

import math

import cProfile, pstats


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

def main():
    dude = Character.load_from_json("dude")
    dude.x, dude.y = 525, 290
    dude.xx, dude.yy = 525, 290
    dude.play_animation("idle")

    badguy = Character.load_from_json("cyan")
    badguy.x, badguy.y = 280, 290
    badguy.xx, badguy.yy = badguy.x, badguy.y
    badguy.play_animation("idle")

    #hb2 = StaticSprite(-35, 75, loader.load_image("stage_assets/backyard/houseback2.png"))
    #hb2.scroll_factor = pygame.math.Vector2(0.5, 0.5)

    lady = StaticSprite(340, 275, loader.load_image("stage_assets/ladycutout.png")) # thanks avery
    lady.y -= lady.base_image.get_height()

    bar = HealthBar()

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

    # var songlong=round(((audio_sound_length(obj_song.song)/60)*obj_song.bpm*4));
    songlong = round((song_sound.get_length()/60)*bpm*4)
    songbeat=((songlong/60*bpm*4)*(48*notespeed))

    ui_group = UpscaleGroup()

    player_ui_notes = []
    badguy_ui_notes = []

    player_notes = []
    badguy_notes = []

    global cam_targ_x, cam_targ_y
    cam_targ_x = 0
    cam_targ_y = 0

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
        sucker.update_image()

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
                    dingus.update_image()
                if type == 11 or type == 12:
                    if type == 11:
                        dingus.alpha = 128//2

                    dingus.update_image()
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
    vidsprite.video.toggle_pause()

    # stagehand LITE!
    bg_group = []
    fg_group = [] # idk if ill use this
    match song:
        case 'mus_w3s2-old':
            badguy.x = 185
            badguy.y = 320 + dude.base_image.get_height()

            dude.x = 425
            dude.y = 320 + dude.base_image.get_height()
            
            # budy
            wd = "stage_assets/buddy/"
            scarysin2 = round(2*(math.sin((pygame.time.get_ticks()-300)/350)))

            back = StaticSprite(40, scarysin2, loader.load_image(f"{wd}buddyback_3"))
            back.scroll_factor = (0.33, 0.33)

            tvs = StaticSprite(50, scarysin2-60, loader.load_image(f"{wd}buddyback_2"))
            tvs.scroll_factor = (0.25, 1)

            tvshade = StaticSprite(tvs.x, tvs.y, loader.load_image(f"{wd}buddyback_2"))
            tvshade.scroll_factor = tvs.scroll_factor
            tvshade.color = (0,0,0)
            tvshade.alpha = 255*0.15

            fore = StaticSprite(100, -40, loader.load_image(f"{wd}buddyback"))

            bg_group.append(back)
            bg_group.append(tvs)
            bg_group.append(tvshade)
            bg_group.append(fore)

    global grp
    grp = Camera(bg_group, lady, badguy, dude)
    grp.pos = pygame.math.Vector2(200, 0)

    global note_xoff, note_yoff
    note_xoff = 0
    note_yoff = 0

    global targ_cam_zoom
    targ_cam_zoom = 1

    i_pressed = False
    o_pressed = False

    enter_pressed = False
    paused = False

    pressed_keys = [False, False, False, False]

    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.75)

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

                # cool camera shift thing
                match note.dir_int:
                    case 0:
                        note_xoff = -10
                    case 1:
                        note_yoff = 10
                    case 2:
                        note_yoff = -10
                    case 3:
                        note_xoff = 10

                if note.note_type == 2:
                    anim += "-alt"

                dude.play_animation(anim)
                break

        if not hit_note:
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
    
    global event_hit
    event_hit = False
    global event_num
    event_num = 0
    global video_start_time
    video_start_time = -1
    def execute_special_note(note_type, player_note):
        global cam_targ_x, cam_targ_y, event_hit, event_num, targ_cam_zoom, grp, video_start_time, note_xoff, note_yoff
        char_hit = dude if player_note else badguy
        #print ("execcing " + str(note_type))
        match note_type:
            case 4:
                # dudecam
                cam_targ_x = dude.x-350
                cam_targ_y = dude.y-400
                note_xoff = note_yoff = 0
            case 6:
                # badguy cam
                cam_targ_x = badguy.x-150
                cam_targ_y = badguy.y-400
                note_xoff = note_yoff = 0
            case 7:
                char_hit.play_animation(char_hit.ayy_anim)
                # todo: ayy sound

            case 10:
                # todo: scalability
                global beat_hit_zoom_amount, beat_hit_zoom_interval
                match event_num:
                    case 0:
                        targ_cam_zoom = 1.4
                    case 1:
                        targ_cam_zoom = 1.15
                        grp.fade_color = (255, 255, 255)
                        grp.fade_alpha = 128
                        grp.fade_speed = -15

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

                event_num += 1

            # custom video notetype (thanks for custom notetypes hexose)
            # no problem - hexose
            case 13:
                print("starting video")
                video_start_time = pygame.mixer.music.get_pos() / 1000
                vidsprite.video.toggle_pause()
                vidsprite.video.seek(0.15)
                event_hit = True

    global beat_hit_zoom_interval, beat_hit_zoom_amount
    beat_hit_zoom_interval = 10000000
    beat_hit_zoom_amount = .03
    last_beat = -1

    last_fps_str= ""
    
    fps_surf: pygame.Surface = None
    evil_fps_surf: pygame.Surface = None

    while True:
        dt = (clock.tick(FPS) / 1000) * FPS # get delta time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            #if event.type == pygame.MOUSEWHEEL:
            #    targ_cam_zoom += event.y * 0.03
            
        screen.fill((145, 207, 221))

        keys = pygame.key.get_pressed()

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

        if keys[pygame.K_z]:
            badguy.ayy_anim = "snore up"
        if keys[pygame.K_x]:
            badguy.ayy_anim = "snore down"

        if keys[pygame.K_i] and not i_pressed:
            if not keys[pygame.K_LSHIFT]:
                grp.zoom += .03
            else:
                targ_cam_zoom += 0.1

            i_pressed = True
        if not keys[pygame.K_i]:
            i_pressed = False

        if keys[pygame.K_o] and keys[pygame.K_LSHIFT] and not o_pressed:
            targ_cam_zoom -= 0.1
            o_pressed = True
        if not keys[pygame.K_o]:
            o_pressed = False

        if keys[pygame.K_d] and not pressed_keys[0]:
            player_ui_notes[0].ui_press()
            pressed_keys[0] = True
            check_note(0, "singLEFT")
        elif not keys[pygame.K_d]:
            pressed_keys[0] = False
        elif pressed_keys[0]:
            check_hold_note(0, "singLEFT")

        if keys[pygame.K_f] and not pressed_keys[1]:
            player_ui_notes[1].ui_press()
            pressed_keys[1] = True
            check_note(1, "singDOWN")
        elif not keys[pygame.K_f]:
            pressed_keys[1] = False
        elif pressed_keys[1]:
            check_hold_note(1, "singDOWN")

        if keys[pygame.K_j] and not pressed_keys[2]:
            player_ui_notes[2].ui_press()
            pressed_keys[2] = True
            check_note(2, "singUP")
        elif not keys[pygame.K_j]:
            pressed_keys[2] = False
        elif pressed_keys[2]:
            check_hold_note(2, "singUP")
            
        if keys[pygame.K_k] and not pressed_keys[3]:
            player_ui_notes[3].ui_press()
            pressed_keys[3] = True
            check_note(3, "singRIGHT")
        elif not keys[pygame.K_k]:
            pressed_keys[3] = False
        elif pressed_keys[3]:
            check_hold_note(3, "singRIGHT")

        if keys[pygame.K_RETURN] and not enter_pressed:
            enter_pressed = True
        elif not keys[pygame.K_RETURN] and enter_pressed:
            enter_pressed = False
            paused = not paused
            if event_hit:
                vidsprite.video.toggle_pause()
            if paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()


        cam_lerp_amt = 0.075/2*dt

        if not paused:
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

            grp.update(dt)
        grp.draw(screen)

        if globals.HAS_FFMPEG and event_hit:
            vidsprite.update(dt)
            # make sure we still have ffmpeg (itll be invalidated in update if we dont) before going any further
            if globals.HAS_FFMPEG:
                relative_time = (pygame.mixer.music.get_pos()/1000 - video_start_time) #+ 0.15
                if abs(vidsprite.video.get_pos() - relative_time) > 0.15:
                    vidsprite.video.seek(relative_time, False) 
                screen.blit(vidsprite.image, vidsprite.rect) 
        

        for note in player_ui_notes + badguy_ui_notes:
            note.update(dt)
        bar.update(dt)
        ui_group.draw(screen)

        conductor.time = (pygame.mixer.music.get_pos() + 0.01) / 1000

        if last_beat < conductor.beat:
            if conductor.beat % 2 == 0:
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
                if note.y < 400 and note.rect.bottom > 0: # cull offscreen notes
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
        fps_str = f"FPS: {int(clock.get_fps())}"
        
        if fps_str != last_fps_str:
            fps_surf = globals.small_font.render(fps_str, False, pygame.Color(255,255,255))
            evil_fps_surf = globals.small_font.render(fps_str, False, pygame.Color(0,0,0,128))
        screen.blit(evil_fps_surf, (17, 17))
        screen.blit(fps_surf, (15, 15))
        last_fps_str = fps_str

        globals.screen_shader.render()

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    profile = True
    if profile:
        cProfile.run('main()', 'debug/output.prof')

        with open("debug/profile_results.txt", "w") as f:
            stats = pstats.Stats('debug/output.prof', stream=f)
            stats.strip_dirs().sort_stats("cumulative").print_stats()
    else:
        main()