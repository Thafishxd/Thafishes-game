import json
import pygame
import sys
import config
import object
import world
from draw import loading_screen
from draw import menu_screen
from draw import setting_screen
from draw import pause_screen
from draw import save_screen
from draw import game_world

if __name__ == "__main__":
    loading_screen.start_loading()

    # --- MAIN LOOP ---
    last_game_state = config.game_state
    while True:
        walls = world.get_world_objects(config.current_map)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                last_game_state = config.game_state
                match config.game_state:
                    case config.GameState.MENU:
                        if event.key == pygame.K_DOWN:
                            config.menu_selected = (config.menu_selected + 1) % len(config.MENU_ITEMS)
                        elif event.key == pygame.K_UP:
                            config.menu_selected = (config.menu_selected - 1) % len(config.MENU_ITEMS)
                        elif event.key == pygame.K_RETURN:
                            if config.menu_selected == 0:
                                config.init()
                                object.init()
                                config.game_state = config.GameState.GAME
                            elif config.menu_selected == 1:
                                with open("saves/save.json", "r") as f:
                                    data = json.load(f)
                                    object.player.name = data["player"]["name"]
                                    object.player.x = data["player"]["x"]
                                    object.player.y = data["player"]["y"]
                                    object.player.size = data["player"]["size"]
                                    object.player.color = data["player"]["color"]
                                    object.player.speed = data["player"]["speed"]
                                config.game_state = config.GameState.GAME
                            elif config.menu_selected == 2: config.game_state = config.GameState.SETTING
                            elif config.menu_selected == 3:
                                pygame.quit()
                                sys.exit()

                    case config.GameState.SETTING:
                        if event.key == pygame.K_DOWN:
                            config.settings_selected = (config.settings_selected + 1) % len(config.SETTINGS_ITEMS)
                        elif event.key == pygame.K_UP:
                            config.settings_selected = (config.settings_selected - 1) % len(config.SETTINGS_ITEMS)
                        elif event.key == pygame.K_RETURN:
                            if config.settings_selected == 0: config.debug_mode = not config.debug_mode
                            elif config.settings_selected == 3: config.game_state = config.GameState.PAUSE if last_game_state == config.GameState.PAUSE else config.GameState.MENU
                        elif event.key == pygame.K_LEFT:
                            if config.settings_selected == 1:
                                config.side_bracket_blink_interval = max(config.BLINK_SPEED_MIN, config.side_bracket_blink_interval - config.BLINK_SPEED_STEP)
                            elif config.settings_selected == 2:
                                config.side_bracket_ghost_travel = max(config.GHOST_TRAVEL_MIN, config.side_bracket_ghost_travel - config.GHOST_TRAVEL_STEP)
                        elif event.key == pygame.K_RIGHT:
                            if config.settings_selected == 1:
                                config.side_bracket_blink_interval = min(config.BLINK_SPEED_MAX, config.side_bracket_blink_interval + config.BLINK_SPEED_STEP)
                            elif config.settings_selected == 2:
                                config.side_bracket_ghost_travel = min(config.GHOST_TRAVEL_MAX, config.side_bracket_ghost_travel + config.GHOST_TRAVEL_STEP)
                        elif event.key == pygame.K_ESCAPE:
                            config.GameState.PAUSE if last_game_state == config.GameState.PAUSE else config.GameState.MENU

                    case config.GameState.PAUSE:
                        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            config.pause_selected = (config.pause_selected + 1) % len(config.PAUSE_ITEMS)
                        elif event.key == pygame.K_w or event.key == pygame.K_UP:
                            config.pause_selected = (config.pause_selected - 1) % len(config.PAUSE_ITEMS)
                        elif event.key == pygame.K_RETURN:
                            if config.pause_selected == 0: config.game_state = config.GameState.GAME
                            elif config.pause_selected == 1: config.game_state = config.GameState.SETTING
                            elif config.pause_selected == 2: config.game_state = config.GameState.SAVE
                        elif event.key == pygame.K_ESCAPE:
                            config.game_state = config.GameState.GAME
                    
                    case config.GameState.SAVE:
                        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            config.save_selected = (config.save_selected + 1) % len(config.SAVE_ITEMS)
                        elif event.key == pygame.K_w or event.key == pygame.K_UP:
                            config.save_selected = (config.save_selected - 1) % len(config.SAVE_ITEMS)
                        elif event.key == pygame.K_RETURN:
                            if config.save_selected == 0:
                                with open("saves/save.json", "w") as f:
                                    data = {
                                        "player": {
                                            "name": object.player.name,
                                            "x": object.player.x,
                                            "y": object.player.y,
                                            "size": object.player.size,
                                            "color": object.player.color,
                                            "speed": object.player.speed
                                        }
                                    }
                                    json.dump(data, f)
                                config.game_state = config.game_state = config.GameState.MENU
                            elif config.save_selected == 1: config.game_state = config.GameState.MENU
                            elif config.save_selected == 2: config.game_state = config.GameState.PAUSE
                        elif event.key == pygame.K_ESCAPE:
                            config.game_state = config.GameState.PAUSE

                    case config.GameState.GAME:
                        if event.key == pygame.K_ESCAPE:
                            config.game_state = config.GameState.PAUSE
                            pause_selected = 0
                        if event.key == pygame.K_F3:
                            config.debug_mode = not config.debug_mode

                        for i in range(len(object.NPC)):
                            if event.key == pygame.K_e and config.current_map == object.NPC[i].map:
                                dist = ((object.player.x - object.NPC[i].x)**2 + (object.player.y - object.NPC[i].y)**2)**0.5
                                if dist < 80:
                                    config.dialogue_timer = pygame.time.get_ticks()
                                    if config.show_dialogue == i:
                                        config.current_dialogue += 1
                                        if not config.current_dialogue < len(object.NPC[config.show_dialogue].dialogue):
                                            config.show_dialogue = None
                                            break
                                    else:
                                        config.current_dialogue = 0
                                        config.show_dialogue = i
                                    break

        # LOGIC
        if config.game_state == config.GameState.LOADING:
            if loading_screen.update_loading():
                config.game_state = config.GameState.MENU

        mw, mh = world.MAPS[config.current_map].size
        if config.game_state == config.GameState.GAME:
            keys = pygame.key.get_pressed()
            old_x, old_y = object.player.x, object.player.y

            # MOVE
            dx = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= object.player.speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += object.player.speed

            object.player.x += dx
            p_rect = pygame.Rect(object.player.x, object.player.y, object.player.size, object.player.size)

            for wall in walls:
                if p_rect.colliderect(wall):
                    if dx > 0:  # Left
                        object.player.x = wall.left - object.player.size
                    elif dx < 0:  # Right
                        object.player.x = wall.right
                    break

            dy = 0
            if keys[pygame.K_w] or keys[pygame.K_UP]: dy -= object.player.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += object.player.speed

            object.player.y += dy
            p_rect = pygame.Rect(object.player.x, object.player.y, object.player.size, object.player.size)

            for wall in walls:
                if p_rect.colliderect(wall):
                    if dy > 0:  # Up
                        object.player.y = wall.top - object.player.size
                    elif dy < 0:  # Down
                        object.player.y = wall.bottom
                    break
            
            # CHANGE MAP
            if object.player.x > mw: # Right
                if   config.current_map == 0: config.current_map = 1
                elif config.current_map == 2: config.current_map = 3
                elif config.current_map == 3: config.current_map = 5; object.player.y = world.MAPS[5].size[1] // 2
                object.player.x = 20
            elif object.player.x < -object.player.size: # Left
                if   config.current_map == 1: config.current_map = 0
                elif config.current_map == 3: config.current_map = 2
                elif config.current_map == 5: config.current_map = 3; object.player.y = world.MAPS[3].size[1] // 2
                object.player.x = config.WIDTH - 40
            elif object.player.y < -object.player.size: # Top
                if   config.current_map == 1: config.current_map = 2; object.player.y = config.HEIGHT - 40
                elif config.current_map == 2: config.current_map = 4; object.player.y = world.MAPS[4].size[1] - 40; object.player.x = config.WIDTH // 2
            elif object.player.y > mh: # Bottom
                if   config.current_map == 4: config.current_map = 2; object.player.x = config.WIDTH // 2
                elif config.current_map == 2: config.current_map = 1
                object.player.y = 20

        # CAMERA
        scale = min(config.WIDTH / mw, config.HEIGHT / mh) if config.debug_mode else 1.0
        cam_x = max(0, min(object.player.x - config.WIDTH // 2, mw - config.WIDTH))
        cam_y = max(0, min(object.player.y - config.HEIGHT // 2, mh - config.HEIGHT))

        # DRAW
        match config.game_state:
            case config.GameState.LOADING:
                loading_screen.draw_loading(config.WIDTH, config.HEIGHT)
            case config.GameState.MENU:
                menu_screen.draw_menu_screen()
            case config.GameState.SETTING:
                setting_screen.draw_settings_screen()
            case config.GameState.PAUSE:
                pause_screen.draw_pause_screen()
            case config.GameState.SAVE:
                save_screen.draw_save_screen()
            case config.GameState.GAME:
                game_world.draw_game_world()

        pygame.display.flip()
        config.clock.tick(60)