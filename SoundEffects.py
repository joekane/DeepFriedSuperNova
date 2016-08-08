import pygame
import Constants


# MUSIC

music_library = {
    'SSA': 'Sound/ssa_test.mp3',
    'MAIN_MENU': 'Sound/test.mp3'
    }

sound_library = {
    'PUNCH' : 'Sound/test.wav'
}

current_track = None


def initilize():
    pygame.init()
    pygame.mixer.init()


def play_music(music_name):
    global current_track
    if Constants.MUSIC_ON:
        if current_track is not music_name:
            if music_name in music_library:
                current_track = music_name
                music_filename = music_library[music_name]
                pygame.mixer.music.load(music_filename)
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play()


def play_sound(sound_name):
    if Constants.SOUND_ON:
        if sound_name in sound_library:
            sound_filename = sound_library[sound_name]
            sound = pygame.mixer.Sound(sound_filename)
            sound.play()








