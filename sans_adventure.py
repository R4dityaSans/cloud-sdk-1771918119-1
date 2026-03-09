import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import random
import pgzrun
import math
current_tutorial_map = 1
bg = Actor('bg')
bg1 = Actor("wood_a")
bg2 = Actor("wood_b")
tree_trunks = Actor("trunks")
path_rocks = Actor("path_rocks")
grass = Actor("tall_grass")
leaves = Actor("bigleaves")
snow = Actor("snow")
door = Actor("door")
menu = Actor("menu")
win_screen = Actor("win_screen")
lose_screen = Actor("lose_screen")
#buttons|---------------------------------------------------
play_button = Actor("play_button")
menu_button = Actor("menu_button")
easydiff_button = Actor("easy_button")
normaldiff_button = Actor("normal_button")
harddiff_button = Actor("hard_button")
tutorial_button = Actor("tutorial_button")
play_again_button = Actor("play_again_button")
home_button = Actor("home_button")
back_button = Actor("back_arrow_button")
skins_button = Actor("skins_button")
#|---------------------------------------------------------

#sounds|---------------------------------------------------
menu_playing = False
win_sound_played = False
lose_sound_played = False
ingame_bsound_playing = False
showing_tutorial = False
boss_music_playing = False
skins_bgm_playing = False
size_w = 10 # Lebar dari bidang dalam sel
size_h = 10 # Tinggi dari bidang dalam sel
WIDTH = bg.width * size_w
HEIGHT = bg.height * size_h
mode = "menu" # Mode permainan
# Boss attack settings by difficulty
BOSS_ATTACK_SETTINGS = {
    "easy_game_difficulty": {
        "beam_damage": 1,
        "beam_tick": 0.3,
        "bone_damage": 1,
        "bone_tick": 0.3,
        "random_blaster_count": 3,
        "ground_bone_count": 5,
        "line_shots": 5,
        "spin_shots": 30,
        "move_interval": 1.2,
        "random_blaster_spawn_rate": 1.5,  # seconds between random blaster spawns
        "line_blaster_spawn_rate": 1.3,    # seconds between line blaster spawns
        "circle_blaster_spawn_rate": 0.5, # seconds between circle blaster spawns
        "ground_bone_spawn_rate": 1.3,     # seconds between ground bone spawns
    },
    "normal_game_difficulty": {
        "beam_damage": 2,
        "beam_tick": 0.2,
        "bone_damage": 2,
        "bone_tick": 0.2,
        "random_blaster_count": 5,
        "ground_bone_count": 7,
        "line_shots": 8,
        "spin_shots": 50,
        "move_interval": 1.0,
        "random_blaster_spawn_rate": 1,  # seconds between random blaster spawns
        "line_blaster_spawn_rate": 1,    # seconds between line blaster spawns
        "circle_blaster_spawn_rate": 0.4, # seconds between circle blaster spawns
        "ground_bone_spawn_rate": 1,     # seconds between ground bone spawns
    },
    "hard_game_difficulty": {
        "beam_damage": 2.5,
        "beam_tick": 0.2,
        "bone_damage": 2.5,
        "bone_tick": 0.2,
        "random_blaster_count": 7,
        "ground_bone_count": 12,
        "line_shots": 10,
        "spin_shots": 70,
        "move_interval": 0.7,
        "random_blaster_spawn_rate": 0.7,  # seconds between random blaster spawns
        "line_blaster_spawn_rate": 0.7,    # seconds between line blaster spawns
        "circle_blaster_spawn_rate": 0.2, # seconds between circle blaster spawns
        "ground_bone_spawn_rate": 0.7,     # seconds between ground bone spawns
    }
}
last_difficulty_mode = "normal_game_difficulty"  # Default
win = 0 # Menang
def get_player_grid():
    # Returns (col, row) of char1's current tile
    return int((char1.x - bg.width // 2) // bg.width), int((char1.y - bg.height // 2) // bg.height)

def is_enemy_at(grid_x, grid_y, enemy_list=None):
    if enemy_list is None:
        enemy_list = enemies
    for enemy in enemy_list:
        enemy_grid_x = int((enemy.x - bg.width // 2) // bg.width)
        enemy_grid_y = int((enemy.y - bg.height // 2) // bg.height)
        if enemy_grid_x == grid_x and enemy_grid_y == grid_y:
            return True
    return False

def get_all_chest_pixel_positions():
    # Returns a set of (x, y) pixel positions for all chests
    return set(
        (bg.width * (gx + 0.5), bg.height * (gy + 0.5))
        for gx, gy in chest_positions
    )

current_map = 1  # 1 for my_map1, 2 for my_map2
TITLE = "Sans Adventure" # Judul dari jendela permainan
FPS = 30 # Jumlah Frame Per Detik

tutorial_map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 8],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

tutorial_map2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [8, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 7, 7, 7, 7, 7, 7, 7, 7, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

forest_map1 =  [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [9, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
                [9, 11, 11, 11, 11, 11, 11, 11, 11, 11], 
                [9, 11, 12, 12, 12, 12, 12, 12, 12, 13], 
                [9, 11, 12, 12, 12, 12, 12, 12, 12, 13], 
                [9, 11, 12, 12, 12, 12, 12, 12, 12, 13], 
                [9, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],]

forest_map2 =  [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
                [11, 11, 11, 11, 11, 11, 11, 11, 11, 11], 
                [13, 12, 12, 12, 12, 12, 12, 12, 12, 14], 
                [13, 12, 12, 12, 12, 12, 12, 12, 12, 14], 
                [13, 12, 12, 12, 12, 12, 12, 12, 12, 14], 
                [11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],]

forest_map3 =  [[9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
                [11, 11, 11, 11, 11, 11, 11, 11, 0, 0], 
                [14, 12, 12, 12, 12, 12, 12, 12, 0, 0], 
                [14, 12, 12, 12, 12, 12, 12, 12, 15, 0], 
                [14, 12, 12, 12, 12, 12, 12, 12, 0, 0], 
                [11, 11, 11, 11, 11, 11, 11, 11, 0, 0],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9], 
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],]                

my_map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 2, 2, 1, 2, 1, 0], 
          [0, 1, 1, 2, 1, 2, 1, 1, 2, 0], 
          [0, 2, 1, 1, 2, 1, 1, 1, 1, 0], 
          [15, 1, 2, 1, 1, 1, 2, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 2, 0], 
          [0, 1, 2, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 2, 1, 1, 3], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

my_map2 = [[0, 0, 0, 0, 4, 0, 0, 0, 0, 0], 
          [0, 1, 1, 2, 1, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 2, 2, 1, 2, 1, 0], 
          [0, 1, 1, 2, 1, 2, 2, 1, 2, 0], 
          [0, 2, 1, 1, 2, 1, 1, 2, 1, 0], 
          [0, 1, 2, 1, 1, 1, 2, 1, 1, 0], 
          [0, 2, 1, 1, 2, 1, 2, 1, 2, 0], 
          [0, 1, 2, 1, 1, 1, 1, 1, 1, 0],
          [3, 1, 1, 1, 2, 1, 2, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

my_map3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 2, 1, 1, 1, 2, 1, 0],
           [0, 1, 2, 1, 2, 1, 2, 1, 1, 0],
           [0, 1, 1, 1, 1, 2, 1, 2, 1, 0],
           [5, 2, 1, 2, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 2, 1, 2, 2, 1, 0],
           [0, 1, 2, 1, 1, 1, 1, 1, 2, 0],
           [0, 1, 1, 1, 2, 2, 1, 1, 1, 0],
           [0, 1, 2, 1, 1, 1, 1, 2, 1, 0],
           [0, 0, 0, 0, 4, 0, 0, 0, 0, 0]]

my_map4 = [[0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
           [0, 1, 2, 1, 1, 1, 2, 1, 1, 0],
           [0, 1, 1, 1, 2, 1, 1, 1, 2, 0],
           [0, 2, 1, 2, 1, 1, 2, 1, 1, 0],
           [0, 1, 1, 1, 1, 2, 1, 1, 1, 0],
           [0, 1, 2, 1, 1, 1, 2, 1, 2, 5],
           [0, 1, 1, 1, 2, 1, 1, 1, 1, 0],
           [0, 2, 1, 2, 1, 1, 2, 2, 1, 0],
           [0, 1, 1, 1, 1, 2, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

my_map5 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 2, 1, 1, 1, 2, 0],
           [0, 2, 1, 2, 1, 1, 2, 1, 1, 0],
           [0, 1, 1, 1, 1, 2, 1, 2, 1, 0],
           [0, 1, 2, 1, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 2, 2, 1, 2, 2, 1, 0],
           [0, 2, 1, 1, 1, 1, 1, 1, 2, 0],
           [0, 1, 2, 2, 1, 2, 1, 1, 1, 0],
           [0, 1, 1, 1, 2, 1, 1, 2, 1, 0],
           [0, 0, 0, 0, 6, 0, 0, 0, 0, 0]]

def is_dungeon_map():
    return current_map > len(forest_maps)

def map_draw():

    my_map = maps[current_map - 1]  # Always use the current map
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            tile = my_map[i][j]
            if tile == 0:
                bg.left = bg.width * j
                bg.top = bg.height * i
                bg.draw()
            elif tile == 1:
                bg1.left = bg.width * j
                bg1.top = bg.height * i
                bg1.draw()
            elif tile == 2:
                bg2.left = bg.width * j
                bg2.top = bg.height * i
                bg2.draw()
            elif tile == 9:
                leaves.left = bg.width * j
                leaves.top = bg.height * i
                leaves.draw()
            elif tile == 10:
                tree_trunks.left = bg.width * j
                tree_trunks.top = bg.height * i
                tree_trunks.draw()
            elif tile == 11:
                grass.left = bg.width * j
                grass.top = bg.height * i
                grass.draw()
            elif tile in [12, 13, 14]:
                path_rocks.left = bg.width * j
                path_rocks.top = bg.height * i
                path_rocks.draw()
            elif tile in [3, 4, 5, 6, 8, 15]:
                door.left = bg.width * j
                door.top = bg.height * i
                door.draw()
            elif tile == 7:
                snow.left = bg.width * j
                snow.top = bg.height * i
                snow.draw()

def reset_game():
    global enemies, hearts, swords, char1, used_positions
    global enemies_map0, enemies_map1, enemies_map2, enemies_map3, enemies_map4, enemies_map5
    global hearts_map0, hearts_map1, hearts_map2, hearts_map3, hearts_map4, hearts_map5
    global swords_map0, swords_map1, swords_map2, swords_map3, swords_map4, swords_map5
    global current_map, win_sound_played, lose_sound_played
    global boss_door_locked, boss_key_found, boss_key_chest_index, boss_key_obtained, show_find_key_text, find_key_text_timer, boss_intro_dialog_active, boss_intro_dialog_index, boss_intro_dialog_timer, boss_outro_dialog_active, boss_outro_dialog_index, boss_outro_dialog_timer, boss_outro_fade_started, gaster_dialog_index, gaster_fading, gaster_alpha

    win_sound_played = False
    lose_sound_played = False
    current_map = 1  # Always start on map 1 (forest_map1)
    char1.health = 100
    char1.attack = 5
    char1.x = bg.width * (5 + 0.5)
    char1.y = bg.height * (5 + 0.5)

    used_positions.clear()
    boss_door_locked = True
    boss_key_found = False
    boss_key_chest_index = random.randint(0, 3)
    boss_key_obtained = False
    show_find_key_text = False
    find_key_text_timer = 0

    boss_intro_dialog_active = False
    boss_intro_dialog_index = 0
    boss_intro_dialog_timer = 0
    boss_outro_dialog_active = False
    boss_outro_dialog_index = 0
    boss_outro_dialog_timer = 0
    boss_outro_fade_started = False


    # Stop boss music if playing
    if hasattr(sounds, "boss_fight_music"):
        sounds.boss_fight_music.stop()

    # Reset Gaster state
    gaster.visible = True
    gaster_dialog_index = 0
    gaster_fading = False
    gaster_alpha = 255

    # Clear all lists
    for h in hearts_maps: h.clear()
    for s in swords_maps: s.clear()
    for e in enemies_maps: e.clear()
    # Make sure forest enemies are always empty
    for e in enemies_maps_forest:
        e.clear()
    hearts = hearts_maps[0]
    swords = swords_maps[0]
    enemies = enemies_maps[0]

    # Only spawn for dungeon maps (not forest)
    spawn_enemies_for_map1()
    spawn_enemies_for_map2()
    spawn_enemies_for_map3()
    spawn_enemies_for_map4()
    spawn_enemies_for_map5()
    spawn_enemies_for_map6()
    spawn_enemies_for_map7()
    # Do NOT spawn for forest maps!

    boss_door_bone["alpha"] = 255
    boss_door_bone["fading"] = False
    boss_door_bone["fade_timer"] = 0
    boss_fade["active"] = False
    boss_fade["alpha"] = 255
    boss_fade["fade_timer"] = 0

    # Set boss HP based on difficulty
    if mode == "easy_game_difficulty":
        boss.hp = 1000
    elif mode == "normal_game_difficulty":
        boss.hp = 1500
    elif mode == "hard_game_difficulty":
        boss.hp = 2000
    else:
        boss.hp = 1000

    for chest in chests:
        chest.image = "chest_closed"

#boss setup|---------------------------------------------------
boss = Actor("virus_sans_down")  # Replace with your boss sprite name
boss.x = bg.width * (len(my_map5[0]) // 2 + 0.5)
boss.y = bg.height * (len(my_map5) // 2 + 0.5)
boss.hp = 1000  # Default HP, will be set based on difficulty
boss.visible = False
boss_appearing = False
boss_appeared = False
boss_timer = 0
boss_attack_timer = 0
boss_attack_phase = "wait"  # "wait", "appear", "fight", "dead"
boss_bones = []
boss_blasters = []
boss_blaster_count = 0
boss_line_shots = 0
spin_shots = 0
spin_index = 0
spin_positions = []
spin_initialized = False
ground_bone_attacks = []
TILE_SIZE = bg.width  # or set to your tile size
boss_attack_phase_timer = 0
boss_attack_in_progress = False
boss_line_phase_done = False
last_boss_attack = None

boss_door_bone = {
    "alpha": 255,
    "fading": False,
    "fade_timer": 0,
    "pos": None  # (x, y) in pixels
}
boss_fade = {
    "active": False,
    "alpha": 255,
    "fade_time": 0
}
def get_boss_settings():
    return BOSS_ATTACK_SETTINGS.get(mode, BOSS_ATTACK_SETTINGS["normal_game_difficulty"])
boss_attack_next_delay = 0
boss_random_blaster_timer = 0
boss_line_blaster_timer = 0
boss_circle_blaster_timer = 0
boss_ground_bone_timer = 0
boss_ground_bone_count = 0
boss_intro_dialogs = [
    "Well hello there, challenger...",
    "You've made it quite far for someone \nwho barely remembers their own code.",
    "But this... is where your path ends."
]
boss_intro_dialog_index = 0
boss_intro_dialog_timer = 0
boss_intro_dialog_active = False

boss_outro_dialogs = [
    "You think this is over?",
    "The virus... it’s already spread.",
    "I was just... a pawn.",
    "You’ve won nothing, skeleton."
]
boss_outro_dialog_index = 0
boss_outro_dialog_timer = 0
boss_outro_dialog_active = False
boss_outro_fade_started = False


# Boss door lock/key system|---------------------------------------------------
boss_door_locked = True
boss_key_found = False
boss_key_chest_index = random.randint(0, 3)  # 0-3 for the 4 chests in the 4 rooms
boss_key_obtained = False
show_find_key_text = False
find_key_text_timer = 0

# Gaster NPC setup|---------------------------------------------------
gaster = Actor("gaster_idle", (bg.width * (size_w // 2 + 0.5), bg.height * (3 + 0.5)))
gaster.visible = True
gaster_dialog_index = 0
gaster_dialogs = [
    "You feel a strange presence...",
    "Gaster: The world is not what it seems.",
    "Gaster: Be careful, Sans. \nYour journey is just beginning."
]
gaster_fading = False
gaster_alpha = 255

#extras|---------------------------------------------------
blasters = []
beams = []
SUMMON_DURATION = 0.5
FIRE_DURATION = 2.0
FADEOUT_DURATION = 0.5
MOVE_HOLD_DELAY = 0.15
move_hold_dir = None
move_hold_timer = 0
mouse_pos = (WIDTH // 2, HEIGHT // 2)
BLASTER_COOLDOWN = 5.0  # seconds
blaster_cooldown_timer = 0.0
boss_attack_next_delay = 0

#title/texts|---------------------------------------------------
title = Actor("sa_title")
title.center = (WIDTH // 2, HEIGHT // 2 - 240)
title_anim_dir = 1  # 1 for down, -1 for up
title_anim_speed = 0.3  # Adjust for slower/faster animation
title_anim_range = 10   # How many pixels up and down
title_anim_base_y = title.y
#--------------------------------------------------------------
win_text = Actor("win_text")
lose_text = Actor("lose_text")
end_text_anim_y = 80
end_text_anim_dir = 1
end_text_anim_speed = 0.8  # Adjust for faster/slower animation
end_text_anim_range = 20   # How many pixels up and down
end_text_anim_base_y = 80

#--------------------------------------------------------------
select_difficulty_text = Actor("select_difficulty_text")
select_difficulty_text_anim_y = 100
select_difficulty_text_anim_dir = 1
select_difficulty_text_anim_speed = 0.3  # Adjust for faster/slower animation
select_difficulty_text_anim_range = 10   # How many pixels up and down
select_difficulty_text_anim_base_y = 100
#--------------------------------------------------------------
skins_selection_text = Actor("skins_selection_tittle")
skins_selection_text_anim_y = 100
skins_selection_text_anim_dir = 1
skins_selection_text_anim_speed = 0.3  # Adjust for faster/slower animation
skins_selection_text_anim_range = 10   # How many pixels up and down
skins_selection_text_anim_base_y = 100
#--------------------------------------------------------------
#Protagonis|---------------------------------------------------
char1 = Actor('classic_sans_right')
char1.top = bg.height
char1.left = bg.width
char1.health = 100
char1.attack = 5
char1_direction = "right"  # Possible values: "right", "left", "up", "down"
char1_skins = {
    "classic_sans": {
        "right": "classic_sans_right",
        "left": "classic_sans_left",
        "up": "classic_sans_up",
        "down": "classic_sans_down"
    },
    "king_sans": {
        "right": "king_sans_right",
        "left": "king_sans_left",
        "up": "king_sans_up",
        "down": "king_sans_down"
    },
    "swap_sans": {
        "right": "swap_sans_right",
        "left": "swap_sans_left",
        "up": "swap_sans_up",
        "down": "swap_sans_down"
    },
    "dust_sans": {
        "right": "dust_sans_right",
        "left": "dust_sans_left",
        "up": "dust_sans_up",
        "down": "dust_sans_down"
    },
    "ink_sans": {
        "right": "ink_sans_right",
        "left": "ink_sans_left",
        "up": "ink_sans_up",
        "down": "ink_sans_down"
    },
    "geno_sans": {
        "right": "geno_sans_right",
        "left": "geno_sans_left",
        "up": "geno_sans_up",
        "down": "geno_sans_down"
    },
    "aftertale_sans": {
        "right": "aftertale_sans_right",
        "left": "aftertale_sans_left",
        "up": "aftertale_sans_up",
        "down": "aftertale_sans_down"
    },
    "fell_sans": {
        "right": "fell_sans_right",
        "left": "fell_sans_left",
        "up": "fell_sans_up",
        "down": "fell_sans_down"
    }
}
# Set the current skin
current_skin = "classic_sans"
heart_spawn_timer = 0
#chest|---------------------------------------------------
chest = Actor("chest_closed")
chest_grid_pos = (5, 5)  # Example: grid position (col, row)
# One chest and position per map
chest_positions = [
    (2, 2),  # my_map1
    (7, 7),  # my_map2
    (4, 4),  # my_map3
    (6, 6),  # my_map4
    (5, 5),  # my_map5
]
chests = [Actor("chest_closed") for _ in chest_positions]
for i, (gx, gy) in enumerate(chest_positions):
    chests[i].x = bg.width * (gx + 0.5)
    chests[i].y = bg.height * (gy + 0.5)

health_bars = [
    "health_bar_0", "health_bar_1", "health_bar_2", "health_bar_3", "health_bar_4", "health_bar_5",
    "health_bar_6", "health_bar_7", "health_bar_8", "health_bar_9", "health_bar_10"
]
#bonus
hearts = []
swords = []

hearts_map0 = []
hearts_map1 = []
hearts_map2 = []
hearts_map3 = []
hearts_map4 = []
hearts_map5 = []
hearts_map6 = []
hearts_map7 = []

swords_map0 = []
swords_map1 = []
swords_map2 = []
swords_map3 = []
swords_map4 = []
swords_map5 = []
swords_map6 = []
swords_map7 = []

hearts = hearts_map1
swords = swords_map1

#membangkitkan musuh
enemies_map0 = []
enemies_map1 = []
enemies_map2 = []
enemies_map3 = []
enemies_map4 = []
enemies_map5 = []
enemies_map6 = []
enemies_map7 = []
tutorial_enemies_map1 = []
tutorial_enemies_map2 = []
enemies = enemies_map1
used_positions = set()

forest_maps = [forest_map1, forest_map2, forest_map3]
dungeon_maps = [my_map1, my_map2, my_map3, my_map4, my_map5]
maps = forest_maps + dungeon_maps

hearts_maps_forest = [hearts_map0, hearts_map1, hearts_map2]
hearts_maps_dungeon = [hearts_map3, hearts_map4, hearts_map5, hearts_map6, hearts_map7]
hearts_maps = hearts_maps_forest + hearts_maps_dungeon

swords_maps_forest = [swords_map0, swords_map1, swords_map2]
swords_maps_dungeon = [swords_map3, swords_map4, swords_map5, swords_map6, swords_map7]
swords_maps = swords_maps_forest + swords_maps_dungeon

enemies_maps_forest = [enemies_map0, enemies_map1, enemies_map2]
enemies_maps_dungeon = [enemies_map3, enemies_map4, enemies_map5, enemies_map6, enemies_map7]
enemies_maps = enemies_maps_forest + enemies_maps_dungeon

def move_sans_tile(direction):
    global char1_direction, current_map, char1, hearts, swords, enemies

    grid_x, grid_y = get_player_grid()
    my_map = maps[current_map - 1]
    nx, ny = grid_x, grid_y

    if direction == "right":
        char1_direction = "right"
        nx += 1
    elif direction == "left":
        char1_direction = "left"
        nx -= 1
    elif direction == "up":
        char1_direction = "up"
        ny -= 1
    elif direction == "down":
        char1_direction = "down"
        ny += 1

    # --- Block movement ONTO Gaster's tile if in forest_map1 and Gaster is visible ---
    if current_map == 1 and gaster.visible:
        if nx == 5 and ny == 3:
            return  # Block movement if trying to move onto Gaster
        
    # --- Boss blocking logic ---
    if current_map == maps.index(my_map5) + 1 and boss.visible:
        boss_grid_x = int((boss.x - bg.width // 2) // bg.width)
        boss_grid_y = int((boss.y - bg.height // 2) // bg.height)
        if nx == boss_grid_x and ny == boss_grid_y:
            return  # Block movement if trying to move onto boss

    # --- Boss room door bone block ---
    if current_map == maps.index(my_map5) + 1 and boss_door_bone["pos"]:
        door_x, door_y = boss_door_bone["pos"]
        door_grid_x = int((door_x - TILE_SIZE // 2) // TILE_SIZE)
        door_grid_y = int((door_y - TILE_SIZE // 2) // TILE_SIZE)
        if nx == door_grid_x and ny == door_grid_y and boss_door_bone["alpha"] > 0:
            return  # Block movement if bone is present
        
    # --- Forest map teleport logic ---
    if current_map == 1 and direction == "right" and nx < len(my_map[0]) and my_map[ny][nx] == 13:
        # Forest 1 to Forest 2
        for y in range(len(forest_map2)):
            for x in range(len(forest_map2[0])):
                if forest_map2[y][x] == 13:
                    current_map = 2
                    char1.x = bg.width * (x + 0.5)
                    char1.y = bg.height * (y + 0.5)
                    blasters.clear()
                    beams.clear()
                    return
    if current_map == 2 and direction == "left" and nx >= 0 and my_map[ny][nx] == 13:
        # Forest 2 to Forest 1
        for y in range(len(forest_map1)):
            for x in range(len(forest_map1[0])):
                if forest_map1[y][x] == 13:
                    current_map = 1
                    char1.x = bg.width * (x + 0.5)
                    char1.y = bg.height * (y + 0.5)
                    blasters.clear()
                    beams.clear()
                    return
    if current_map == 2 and direction == "right" and nx < len(my_map[0]) and my_map[ny][nx] == 14:
        # Forest 2 to Forest 3
        for y in range(len(forest_map3)):
            for x in range(len(forest_map3[0])):
                if forest_map3[y][x] == 14:
                    current_map = 3
                    char1.x = bg.width * (x + 0.5)
                    char1.y = bg.height * (y + 0.5)
                    blasters.clear()
                    beams.clear()
                    return
    if current_map == 3 and direction == "left" and nx >= 0 and my_map[ny][nx] == 14:
        # Forest 3 to Forest 2
        for y in range(len(forest_map2)):
            for x in range(len(forest_map2[0])):
                if forest_map2[y][x] == 14:
                    current_map = 2
                    char1.x = bg.width * (x + 0.5)
                    char1.y = bg.height * (y + 0.5)
                    blasters.clear()
                    beams.clear()
                    return

    # --- Normal tile movement ---
    if 0 <= nx < len(my_map[0]) and 0 <= ny < len(my_map):
        blocked_by_chest = False
        # Only block by chest if NOT in boss room (my_map5)
        if current_map > 3 and current_map != maps.index(my_map5) + 1:
            chest = chests[current_map - 4]
            chest_grid_pos = chest_positions[current_map - 4]
            if (nx, ny) == chest_grid_pos and chest.image == "chest_closed":
                blocked_by_chest = True
        if my_map[ny][nx] not in [0, 9, 10] and not is_enemy_at(nx, ny, enemies) and not blocked_by_chest:
            char1.x = bg.width * (nx + 0.5)
            char1.y = bg.height * (ny + 0.5)

def tutorial_movement_logic(key):
    global char1_direction
    tutorial_map = tutorial_map1 if current_tutorial_map == 1 else tutorial_map2
    grid_x, grid_y = get_player_grid()
    current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2

    if (keyboard.right or keyboard.d):
        char1_direction = "right"
        char1.image = char1_skins[current_skin][char1_direction]
        nx, ny = grid_x + 1, grid_y
        if nx < len(tutorial_map[0]) and (tutorial_map[ny][nx] != 0 or tutorial_map[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.x += bg.width

    elif (keyboard.left or keyboard.a):
        char1_direction = "left"
        char1.image = char1_skins[current_skin][char1_direction]
        nx, ny = grid_x - 1, grid_y
        if nx < len(tutorial_map[0]) and (tutorial_map[ny][nx] != 0 or tutorial_map[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.x -= bg.width

    elif (keyboard.down or keyboard.s):
        char1_direction = "down"
        char1.image = char1_skins[current_skin][char1_direction]
        nx, ny = grid_x, grid_y + 1
        if nx < len(tutorial_map[0]) and (tutorial_map[ny][nx] != 0 or tutorial_map[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.y += bg.height

    elif (keyboard.up or keyboard.w):
        char1_direction = "up"
        char1.image = char1_skins[current_skin][char1_direction]
        nx, ny = grid_x, grid_y - 1
        if nx < len(tutorial_map[0]) and (tutorial_map[ny][nx] != 0 or tutorial_map[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.y -= bg.height

def tutorial_door_logic(key):
    global current_tutorial_map
    if key == keys.SPACE:
        grid_x, grid_y = get_player_grid()
        tutorial_map = tutorial_map1 if current_tutorial_map == 1 else tutorial_map2
        tile = tutorial_map[grid_y][grid_x]
        if tile == 8:
            # Find the other tutorial map and the position of door 8
            if current_tutorial_map == 1:
                for y in range(len(tutorial_map2)):
                    for x in range(len(tutorial_map2[0])):
                        if tutorial_map2[y][x] == 8:
                            current_tutorial_map = 2
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            else:
                for y in range(len(tutorial_map1)):
                    for x in range(len(tutorial_map1[0])):
                        if tutorial_map1[y][x] == 8:
                            current_tutorial_map = 1
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return

def tutorial_attack_logic(key):
    if key == keys.F:
        grid_x, grid_y = get_player_grid()
        if char1_direction == "right":
            atk_x, atk_y = grid_x + 1, grid_y
        elif char1_direction == "left":
            atk_x, atk_y = grid_x - 1, grid_y
        elif char1_direction == "up":
            atk_x, atk_y = grid_x, grid_y - 1
        elif char1_direction == "down":
            atk_x, atk_y = grid_x, grid_y + 1
        else:
            atk_x, atk_y = grid_x, grid_y
        current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2
        for idx, enemy in enumerate(current_enemy_list):
            enemy_grid_x = int((enemy.x - bg.width // 2) // bg.width)
            enemy_grid_y = int((enemy.y - bg.height // 2) // bg.height)
            if enemy_grid_x == atk_x and enemy_grid_y == atk_y:
                sounds.slash.play()
                enemy.health -= char1.attack
                char1.health -= enemy.attack
                if enemy.health <= 0:
                    drop_enemy_bonus(enemy)
                    current_enemy_list.pop(idx)
                break

# Add a 2x2 gap around the player spawn
for dx in range(2):
    for dy in range(2):
        used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))

def spawn_tutorial_enemies_map1():
    global tutorial_enemies_map1
    tutorial_enemies_map1.clear()
    # No enemies for tutorial_map1

def spawn_tutorial_enemies_map2():
    global tutorial_enemies_map2
    tutorial_enemies_map2.clear()
    # Place 1 knight at (2,2) and 1 juggernaut at (7,7) (adjust as needed)
    knight = Actor("knight", topleft=(bg.width * 2, bg.height * 2))
    knight.health = 10
    knight.attack = 5
    knight.bonus = 0
    tutorial_enemies_map2.append(knight)

    juggernaut = Actor("juggernaut", topleft=(bg.width * 7, bg.height * 7))
    juggernaut.health = 20
    juggernaut.attack = 8
    juggernaut.bonus = 0
    tutorial_enemies_map2.append(juggernaut)

def spawn_enemies_for_map1():
    global enemies_map1
    enemies_map1.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[0][0] + 0.5), bg.height * (chest_positions[0][1] + 0.5))}
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy1.health = 8   # Easy HP
            enemy1.attack = random.randint(3, 6)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy1.health = 10  # Normal HP
            enemy1.attack = random.randint(5, 10) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy1.health = 15  # Hard HP
            enemy1.attack = random.randint(8, 15) # Hard Damage
        # -------------------------------
        enemy1.bonus = random.randint(1, 2)
        enemies_map1.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy2.health = 15  # Easy HP
            enemy2.attack = random.randint(5, 8)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy2.health = 20  # Normal HP
            enemy2.attack = random.randint(8, 12) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy2.health = 30  # Hard HP
            enemy2.attack = random.randint(12, 20) # Hard Damage
        # -------------------------------
        enemy2.bonus = random.randint(1, 2)
        enemies_map1.append(enemy2)

def spawn_enemies_for_map2():
    global enemies_map2
    enemies_map2.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[1][0] + 0.5), bg.height * (chest_positions[1][1] + 0.5))}
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy1.health = 8   # Easy HP
            enemy1.attack = random.randint(3, 6)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy1.health = 10  # Normal HP
            enemy1.attack = random.randint(5, 10) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy1.health = 15  # Hard HP
            enemy1.attack = random.randint(8, 15) # Hard Damage
        # -------------------------------
        enemy1.bonus = random.randint(1, 2)
        enemies_map2.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy2.health = 15  # Easy HP
            enemy2.attack = random.randint(5, 8)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy2.health = 20  # Normal HP
            enemy2.attack = random.randint(8, 12) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy2.health = 30  # Hard HP
            enemy2.attack = random.randint(12, 20) # Hard Damage
        # -------------------------------
        enemy2.bonus = random.randint(1, 2)
        enemies_map2.append(enemy2)

def spawn_enemies_for_map3():
    global enemies_map3
    enemies_map3.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[2][0] + 0.5), bg.height * (chest_positions[2][1] + 0.5))}

    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy1.health = 8   # Easy HP
            enemy1.attack = random.randint(3, 6)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy1.health = 10  # Normal HP
            enemy1.attack = random.randint(5, 10) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy1.health = 15  # Hard HP
            enemy1.attack = random.randint(8, 15) # Hard Damage
        # -------------------------------
        enemy1.bonus = random.randint(1, 2)
        enemies_map3.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy2.health = 15  # Easy HP
            enemy2.attack = random.randint(5, 8)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy2.health = 20  # Normal HP
            enemy2.attack = random.randint(8, 12) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy2.health = 30  # Hard HP
            enemy2.attack = random.randint(12, 20) # Hard Damage
        # -------------------------------
        enemy2.bonus = random.randint(1, 2)
        enemies_map3.append(enemy2)

def spawn_enemies_for_map4():
    global enemies_map4
    enemies_map4.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[3][0] + 0.5), bg.height * (chest_positions[3][1] + 0.5))}

    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
         # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy1.health = 8   # Easy HP
            enemy1.attack = random.randint(3, 6)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy1.health = 10  # Normal HP
            enemy1.attack = random.randint(5, 10) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy1.health = 15  # Hard HP
            enemy1.attack = random.randint(8, 15) # Hard Damage
        # -------------------------------
        enemy1.bonus = random.randint(1, 2)
        enemies_map4.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy2.health = 15  # Easy HP
            enemy2.attack = random.randint(5, 8)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy2.health = 20  # Normal HP
            enemy2.attack = random.randint(8, 12) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy2.health = 30  # Hard HP
            enemy2.attack = random.randint(12, 20) # Hard Damage
        # -------------------------------
        enemy2.bonus = random.randint(1, 2)
        enemies_map4.append(enemy2)

def spawn_enemies_for_map5():
    global enemies_map5
    enemies_map5.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[4][0] + 0.5), bg.height * (chest_positions[4][1] + 0.5))}
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
         # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy1.health = 8   # Easy HP
            enemy1.attack = random.randint(3, 6)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy1.health = 10  # Normal HP
            enemy1.attack = random.randint(5, 10) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy1.health = 15  # Hard HP
            enemy1.attack = random.randint(8, 15) # Hard Damage
        # -------------------------------
        enemy1.bonus = random.randint(1, 2)
        enemies_map5.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        # --- DIFFICULTY CUSTOMIZATION ---
        if mode == "easy_game_difficulty":
            enemy2.health = 15  # Easy HP
            enemy2.attack = random.randint(5, 8)  # Easy Damage
        elif mode == "normal_game_difficulty":
            enemy2.health = 20  # Normal HP
            enemy2.attack = random.randint(8, 12) # Normal Damage
        elif mode == "hard_game_difficulty":
            enemy2.health = 30  # Hard HP
            enemy2.attack = random.randint(12, 20) # Hard Damage
        # -------------------------------
        enemy2.bonus = random.randint(1, 2)
        enemies_map5.append(enemy2)

def spawn_enemies_for_map6():
    global enemies_map6
    enemies_map6.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[3][0] + 0.5), bg.height * (chest_positions[3][1] + 0.5))}
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft=(x, y))
        if mode == "easy_game_difficulty":
            enemy1.health = 8
            enemy1.attack = random.randint(3, 6)
        elif mode == "normal_game_difficulty":
            enemy1.health = 10
            enemy1.attack = random.randint(5, 10)
        elif mode == "hard_game_difficulty":
            enemy1.health = 15
            enemy1.attack = random.randint(8, 15)
        enemy1.bonus = random.randint(1, 2)
        enemies_map6.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft=(x, y))
        if mode == "easy_game_difficulty":
            enemy2.health = 15
            enemy2.attack = random.randint(5, 8)
        elif mode == "normal_game_difficulty":
            enemy2.health = 20
            enemy2.attack = random.randint(8, 12)
        elif mode == "hard_game_difficulty":
            enemy2.health = 30
            enemy2.attack = random.randint(12, 20)
        enemy2.bonus = random.randint(1, 2)
        enemies_map6.append(enemy2)

def spawn_enemies_for_map7():
    global enemies_map7
    enemies_map7.clear()
    used_positions = set()
    chest_pixel_positions = {(bg.width * (chest_positions[4][0] + 0.5), bg.height * (chest_positions[4][1] + 0.5))}
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft=(x, y))
        if mode == "easy_game_difficulty":
            enemy1.health = 8
            enemy1.attack = random.randint(3, 6)
        elif mode == "normal_game_difficulty":
            enemy1.health = 10
            enemy1.attack = random.randint(5, 10)
        elif mode == "hard_game_difficulty":
            enemy1.health = 15
            enemy1.attack = random.randint(8, 15)
        enemy1.bonus = random.randint(1, 2)
        enemies_map7.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions and pos not in chest_pixel_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft=(x, y))
        if mode == "easy_game_difficulty":
            enemy2.health = 15
            enemy2.attack = random.randint(5, 8)
        elif mode == "normal_game_difficulty":
            enemy2.health = 20
            enemy2.attack = random.randint(8, 12)
        elif mode == "hard_game_difficulty":
            enemy2.health = 30
            enemy2.attack = random.randint(12, 20)
        enemy2.bonus = random.randint(1, 2)
        enemies_map7.append(enemy2)

def drop_enemy_bonus(enemy):
    if enemy.bonus == 1:
        heart = Actor("heart")
        heart.pos = enemy.pos
        hearts_maps[current_map - 1].append(heart)
    elif enemy.bonus == 2:
        sword = Actor("knive")
        sword.pos = enemy.pos
        swords_maps[current_map - 1].append(sword)
    else:
        # No bonus drop
        return

def draw():
    global menu_playing, ingame_bsound_playing, skins_bgm_playing, menu_playing, ingame_bsound_playing, hearts, swords, enemies
    if mode == "menu":
        screen.fill("#000000")
        menu.center = (WIDTH // 2, HEIGHT // 2)
        menu.draw()
        title.draw()
        play_button.center = (WIDTH // 2, HEIGHT // 2 + 120)
        play_button.draw()
        skins_button.center = (WIDTH // 2, HEIGHT // 2 + 200)
        skins_button.draw()

        # Play menu music
        if not menu_playing:
            sounds.menu.set_volume(0.5)
            sounds.menu.play(-1)
            menu_playing = True
        # Stop ingame music if playing
        if ingame_bsound_playing:
            sounds.ingame_bsound.stop()
            ingame_bsound_playing = False
        return
    
    elif mode == "difficulty_selection":
        screen.fill("#000000")
        select_difficulty_text.center = (WIDTH // 2, select_difficulty_text_anim_y)
        select_difficulty_text.draw()
        easydiff_button.center = (WIDTH // 2 - 100, HEIGHT // 2 - 40)
        easydiff_button.draw()
        normaldiff_button.center = (WIDTH // 2 + 100, HEIGHT // 2 - 40)
        normaldiff_button.draw()
        harddiff_button.center = (WIDTH // 2, HEIGHT // 2 + 90)
        harddiff_button.draw()
        tutorial_button.center = (WIDTH // 2, HEIGHT // 2 + 200)
        tutorial_button.draw()
        # Draw back button at top left
        back_button.topleft = (10, 10)
        back_button.draw()
            # Play menu music
        if not menu_playing:
            sounds.menu.set_volume(0.5)
            sounds.menu.play(-1)
            menu_playing = True
        # Stop ingame music if playing
        if ingame_bsound_playing:
            sounds.ingame_bsound.stop()
            ingame_bsound_playing = False
        return

    elif mode == "tutorial":
        # Draw the correct tutorial map
        screen.fill("#222244")  # Fill background first!
        # Draw the correct tutorial map
        tutorial_map = tutorial_map1 if current_tutorial_map == 1 else tutorial_map2
        for i in range(len(tutorial_map)):
            for j in range(len(tutorial_map[0])):
                tile = tutorial_map[i][j]
                if tile == 0:
                    bg.left = bg.width * j
                    bg.top = bg.height * i
                    bg.draw()
                elif tile == 1:
                    bg1.left = bg.width * j
                    bg1.top = bg.height * i
                    bg1.draw()
                elif tile == 2:
                    bg2.left = bg.width * j
                    bg2.top = bg.height * i
                    bg2.draw()
                elif tile in [3, 4, 5, 6, 8]:
                    door.left = bg.width * j
                    door.top = bg.height * i
                    door.draw()
                elif tile == 7:
                    snow.left = bg.width * j
                    snow.top = bg.height * i
                    snow.draw()
        
        # Draw the player character in the tutorial
        char1.draw()
        # Draw HP and AP above char1
        hp_index = max(0, min(10, char1.health // 10))
        hp_bar = Actor(health_bars[hp_index])
        hp_bar.x = char1.x
        hp_bar.y = char1.y - 50  # Adjust as needed
        hp_bar.draw()
        screen.draw.text(
            f"AP: {char1.attack}",
            center=(char1.x, char1.y - 35),
            color='white',
            fontsize=20,
            owidth=1.5, ocolor="black"
        )
        screen.draw.text(
            "Tutorial:\n\n- Use WASD or Arrow keys to move\n- Press F to attack in the direction you are facing\n- Collect hearts and knives for bonuses\n- press Spacebar Use doors to move between rooms\n- Press E to open chests\n- press G to summon Gaster Blasters\n\nPress ESC to return to menu.",
            center=(WIDTH // 2, HEIGHT // 2),
            color="white",
            fontsize=24,
            owidth=2, ocolor="black"
        )
        # Draw enemies for tutorial_map2 only
        if current_tutorial_map == 1:
            for enemy in tutorial_enemies_map1:
                enemy.draw()
        elif current_tutorial_map == 2:
            for enemy in tutorial_enemies_map2:
                enemy.draw()
        # Draw blasters in tutorial
        for blaster in blasters:
            blaster["actor"].angle = -math.degrees(blaster["angle"]) + 90
            blaster["actor"]._surf.set_alpha(int(blaster["alpha"]))
            blaster["actor"].draw()
        # Draw beams in tutorial
        max_thickness = 32
        min_thickness = 8
        amp = 0.3
        osc_speed = 6
        for beam in beams:
            x, y = beam["x"], beam["y"]
            angle = beam["angle"]
            t = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
            if t < 0.2:
                thickness = min_thickness + (max_thickness - min_thickness) * (t / 0.2)
            elif t > 0.85:
                thickness = max_thickness * (1 - (t - 0.85) / 0.15)
                thickness = max(thickness, 1)
            else:
                base = max_thickness * (1 - amp)
                osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t - 0.2))) / 2
                thickness = base + osc
            thickness = int(thickness)
            length = 1000
            end_x = x + math.cos(angle) * length
            end_y = y + math.sin(angle) * length
            steps = 100
            for i in range(steps):
                px = x + (end_x - x) * i / steps
                py = y + (end_y - y) * i / steps
                screen.draw.filled_circle((px, py), thickness // 2, "white")
        # --- Gaster Blaster cooldown indicator (top right) ---
        indicator_x = WIDTH - 80
        indicator_y = 40
        box_w, box_h = 64, 64
        # Draw background box
        screen.draw.filled_rect(Rect((indicator_x, indicator_y), (box_w, box_h)), (30, 30, 30))
        screen.draw.rect(Rect((indicator_x, indicator_y), (box_w, box_h)), (200, 200, 200))

        # Draw blaster icon (centered in box)
        blaster_icon = Actor("gblaster_idle")
        blaster_icon.center = (indicator_x + box_w // 2, indicator_y + box_h // 2)
        if blaster_cooldown_timer > 0:
            blaster_icon._surf.set_alpha(100)  # Lower opacity if on cooldown
        else:
            blaster_icon._surf.set_alpha(255)
        blaster_icon.draw()

        # Draw cooldown timer if on cooldown
        if blaster_cooldown_timer > 0:
            timer_text = f"{blaster_cooldown_timer:.1f}s"
            screen.draw.text(
                timer_text,
                center=(indicator_x + box_w // 2, indicator_y + box_h - 12),
                color="white",
                fontsize=24,
                owidth=2, ocolor="black"
            )
        return

    elif mode == "skins_selection":
        screen.fill("#000000")
        # Play skins bgm
        if not skins_bgm_playing:
            sounds.skins_bgmusic.set_volume(0.5)
            sounds.skins_bgmusic.play(-1)
            skins_bgm_playing = True
        # Stop other music
        if menu_playing:
            sounds.menu.stop()
            menu_playing = False
        if ingame_bsound_playing:
            sounds.ingame_bsound.stop()
            ingame_bsound_playing = False
        # Draw the animated title
        skins_selection_text.center = (WIDTH // 2, skins_selection_text_anim_y)
        skins_selection_text.draw()

        skin_keys = list(char1_skins.keys())
        skin_display_names = [
            "Classic Sans", "King Sans", "Swap Sans", "Dust Sans",
            "Ink Sans", "Geno Sans", "Aftertale Sans", "Fell Sans"
        ]
        skin_positions = [
            (WIDTH // 2 - 220, HEIGHT // 2 - 60),
            (WIDTH // 2 - 70, HEIGHT // 2 - 60),
            (WIDTH // 2 + 80, HEIGHT // 2 - 60),
            (WIDTH // 2 + 230, HEIGHT // 2 - 60),
            (WIDTH // 2 - 220, HEIGHT // 2 + 80),
            (WIDTH // 2 - 70, HEIGHT // 2 + 80),
            (WIDTH // 2 + 80, HEIGHT // 2 + 80),
            (WIDTH // 2 + 230, HEIGHT // 2 + 80),
        ]
        for i, (skin, pos) in enumerate(zip(skin_keys, skin_positions)):
            actor = Actor(char1_skins[skin]["down"])
            actor.center = pos
            actor.draw()
            # Draw yellow rect if selected
            if current_skin == skin:
                screen.draw.rect(Rect((pos[0] - 44, pos[1] - 44), (88, 88)), (255, 255, 0))
            # Draw the name below each skin
            screen.draw.text(
                skin_display_names[i],
                center=(pos[0], pos[1] + 60),
                color="white",
                fontsize=24,
                owidth=2, ocolor="black"
            )
        back_button.topleft = (10, 10)
        back_button.draw()
        return

    if mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
        map_draw()
        if current_map == maps.index(my_map5) + 1 and boss_attack_phase in ["wait", "appear", "fight"]:
        # Find the door tile (6) in my_map5 and draw a blocking bone on it
            for y in range(len(my_map5)):
                for x in range(len(my_map5[0])):
                    if my_map5[y][x] == 6:
                        bone_actor = Actor("virus_sans_groundbones", (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                        bone_actor.draw()
        hearts = hearts_maps[current_map - 1]
        swords = swords_maps[current_map - 1]
        enemies = enemies_maps[current_map - 1]
        if is_dungeon_map():
            # Draw chest, but NOT in boss room
            if current_map != maps.index(my_map5) + 1:
                chest = chests[current_map - len(forest_maps) - 1]
                chest.draw()
            # Draw enemies
            for enemy in enemies:
                enemy.draw()
        # Draw player and bonuses always
        if current_map == maps.index(my_map5) + 1 and boss_door_bone["pos"]:
            bone_actor = Actor("virus_sans_groundbones", boss_door_bone["pos"])
            bone_actor._surf.set_alpha(int(boss_door_bone["alpha"]))
            bone_actor.draw()
        char1.draw()
        if current_map == maps.index(my_map5) + 1 and boss.visible:
            boss.draw()
            # Draw boss HP bar
            bar_w = 300
            bar_h = 20
            bar_x = WIDTH // 2 - bar_w // 2
            bar_y = 30
            hp_ratio = max(0, boss.hp / get_boss_max_hp())
            screen.draw.filled_rect(Rect((bar_x, bar_y), (bar_w, bar_h)), (60, 60, 60))
            screen.draw.filled_rect(Rect((bar_x, bar_y), (int(bar_w * hp_ratio), bar_h)), (255, 80, 80))
            screen.draw.rect(Rect((bar_x, bar_y), (bar_w, bar_h)), (255, 255, 255))
            screen.draw.text(f"Boss HP: {boss.hp}", center=(bar_x + bar_w // 2, bar_y + bar_h // 2), color="white", fontsize=24)

        # Boss intro dialog
        if current_map == maps.index(my_map5) + 1 and boss_attack_phase == "appear" and boss_intro_dialog_active:
            dialog = boss_intro_dialogs[boss_intro_dialog_index]
            dialog_w, dialog_h = 600, 80
            dialog_x = WIDTH // 2 - dialog_w // 2
            dialog_y = HEIGHT // 2 + 120
            screen.draw.filled_rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (30, 30, 30))
            screen.draw.rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (200, 200, 200))
            screen.draw.text(
                dialog,
                center=(WIDTH // 2, dialog_y + dialog_h // 2),
                color="white",
                fontsize=32,
                owidth=2, ocolor="black"
            )

        # Boss outro dialog
        if current_map == maps.index(my_map5) + 1 and boss_outro_dialog_active:
            dialog = boss_outro_dialogs[boss_outro_dialog_index]
            dialog_w, dialog_h = 700, 80
            dialog_x = WIDTH // 2 - dialog_w // 2
            dialog_y = HEIGHT // 2 + 120
            screen.draw.filled_rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (30, 30, 30))
            screen.draw.rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (200, 200, 200))
            screen.draw.text(
                dialog,
                center=(WIDTH // 2, dialog_y + dialog_h // 2),
                color="white",
                fontsize=32,
                owidth=2, ocolor="black"
            )

        # Draw lock on boss door in my_map4 if locked
        if current_map == maps.index(my_map4) + 1 and boss_door_locked:
            # Find the door tile (6) in my_map4
            for y in range(len(my_map4)):
                for x in range(len(my_map4[0])):
                    if my_map4[y][x] == 6:
                        lock_actor = Actor("lock", (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                        lock_actor.draw()

        # Draw lock on boss door if locked
        if current_map == maps.index(my_map5) + 1 and boss_door_locked and boss_door_bone["pos"]:
            lock_actor = Actor("lock", boss_door_bone["pos"])
            lock_actor.draw()

        # Draw key on the chest that has it (optional)
        if current_map > 3 and current_map != maps.index(my_map5) + 1:
            chest_index = current_map - 4
            chest = chests[chest_index]
            if chest_index == boss_key_chest_index and not boss_key_obtained:
                key_actor = Actor("key")
                key_actor.x = chest.x
                key_actor.y = chest.y - 30  # Above the chest
                key_actor.draw()

        if show_find_key_text:
            screen.draw.text(
                "Find the key in the chest!",
                center=(WIDTH // 2, HEIGHT // 2 + 180),
                color="yellow",
                fontsize=36,
                owidth=2, ocolor="black"
            )

        # Draw blasters
        for blaster in blasters:
            blaster["actor"].angle = -math.degrees(blaster["angle"]) + 90
            blaster["actor"]._surf.set_alpha(int(blaster["alpha"]))
            blaster["actor"].draw()
        for blaster in boss_blasters:
            blaster["actor"].draw()
        for bone in boss_bones:
            bone["actor"].draw()

        # Draw beams
        max_thickness = 32
        min_thickness = 8
        amp = 0.3
        osc_speed = 6
        for beam in beams:
            x, y = beam["x"], beam["y"]
            angle = beam["angle"]
            t = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
            if t < 0.2:
                thickness = min_thickness + (max_thickness - min_thickness) * (t / 0.2)
            elif t > 0.85:
                thickness = max_thickness * (1 - (t - 0.85) / 0.15)
                thickness = max(thickness, 1)
            else:
                base = max_thickness * (1 - amp)
                osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t - 0.2))) / 2
                thickness = base + osc
            thickness = int(thickness)
            length = 1000
            end_x = x + math.cos(angle) * length
            end_y = y + math.sin(angle) * length
            steps = 100
            for i in range(steps):
                px = x + (end_x - x) * i / steps
                py = y + (end_y - y) * i / steps
                screen.draw.filled_circle((px, py), thickness // 2, "white")
        
        # Draw ground bone attacks (boss ground bones)
        for attack in ground_bone_attacks:
            for tx, ty in attack["tiles"]:
                bone_x = tx * TILE_SIZE + TILE_SIZE // 2
                bone_y = ty * TILE_SIZE + TILE_SIZE // 2
                bone_actor = Actor("virus_sans_groundbones", (bone_x, bone_y))
                # Set alpha based on state
                if attack["state"] == "warn":
                    bone_actor._surf.set_alpha(80)
                elif attack["state"] == "fadein":
                    alpha = int(80 + 175 * (attack["timer"] / 0.5))
                    bone_actor._surf.set_alpha(alpha)
                elif attack["state"] == "stay":
                    bone_actor._surf.set_alpha(255)
                elif attack["state"] == "fadeout":
                    alpha = int(255 * (1 - attack["timer"] / 0.5))
                    bone_actor._surf.set_alpha(alpha)
                bone_actor.draw()

        hp_index = max(0, min(10, int(char1.health // 10)))
        hp_bar = Actor(health_bars[hp_index])
        hp_bar.x = char1.x
        hp_bar.y = char1.y - 50
        hp_bar.draw()
        screen.draw.text(
            f"AP: {char1.attack}",
            center=(char1.x, char1.y - 35),
            color='white',
            fontsize=20,
            owidth=1.5, ocolor="black"
        )

       # Draw Gaster if in forest_map1 and visible
        if current_map == 1 and gaster.visible:
            gaster._surf.set_alpha(gaster_alpha)
            gaster.draw()
            # Draw dialog box if player is adjacent and dialog active
            grid_x, grid_y = get_player_grid()
            gaster_grid_x = int((gaster.x - bg.width // 2) // bg.width)
            gaster_grid_y = int((gaster.y - bg.height // 2) // bg.height)
            adjacent = (
                abs(grid_x - gaster_grid_x) + abs(grid_y - gaster_grid_y) == 1
            )
            if adjacent:
                # Draw dialog rect
                dialog_w, dialog_h = 420, 80
                dialog_x = WIDTH // 2 - dialog_w // 2
                dialog_y = HEIGHT // 2 + 120
                screen.draw.filled_rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (30, 30, 30))
                screen.draw.rect(Rect((dialog_x, dialog_y), (dialog_w, dialog_h)), (200, 200, 200))
                # Draw dialog text
                if gaster_dialog_index < len(gaster_dialogs):
                    screen.draw.text(
                        gaster_dialogs[gaster_dialog_index],
                        center=(WIDTH // 2, dialog_y + dialog_h // 2),
                        color="white",
                        fontsize=28,
                        owidth=2, ocolor="black"
                    )
                # Draw 'R' prompt above Gaster
                screen.draw.text(
                    "Press R",
                    center=(gaster.x, gaster.y - 60),
                    color="yellow",
                    fontsize=32,
                    owidth=2, ocolor="black"
                )

        for heart in hearts:
            heart.draw()
        for sword in swords:
            sword.draw()
        # Draw home button
        home_button.topleft = (10, 10)
        home_button.draw()
        # Draw Gaster Blaster cooldown indicator (top right)
        indicator_x = WIDTH - 80
        indicator_y = 40
        box_w, box_h = 64, 64

        # Draw background box
        screen.draw.filled_rect(Rect((indicator_x, indicator_y), (box_w, box_h)), (30, 30, 30))
        screen.draw.rect(Rect((indicator_x, indicator_y), (box_w, box_h)), (200, 200, 200))

        # Draw blaster icon (centered in box)
        blaster_icon = Actor("gblaster_idle")
        blaster_icon.center = (indicator_x + box_w // 2, indicator_y + box_h // 2)
        if blaster_cooldown_timer > 0:
            blaster_icon._surf.set_alpha(100)  # Lower opacity if on cooldown
        else:
            blaster_icon._surf.set_alpha(255)
        blaster_icon.draw()

        # Draw cooldown timer if on cooldown
        if blaster_cooldown_timer > 0:
            timer_text = f"{blaster_cooldown_timer:.1f}s"
            screen.draw.text(
                timer_text,
                center=(indicator_x + box_w // 2, indicator_y + box_h - 12),
                color="white",
                fontsize=24,
                owidth=2, ocolor="black"
            )

        # Play ingame music ONLY if NOT in boss room (my_map5)
        if current_map != maps.index(my_map5) + 1:
            if not ingame_bsound_playing:
                sounds.menu.stop()
                menu_playing = False
                sounds.ingame_bsound.set_volume(0.3)
                sounds.ingame_bsound.play(-1)
                ingame_bsound_playing = True
        else:
            # If in boss room, stop ingame music
            if ingame_bsound_playing:
                sounds.ingame_bsound.stop()
                ingame_bsound_playing = False

    elif mode == "end":
        screen.fill("#000000")
        global win_sound_played, lose_sound_played
        if win == 1:
            win_screen.center = (WIDTH // 2, HEIGHT // 2 + 50)
            win_screen.draw()
            win_text.center = (WIDTH // 2, end_text_anim_y)
            win_text.draw()
            if not win_sound_played:
                sounds.win.set_volume(0.5)
                sounds.win.play(-1)  # <-- Loop win music
                win_sound_played = True
        else:
            lose_screen.center = (WIDTH // 2, HEIGHT // 2 + 50)
            lose_screen.draw()
            lose_text.center = (WIDTH // 2, end_text_anim_y)
            lose_text.draw()
            if not lose_sound_played:
                sounds.lose.set_volume(0.5)
                sounds.lose.play(-1)  # <-- Loop lose music
                lose_sound_played = True

        # Draw buttons
        menu_button.center = (WIDTH // 2 - 100, HEIGHT // 2 + 120)
        menu_button.draw()
        play_again_button.center = (WIDTH // 2 + 100, HEIGHT // 2 + 120)
        play_again_button.draw()

        # Stop ingame music if playing
        if ingame_bsound_playing:
            sounds.ingame_bsound.stop()
            ingame_bsound_playing = False

    else:
        if menu_playing:
            sounds.menu.stop()
            menu_playing = False
        return
    
def victory():
    global mode, win, boss_music_playing
    # Only check for player death here!
    if char1.health <= 0:
        mode = "end"
        win = -1
    # Always stop boss music
    if boss_music_playing:
        sounds.boss_fight_music.stop()
        boss_music_playing = False

def on_mouse_down(pos):
    global mode, menu_playing, skins_bgm_playing, last_difficulty_mode
    if mode == "menu":
        if play_button.collidepoint(pos):
            sounds.select.play()
            mode = "difficulty_selection"
            if menu_playing:
                sounds.menu.stop()
                menu_playing = False
        elif skins_button.collidepoint(pos):
            sounds.select.play()
            mode = "skins_selection"
    elif mode == "difficulty_selection":
        if easydiff_button.collidepoint(pos):
            sounds.select_2.play()
            mode = "easy_game_difficulty"
            last_difficulty_mode = mode
            reset_game()
        elif normaldiff_button.collidepoint(pos):
            sounds.select_2.play()
            mode = "normal_game_difficulty"
            last_difficulty_mode = mode
            reset_game()
        elif harddiff_button.collidepoint(pos):
            sounds.select_2.play()
            mode = "hard_game_difficulty"
            last_difficulty_mode = mode
            reset_game()
        elif tutorial_button.collidepoint(pos):
            sounds.select_2.play()
            mode = "tutorial"
            spawn_tutorial_enemies_map1()
            spawn_tutorial_enemies_map2()
        elif back_button.collidepoint(pos) or home_button.collidepoint(pos):
            sounds.select.play()
            mode = "menu"
    elif mode == "skins_selection":
        skin_positions = [
            (WIDTH // 2 - 220, HEIGHT // 2 - 60),
            (WIDTH // 2 - 70, HEIGHT // 2 - 60),
            (WIDTH // 2 + 80, HEIGHT // 2 - 60),
            (WIDTH // 2 + 230, HEIGHT // 2 - 60),
            (WIDTH // 2 - 220, HEIGHT // 2 + 80),
            (WIDTH // 2 - 70, HEIGHT // 2 + 80),
            (WIDTH // 2 + 80, HEIGHT // 2 + 80),
            (WIDTH // 2 + 230, HEIGHT // 2 + 80),
        ]
        for i, skin_pos in enumerate(skin_positions):
            rect = Rect((skin_pos[0] - 40, skin_pos[1] - 40), (80, 80))
            if rect.collidepoint(pos):
                sounds.select_2.play()
                global current_skin
                current_skin = list(char1_skins.keys())[i]
        if back_button.collidepoint(pos):
            sounds.select.play()
            mode = "menu"
            if skins_bgm_playing:
                sounds.skins_bgmusic.stop()
                skins_bgm_playing = False
    elif mode == "end":
        if menu_button.collidepoint(pos):
            sounds.select.play()
            mode = "menu"
            reset_game()
            sounds.lose.stop()
            sounds.win.stop()
            if not menu_playing:
                sounds.menu.set_volume(0.5)
                sounds.menu.play(-1)
                menu_playing = True
        elif play_again_button.collidepoint(pos):
            sounds.select.play()
            mode = last_difficulty_mode
            reset_game()
            sounds.lose.stop()
            sounds.win.stop()
    elif mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
    # ...existing code for other buttons...
        if home_button.collidepoint(pos):
            sounds.select.play()
            mode = "menu"
            reset_game()

def on_key_down(key):
    global mode, menu_playing, current_map, enemies, hearts, swords, char1_direction, current_tutorial_map, current_enemy_list, current_map_data, blaster_cooldown_timer, boss_key_obtained, boss_door_locked
    # --- TUTORIAL MODE ---
    if mode == "tutorial":
        if key == keys.ESCAPE:
            mode = "menu"
            return
        # Gaster Blaster Logic in tutorial
        if key == keys.G:
            if blaster_cooldown_timer > 0:
                return
            mx, my = mouse_pos
            x, y = char1.x, char1.y
            angle = math.atan2(my - y, mx - x)
            blaster = {
                "x": x,
                "y": y,
                "angle": angle,
                "state": "summon",
                "timer": 0,
                "alpha": 0,
                "actor": Actor("gblaster_idle", (x, y))
            }
            blaster["actor"].angle = -math.degrees(angle) + 90
            blasters.append(blaster)
            sounds.gaster_blaster_sound.play()
            blaster_cooldown_timer = BLASTER_COOLDOWN
            return
        tutorial_door_logic(key)
        tutorial_attack_logic(key)
        return

    if mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
        old_x = char1.x
        old_y = char1.y

        my_map = maps[current_map - 1]
        grid_x, grid_y = get_player_grid()
        current_map_data = maps[current_map - 1]
        # Only use enemies if in dungeon map
        current_enemy_list = enemies if is_dungeon_map() else []

        # --- MOVEMENT LOGIC ---
        #move_sans_tile(direction)

        # Gaster dialog interaction
    
    if current_map == 1 and gaster.visible:
        grid_x, grid_y = get_player_grid()
        gaster_grid_x = int((gaster.x - bg.width // 2) // bg.width)
        gaster_grid_y = int((gaster.y - bg.height // 2) // bg.height)
        adjacent = (
            abs(grid_x - gaster_grid_x) + abs(grid_y - gaster_grid_y) == 1
        )
        if adjacent and key == keys.R:
            global gaster_dialog_index, gaster_fading
            if gaster_dialog_index < len(gaster_dialogs) - 1:
                sounds.gaster_sound.play()
                gaster_dialog_index += 1
            elif not gaster_fading:
                sounds.gaster_vanish.play()
                gaster_fading = True

    #Gaster Blaster Logic|------------- 
    if key == keys.G:
        if blaster_cooldown_timer > 0:
            return  # Still on cooldown, do nothing
        mx, my = mouse_pos
        x, y = char1.x, char1.y
        angle = math.atan2(my - y, mx - x)
        blaster = {
            "x": x,
            "y": y,
            "angle": angle,
            "state": "summon",
            "timer": 0,
            "alpha": 0,
            "actor": Actor("gblaster_idle", (x, y))
        }
        blaster["actor"].angle = -math.degrees(angle) + 90
        blasters.append(blaster)
        sounds.gaster_blaster_sound.play()
        blaster_cooldown_timer = BLASTER_COOLDOWN
        return

    # --- ATTACK LOGIC ---
    if key == keys.F:
        grid_x, grid_y = get_player_grid()
        if char1_direction == "right":
            atk_x, atk_y = grid_x + 1, grid_y
        elif char1_direction == "left":
            atk_x, atk_y = grid_x - 1, grid_y
        elif char1_direction == "up":
            atk_x, atk_y = grid_x, grid_y - 1
        elif char1_direction == "down":
            atk_x, atk_y = grid_x, grid_y + 1
        else:
            atk_x, atk_y = grid_x, grid_y

        # --- Boss attack ---
        if current_map == maps.index(my_map5) + 1 and boss.visible and boss.hp > 0:
            boss_grid_x = int((boss.x - bg.width // 2) // bg.width)
            boss_grid_y = int((boss.y - bg.height // 2) // bg.height)
            if atk_x == boss_grid_x and atk_y == boss_grid_y:
                sounds.slash.play()
                boss.hp -= char1.attack
                char1.health -= 10  # Boss counterattacks

        # --- Enemy attack (always runs, even in boss room) ---
        if mode == "tutorial":
            current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2
        elif is_dungeon_map():
            current_enemy_list = enemies
        else:
            current_enemy_list = []

        for idx, enemy in enumerate(current_enemy_list):
            enemy_grid_x = int((enemy.x - bg.width // 2) // bg.width)
            enemy_grid_y = int((enemy.y - bg.height // 2) // bg.height)
            if enemy_grid_x == atk_x and enemy_grid_y == atk_y:
                sounds.slash.play()
                enemy.health -= char1.attack
                char1.health -= enemy.attack
                if enemy.health <= 0:
                    if mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
                        drop_enemy_bonus(enemy)
                    current_enemy_list.pop(idx)
                break  # Only attack one enemy per press

    # --- CHEST OPEN LOGIC ---
    if key == keys.E and current_map > 3 and current_map != maps.index(my_map5) + 1:
        grid_x, grid_y = get_player_grid()
        chest = chests[current_map - 4]
        chest_grid_pos = chest_positions[current_map - 4]
        # Check if facing the chest
        if char1_direction == "right":
            check_x, check_y = grid_x + 1, grid_y
        elif char1_direction == "left":
            check_x, check_y = grid_x - 1, grid_y
        elif char1_direction == "up":
            check_x, check_y = grid_x, grid_y - 1
        elif char1_direction == "down":
            check_x, check_y = grid_x, grid_y + 1
        else:
            check_x, check_y = grid_x, grid_y

        if (check_x, check_y) == chest_grid_pos and chest.image == "chest_closed":
            chest.image = "chest_opened"
            # Drop a heart and a sword at the chest's position
            heart = Actor("heart")
            heart.x = chest.x
            heart.y = chest.y
            heart.big = True
            hearts_maps[current_map - 1].append(heart)
            sword = Actor("knive")
            sword.x = chest.x
            sword.y = chest.y
            swords_maps[current_map - 1].append(sword)
            # Check if this chest has the key
            if (current_map - 4) == boss_key_chest_index and not boss_key_obtained:
                boss_key_obtained = True
                boss_door_locked = False


    # --- DOOR TELEPORT LOGIC ---
    if key == keys.SPACE:
        my_map = maps[current_map - 1]
        grid_x, grid_y = get_player_grid()
        tile = my_map[grid_y][grid_x]
        # Only teleport if standing on a DOOR tile (not chest)
        if tile in [3, 4, 5, 6, 15]:
            # Boss door lock check
            if current_map == maps.index(my_map4) + 1 and tile == 6 and boss_door_locked:
                global show_find_key_text, find_key_text_timer
                show_find_key_text = True
                find_key_text_timer = 2.0  # Show for 2 seconds
                return
            # Special case: door 15 in forest_map3 goes to my_map1
            if tile == 15 and current_map == 3:
                target_map_index = 3  # my_map1 is the 4th map in the list (index 3)
                for y in range(len(maps[target_map_index])):
                    for x in range(len(maps[target_map_index][0])):
                        if maps[target_map_index][y][x] == 15:
                            current_map = target_map_index + 1
                            hearts = hearts_maps[current_map - 1]
                            swords = swords_maps[current_map - 1]
                            enemies = enemies_maps[current_map - 1]
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            blasters.clear()
                            beams.clear()
                            return
                        if current_map == maps.index(my_map5) + 1:
                            enemies.clear()
                            boss.x = bg.width * (len(my_map5[0]) // 2 + 0.5)
                            boss.y = bg.height * (len(my_map5) // 2 + 0.5)
                            boss.hp = 1000
                            boss.visible = False
                            boss_appearing = False
                            boss_appeared = False
                            boss_timer = 0
                            boss_attack_timer = 0
                            boss_attack_phase = "wait"
            else:
                for i, m in enumerate(maps):
                    if i != (current_map - 1):  # Only check other maps
                        for y in range(len(m)):
                            for x in range(len(m[0])):
                                if m[y][x] == tile:
                                    # Only teleport if not already at this position
                                    current_map = i + 1
                                    hearts = hearts_maps[current_map - 1]
                                    swords = swords_maps[current_map - 1]
                                    enemies = enemies_maps[current_map - 1]
                                    char1.x = bg.width * (x + 0.5)
                                    char1.y = bg.height * (y + 0.5)
                                    blasters.clear()
                                    beams.clear()
                                    return
                    
    if is_dungeon_map():
        enemy_index = char1.collidelist(enemies)
        if enemy_index != -1:
            sounds.slash.play()
            char1.x = old_x
            char1.y = old_y
            enemy = enemies[enemy_index]
            enemy.health -= char1.attack
            char1.health -= enemy.attack
            if enemy.health <= 0:
                drop_enemy_bonus(enemy)
                enemies.pop(enemy_index)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def update(dt):
    global title_anim_dir, title_anim_base_y, end_text_anim_y, end_text_anim_dir, end_text_anim_base_y
    global select_difficulty_text_anim_y, select_difficulty_text_anim_dir, select_difficulty_text_anim_base_y
    global skins_selection_text_anim_y, skins_selection_text_anim_dir, skins_selection_text_anim_base_y
    global hearts, swords, enemies, move_hold_dir, move_hold_timer, char1_direction, beam_lifetime
    global blaster_cooldown_timer
    global boss_attack_phase, boss_timer, boss_appearing, boss_appeared, boss_attack_timer, boss_attack_mode
    global boss_attack_phase_timer, boss_attack_in_progress, spin_index, spin_positions, spin_initialized
    global boss_blaster_count, boss_line_shots, spin_shots, boss_line_phase_done, boss_attack_next_delay, boss_attack_choice, boss_random_blaster_timer, boss_line_blaster_timer, boss_circle_blaster_timer, boss_ground_bone_timer, boss_ground_bone_count
    global heart_spawn_timer, moved, gaster_alpha, gaster_fading
    global show_find_key_text, find_key_text_timer
    global boss_intro_dialog_active, boss_intro_dialog_index, boss_intro_dialog_timer
    global boss_outro_dialog_active, boss_outro_dialog_index, boss_outro_dialog_timer, boss_outro_fade_started, ingame_bsound_playing, mode, boss_music_playing, win

    if show_find_key_text:
        find_key_text_timer -= dt
        if find_key_text_timer <= 0:
            show_find_key_text = False

    # Gaster fade out logic
    if gaster_fading and gaster.visible:
        gaster_alpha -= 300 * dt  # Fade speed (adjust as needed)
        if gaster_alpha <= 0:
            gaster.visible = False
            gaster_alpha = 0

    # --- Random heart spawn every 5 seconds (only in boss room during fight) ---
    if current_map == maps.index(my_map5) + 1 and boss_attack_phase == "fight":
        heart_spawn_timer += dt
        if heart_spawn_timer >= 5.0:
            heart_spawn_timer = 0
            # Pick a random walkable tile in the boss room
            my_map = my_map5
            walkable = []
            for ty in range(len(my_map)):
                for tx in range(len(my_map[0])):
                    tile = my_map[ty][tx]
                    if tile in [1, 2]:  # Add more walkable tile numbers if needed
                        walkable.append((tx, ty))
            if walkable:
                tx, ty = random.choice(walkable)
                heart = Actor("heart")
                heart.x = tx * TILE_SIZE + TILE_SIZE // 2
                heart.y = ty * TILE_SIZE + TILE_SIZE // 2
                heart.heal = 20  # Custom attribute for 20 HP heal
                hearts_maps[current_map - 1].append(heart)
    else:
        heart_spawn_timer = 0  # Reset timer if not in boss fight

    if current_map == maps.index(my_map5) + 1:
        enemies_map5.clear()
        enemies.clear()
    # --- Fade out boss and door bone when boss HP is 0 and enemies remain ---
    if current_map == maps.index(my_map5) + 1 and boss.visible and boss.hp <= 0:
        all_enemies_dead = all(len(e) == 0 for e in enemies_maps_dungeon)
        if not all_enemies_dead:
            # Start fading boss and door bone
            boss_fade["active"] = True
            boss_fade["fade_timer"] += dt
            fade_speed = 200  # alpha per second
            boss_fade["alpha"] = max(0, boss_fade["alpha"] - fade_speed * dt)
            boss_door_bone["fading"] = True
            boss_door_bone["fade_timer"] += dt
            boss_door_bone["alpha"] = max(0, boss_door_bone["alpha"] - fade_speed * dt)
            boss.visible = boss_fade["alpha"] > 0
            # Set boss alpha (if your Actor supports it)
            if hasattr(boss, "_surf"):
                boss._surf.set_alpha(int(boss_fade["alpha"]))
            if boss_fade["alpha"] <= 0 and boss_door_bone["alpha"] <= 0:
                boss.visible = False
                boss_door_bone["pos"] = None
                boss_fade["active"] = False
                boss_attack_phase = "dead"  # Stop boss attacks

    if blaster_cooldown_timer > 0:
        blaster_cooldown_timer -= dt
        if blaster_cooldown_timer < 0:
            blaster_cooldown_timer = 0
    if not is_dungeon_map():
        enemies = []
        for e in enemies_maps_forest:
            e.clear()
    # --- Gaster Blaster state machine ---
    for blaster in blasters[:]:
        if blaster["state"] == "summon":
            blaster["timer"] += dt
            blaster["alpha"] = min(255, int(255 * (blaster["timer"] / SUMMON_DURATION)))
            if blaster["timer"] >= SUMMON_DURATION:
                blaster["state"] = "fire"
                blaster["timer"] = 0
                blaster["alpha"] = 255
                if blaster["actor"].image.startswith("virus_gblaster_idle"):
                    blaster["actor"].image = "virus_gblaster_shoot"
                else:
                    blaster["actor"].image = "gblaster_shoot"
                beams.append({
                    "x": blaster["x"],
                    "y": blaster["y"],
                    "angle": blaster["angle"],
                    "timer": FIRE_DURATION + FADEOUT_DURATION
                })
        elif blaster["state"] == "fire":
            blaster["timer"] += dt
            blaster["alpha"] = 255
            if blaster["timer"] >= FIRE_DURATION:
                blaster["state"] = "fadeout"
                blaster["timer"] = 0
        elif blaster["state"] == "fadeout":
            blaster["timer"] += dt
            blaster["alpha"] = max(0, int(255 * (1 - blaster["timer"] / FADEOUT_DURATION)))
            if blaster["timer"] >= FADEOUT_DURATION:
                blasters.remove(blaster)

    for blaster in blasters:
        if blaster["state"] == "fire":
            # Only boss blasters damage the player
            if blaster["actor"].image.startswith("virus_gblaster_shoot"):
                if math.hypot(char1.x - blaster["x"], char1.y - blaster["y"]) < 48:
                    if not hasattr(blaster, "player_tick") or blaster["timer"] - getattr(blaster, "player_tick", 0) >= 0.2:
                        char1.health -= 2
                        blaster["player_tick"] = blaster["timer"]
    # Update all beams and remove expired ones
    for b in beams:
        b["timer"] -= dt
    beams[:] = [b for b in beams if b["timer"] > 0]

    # --- Boss beam damage to player ---
    if is_dungeon_map() and current_map == maps.index(my_map5) + 1:
        if not hasattr(char1, "next_beam_tick"):
            char1.next_beam_tick = 0
        for beam in beams:
            # Only damage if beam is from a boss blaster (virus_gblaster)
            # Find the blaster that fired this beam
            for blaster in blasters:
                if (abs(blaster["x"] - beam["x"]) < 1 and abs(blaster["y"] - beam["y"]) < 1
                    and blaster["actor"].image.startswith("virus_gblaster_shoot")):
                    beam_lifetime = FIRE_DURATION
                    beam_time = beam["timer"]
                    if beam_time > FADEOUT_DURATION:
                        # Calculate closest point on beam to player
                        px, py = char1.x, char1.y
                        bx, by = beam["x"], beam["y"]
                        angle = beam["angle"]
                        dx = math.cos(angle)
                        dy = math.sin(angle)
                        t = ((px - bx) * dx + (py - by) * dy)
                        t = max(0, min(t, 1000))  # Clamp to beam length
                        closest_x = bx + dx * t
                        closest_y = by + dy * t
                        # Animate thickness same as in draw()
                        t_beam = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
                        max_thickness = 32
                        min_thickness = 8
                        amp = 0.3
                        osc_speed = 6
                        if t_beam < 0.2:
                            thickness = min_thickness + (max_thickness - min_thickness) * (t_beam / 0.2)
                        elif t_beam > 0.85:
                            thickness = max_thickness * (1 - (t_beam - 0.85) / 0.15)
                            thickness = max(thickness, 1)
                        else:
                            base = max_thickness * (1 - amp)
                            osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t_beam - 0.2))) / 2
                            thickness = base + osc
                        thickness = int(thickness)
                        # Check collision (distance to beam centerline)
                        dist = math.hypot(px - closest_x, py - closest_y)
                        extra_hitbox = 24
                        if dist <= (thickness // 2) + extra_hitbox:
                            # Damage tick every 0.2s
                            if char1.next_beam_tick <= 0:
                                settings = get_boss_settings()
                                char1.health -= settings["beam_damage"]
                                char1.next_beam_tick = settings["beam_tick"]
        if char1.next_beam_tick > 0:
            char1.next_beam_tick -= dt

    # --- Blaster beam damage to enemies ---
    if is_dungeon_map():
        for enemy in enemies:
            if not hasattr(enemy, "next_blaster_tick"):
                enemy.next_blaster_tick = 0
            for beam in beams:
                # Only damage if beam is in "fire" state (not fading in/out)
                beam_lifetime = FIRE_DURATION
                beam_time = beam["timer"]
                if beam_time > FADEOUT_DURATION:
                    # Calculate closest point on beam to enemy
                    ex, ey = enemy.x, enemy.y
                    bx, by = beam["x"], beam["y"]
                    angle = beam["angle"]
                    # Project enemy position onto beam line
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                    t = ((ex - bx) * dx + (ey - by) * dy)
                    t = max(0, min(t, 1000))  # Clamp to beam length
                    closest_x = bx + dx * t
                    closest_y = by + dy * t
                    # Animate thickness same as in draw()
                    t_beam = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
                    max_thickness = 32
                    min_thickness = 8
                    amp = 0.3
                    osc_speed = 6
                    if t_beam < 0.2:
                        thickness = min_thickness + (max_thickness - min_thickness) * (t_beam / 0.2)
                    elif t_beam > 0.85:
                        thickness = max_thickness * (1 - (t_beam - 0.85) / 0.15)
                        thickness = max(thickness, 1)
                    else:
                        base = max_thickness * (1 - amp)
                        osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t_beam - 0.2))) / 2
                        thickness = base + osc
                    thickness = int(thickness)
                    # Check collision (distance to beam centerline)
                    dist = math.hypot(ex - closest_x, ey - closest_y)
                    extra_hitbox = 24  # You can tweak this value (16, 24, 32, etc)
                    if dist <= (thickness // 2) + extra_hitbox:
                        # Damage tick every 0.2s
                        if enemy.next_blaster_tick <= 0:
                            enemy.health -= 2
                            enemy.next_blaster_tick = 0.2
                            # Optional: play a sound or effect here
                    # Tick down timer
            if enemy.next_blaster_tick > 0:
                enemy.next_blaster_tick -= dt

        # Remove dead enemies AFTER the loop and drop their bonus
        dead_enemies = [e for e in enemies if e.health <= 0]
        for e in dead_enemies:
            drop_enemy_bonus(e)
        enemies[:] = [e for e in enemies if e.health > 0] 

    # --- Blaster beam damage to boss ---
    if current_map == maps.index(my_map5) + 1 and boss.visible and boss.hp > 0:
        if not hasattr(boss, "next_blaster_tick"):
            boss.next_blaster_tick = 0
        for beam in beams:
            beam_time = beam["timer"]
            if beam_time > FADEOUT_DURATION:
                bx, by = beam["x"], beam["y"]
                angle = beam["angle"]
                boss_x, boss_y = boss.x, boss.y
                dx = math.cos(angle)
                dy = math.sin(angle)
                t = ((boss_x - bx) * dx + (boss_y - by) * dy)
                t = max(0, min(t, 1000))
                closest_x = bx + dx * t
                closest_y = by + dy * t
                t_beam = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
                max_thickness = 32
                min_thickness = 8
                amp = 0.3
                osc_speed = 6
                if t_beam < 0.2:
                    thickness = min_thickness + (max_thickness - min_thickness) * (t_beam / 0.2)
                elif t_beam > 0.85:
                    thickness = max_thickness * (1 - (t_beam - 0.85) / 0.15)
                    thickness = max(thickness, 1)
                else:
                    base = max_thickness * (1 - amp)
                    osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t_beam - 0.2))) / 2
                    thickness = base + osc
                thickness = int(thickness)
                dist = math.hypot(boss_x - closest_x, boss_y - closest_y)
                extra_hitbox = 24
                # IMMUNITY: Only allow player blaster beams to damage boss
                # Find the blaster that fired this beam
                for blaster in blasters:
                    if (abs(blaster["x"] - beam["x"]) < 1 and abs(blaster["y"] - beam["y"]) < 1):
                        # If it's a virus_gblaster, skip (boss's own)
                        if blaster["actor"].image.startswith("virus_gblaster"):
                            break  # Boss is immune to its own blasters
                        # Otherwise, it's player's blaster
                        if dist <= (thickness // 2) + extra_hitbox:
                            if boss.next_blaster_tick <= 0:
                                boss.hp -= 2
                                boss.next_blaster_tick = 0.2
                # End for blaster
        if boss.next_blaster_tick > 0:
            boss.next_blaster_tick -= dt

    elif mode == "tutorial":
        # Damage tutorial enemies with beams
        current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2
        for enemy in current_enemy_list:
            if not hasattr(enemy, "next_blaster_tick"):
                enemy.next_blaster_tick = 0
            for beam in beams:
                beam_time = beam["timer"]
                if beam_time > FADEOUT_DURATION:
                    ex, ey = enemy.x, enemy.y
                    bx, by = beam["x"], beam["y"]
                    angle = beam["angle"]
                    dx = math.cos(angle)
                    dy = math.sin(angle)
                    t = ((ex - bx) * dx + (ey - by) * dy)
                    t = max(0, min(t, 1000))
                    closest_x = bx + dx * t
                    closest_y = by + dy * t
                    t_beam = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
                    max_thickness = 32
                    min_thickness = 8
                    amp = 0.3
                    osc_speed = 6
                    if t_beam < 0.2:
                        thickness = min_thickness + (max_thickness - min_thickness) * (t_beam / 0.2)
                    elif t_beam > 0.85:
                        thickness = max_thickness * (1 - (t_beam - 0.85) / 0.15)
                        thickness = max(thickness, 1)
                    else:
                        base = max_thickness * (1 - amp)
                        osc = max_thickness * amp * (1 + math.sin(2 * math.pi * osc_speed * (t_beam - 0.2))) / 2
                        thickness = base + osc
                    thickness = int(thickness)
                    dist = math.hypot(ex - closest_x, ey - closest_y)
                    extra_hitbox = 24
                    if dist <= (thickness // 2) + extra_hitbox:
                        if enemy.next_blaster_tick <= 0:
                            enemy.health -= 2
                            enemy.next_blaster_tick = 0.2
            if enemy.next_blaster_tick > 0:
                enemy.next_blaster_tick -= dt
        # Remove dead tutorial enemies
        current_enemy_list[:] = [e for e in current_enemy_list if e.health > 0]

    # --- Tile-based movement with hold-to-repeat ---
    direction = None
    if keyboard.right or keyboard.d:
        direction = "right"
    elif keyboard.left or keyboard.a:
        direction = "left"
    elif keyboard.up or keyboard.w:
        direction = "up"
    elif keyboard.down or keyboard.s:
        direction = "down"

    if direction:
        if move_hold_dir != direction:
            move_hold_dir = direction
            move_hold_timer = MOVE_HOLD_DELAY
            if mode == "tutorial":
                tutorial_movement_logic(None)
            else:
                move_sans_tile(direction)
        else:
            move_hold_timer -= dt
            if move_hold_timer <= 0:
                if mode == "tutorial":
                    tutorial_movement_logic(None)
                else:
                    move_sans_tile(direction)
                move_hold_timer = MOVE_HOLD_DELAY
    else:
        move_hold_dir = None
        move_hold_timer = 0

    if current_map == maps.index(my_map5) + 1:
        enemies_map5.clear()
        enemies.clear()

        if boss_attack_phase == "wait":
            boss_timer += dt
            if boss_timer >= 3.0:
                boss_attack_phase = "appear"
                boss_timer = 0
                boss.visible = True
                boss_appearing = True

        # --- Boss Intro Dialog Logic ---
        if boss_attack_phase == "appear":
            if not boss_intro_dialog_active:
                boss_intro_dialog_active = True
                boss_intro_dialog_index = 0
                boss_intro_dialog_timer = 0
                boss.visible = True
                boss_appearing = True
            else:
                boss_intro_dialog_timer += dt
                if boss_intro_dialog_timer >= 3.0:
                    boss_intro_dialog_timer = 0
                    boss_intro_dialog_index += 1
                    if boss_intro_dialog_index < len(boss_intro_dialogs):
                        sounds.deep_sans_sound.play()
                    if boss_intro_dialog_index >= len(boss_intro_dialogs):
                        boss_intro_dialog_active = False
                        boss_attack_phase = "fight"
                        boss_appearing = False
                        boss_appeared = True
                        boss_timer = 0
                        boss_attack_mode = "random"
                        boss_blaster_count = 0
                        boss_line_shots = 0
                        spin_shots = 0
                        spin_index = 0
                        spin_positions = []
                        spin_initialized = False
                        boss_attack_phase_timer = 0
                        boss_attack_in_progress = False
                        boss_attack_next_delay = 0
                        # Play boss fight music
                        if ingame_bsound_playing:
                            sounds.ingame_bsound.stop()
                            ingame_bsound_playing = False
                        sounds.boss_fight_music.set_volume(0.5)
                        sounds.boss_fight_music.play(-1)
        # --- Boss Outro Dialog Logic ---
        elif boss_attack_phase == "fight" and boss.visible and boss.hp <= 0:
            all_enemies_dead = all(len(e) == 0 for e in enemies_maps_dungeon)
            if not all_enemies_dead:
                # Fade logic as before
                pass
            else:
                if not boss_outro_dialog_active and not boss_outro_fade_started:
                    boss_outro_dialog_active = True
                    boss_outro_dialog_index = 0
                    boss_outro_dialog_timer = 0
                    if boss_music_playing:
                        sounds.boss_fight_music.stop()
                        boss_music_playing = False
                    sounds.deep_sans_sound.play()
                elif boss_outro_dialog_active:
                    boss_outro_dialog_timer += dt
                    if boss_outro_dialog_timer >= 3.0:
                        boss_outro_dialog_timer = 0
                        boss_outro_dialog_index += 1
                        if boss_outro_dialog_index < len(boss_outro_dialogs):
                            sounds.deep_sans_sound.play()
                        if boss_outro_dialog_index >= len(boss_outro_dialogs):
                            boss_outro_dialog_active = False
                            boss_outro_fade_started = True
                elif boss_outro_fade_started:
                    # Start fading boss and door bone
                    boss_fade["active"] = True
                    boss_fade["fade_timer"] += dt
                    fade_speed = 200  # alpha per second
                    boss_fade["alpha"] = max(0, boss_fade["alpha"] - fade_speed * dt)
                    boss_door_bone["fading"] = True
                    boss_door_bone["fade_timer"] += dt
                    boss_door_bone["alpha"] = max(0, boss_door_bone["alpha"] - fade_speed * dt)
                    boss.visible = boss_fade["alpha"] > 0
                    if hasattr(boss, "_surf"):
                        boss._surf.set_alpha(int(boss_fade["alpha"]))
                    if boss_fade["alpha"] <= 0 and boss_door_bone["alpha"] <= 0:
                        boss.visible = False
                        boss_door_bone["pos"] = None
                        boss_fade["active"] = False
                        boss_attack_phase = "dead"
                        mode = "end"
                        win = 1
                        victory()
        elif boss_attack_phase == "fight" and boss.visible and boss.hp > 0:
            boss_attack_phase_timer += dt
            # Play boss music if not already playing
            if not boss_music_playing:
                if ingame_bsound_playing:
                    sounds.ingame_bsound.stop()
                    ingame_bsound_playing = False
                sounds.boss_fight_music.set_volume(0.5)
                sounds.boss_fight_music.play(-1)
                boss_music_playing = True
            # Boss random walk logic (normal walking, not teleport)
            if current_map == maps.index(my_map5) + 1 and boss.visible and boss.hp > 0 and boss_attack_phase == "fight":
                if not hasattr(boss, "move_timer"):
                    boss.move_timer = 0
                boss.move_timer += dt
                settings = get_boss_settings()
                if boss.move_timer >= settings["move_interval"]:  # Move every 1 second (adjust as needed)
                    directions = ["up", "down", "left", "right"]
                    random.shuffle(directions)
                    moved = False
                    for direction in directions:
                        steps = 1
                        grid_x = int((boss.x - bg.width // 2) // bg.width)
                        grid_y = int((boss.y - bg.height // 2) // bg.height)
                        nx, ny = grid_x, grid_y
                        if direction == "up":
                            ny -= steps
                            boss.image = "virus_sans_up"
                        elif direction == "down":
                            ny += steps
                            boss.image = "virus_sans_down"
                        elif direction == "left":
                            nx -= steps
                            boss.image = "virus_sans_left"
                        elif direction == "right":
                            nx += steps
                            boss.image = "virus_sans_right"
                        # Stay in bounds and only walk on walkable tiles
                        if 0 <= nx < len(my_map5[0]) and 0 <= ny < len(my_map5):
                            if my_map5[ny][nx] in [1, 2]:  # Walkable tiles
                                boss.x = nx * TILE_SIZE + TILE_SIZE // 2
                                boss.y = ny * TILE_SIZE + TILE_SIZE // 2
                                moved = True
                                break
                    boss.move_timer = 0

            # Start a new attack if not in progress and cooldown is over
            if not boss_attack_in_progress and boss_attack_next_delay <= 0:
                boss_attack_in_progress = True
                boss_blaster_count = 0
                boss_line_shots = 0
                spin_shots = 0
                boss_ground_bone_count = 0
                boss_attack_phase_timer = 0
                boss_attack_choice = boss_choose_attack()  # <-- randomize every time!
                boss_random_blaster_timer = 0
                boss_line_blaster_timer = 0
                boss_circle_blaster_timer = 0
                boss_ground_bone_timer = 0

            # Call the current attack function while in progress
            if boss_attack_in_progress:
                if boss_attack_choice == 1:
                    boss_attack_random_blaster(dt)
                elif boss_attack_choice == 2:
                    boss_attack_line_blaster(dt)
                elif boss_attack_choice == 3:
                    boss_attack_circle_blaster(dt)
                elif boss_attack_choice == 4:
                    boss_attack_ground_bone_phase(dt)

            # If attack just finished, start cooldown before next attack
            if not boss_attack_in_progress and boss_attack_next_delay <= 0:
                boss_attack_next_delay = 1.0  # 1 second delay between attacks

            # Tick down the cooldown
            if boss_attack_next_delay > 0:
                boss_attack_next_delay -= dt
                if boss_attack_next_delay < 0:
                    boss_attack_next_delay = 0

    # Update ground bone attacks
    for attack in ground_bone_attacks[:]:
        attack["timer"] += dt
        if attack["state"] == "warn" and attack["timer"] >= 0.5:
            attack["state"] = "fadein"
            attack["timer"] = 0
        elif attack["state"] == "fadein" and attack["timer"] >= 0.5:
            attack["state"] = "stay"
            attack["timer"] = 0
        elif attack["state"] == "stay" and attack["timer"] >= 2.0:
            attack["state"] = "fadeout"
            attack["timer"] = 0
        elif attack["state"] == "fadeout" and attack["timer"] >= 0.5:
            ground_bone_attacks.remove(attack)
        # Damage player only during "stay"
        elif attack["state"] == "stay":
            for tx, ty in attack["tiles"]:
                bone_x = tx * TILE_SIZE + TILE_SIZE // 2
                bone_y = ty * TILE_SIZE + TILE_SIZE // 2
                if math.hypot(char1.x - bone_x, char1.y - bone_y) < 32:
                    if not hasattr(attack, "player_tick") or attack["timer"] - getattr(attack, "player_tick", 0) >= settings["bone_tick"]:
                        settings = get_boss_settings()
                        char1.health -= settings["bone_damage"]
                        attack["player_tick"] = attack["timer"]

    # Update boss_blasters
    for blaster in boss_blasters[:]:
        blaster["timer"] += dt
        if blaster["timer"] > 1.0:  # Show for 1 second, then remove
            boss_blasters.remove(blaster)
            #REMOVE this block to prevent damage from colliding with the blaster/skull:
            #if math.hypot(char1.x - blaster["x"], char1.y - blaster["y"]) < 48:
            #    if not hasattr(blaster, "player_tick") or blaster["timer"] - getattr(blaster, "player_tick", 0) >= 0.2:
            #        char1.health -= 2
            #        blaster["player_tick"] = blaster["timer"]

    # Update boss_bones
    for bone in boss_bones[:]:
        bone["timer"] += dt
        if bone["timer"] > 1.0:
            boss_bones.remove(bone)
            #REMOVE this block to prevent damage from colliding with the bone:
            #if math.hypot(char1.x - bone["actor"].x, char1.y - bone["actor"].y) < 32:
            #    if not hasattr(bone, "player_tick") or bone["timer"] - getattr(bone, "player_tick", 0) >= 0.2:
            #        char1.health -= 1
            #        bone["player_tick"] = bone["timer"]

    # When updating char1's image:
    char1.image = char1_skins[current_skin][char1_direction]
    hearts = hearts_maps[current_map - 1]
    swords = swords_maps[current_map - 1]
    enemies = enemies_maps[current_map - 1]
    # Animate title only in menu
    if mode == "menu":
        title.y += title_anim_dir * title_anim_speed
        if abs(title.y - title_anim_base_y) > title_anim_range:
            title_anim_dir *= -1

    # Animate end text only in end mode
    if mode == "end":
        end_text_anim_y += end_text_anim_dir * end_text_anim_speed
        if abs(end_text_anim_y - end_text_anim_base_y) > end_text_anim_range:
            end_text_anim_dir *= -1
    
    # Animate select difficulty text in difficulty_selection":
    if mode == "difficulty_selection":
        select_difficulty_text_anim_y += select_difficulty_text_anim_dir * select_difficulty_text_anim_speed
        if abs(select_difficulty_text_anim_y - select_difficulty_text_anim_base_y) > select_difficulty_text_anim_range:
            select_difficulty_text_anim_dir *= -1

    # Animate skins selection title in skins_selection mode
    if mode == "skins_selection":
        skins_selection_text_anim_y += skins_selection_text_anim_dir * skins_selection_text_anim_speed
        if abs(skins_selection_text_anim_y - skins_selection_text_anim_base_y) > skins_selection_text_anim_range:
            skins_selection_text_anim_dir *= -1
    #|----------------------------------------------------

    for i in range(len(hearts)):
        if char1.colliderect(hearts[i]):
            if hasattr(hearts[i], "big") and hearts[i].big:
                char1.health += 50
            elif hasattr(hearts[i], "heal"):
                char1.health += hearts[i].heal
            else:
                char1.health += 20
            hearts.pop(i)
            break
    for i in range(len(swords)):
        if char1.colliderect(swords[i]):
            char1.attack += 5
            swords.pop(i)
            break

    if not is_dungeon_map():
        enemies = []  # Always empty in forest maps


def boss_attack(dt):
    global boss_attack_timer, boss_blasters, boss_bones
    boss_attack_timer += dt
    if boss_attack_timer >= 0.2:
        boss_attack_timer = 0
        # --- Spawn a Gaster Blaster ---
        bx = random.randint(1, len(my_map5[0]) - 2) * bg.width + bg.width // 2
        by = random.randint(1, len(my_map5) - 2) * bg.height + bg.height // 2
        angle = math.atan2(char1.y - by, char1.x - bx)
        blaster = {
            "x": bx,
            "y": by,
            "angle": angle,
            "state": "summon",
            "timer": 0,
            "alpha": 0,
            "actor": Actor("gblaster_idle", (bx, by))
        }
        blaster["actor"].angle = -math.degrees(angle) + 90
        boss_blasters.append(blaster)
        # --- Spawn a Bone ---
        bone_x = random.randint(1, len(my_map5[0]) - 2) * bg.width + bg.width // 2
        bone_y = random.randint(1, len(my_map5) - 2) * bg.height + bg.height // 2
        bone = Actor("bone_sprite", (bone_x, bone_y))
        boss_bones.append({"actor": bone, "timer": 0, "state": "warn"})

def boss_attack_random():
    global boss_blaster_count, boss_attack_mode, boss_line_shots
    margin = 64
    tiles_x = (WIDTH - 2 * margin) // TILE_SIZE
    tiles_y = (HEIGHT - 2 * margin) // TILE_SIZE
    tx = random.randint(0, tiles_x - 1)
    ty = random.randint(0, tiles_y - 1)
    bx = margin + tx * TILE_SIZE + TILE_SIZE // 2
    by = margin + ty * TILE_SIZE + TILE_SIZE // 2
    angle = math.atan2(char1.y - by, char1.x - bx)
    blaster = {
        "x": bx,
        "y": by,
        "angle": angle,
        "state": "summon",
        "timer": 0,
        "alpha": 0,
        "actor": Actor("virus_gblaster_idle", (bx, by))
    }
    blaster["actor"].angle = -math.degrees(angle) + 90
    blasters.append(blaster)
    sounds.gaster_blaster_sound.play()

def boss_attack_line():
    global boss_line_shots
    rows = HEIGHT // TILE_SIZE
    cols = WIDTH // TILE_SIZE
    # Avoid corners: use 1..rows-2 and 1..cols-2
    if boss_line_shots % 2 == 0:
        # Horizontal lines
        chosen_rows = random.sample(range(1, rows-1), 3)
        for row in chosen_rows:
            bx = row * TILE_SIZE + TILE_SIZE // 2
            if row < rows // 2:
                by = TILE_SIZE // 2
                angle = math.pi / 2
            else:
                by = HEIGHT - TILE_SIZE // 2
                angle = -math.pi / 2
            blaster = {
                "x": bx,
                "y": by,
                "angle": angle,
                "state": "summon",
                "timer": 0,
                "alpha": 0,
                "actor": Actor("virus_gblaster_idle", (bx, by))
            }
            blaster["actor"].angle = -math.degrees(angle) + 90
            blasters.append(blaster)
            sounds.gaster_blaster_sound.play()
    else:
        # Vertical lines
        chosen_cols = random.sample(range(1, cols-1), 3)
        for col in chosen_cols:
            by = col * TILE_SIZE + TILE_SIZE // 2
            if col < cols // 2:
                bx = TILE_SIZE // 2
                angle = 0
            else:
                bx = WIDTH - TILE_SIZE // 2
                angle = math.pi
            blaster = {
                "x": bx,
                "y": by,
                "angle": angle,
                "state": "summon",
                "timer": 0,
                "alpha": 0,
                "actor": Actor("gblaster_idle", (bx, by))
            }
            blaster["actor"].angle = -math.degrees(angle) + 90
            blasters.append(blaster)
            sounds.gaster_blaster_sound.play()
    boss_line_shots += 1

def boss_attack_ground_bone():
    walkable = get_walkable_tiles_for_boss_room()
    settings = get_boss_settings()
    if len(walkable) < settings["ground_bone_count"]:
        bone_tiles = walkable[:]
    else:
        bone_tiles = random.sample(walkable, settings["ground_bone_count"])
    # Actually spawn the attack!
    ground_bone_attacks.append({
        "tiles": bone_tiles,
        "timer": 0,
        "state": "warn"
    })

def boss_attack_spin():
    global spin_positions, spin_shots, spin_index, spin_initialized, boss_attack_mode
    # Only initialize spin_positions ONCE per spin attack
    if not spin_initialized:
        spin_positions = []
        for i in range(WIDTH // TILE_SIZE):
            spin_positions.append((i * TILE_SIZE + TILE_SIZE // 2, TILE_SIZE // 2))  # Top edge
        for j in range(1, HEIGHT // TILE_SIZE):
            spin_positions.append((WIDTH - TILE_SIZE // 2, j * TILE_SIZE + TILE_SIZE // 2))  # Right edge
        for i in range(WIDTH // TILE_SIZE - 2, -1, -1):
            spin_positions.append((i * TILE_SIZE + TILE_SIZE // 2, HEIGHT - TILE_SIZE // 2))  # Bottom edge
        for j in range(HEIGHT // TILE_SIZE - 2, 0, -1):
            spin_positions.append((TILE_SIZE // 2, j * TILE_SIZE + TILE_SIZE // 2))  # Left edge
        spin_index = 0
        spin_shots = 0
        spin_initialized = True

    # Do NOT increment spin_shots here!
    x, y = spin_positions[spin_index]
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    angle = math.atan2(center_y - y, center_x - x)
    blaster = {
        "x": x,
        "y": y,
        "angle": angle,
        "state": "summon",
        "timer": 0,
        "alpha": 0,
        "actor": Actor("virus_gblaster_idle", (x, y))
    }
    blaster["actor"].angle = -math.degrees(angle) + 90
    blasters.append(blaster)
    sounds.gaster_blaster_sound.play()
    spin_index = (spin_index + 1) % len(spin_positions)

def get_walkable_tiles_for_boss_room():
    walkable = []
    my_map = my_map5
    for ty in range(len(my_map)):
        for tx in range(len(my_map[0])):
            tile = my_map[ty][tx]
            # Only allow walkable tiles (not wall/edge)
            if tile in [1, 2]:  # Add other walkable tile numbers if needed
                walkable.append((tx, ty))
    return walkable


def boss_attack_random_blaster(dt):
    global boss_blaster_count, boss_attack_in_progress, boss_random_blaster_timer
    settings = get_boss_settings()
    boss_random_blaster_timer += dt
    if boss_blaster_count < settings["random_blaster_count"]:
        if boss_random_blaster_timer >= settings["random_blaster_spawn_rate"]:
            boss_attack_random()
            boss_blaster_count += 1
            boss_random_blaster_timer = 0
    else:
        boss_attack_in_progress = False
        boss_random_blaster_timer = 0

def boss_attack_line_blaster(dt):
    global boss_line_shots, boss_attack_in_progress, boss_line_blaster_timer
    settings = get_boss_settings()
    boss_line_blaster_timer += dt
    if boss_line_shots < settings["line_shots"]:
        if boss_line_blaster_timer >= settings["line_blaster_spawn_rate"]:
            boss_attack_line()
            boss_line_shots += 1
            boss_line_blaster_timer = 0
    else:
        boss_attack_in_progress = False
        boss_line_blaster_timer = 0

def boss_attack_ground_bone_phase(dt):
    global boss_ground_bone_count, boss_attack_in_progress, boss_ground_bone_timer
    settings = get_boss_settings()
    boss_ground_bone_timer += dt
    if boss_ground_bone_count < settings["ground_bone_count"]:
        if boss_ground_bone_timer >= settings["ground_bone_spawn_rate"]:
            boss_attack_ground_bone()
            boss_ground_bone_count += 1
            boss_ground_bone_timer = 0
    else:
        boss_attack_in_progress = False
        boss_ground_bone_timer = 0
        boss_ground_bone_count = 0

def boss_attack_circle_blaster(dt):
    global spin_shots, boss_attack_in_progress, boss_circle_blaster_timer, spin_initialized
    settings = get_boss_settings()
    boss_circle_blaster_timer += dt
    if spin_shots < settings["spin_shots"]:
        if boss_circle_blaster_timer >= settings["circle_blaster_spawn_rate"]:
            boss_attack_spin()
            spin_shots += 1
            boss_circle_blaster_timer = 0
    else:
        boss_attack_in_progress = False
        boss_circle_blaster_timer = 0
        spin_initialized = False  # Reset for next time!

def boss_choose_attack():
    global last_boss_attack
    choices = [1, 2, 3, 4]
    if last_boss_attack in choices:
        choices.remove(last_boss_attack)
    attack = random.choice(choices)
    last_boss_attack = attack
    return attack

def get_boss_max_hp():
    if mode == "easy_game_difficulty":
        return 1000
    elif mode == "normal_game_difficulty":
        return 1500
    elif mode == "hard_game_difficulty":
        return 2000
    else:
        return 1000



















pgzrun.go()