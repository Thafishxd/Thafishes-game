import pygame
from enum import Enum

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Indie testing - In Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 16)
big_font = pygame.font.SysFont("Courier New", 38, bold=True)
sub_font = pygame.font.SysFont("Courier New", 14)
item_font = pygame.font.SysFont("Courier New", 18)

class GameState(Enum):
    LOADING = "loading"
    MENU = "menu"
    SETTING = "setting"
    PAUSE = "pause"
    SAVE = "save"
    GAME = "game"

# --- GAME STATE ---
def init():
    global current_map, debug_mode, show_dialogue, current_dialogue, dialogue_timer
    current_map = 0
    debug_mode = False
    show_dialogue = None
    current_dialogue = 0
    dialogue_timer = 0
init()
game_state = GameState.LOADING

# --- LOADING STATE ---
loading_start_time = 0
loading_duration = 3000        # Duration of the progress bar (milli secs)
complete_char_delay = 22       # ms per character for the "Loading Complete" typewriter effect
overlap_start_progress = 0.5   # SYNCED starts fading in once typing reaches this fraction
overlap_fade_duration = 650    # How long SYNCED takes to fade in over the typing screen
complete_hold_duration = 300   # Extra hold after typing finishes, before phase fully switches
flash_duration = 500           # White flash bridging into the SYNCED screen
focus_duration = 1800          # How long the corner brackets take to zoom in
synced_hold_duration = 1900    # How long SYNCED sits still after brackets settle

# --- Big side brackets ("[" and "]") that blink on the screen edges ---
side_bracket_height = 580     # How tall each bracket is
side_bracket_margin = 14       # Distance from the screen edge (small gap — "hugging", not touching)
side_bracket_cap = 28          # Length of the top/bottom end ticks
side_bracket_thickness = 7     # Line thickness of the main brackets

# Zoom entrance: the side brackets start slightly smaller (both height AND cap
# length scale together) and grow outward to full size, using the same timing
# as everything else in the SYNCED sequence (focus_duration).
side_bracket_zoom_start_scale = 0.85   # Starting size as a fraction of full size (0-1) — kept subtle

# Ghost copies of the side brackets that spawn continuously and drift inward
# toward "SYNCED", fading out as they travel, then disappearing
side_bracket_ghost_spawn_interval = 500  # ms between each new ghost spawning
side_bracket_ghost_lifetime = 650        # ms a ghost lives — travel + fade both finish by then
side_bracket_ghost_thickness = 4         # Line thickness of ghost copies (thinner than the main ones)
side_bracket_ghost_spawn_cutoff = 1010   # Stop spawning new ghosts once the SYNCED timer passes this (ms)

# Adjustable-in-Settings-menu values. These ARE the live values loading_screen.py
# reads directly — the settings menu just nudges them up/down with LEFT/RIGHT.
side_bracket_blink_interval = 700  # ms per on/off half-cycle (smaller = faster blink)
BLINK_SPEED_MIN = 100
BLINK_SPEED_MAX = 1000
BLINK_SPEED_STEP = 25

side_bracket_ghost_travel = 30      # px a ghost moves inward over its lifetime
GHOST_TRAVEL_MIN = 0
GHOST_TRAVEL_MAX = 300
GHOST_TRAVEL_STEP = 5

outflash_duration = 750        # Quick flash-and-fade before the menu opens
# Fixed flicker rhythm for the outflash: (on_start_ms, on_end_ms) pairs, relative to
# the start of the outflash phase. Gaps between pairs are the "off" beats. Edit the
# numbers directly to change the rhythm — it's the same pattern every time, on purpose.
OUTFLASH_FLICKER_SCHEDULE = [
    (0, 90),
    (150, 230),
    (260, 280),
    (320, 420),
    (450, 470),
    (520, 610),
    (640, 660),
    (690, 750),
]
STATUS_MESSAGES = [
    "Reading 'main.py'...",
    "Reading 'loading_screen.py'...",
    "Loading assets...",
    "Building world data...",
    "Spawning NPCs...",
    "Almost there...",
    ";) *winky face*"
]
TIPS = [
#    "Using the Settings, you can tweak various options to make your experience better.",
#    "Press F3 to toggle debug mode.",
#    "Press E near an NPC to talk to them.",
    "One of the dev Messed up the code cuz he didnt know that u can press E near an NPC to talk to them.",
]

# --- MENU STATE ---
menu_selected = 0
MENU_ITEMS = ["NEW GAME", "LOAD GAME", "SETTINGS", "QUIT"]

# --- PAUSE STATE ---
pause_selected = 0
PAUSE_ITEMS = ["RESUME", "SETTINGS", "MENU"]

# --- SAVE STATE ---
save_selected = 0
SAVE_ITEMS = ["YES", "NO", "CANCEL"]

# --- SETTINGS STATE ---
settings_selected = 0
SETTINGS_ITEMS = ["DEBUG MODE: OFF", "BLINK SPEED: 700", "GHOST TRAVEL: 30", "BACK"]