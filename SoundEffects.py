import pygame

# MUSIC

music_library = { 'SSA': 'Sound/ssa_test.mp3', 'MAIN_MENU': 'Sound/test.mp3'  }
current_track = None

def initilize():
    pygame.init()
    pygame.mixer.init()


def play_music(music):
    global current_track
    if current_track is not music:
        if music in music_library:
            current_track = music
            file = music_library[music]
            pygame.mixer.music.load(file)
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play()










