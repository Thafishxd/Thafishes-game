import config

def draw_items(items, selected, center_y, gap=30):
    center_y -= len(items) // 2 * gap
    prefix_surf = config.item_font.render("> ", True, (255, 255, 255))
    prefix_w = prefix_surf.get_width()
    for i, label in enumerate(items):
        color = (255, 255, 255) if i == selected else (80, 80, 80)
        text_surf = config.item_font.render(label, True, color)
        x = config.WIDTH // 2 - text_surf.get_width() // 2
        y = center_y + i * gap
        config.screen.blit(text_surf, (x, y))
        if i == selected:
            arrow = config.item_font.render(">", True, (255, 255, 255))
            config.screen.blit(arrow, (x - prefix_w, y))

def draw_header(title_text, sub_text, center_y):
    title = config.big_font.render(title_text, True, (255, 255, 255))
    subtitle = config.sub_font.render(sub_text, True, (80, 80, 80))
    config.screen.blit(title,    (config.WIDTH//2 - title.get_width()//2, center_y))
    config.screen.blit(subtitle, (config.WIDTH//2 - subtitle.get_width()//2, center_y + 48))

def draw_hint(text):
    hint = config.sub_font.render(text, True, (80, 80, 80))
    config.screen.blit(hint, (config.WIDTH//2 - hint.get_width()//2, config.HEIGHT - 25))

def to_screen(x, y, cam_x, cam_y, scale):
    if config.debug_mode: return x * scale, y * scale
    return x - cam_x, y - cam_y