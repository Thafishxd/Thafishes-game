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

    # --- LOADING LOOP ---
    loader = loading_screen.load()
    while not next(loader, True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        loading_screen.draw_loading(config.WIDTH, config.HEIGHT)
        
        pygame.display.flip()
        config.clock.tick(60)

    # --- MAIN LOOP ---
    while True:
        # GOTO
        match config.game_state[-1]:
            case config.GameState.MENU:
                def in_menu():
                    while True:
                        for event in pygame.event.get():
                            match event.type:
                                case pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                case pygame.KEYDOWN:
                                    match event.key:
                                        case pygame.K_DOWN:
                                            config.menu_selected = (config.menu_selected + 1) % len(config.MENU_ITEMS)
                                        case pygame.K_UP:
                                            config.menu_selected = (config.menu_selected - 1) % len(config.MENU_ITEMS)
                                        case pygame.K_RETURN:
                                            match config.menu_selected:
                                                case 0:
                                                    config.init()
                                                    object.init()
                                                    config.game_state.append(config.GameState.GAME)
                                                    return
                                                case 1:
                                                    with open("saves/save.json", "r") as f:
                                                        data = json.load(f)
                                                        object.player.name = data["player"]["name"]
                                                        object.player.x = data["player"]["x"]
                                                        object.player.y = data["player"]["y"]
                                                        object.player.size = data["player"]["size"]
                                                        object.player.color = data["player"]["color"]
                                                        object.player.speed = data["player"]["speed"]
                                                    config.game_state.append(config.GameState.GAME)
                                                    return
                                                case 2:
                                                    config.game_state.append(config.GameState.SETTING)
                                                    return
                                                case 3:
                                                    pygame.quit()
                                                    sys.exit()
                        
                        menu_screen.draw_menu_screen()
                        
                        pygame.display.flip()
                        config.clock.tick(60)

                in_menu()
                    
            case config.GameState.SETTING:
                def in_setting():
                    while True:
                        for event in pygame.event.get():
                            match event.type:
                                case pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                case pygame.KEYDOWN:
                                    match event.key:
                                        case pygame.K_DOWN:
                                            config.settings_selected = (config.settings_selected + 1) % len(config.SETTINGS_ITEMS)
                                        case pygame.K_UP:
                                            config.settings_selected = (config.settings_selected - 1) % len(config.SETTINGS_ITEMS)
                                        case pygame.K_RETURN:
                                            match config.settings_selected:
                                                case 0: config.debug_mode = not config.debug_mode
                                                case 3:
                                                    config.game_state.pop()
                                                    return
                                        case pygame.K_LEFT:
                                            match config.settings_selected:
                                                case 1:
                                                    config.side_bracket_blink_interval = max(config.BLINK_SPEED_MIN, config.side_bracket_blink_interval - config.BLINK_SPEED_STEP)
                                                case 2:
                                                    config.side_bracket_ghost_travel = max(config.GHOST_TRAVEL_MIN, config.side_bracket_ghost_travel - config.GHOST_TRAVEL_STEP)
                                        case pygame.K_RIGHT:
                                            match config.settings_selected:
                                                case 1:
                                                    config.side_bracket_blink_interval = min(config.BLINK_SPEED_MAX, config.side_bracket_blink_interval + config.BLINK_SPEED_STEP)
                                                case 2:
                                                    config.side_bracket_ghost_travel = min(config.GHOST_TRAVEL_MAX, config.side_bracket_ghost_travel + config.GHOST_TRAVEL_STEP)
                                        case pygame.K_ESCAPE:
                                            config.game_state.pop()
                                            return

                        setting_screen.draw_settings_screen()
                        
                        pygame.display.flip()
                        config.clock.tick(60)

                in_setting()

            case config.GameState.PAUSE:
                def in_pause():
                    while True:
                        for event in pygame.event.get():
                            match event.type:
                                case pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                case pygame.KEYDOWN:
                                    match event.key:
                                        case pygame.K_s | pygame.K_DOWN:
                                            config.pause_selected = (config.pause_selected + 1) % len(config.PAUSE_ITEMS)
                                        case pygame.K_w | pygame.K_UP:
                                            config.pause_selected = (config.pause_selected - 1) % len(config.PAUSE_ITEMS)
                                        case pygame.K_RETURN:
                                            match config.pause_selected:
                                                case 0: config.game_state.append(config.GameState.GAME)
                                                case 1: config.game_state.append(config.GameState.SETTING)
                                                case 2: config.game_state.append(config.GameState.SAVE)
                                            return
                                        case pygame.K_ESCAPE:
                                            config.game_state.append(config.GameState.GAME)
                                            return

                        pause_screen.draw_pause_screen()
                        
                        pygame.display.flip()
                        config.clock.tick(60)

                in_pause()

            case config.GameState.SAVE:
                def in_save():
                    while True:
                        for event in pygame.event.get():
                            match event.type:
                                case pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                case pygame.KEYDOWN:
                                    match event.key:
                                        case pygame.K_s | pygame.K_DOWN:
                                            config.save_selected = (config.save_selected + 1) % len(config.SAVE_ITEMS)
                                        case pygame.K_w | pygame.K_UP:
                                            config.save_selected = (config.save_selected - 1) % len(config.SAVE_ITEMS)
                                        case pygame.K_RETURN:
                                            match config.save_selected:
                                                case 0:
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
                                                    config.game_state = [config.GameState.MENU]      # |> reset the stack
                                                case 1: config.game_state = [config.GameState.MENU]  # |
                                                case 2: config.game_state.pop()
                                            return
                                        case pygame.K_ESCAPE:
                                            config.game_state.pop()
                                            return

                        save_screen.draw_save_screen()
                        
                        pygame.display.flip()
                        config.clock.tick(60)

                in_save()

            case config.GameState.GAME:
                def in_game():
                    while True:
                        walls = world.get_world_objects(config.current_map)

                        for event in pygame.event.get():
                            match event.type:
                                case pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                case pygame.KEYDOWN:
                                    match event.key:
                                        case pygame.K_ESCAPE:
                                            config.game_state.append(config.GameState.PAUSE)
                                            config.pause_selected = 0
                                            return
                                        case pygame.K_F3:
                                            config.debug_mode = not config.debug_mode

                                    for i in range(len(object.NPC)):
                                        if event.key == pygame.K_e and config.current_map == object.NPC[i].map:
                                            dist = ((object.player.x - object.NPC[i].x)**2 + (object.player.y - object.NPC[i].y)**2)**0.5
                                            if dist >= 80: continue

                                            config.dialogue_timer = pygame.time.get_ticks()
                                            if config.show_dialogue == i:
                                                config.current_dialogue += 1
                                                if config.current_dialogue >= len(object.NPC[config.show_dialogue].dialogue):
                                                    config.show_dialogue = None
                                                    break
                                            else:
                                                config.current_dialogue = 0
                                                config.show_dialogue = i
                                            break

                        mw, mh = world.MAPS[config.current_map].size
                        if config.game_state[-1] == config.GameState.GAME:
                            keys = pygame.key.get_pressed()

                            # MOVE
                            dx = 0
                            if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx -= object.player.speed
                            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += object.player.speed

                            object.player.x += dx
                            p_rect = pygame.Rect(object.player.x, object.player.y, object.player.size, object.player.size)

                            for wall in walls:
                                if p_rect.colliderect(wall):
                                    if dx > 0: object.player.x = wall.left - object.player.size  # Left
                                    elif dx < 0: object.player.x = wall.right                    # Right

                                    break

                            dy = 0
                            if keys[pygame.K_w] or keys[pygame.K_UP]:   dy -= object.player.speed
                            if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += object.player.speed

                            object.player.y += dy
                            p_rect = pygame.Rect(object.player.x, object.player.y, object.player.size, object.player.size)

                            for wall in walls:
                                if p_rect.colliderect(wall):
                                    if dy > 0: object.player.y = wall.top - object.player.size  # Up
                                    elif dy < 0: object.player.y = wall.bottom                  # Down

                                    break
                            
                            # CHANGE MAP
                            if object.player.x > mw: # Right
                                match config.current_map:
                                    case 0: config.current_map = 1
                                    case 2: config.current_map = 3
                                    case 3: config.current_map = 5; object.player.y = world.MAPS[5].size[1] // 2
                                object.player.x = 20

                            elif object.player.x < -object.player.size: # Left
                                match config.current_map:
                                    case 1: config.current_map = 0
                                    case 3: config.current_map = 2
                                    case 5: config.current_map = 3; object.player.y = world.MAPS[3].size[1] // 2
                                object.player.x = config.WIDTH - 40

                            elif object.player.y < -object.player.size: # Top
                                match config.current_map:
                                    case 1: config.current_map = 2; object.player.y = config.HEIGHT - 40
                                    case 2: config.current_map = 4; object.player.y = world.MAPS[4].size[1] - 40; object.player.x = config.WIDTH // 2

                            elif object.player.y > mh: # Bottom
                                match config.current_map:
                                    case 4: config.current_map = 2; object.player.x = config.WIDTH // 2
                                    case 2: config.current_map = 1
                                object.player.y = 20

                        game_world.draw_game_world()
                        
                        pygame.display.flip()
                        config.clock.tick(60)

                in_game()
                    
            case _:
                pygame.quit()
                sys.exit()