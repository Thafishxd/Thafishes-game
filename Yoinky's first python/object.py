import config

class Object:
    def __init__(self, name, x, y, size, color, dialogue, map):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dialogue = dialogue
        self.map = map

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