import config
from draw import core

def draw_save_screen():
    config.screen.fill((10, 10, 10))
    core.draw_header("SAVE", "- DO YOU WANT TO SAVE YOUR GAME? -", 150)
    core.draw_items(config.SAVE_ITEMS, config.save_selected, config.HEIGHT//2)
    core.draw_hint("[ ESC ] resume    [ ARROW KEYS ] navigate    [ ENTER ] select")