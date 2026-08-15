import config
from draw import core

def draw_settings_screen():
    config.screen.fill((10, 10, 10))
    config.SETTINGS_ITEMS[0] = f"DEBUG MODE: {'ON ' if config.debug_mode else 'OFF'}"
    config.SETTINGS_ITEMS[1] = f"BLINK SPEED: {config.side_bracket_blink_interval}"
    config.SETTINGS_ITEMS[2] = f"GHOST TRAVEL: {config.side_bracket_ghost_travel}"
    core.draw_header("SETTINGS", "- OPTIONS -", 150)
    core.draw_items(config.SETTINGS_ITEMS, config.settings_selected, config.HEIGHT//2)
    core.draw_hint("[ ARROW KEYS ] navigate    [ LEFT/RIGHT ] adjust    [ ENTER ] select")