import pygame
from base.config import music_path


class Audio:
    def __init__(self):
        pygame.mixer.music.load(music_path['BGM'])
        pygame.mixer.music.set_volume(0.5)
        self.next_available_channel = 1

    def play_BGM(self):
        pygame.mixer.music.play(loops=-1)

    def pause_BGM(self):
        pygame.mixer.music.pause()

    def unpause_BGM(self):
        pygame.mixer.music.unpause()

    def restart_BGM(self):
        pygame.mixer.music.load(music_path['BGM'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    def add_sound_effect(self, sound_list):
        for name in sound_list:
            pygame.mixer.find_channel(True).play(
                pygame.mixer.Sound(music_path[name])
            )
