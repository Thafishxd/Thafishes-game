import pygame
import config
import object

last_chars = 0
communicate_done = None
show_dialogue = None
current_dialogue = 0
dialogue_timer = 0

def draw_dialogue():
    global last_chars, communicate_done, show_dialogue, current_dialogue, dialogue_timer

    now = pygame.time.get_ticks()
    current_npc = object.NPC[show_dialogue]
    elapsed = now - dialogue_timer
    text = current_npc.dialogue[current_dialogue][1]
    duration = current_npc.dialogue[current_dialogue][0]

    box = pygame.Rect(0, 0, 540, 90)
    box.center = (config.WIDTH/2, config.HEIGHT - 60)
    pygame.draw.rect(config.screen, (10, 10, 10), box)
    pygame.draw.rect(config.screen, (50, 50, 50), box, 1)

    nametag = config.sub_font.render(f"< {current_npc.name} >", True, current_npc.color)
    config.screen.blit(nametag, (box.x + 12, box.y - 18))

    chars = min(len(text), elapsed // 40)
    shown_text = text[:chars]
    text_surf = config.font.render(shown_text, True, (220, 220, 220))
    config.screen.blit(text_surf, (box.x + 14, box.y + 18))

    if last_chars != chars:
        if shown_text and not shown_text[-1].isspace() and shown_text[-1] != config.ZERO_WIDTH_CHAR:
            current_npc.sound.play()
        last_chars = chars
    elif (elapsed // 500) % 2 == 0:
        cursor = config.font.render("_", True, (150, 150, 150))
        config.screen.blit(cursor, (box.x + 14 + text_surf.get_width() + 3, box.y + 18))

    if shown_text == text:
        if communicate_done is None: communicate_done = now
        elapsed_done = now - communicate_done

        bar_w = int((box.width - 4) * max(0, 1 - elapsed_done / duration))
        pygame.draw.rect(config.screen, current_npc.color, (box.x + 2, box.y + box.height - 4, bar_w, 3))

        if elapsed_done >= duration: return False
    else: pygame.draw.rect(config.screen, current_npc.color, (box.x + 2, box.y + box.height - 4, box.width - 4, 3))

    return True