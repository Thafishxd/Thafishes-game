import config
import pygame
import numpy
import hashlib

class Object:
    def __init__(self, name, x, y, size, color, dialogue, map):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dialogue = dialogue
        self.map = map

        seed = int(hashlib.md5(f"{name}{sum(color) * 10}".encode()).hexdigest()[:8], 16)
        frequency = numpy.random.default_rng(seed).integers(300, 700)

        sample_rate = 44100
        sound_duration = 0.05

        t = numpy.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

        wave = numpy.sin(2 * numpy.pi * frequency * t)
        fade_samples = int(sample_rate * 0.005)

        fade_in = numpy.linspace(0, 1, fade_samples)
        fade_out = numpy.linspace(1, 0, fade_samples)

        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out

        audio = (wave * 15000).astype(numpy.int16)
        self.sound = pygame.sndarray.make_sound(numpy.column_stack((audio, audio)))

class Player:
    def __init__(self, name, x, y, speed, size, color):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = speed

def init():
    global player, NPC
    player = Player("Yoinky Yoinky", config.WIDTH//2, config.HEIGHT//2, 8, 32, (0, 120, 255))
    NPC = [
        Object("Sarah", 450, 150, 32, (255, 0, 0), [(10000, "Yo It's still in progress"), (5000, "Stay tuned! ...")], 1),
        Object("Stupid", 100, 150, 32, (0, 60, 60), [(5000, "I'm stupid"), (5000, "...")], 2)
    ]
init()