import pygame
import config
import object

def draw_dialogue():
    elapsed = pygame.time.get_ticks() - config.dialogue_timer
    text = object.NPC[config.show_dialogue].dialogue[config.current_dialogue][1]
    duration = object.NPC[config.show_dialogue].dialogue[config.current_dialogue][0]

    box = pygame.Rect(0, 0, 540, 90)
    box.center = (config.WIDTH/2, config.HEIGHT - 60)
    pygame.draw.rect(config.screen, (10, 10, 10), box)
    pygame.draw.rect(config.screen, (50, 50, 50), box, 1)

    nametag = config.sub_font.render(f"< {object.NPC[config.show_dialogue].name} >", True, object.NPC[config.show_dialogue].color)
    config.screen.blit(nametag, (box.x + 12, box.y - 18))

    chars = min(len(text), elapsed // 40)
    text_surf = config.font.render(text[:chars], True, (220, 220, 220))
    config.screen.blit(text_surf, (box.x + 14, box.y + 18))

    if (elapsed // 500) % 2 == 0:
        cursor = config.font.render("_", True, (150, 150, 150))
        config.screen.blit(cursor, (box.x + 14 + text_surf.get_width() + 3, box.y + 18))

    bar_w = int((box.width - 4) * max(0, 1 - elapsed / duration))
    pygame.draw.rect(config.screen, object.NPC[config.show_dialogue].color, (box.x + 2, box.y + box.height - 4, bar_w, 3))

    if elapsed > duration:
        return False
    return True