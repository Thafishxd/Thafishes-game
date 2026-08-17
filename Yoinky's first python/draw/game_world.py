import pygame
import config
import object
import world
from draw import core
from draw import map_objects
from draw import dialogue

def draw_game_world():
    mw, mh = world.MAPS[config.current_map].size
    walls = world.get_world_objects(config.current_map)
    scale = min(config.WIDTH / mw, config.HEIGHT / mh) if config.debug_mode else 1.0
    cam_x = max(0, min(object.player.x - config.WIDTH // 2, mw - config.WIDTH))
    cam_y = max(0, min(object.player.y - config.HEIGHT // 2, mh - config.HEIGHT))

    config.screen.fill(world.MAPS[config.current_map].color)

    # MAP DRAWINGS
    map_objects.draw_map_objects(mw, cam_x, cam_y, scale)

    # GRID
    if config.debug_mode or config.current_map in [4, 5]:
        grid_col = (70, 70, 70) if config.current_map != 0 else (120, 120, 120)
        for x in range(0, mw + 1, 100):
            sx = core.to_screen(x, 0, cam_x, cam_y, scale)[0]
            pygame.draw.line(config.screen, grid_col, (sx, 0), (sx, int(mh*scale) if config.debug_mode else config.HEIGHT))

        for y in range(0, mh + 1, 100):
            sy = core.to_screen(0, y, cam_x, cam_y, scale)[1]
            pygame.draw.line(config.screen, grid_col, (0, sy), (int(mw*scale) if config.debug_mode else config.WIDTH, sy))

    # NPC
    for i in range(len(object.NPC)):
        if config.current_map != object.NPC[i].map: continue

        nx, ny = core.to_screen(object.NPC[i].x, object.NPC[i].y, cam_x, cam_y, scale)
        pygame.draw.rect(config.screen, object.NPC[i].color, (int(nx), int(ny), int(object.NPC[i].size*scale), int(object.NPC[i].size*scale)))

    # PLAYER
    px, py = core.to_screen(object.player.x, object.player.y, cam_x, cam_y, scale)
    pygame.draw.rect(config.screen, object.player.color, (int(px), int(py), int(object.player.size*scale), int(object.player.size*scale)))

    # DEBUG
    if config.debug_mode:
        cx, cy = core.to_screen(cam_x, cam_y, cam_x, cam_y, scale)
        pygame.draw.rect(config.screen, (255, 255, 255), (int(cx), int(cy), int(config.WIDTH*scale), int(config.HEIGHT*scale)), 2)
        pygame.draw.rect(config.screen, (255, 0, 0), (int(object.player.x), int(object.player.y), int(object.player.size*scale), int(object.player.size*scale)), 1)
        for wall in walls:
            wx, wy = core.to_screen(wall.x, wall.y, cam_x, cam_y, scale)
            pygame.draw.rect(config.screen, (255, 0, 0), (int(wx), int(wy), int(wall.width*scale), int(wall.height*scale)), 1)
        txt_c = (255,255,255) if config.current_map in [0, 4] else (0,0,0)
        config.screen.blit(config.font.render(
            f"DEBUG MODE | MAP: {config.current_map} | POS: {int(object.player.x)}, {int(object.player.y)}",
            True, txt_c
        ), (10, 10))

    # DIALOGUE
    if config.show_dialogue != None:
        if not dialogue.draw_dialogue():
            config.dialogue_timer = pygame.time.get_ticks()
            config.current_dialogue += 1
            if not config.current_dialogue < len(object.NPC[config.show_dialogue].dialogue):
                config.show_dialogue = None