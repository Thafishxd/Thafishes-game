import pygame
import config
from draw import core

def draw_map_objects(mw, cam_x, cam_y, scale):
    match config.current_map:
        case 0: pass
        case 1: pass
        case 2: pass
        case 3: pass

        case 4:
            sx1, sy1 = core.to_screen(0, 370, cam_x, cam_y, scale)
            pygame.draw.rect(config.screen, (0, 0, 255), (int(sx1), int(sy1), mw//2 - 25, 10))

            sx2, sy2 = core.to_screen(mw//2 + 50, 370, cam_x, cam_y, scale)
            pygame.draw.rect(config.screen, (0, 0, 255), (int(sx2), int(sy2), mw//2 - 25, 10))

        case 5: pass