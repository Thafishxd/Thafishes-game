import pygame
import config
import object

class Map:
    def __init__(self, size, color, walls):
        self.size = size
        self.color = color
        self.walls = [pygame.Rect(*wall) for wall in walls]

# --- WORLD DATA ---
w = config.WIDTH
h = config.HEIGHT
MAPS = [
    Map((w,   h),   (15,  15,  15),  [(0,    0, 10,  h),  (0,      0,    w,  10),  (0,      h-10,   w,   10)]),
    Map((w,   h),   (245, 245, 245), [(w-10, 0, 10,  h),  (0,      h-10, w,  10)]),
    Map((w,   h),   (80,  80,  80),  [(0,    0, 10,  h)]),
    Map((w,   h),   (0,   180, 180), [(0,    0, w,   10), (0,      h-10, w,  10)]),
    Map((w*2, h*2), (25,  35,  55),  [(0,    0, w*2, 10), (0,      0,    10, h*2), (w*2-10, 0,      10,  h*2), (0, 370, w, 10), (w + 50, 370, w, 10)]),
    Map((w*2, h*2), (255, 210, 0),   [(0,    0, w*2, 10), (w*2-10, 0,    10, h*2), (0,      h*2-10, w*2, 10)])
]

def get_world_objects(map_id):
    walls = MAPS[map_id].walls

    for npc in object.NPC:
        if map_id == npc.map:
            walls.append(pygame.Rect(npc.x, npc.y, npc.size, npc.size))
    
    return walls