import pygame, os, sys
sys.path.append('../base')

from base.player import Player


class Game():
    def __init__(self,game_id):
        self.game_id = game_id
        self.enemies = []
        self.players = {}
        self.bullets = []
        self.props = []
        self.running_state = False
