import pygame as pg
import os

class Audio:
    '''Stores the audio used in the game'''
    audio=None
    music=None
    
    def __init__(self):
        self.audio={}
        self.music={}        
        self.audio["walk"] = pg.mixer.Sound(os.path.join(os.path.dirname(__file__),"footsteps_test.ogg"))
        self.audio["grab"] = pg.mixer.Sound(os.path.join(os.path.dirname(__file__),"grab.ogg"))
        self.music["test"] = pg.mixer.Sound(os.path.join(os.path.dirname(__file__),"pelimuzaa.ogg"))

    