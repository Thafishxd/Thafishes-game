import random
import pygame
import config

loading_start_time = 0
complete_start_time = 0
syncing_start_time = None
outflash_start_time = 0
current_tip = ""
complete_text = ""

def start_loading():
    global loading_start_time
    loading_start_time = pygame.time.get_ticks()


def load(WIDTH, HEIGHT):
    """Call once. Loop it with next"""
    global complete_start_time, syncing_start_time, outflash_start_time, current_tip, complete_text

    while True:
        now = pygame.time.get_ticks()

        elapsed = now - loading_start_time
        if elapsed >= config.loading_duration: break

        _draw_bar(WIDTH, HEIGHT)
        yield

    complete_start_time = now
    syncing_start_time = None
    current_tip = random.choice(config.TIPS)
    complete_text = f"Loading Complete. Welcome"
    pygame.mixer.Sound(config.INTRO_EFFECT).play()

    while True:
        now = pygame.time.get_ticks()

        elapsed = now - complete_start_time
        typed_chars = min(len(complete_text), elapsed // config.complete_char_delay)
        typing_progress = (typed_chars / len(complete_text)) if complete_text else 1.0

        # Kick off SYNCING once the typing is halfway through, so they run side by side
        if syncing_start_time is None and typing_progress >= config.overlap_start_progress:
            syncing_start_time = now

        type_duration = len(complete_text) * config.complete_char_delay
        total_complete_duration = type_duration + config.complete_hold_duration
        if elapsed >= total_complete_duration: break

        config.screen.fill((10, 10, 10))
        _draw_welcome_text(WIDTH, HEIGHT)
        if syncing_start_time is not None:
            _draw_syncing_overlay(WIDTH, HEIGHT, background=False)
            
        yield
        
    if syncing_start_time is None:
        syncing_start_time = now

    while True:
        now = pygame.time.get_ticks()

        elapsed = now - syncing_start_time
        total = config.focus_duration + config.syncing_hold_duration
        if elapsed >= total: break

        _draw_syncing_overlay(WIDTH, HEIGHT, background=True)
        _draw_welcome_text(WIDTH, HEIGHT)
        yield

    outflash_start_time = now

    while True:
        now = pygame.time.get_ticks()

        elapsed = now - outflash_start_time
        if elapsed >= config.outflash_duration: break

        _draw_outflash_stage(WIDTH, HEIGHT)
        yield


def _draw_bar(WIDTH, HEIGHT):
    config.screen.fill((10, 10, 10))

    elapsed = pygame.time.get_ticks() - loading_start_time
    progress = min(elapsed / config.loading_duration, 1.0)

    total_blocks = 16
    filled = int(progress * total_blocks) + 1
    bar = "/" * filled + "-" * (total_blocks - filled) + "/"
    dots = "." * (elapsed // 300 % 4)

    status_index = min(int(progress * len(config.STATUS_MESSAGES)), len(config.STATUS_MESSAGES) - 1)
    status_text = config.STATUS_MESSAGES[status_index]
    title_text = "LOADING " + dots

    bar_color, loading_color = (200, 200, 200), (255, 255, 255)

    if filled == total_blocks:
        bar_color = (120, 255, 120)
        loading_color = (0, 255, 0)
        title_text = "DONE"
        bar = "^______^ hello"

    mono_font = pygame.font.SysFont("Bahnschrift, Segoe UI Semibold, Arial, Helvetica", 34, bold=True)
    bar_font = pygame.font.Font(config.KRYPTON_BOLD, 20)
    status_font = pygame.font.Font(config.KRYPTON_MEDIUM, 20)

    title_surf = mono_font.render(title_text, True, loading_color)
    bar_surf = bar_font.render(bar, True, bar_color)
    status_surf = status_font.render(status_text, True, (80, 80, 80))
    ver_surf = status_font.render("v0.1.0-indev", True, (80, 80, 80))

    config.screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, HEIGHT // 2 - 70))
    config.screen.blit(bar_surf, (WIDTH // 2 - bar_surf.get_width() // 2, HEIGHT // 2 - 10))
    config.screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, HEIGHT // 2 + 25))
    config.screen.blit(ver_surf, (WIDTH - ver_surf.get_width() - 12, HEIGHT - ver_surf.get_height() - 10))


def _draw_welcome_text(WIDTH, HEIGHT):
    elapsed = pygame.time.get_ticks() - complete_start_time
    typed_chars = min(len(complete_text), elapsed // config.complete_char_delay)
    shown_text = complete_text[:typed_chars]

    mono_font = pygame.font.Font(config.KRYPTON_BOLD, 20)
    tip_font = pygame.font.Font(config.KRYPTON_MEDIUM, 14)

    complete_surf = mono_font.render(shown_text, True, (230, 230, 230))
    text_x = WIDTH // 2 - complete_surf.get_width() // 2
    text_y = HEIGHT // 2 + 55
    config.screen.blit(complete_surf, (text_x, text_y))

    # Blinking typewriter cursor while still typing
    if typed_chars < len(complete_text) and (pygame.time.get_ticks() // 250) % 2 == 0:
        cursor_surf = mono_font.render("_", True, (230, 230, 230))
        config.screen.blit(cursor_surf, (text_x + complete_surf.get_width() + 2, text_y))

    # Tip only shows once typing has fully finished
    if typed_chars >= len(complete_text):
        tip_surf = tip_font.render(f"Tip : {current_tip}", True, (140, 140, 140))
        if tip_surf.get_width() > WIDTH - 80:
            words = current_tip.split(" ")
            line1 = line2 = ""

            for w in words:
                if tip_font.size("Tip : " + line1 + w)[0] < WIDTH - 80:
                    line1 += w + " "
                else:
                    line2 += w + " "

            l1_surf = tip_font.render("Tip : " + line1.strip(), True, (140, 140, 140))
            l2_surf = tip_font.render(line2.strip(), True, (140, 140, 140))

            config.screen.blit(l1_surf, (WIDTH // 2 - l1_surf.get_width() // 2, HEIGHT // 2 + 95))
            config.screen.blit(l2_surf, (WIDTH // 2 - l2_surf.get_width() // 2, HEIGHT // 2 + 117))
        else:
            config.screen.blit(tip_surf, (WIDTH // 2 - tip_surf.get_width() // 2, HEIGHT // 2 + 95))


def _draw_corner_brackets(surf, rect, size, thickness, color, side_slide=0):
    """Draws the four corner marks. Left corners get pulled further left by side_slide,
    right corners get pushed further right — so at side_slide > 0 the two halves are
    apart, converging to the normal frame as side_slide eases to 0."""

    x, y, w, h = rect
    pts = [
        (x - side_slide, y, 1, 1),                   # top-left
        (x + w + side_slide, y, -1, 1),              # top-right
        (x - side_slide, y + h, 1, -1),              # bottom-left
        (x + w + side_slide, y + h, -1, -1),         # bottom-right
    ]
    
    for cx, cy, dx, dy in pts:
        pygame.draw.line(surf, color, (cx, cy), (cx + size * dx, cy), thickness)
        pygame.draw.line(surf, color, (cx, cy), (cx, cy + size * dy), thickness)


def _syncing_ease():
    """Shared ease-out progress (0 to 1) for the whole SYNCING entrance animation —
    used by the zoom, the corner-pair slide, and the growing underline so they all
    finish in sync."""

    elapsed = pygame.time.get_ticks() - syncing_start_time
    t = min(elapsed / config.focus_duration, 1.0)
    return 1 - (1 - t) ** 3  # ease-out: fast at first, decelerating into place


def _syncing_zoom_rect(WIDTH, HEIGHT):
    ease = _syncing_ease()

    target_w, target_h = 260, 70
    start_w, start_h = WIDTH * 0.72, HEIGHT * 0.72
    w = start_w + (target_w - start_w) * ease
    h = start_h + (target_h - start_h) * ease

    # Plain centered zoom — the sideways motion now lives entirely in the
    # split corner-pair offset (see _syncing_side_slide), not the box itself.
    x = WIDTH / 2 - w / 2
    y = HEIGHT / 2 - h / 2
    return (x, y, w, h)


def _syncing_side_slide(WIDTH):
    """How far apart the left/right corner pairs still are. Starts fully off-screen
    on each side, decelerating (ease-out) to 0 — i.e. the two halves meeting in the middle."""

    ease = _syncing_ease()
    max_slide = WIDTH * 0.75
    return max_slide * (1 - ease)


def _render_tracked_text(font, text, color, spacing=0):
    """Renders text with extra letter-spacing (tracking) for a cleaner, more modern look."""

    letter_surfs = [font.render(ch, True, color) for ch in text]
    total_w = sum(s.get_width() for s in letter_surfs) + spacing * (len(text) - 1)
    height = max(s.get_height() for s in letter_surfs)
    surf = pygame.Surface((total_w, height), pygame.SRCALPHA)
    x = 0
    for s in letter_surfs:
        surf.blit(s, (x, 0))
        x += s.get_width() + spacing
    return surf


def _bracket_shape_surface(height, cap, thickness, is_left):
    """Draws a single [ or ] shape onto its own small transparent surface, so it can
    be alpha-faded and blitted independently (used for both the main brackets and
    the fading ghost copies)."""

    w = cap + thickness
    surf = pygame.Surface((w, height), pygame.SRCALPHA)
    color = (255, 255, 255)
    if is_left:
        pygame.draw.line(surf, color, (thickness // 2, 0), (thickness // 2, height - 1), thickness)
        pygame.draw.line(surf, color, (0, thickness // 2), (cap, thickness // 2), thickness)
        pygame.draw.line(surf, color, (0, height - 1 - thickness // 2), (cap, height - 1 - thickness // 2), thickness)
    else:
        pygame.draw.line(surf, color, (w - 1 - thickness // 2, 0), (w - 1 - thickness // 2, height - 1), thickness)
        pygame.draw.line(surf, color, (w - cap, thickness // 2), (w, thickness // 2), thickness)
        pygame.draw.line(surf, color, (w - cap, height - 1 - thickness // 2), (w, height - 1 - thickness // 2), thickness)
    return surf


def _draw_side_brackets(target, WIDTH, HEIGHT):
    """Two big [ and ] marks hugging the screen edges, blinking on their own rhythm,
    plus a continuous stream of fading ghost copies drifting inward toward SYNCING.
    Both the height AND the cap length scale together on entrance — a uniform,
    subtle zoom rather than just growing taller — using the same timing/ease as
    the corner-bracket zoom so everything settles together."""

    now = pygame.time.get_ticks()
    blink_on = (now // config.side_bracket_blink_interval) % 2 == 0

    zoom_ease = _syncing_ease()
    scale = config.side_bracket_zoom_start_scale + (1 - config.side_bracket_zoom_start_scale) * zoom_ease
    current_height = config.side_bracket_height * scale
    current_cap = int(config.side_bracket_cap * scale)

    cy = HEIGHT // 2
    top = int(cy - current_height // 2)
    bottom = int(cy + current_height // 2)
    height = bottom - top

    left_x = config.side_bracket_margin
    right_x = WIDTH - config.side_bracket_margin

    if blink_on:
        left_shape = _bracket_shape_surface(height, current_cap, config.side_bracket_thickness, True)
        right_shape = _bracket_shape_surface(height, current_cap, config.side_bracket_thickness, False)
        target.blit(left_shape, (left_x, top))
        target.blit(right_shape, (right_x - right_shape.get_width(), top))

    # Ghost copies: spawn on a fixed rhythm, drift inward toward SYNCING, fade to nothing
    elapsed = now - syncing_start_time
    spawn_i = config.side_bracket_ghost_spawn_interval
    lifetime = config.side_bracket_ghost_lifetime
    latest_index = int(elapsed // spawn_i)
    lookback = int(lifetime // spawn_i) + 2

    for i in range(max(0, latest_index - lookback), latest_index + 1):
        spawn_time = i * spawn_i

        # no new ghosts spawn after the cutoff; earlier ones still finish out
        if spawn_time > config.side_bracket_ghost_spawn_cutoff: continue
        
        ghost_age = elapsed - spawn_time
        if not (0 <= ghost_age <= lifetime): continue

        t = ghost_age / lifetime
        ease = 1 - (1 - t) ** 2  # ease-out drift
        move = config.side_bracket_ghost_travel * ease
        alpha = int(255 * (1 - t))
        if alpha <= 0: continue

        gh_left = _bracket_shape_surface(height, current_cap, config.side_bracket_ghost_thickness, True)
        gh_left.set_alpha(alpha)
        target.blit(gh_left, (left_x + move, top))

        gh_right = _bracket_shape_surface(height, current_cap, config.side_bracket_ghost_thickness, False)
        gh_right.set_alpha(alpha)
        target.blit(gh_right, (right_x - gh_right.get_width() - move, top))


def _render_syncing_content(target, WIDTH, HEIGHT):
    """Draws the SYNCING title, timer, and zooming brackets onto the given surface."""

    elapsed = pygame.time.get_ticks() - syncing_start_time
    rect = _syncing_zoom_rect(WIDTH, HEIGHT)

    title_font = pygame.font.SysFont("Bahnschrift, Segoe UI Semibold, Arial, Helvetica", 34, bold=True)
    timer_font = pygame.font.Font(config.KRYPTON_MEDIUM, 12)

    shadow_surf = _render_tracked_text(title_font, "SYNCING", (0, 0, 0), spacing=7)
    shadow_surf.set_alpha(110)
    base_surf = _render_tracked_text(title_font, "SYNCING", (255, 255, 255), spacing=7)

    title_x = WIDTH // 2 - base_surf.get_width() // 2
    title_y = HEIGHT // 2 - 30
    target.blit(shadow_surf, (title_x + 2, title_y + 3))
    target.blit(base_surf, (title_x, title_y))

    # --- Underline that grows over time until it matches the width of "SYNCING" ---
    # LINE_TARGET_WIDTH is the width it grows to. base_surf.get_width() is the actual
    # rendered width of the "SYNCING" text above, so it already matches exactly — but if
    # you want to override it by hand, just replace the right-hand side with a fixed
    # number (e.g. LINE_TARGET_WIDTH = 130) and adjust until it lines up how you like.
    LINE_TARGET_WIDTH = base_surf.get_width()
    grow_ease = _syncing_ease()
    line_w = LINE_TARGET_WIDTH * grow_ease
    line_y = HEIGHT // 2 + 12
    pygame.draw.line(target, (150, 150, 150), (WIDTH // 2 - line_w / 2, line_y), (WIDTH // 2 + line_w / 2, line_y), 2)

    # Timer just counts up continuously the whole time SYNCING is on screen, no clamp
    seconds = elapsed / 1000
    timer_surf = timer_font.render(f"{seconds:05.2f}", True, (140, 140, 140))
    target.blit(timer_surf, (WIDTH // 2 - timer_surf.get_width() // 2, line_y + 6))

    _draw_corner_brackets(target, rect, size=22, thickness=2, color=(255, 255, 255), side_slide=_syncing_side_slide(WIDTH))
    _draw_side_brackets(target, WIDTH, HEIGHT)


def _draw_syncing_overlay(WIDTH, HEIGHT, background):
    """Draws the SYNCING title, timer, and zooming brackets.
    If background=True, fills an opaque backdrop first (the pure SYNCING screen).
    If background=False, draws on a transparent layer that fades in on top of
    whatever's already on screen (used during the overlap with the typing screen)."""

    elapsed = pygame.time.get_ticks() - syncing_start_time

    if background:
        config.screen.fill((5, 5, 5))
        target = config.screen
    else: target = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    _render_syncing_content(target, WIDTH, HEIGHT)

    if not background:
        fade_alpha = int(255 * min(elapsed / config.overlap_fade_duration, 1.0))
        target.set_alpha(fade_alpha)
        config.screen.blit(target, (0, 0))

    # White flash bridging the typing screen into SYNCING
    if elapsed < config.flash_duration:
        progress = elapsed / config.flash_duration
        alpha = int(255 * (1 - progress) ** 2)
        flash_surf = pygame.Surface((WIDTH, HEIGHT))
        flash_surf.fill((255, 255, 255))
        flash_surf.set_alpha(alpha)
        config.screen.blit(flash_surf, (0, 0))


def _draw_outflash_stage(WIDTH, HEIGHT):
    elapsed = pygame.time.get_ticks() - outflash_start_time
    config.screen.fill((5, 5, 5))

    # Fixed rhythm flicker: check whether we're inside one of the "on" beats
    active_segment = next(
        ((start, end) for start, end in config.OUTFLASH_FLICKER_SCHEDULE if start <= elapsed < end),
        None
    )

    if active_segment is not None:
        _render_syncing_content(config.screen, WIDTH, HEIGHT)
        _draw_welcome_text(WIDTH, HEIGHT)
        # A quick bright pulse right at the start of each "on" beat, for a snappier flash feel
        start = active_segment[0]
        since_beat_start = elapsed - start
        pulse_window = 40
        if since_beat_start < pulse_window:
            pulse_alpha = int(160 * (1 - since_beat_start / pulse_window))
            pulse_surf = pygame.Surface((WIDTH, HEIGHT))
            pulse_surf.fill((255, 255, 255))
            pulse_surf.set_alpha(pulse_alpha)
            config.screen.blit(pulse_surf, (0, 0))

    # A quick bright pop right at the start, then a gradual fade to black
    # that finishes exactly as the outflash duration ends
    progress = min(elapsed / config.outflash_duration, 1.0)
    pop_alpha = int(255 * max(0, 1 - progress * 3))
    fade_alpha = int(255 * progress)

    pop_surf = pygame.Surface((WIDTH, HEIGHT))
    pop_surf.fill((255, 255, 255))
    pop_surf.set_alpha(pop_alpha)
    config.screen.blit(pop_surf, (0, 0))

    fade_surf = pygame.Surface((WIDTH, HEIGHT))
    fade_surf.fill((0, 0, 0))
    fade_surf.set_alpha(fade_alpha)
    config.screen.blit(fade_surf, (0, 0))