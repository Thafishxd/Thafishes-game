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

        seed = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) ^ (sum(color) * 5)
        frequency = numpy.random.default_rng(seed).integers(300, 700)

        sample_rate = 44100
        sound_duration = 0.05

        t = numpy.linspace(0, sound_duration, int(sample_rate * sound_duration), endpoint=False)

        wave = numpy.sin(2 * numpy.pi * frequency * t)
        fade_samples = int(sample_rate * 0.005)

        wave[:fade_samples] *= numpy.linspace(0, 1, fade_samples)   # Fade in
        wave[-fade_samples:] *= numpy.linspace(1, 0, fade_samples)  # Fade out

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

    zero_width_10x = config.ZERO_WIDTH_CHAR * 10
    NPC = [
        Object("Sarah", 450, 150, 32, (255, 0, 0), [(8000, "Yo It's still in progress"), (5000, "Stay tuned! ...")], 1),
        Object("Stupid", 100, 150, 32, (0, 60, 60), [(5000, "I'm stupid"), (5000, f".{zero_width_10x}.{zero_width_10x}.")], 2),
        Object("???", 2236, 536, 32, (155, 0, 60), [(5000, "Have you seen <Stupid>?"), (5000, f"She is truly,{zero_width_10x} genuinely stupid"), (5000, f"yeah {zero_width_10x}.{zero_width_10x}.{zero_width_10x}.{zero_width_10x}")], 5),
        Object("One of the fish", 200, 55, 32, (130, 20, 99), [(5000, "The decisions are made by The fishes ..."), (5000, "Also, Sarah likes femboys")], 3)
    ]
init()