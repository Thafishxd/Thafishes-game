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
from draw import dialogue

def load_game():
    with open("saves/save.json", "r") as f:
        try:
            data = json.load(f)
            object.player.name  = data["player"]["name"]
            object.player.x     = data["player"]["x"]
            object.player.y     = data["player"]["y"]
            object.player.size  = data["player"]["size"]
            object.player.color = data["player"]["color"]
            object.player.speed = data["player"]["speed"]

            npc_data = data["npc"]
            object.NPC = []
            for k, v in npc_data.items():
                object.NPC.append(object.Object(k, v["x"], v["y"], v["size"], tuple(v["color"]), v["dialogue"], v["map"]))

            config.current_map = data["current-map"]
        except KeyError: pass


def save_game():
    with open("saves/save.json", "w") as f:
        npc_data = {}
        for npc in object.NPC:
            npc_data[npc.name] = {
                "x":        npc.x,
                "y":        npc.y,
                "size":     npc.size,
                "color":    npc.color,
                "dialogue": npc.dialogue,
                "map":      npc.map
            }

        data = {
            "player": {
                "name":  object.player.name,
                "x":     object.player.x,
                "y":     object.player.y,
                "size":  object.player.size,
                "color": object.player.color,
                "speed": object.player.speed
            },
            "npc": npc_data,
            "current-map": config.current_map
        }
        json.dump(data, f)


def close_game():
    pygame.quit()
    sys.exit()

        
def in_menu():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_DOWN:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.menu_selected = (config.menu_selected + 1) % len(config.MENU_ITEMS)
                    case pygame.K_UP:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.menu_selected = (config.menu_selected - 1) % len(config.MENU_ITEMS)
                    case pygame.K_RETURN:
                        match config.menu_selected:
                            case 0:
                                pygame.mixer.Sound(config.ENTER_EFFECT).play()
                                config.init()
                                object.init()
                                config.game_state.append(config.GameState.GAME)
                            case 1:
                                pygame.mixer.Sound(config.ENTER_EFFECT).play()
                                load_game()
                                config.game_state.append(config.GameState.GAME)
                            case 2:
                                pygame.mixer.Sound(config.SELECT_EFFECT).play()
                                config.game_state.append(config.GameState.SETTING)
                            case 3:
                                pygame.quit()
                                sys.exit()
    
    menu_screen.draw_menu_screen()


def in_setting():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_DOWN:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.settings_selected = (config.settings_selected + 1) % len(config.SETTINGS_ITEMS)
                    case pygame.K_UP:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.settings_selected = (config.settings_selected - 1) % len(config.SETTINGS_ITEMS)
                    case pygame.K_RETURN:
                        match config.settings_selected:
                            case 0:
                                pygame.mixer.Sound(config.EDIT_EFFECT).play()
                                config.debug_mode = not config.debug_mode
                            case 3:
                                pygame.mixer.Sound(config.BACK_EFFECT).play()
                                config.game_state.pop()
                    case pygame.K_LEFT:
                        match config.settings_selected:
                            case 1:
                                pygame.mixer.Sound(config.EDIT_EFFECT).play()
                                config.side_bracket_blink_interval = max(config.BLINK_SPEED_MIN, config.side_bracket_blink_interval - config.BLINK_SPEED_STEP)
                            case 2:
                                pygame.mixer.Sound(config.EDIT_EFFECT).play()
                                config.side_bracket_ghost_travel = max(config.GHOST_TRAVEL_MIN, config.side_bracket_ghost_travel - config.GHOST_TRAVEL_STEP)
                    case pygame.K_RIGHT:
                        match config.settings_selected:
                            case 1:
                                pygame.mixer.Sound(config.EDIT_EFFECT).play()
                                config.side_bracket_blink_interval = min(config.BLINK_SPEED_MAX, config.side_bracket_blink_interval + config.BLINK_SPEED_STEP)
                            case 2:
                                pygame.mixer.Sound(config.EDIT_EFFECT).play()
                                config.side_bracket_ghost_travel = min(config.GHOST_TRAVEL_MAX, config.side_bracket_ghost_travel + config.GHOST_TRAVEL_STEP)
                    case pygame.K_ESCAPE:
                        pygame.mixer.Sound(config.BACK_EFFECT).play()
                        config.game_state.pop()

    setting_screen.draw_settings_screen()


def in_pause():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_s | pygame.K_DOWN:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.pause_selected = (config.pause_selected + 1) % len(config.PAUSE_ITEMS)
                    case pygame.K_w | pygame.K_UP:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.pause_selected = (config.pause_selected - 1) % len(config.PAUSE_ITEMS)
                    case pygame.K_RETURN:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        match config.pause_selected:
                            case 0: config.game_state.append(config.GameState.GAME)
                            case 1: config.game_state.append(config.GameState.SETTING)
                            case 2: config.game_state.append(config.GameState.SAVE)
                    case pygame.K_ESCAPE:
                        pygame.mixer.Sound(config.BACK_EFFECT).play()
                        config.game_state.append(config.GameState.GAME)

    pause_screen.draw_pause_screen()

        
def in_save():
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_s | pygame.K_DOWN:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.save_selected = (config.save_selected + 1) % len(config.SAVE_ITEMS)
                    case pygame.K_w | pygame.K_UP:
                        pygame.mixer.Sound(config.SELECT_EFFECT).play()
                        config.save_selected = (config.save_selected - 1) % len(config.SAVE_ITEMS)
                    case pygame.K_RETURN:
                        pygame.mixer.Sound(config.BACK_EFFECT).play()
                        match config.save_selected:
                            case 0:
                                save_game()
                                config.game_state = [config.GameState.MENU]      # |> reset the stack
                            case 1: config.game_state = [config.GameState.MENU]  # |
                            case 2: config.game_state.pop()
                    case pygame.K_ESCAPE:
                        pygame.mixer.Sound(config.BACK_EFFECT).play()
                        config.game_state.pop()

    save_screen.draw_save_screen()

        
def in_game():
    walls = world.get_world_objects(config.current_map)

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT: close_game()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        config.game_state.append(config.GameState.PAUSE)
                        config.pause_selected = 0
                    case pygame.K_F3:
                        config.debug_mode = not config.debug_mode

                for i in range(len(object.NPC)):
                    if event.key != pygame.K_e or config.current_map != object.NPC[i].map: continue

                    dist = ((object.player.x - object.NPC[i].x)**2 + (object.player.y - object.NPC[i].y)**2)**0.5
                    if dist >= 80: continue

                    dialogue.dialogue_timer = pygame.time.get_ticks()
                    dialogue.communicate_done = None
                    dialogue.last_chars = 0
                    if dialogue.show_dialogue == i:
                        dialogue.current_dialogue += 1
                        if dialogue.current_dialogue >= len(object.NPC[dialogue.show_dialogue].dialogue):
                            dialogue.show_dialogue = None
                    else:
                        dialogue.current_dialogue = 0
                        dialogue.show_dialogue = i
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
                if   dx > 0: object.player.x = wall.left - object.player.size  # Left
                elif dx < 0: object.player.x = wall.right                      # Right

                break

        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:   dy -= object.player.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy += object.player.speed

        object.player.y += dy
        p_rect = pygame.Rect(object.player.x, object.player.y, object.player.size, object.player.size)

        for wall in walls:
            if p_rect.colliderect(wall):
                if   dy > 0: object.player.y = wall.top - object.player.size  # Up
                elif dy < 0: object.player.y = wall.bottom                    # Down

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


if __name__ == "__main__":
    loading_screen.start_loading()

    # --- LOADING LOOP ---
    loader = loading_screen.load(config.WIDTH, config.HEIGHT)
    while not next(loader, True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: close_game()
        
        pygame.display.flip()
        config.clock.tick(config.TPS)

    # --- MAIN LOOP ---
    while True:
        # GOTO
        match config.game_state[-1]:
            case config.GameState.MENU:    in_menu()
            case config.GameState.SETTING: in_setting()
            case config.GameState.PAUSE:   in_pause()
            case config.GameState.SAVE:    in_save()
            case config.GameState.GAME:    in_game()
            case _: close_game()
        
        pygame.display.flip()
        config.clock.tick(config.TPS)