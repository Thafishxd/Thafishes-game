import config
from draw import core

def draw_pause_screen():
    config.screen.fill((10, 10, 10))
    
    core.draw_header("PAUSED", "- GAME PAUSED -", 150)
    core.draw_items(config.PAUSE_ITEMS, config.pause_selected, config.HEIGHT//2)
    core.draw_hint("[ ESC ] resume    [ ARROW KEYS ] navigate    [ ENTER ] select")