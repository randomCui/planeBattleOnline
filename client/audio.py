import pygame
from audio_lib import music_path


class Audio:
    def __init__(self):
        # 初始化背景音乐
        pygame.mixer.music.load(music_path['BGM'])
        # 设置背景音乐音量
        pygame.mixer.music.set_volume(0.5)

    def play_BGM(self):
        # 播放BGM
        pygame.mixer.music.play(loops=-1)

    def pause_BGM(self):
        # 暂停BGM
        pygame.mixer.music.pause()

    def unpause_BGM(self):
        # 从暂停状态恢复
        pygame.mixer.music.unpause()

    def restart_BGM(self):
        # 重新开始BGM
        pygame.mixer.music.load(music_path['BGM'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)

    def add_sound_effect(self, sound_list):
        # 添加不同的音效
        for name in sound_list:
            pygame.mixer.find_channel(True).play(
                pygame.mixer.Sound(music_path[name])
            )
