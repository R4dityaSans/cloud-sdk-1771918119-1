import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import random
import pgzrun
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
skins_bgm_playing = False  # Add this near your other flags
size_w = 10 # Lebar dari bidang dalam sel
size_h = 10 # Tinggi dari bidang dalam sel
WIDTH = bg.width * size_w
HEIGHT = bg.height * size_h
mode = "menu" # Mode permainan
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

    win_sound_played = False
    lose_sound_played = False
    current_map = 1  # Always start on map 1 (forest_map1)
    char1.health = 100
    char1.attack = 5
    char1.x = bg.width * (5 + 0.5)
    char1.y = bg.height * (5 + 0.5)

    used_positions.clear()

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

    for chest in chests:
        chest.image = "chest_closed"

#title/texts
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
    }
}
# Set the current skin
current_skin = "classic_sans"

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

def tutorial_movement_logic(key):
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
            "Tutorial:\n\n- Use WASD or Arrow keys to move\n- Press F to attack in the direction you are facing\n- Collect hearts and knives for bonuses\n- press Spacebar Use doors to move between rooms\n- Press E to open chests\n\nPress ESC to return to menu.",
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
        skin_display_names = ["Classic Sans", "King Sans", "Swap Sans", "Dust Sans"]
        skin_positions = [
            (WIDTH // 2 - 120, HEIGHT // 2 - 60),
            (WIDTH // 2 + 120, HEIGHT // 2 - 60),
            (WIDTH // 2 - 120, HEIGHT // 2 + 80),
            (WIDTH // 2 + 120, HEIGHT // 2 + 80),
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
                fontsize=28,
                owidth=2, ocolor="black"
            )
        back_button.topleft = (10, 10)
        back_button.draw()
        return

    if mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
        map_draw()
        hearts = hearts_maps[current_map - 1]
        swords = swords_maps[current_map - 1]
        enemies = enemies_maps[current_map - 1]
        if is_dungeon_map():
            # Draw chest
            chest = chests[current_map - len(forest_maps) - 1]
            chest.draw()
            # Draw enemies
            for enemy in enemies:
                enemy.draw()
        # Draw player and bonuses always
        char1.draw()
        hp_index = max(0, min(10, char1.health // 10))
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
        for heart in hearts:
            heart.draw()
        for sword in swords:
            sword.draw()
        # Draw home button
        home_button.topleft = (10, 10)
        home_button.draw()

        # Play ingame music
        if not ingame_bsound_playing:
            sounds.menu.stop()
            menu_playing = False
            sounds.ingame_bsound.set_volume(0.3)
            sounds.ingame_bsound.play(-1)
            ingame_bsound_playing = True

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
                sounds.win.play()
                win_sound_played = True
        else:
            lose_screen.center = (WIDTH // 2, HEIGHT // 2 + 50)
            lose_screen.draw()
            lose_text.center = (WIDTH // 2, end_text_anim_y)
            lose_text.draw()
            if not lose_sound_played:
                sounds.lose.set_volume(0.5)
                sounds.lose.play()
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
    global mode, win
    if mode in ["easy_game_difficulty", "normal_game_difficulty", "hard_game_difficulty"]:
        # Win if all enemies from all dungeon maps are dead and player is alive
        if all(len(e) == 0 for e in enemies_maps_dungeon) and char1.health > 0:
            mode = "end"
            win = 1
        elif char1.health <= 0:
            mode = "end"
            win = -1

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
        for i, skin_pos in enumerate([
            (WIDTH // 2 - 120, HEIGHT // 2 - 60),
            (WIDTH // 2 + 120, HEIGHT // 2 - 60),
            (WIDTH // 2 - 120, HEIGHT // 2 + 80),
            (WIDTH // 2 + 120, HEIGHT // 2 + 80),
        ]):   
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
    global mode, menu_playing, current_map, enemies, hearts, swords, char1_direction, current_tutorial_map, current_enemy_list, chest_open
    # --- TUTORIAL MODE ---
    if mode == "tutorial":
        if key == keys.ESCAPE:
            mode = "menu"
            return
        tutorial_door_logic(key)
        tutorial_movement_logic(key)
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

        # Movement logic
        if (keyboard.right or keyboard.d):
            char1_direction = "right"
            nx, ny = grid_x + 1, grid_y
            # Teleport from forest_map1 to forest_map2 if stepping on 13
            if current_map == 1 and nx < len(current_map_data[0]) and current_map_data[ny][nx] == 13:
                for y in range(len(forest_map2)):
                    for x in range(len(forest_map2[0])):
                        if forest_map2[y][x] == 13:
                            current_map = 2
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            # Teleport from forest_map2 to forest_map3 if stepping on 14
            if current_map == 2 and nx < len(current_map_data[0]) and current_map_data[ny][nx] == 14:
                for y in range(len(forest_map3)):
                    for x in range(len(forest_map3[0])):
                        if forest_map3[y][x] == 14:
                            current_map = 3
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            # Block movement if next tile is a closed chest
            blocked_by_chest = False
            if current_map > 3:
                chest = chests[current_map - 4]
                chest_grid_pos = chest_positions[current_map - 4]
                if (nx, ny) == chest_grid_pos and chest.image == "chest_closed":
                    blocked_by_chest = True
            # Normal movement
            if nx < len(current_map_data[0]) and current_map_data[ny][nx] not in [0, 9, 10] and not is_enemy_at(nx, ny, current_enemy_list) and not blocked_by_chest:
                char1.x += bg.width

        elif (keyboard.left or keyboard.a):
            char1_direction = "left"
            nx, ny = grid_x - 1, grid_y
            # Teleport from forest_map2 to forest_map1 if stepping on 13
            if current_map == 2 and nx >= 0 and current_map_data[ny][nx] == 13:
                for y in range(len(forest_map1)):
                    for x in range(len(forest_map1[0])):
                        if forest_map1[y][x] == 13:
                            current_map = 1
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            # Teleport from forest_map3 to forest_map2 if stepping on 14
            if current_map == 3 and nx >= 0 and current_map_data[ny][nx] == 14:
                for y in range(len(forest_map2)):
                    for x in range(len(forest_map2[0])):
                        if forest_map2[y][x] == 14:
                            current_map = 2
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            # Block movement if next tile is a closed chest
            blocked_by_chest = False
            if current_map > 3:
                chest = chests[current_map - 4]
                chest_grid_pos = chest_positions[current_map - 4]
                if (nx, ny) == chest_grid_pos and chest.image == "chest_closed":
                    blocked_by_chest = True
            # Normal movement
            if nx >= 0 and current_map_data[ny][nx] not in [0, 9, 10] and not is_enemy_at(nx, ny, current_enemy_list) and not blocked_by_chest:
                char1.x -= bg.width

        elif (keyboard.down or keyboard.s):
            char1_direction = "down"
            nx, ny = grid_x, grid_y + 1
            # Block movement if next tile is a closed chest
            blocked_by_chest = False
            if current_map > 3:
                chest = chests[current_map - 4]
                chest_grid_pos = chest_positions[current_map - 4]
                if (nx, ny) == chest_grid_pos and chest.image == "chest_closed":
                    blocked_by_chest = True
            if ny < len(current_map_data) and current_map_data[ny][nx] not in [0, 9, 10] and not is_enemy_at(nx, ny, current_enemy_list) and not blocked_by_chest:
                char1.y += bg.height

        elif (keyboard.up or keyboard.w):
            char1_direction = "up"
            nx, ny = grid_x, grid_y - 1
            # Block movement if next tile is a closed chest
            blocked_by_chest = False
            if current_map > 3:
                chest = chests[current_map - 4]
                chest_grid_pos = chest_positions[current_map - 4]
                if (nx, ny) == chest_grid_pos and chest.image == "chest_closed":
                    blocked_by_chest = True
            if ny >= 0 and current_map_data[ny][nx] not in [0, 9, 10] and not is_enemy_at(nx, ny, current_enemy_list) and not blocked_by_chest:
                char1.y -= bg.height
            
    # --- ATTACK LOGIC ---
    if key == keys.F:
        # Get current grid position
        grid_x, grid_y = get_player_grid()
        # Determine attack tile based on direction
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

        # Choose the correct enemy list
        if mode == "tutorial":
            current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2
        elif is_dungeon_map():
            current_enemy_list = enemies
        else:
            current_enemy_list = []

        # Check for enemy in that tile
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
    if key == keys.E and current_map > 3:
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
            hearts_maps[current_map - 1].append(heart)  # <-- append to the correct map list
            sword = Actor("knive")
            sword.x = chest.x
            sword.y = chest.y
            swords_maps[current_map - 1].append(sword)  # <-- append to the correct map list
            # sounds.slash.play()  # Optional: play a sound

    # --- DOOR TELEPORT LOGIC ---
    if key == keys.SPACE:
        my_map = maps[current_map - 1]
        grid_x, grid_y = get_player_grid()
        tile = my_map[grid_y][grid_x]
        # Only teleport if standing on a DOOR tile (not chest)
        if tile in [3, 4, 5, 6, 15]:
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
                            return
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

def update(dt):
    global title_anim_dir, title_anim_base_y, end_text_anim_y, end_text_anim_dir, end_text_anim_base_y, select_difficulty_text_anim_y, select_difficulty_text_anim_dir, select_difficulty_text_anim_base_y, skins_selection_text_anim_y, skins_selection_text_anim_dir, skins_selection_text_anim_base_y, hearts, swords, enemies

    # When updating char1's image:
    char1.image = char1_skins[current_skin][char1_direction]
    victory()
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
            else:
                char1.health += 5
            hearts.pop(i)
            break
    for i in range(len(swords)):
        if char1.colliderect(swords[i]):
            char1.attack += 5
            swords.pop(i)
            break

    if not is_dungeon_map():
        enemies = []  # Always empty in forest maps















pgzrun.go()