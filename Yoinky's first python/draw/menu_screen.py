import config
from draw import core

def draw_menu_screen():
    config.screen.fill((10, 10, 10))

    core.draw_header("INDIE GAME", "- INDEV -", 150)
    core.draw_items(config.MENU_ITEMS, config.menu_selected, config.HEIGHT//2)
    core.draw_hint("[ ARROW KEYS ] navigate    [ ENTER ] select")