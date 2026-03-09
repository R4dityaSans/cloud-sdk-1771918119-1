import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import random
import pgzrun

bg = Actor('bg')
bg1 = Actor("wood_a")
bg2 = Actor("wood_b")
snow = Actor("snow")
door = Actor("door")
menu = Actor("menu")
win_screen = Actor("win_screen")
lose_screen = Actor("lose_screen")
play_button = Actor("play_button")
menu_button = Actor("menu_button")
current_tutorial_map = 1
tutorial_button = Actor("tutorial_button")
play_again_button = Actor("play_again_button")
menu_playing = False
win_sound_played = False
lose_sound_played = False
ingame_bsound_playing = False
showing_tutorial = False
size_w = 10 # Lebar dari bidang dalam sel
size_h = 10 # Tinggi dari bidang dalam sel
WIDTH = bg.width * size_w
HEIGHT = bg.height * size_h
mode = "menu" # Mode permainan
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

my_map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 2, 2, 1, 2, 1, 0], 
          [0, 1, 1, 2, 1, 2, 1, 1, 2, 0], 
          [0, 2, 1, 1, 2, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 1, 1, 2, 1, 1, 0], 
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


def map_draw():
    my_map = maps[current_map - 1]  # Always use the current map
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                bg.left = bg.width * j
                bg.top = bg.height * i
                bg.draw()
            elif my_map[i][j] == 1:
                bg1.left = bg.width * j
                bg1.top = bg.height * i
                bg1.draw()
            elif my_map[i][j] == 2:
                bg2.left = bg.width * j
                bg2.top = bg.height * i
                bg2.draw()
            elif my_map[i][j] in [3, 4, 5, 6, 8]:
                door.left = bg.width * j
                door.top = bg.height * i
                door.draw()
            elif my_map[i][j] == 7:
                snow.left = bg.width * j
                snow.top = bg.height * i
                snow.draw()

def reset_game():
    global enemies, hearts, swords, char1, used_positions
    global enemies_map1, enemies_map2, enemies_map3, enemies_map4, enemies_map5
    global hearts_map1, hearts_map2, hearts_map3, hearts_map4, hearts_map5
    global swords_map1, swords_map2, swords_map3, swords_map4, swords_map5
    global current_map, win_sound_played, lose_sound_played

    win_sound_played = False
    lose_sound_played = False
    current_map = 1  # Always start on map 1

    char1.health = 100
    char1.attack = 5
    char1.x = bg.width * 1.5
    char1.y = bg.height * 1.5

    # Clear all lists instead of reassigning
    hearts_map1.clear()
    hearts_map2.clear()
    hearts_map3.clear()
    hearts_map4.clear()
    hearts_map5.clear()
    swords_map1.clear()
    swords_map2.clear()
    swords_map3.clear()
    swords_map4.clear()
    swords_map5.clear()
    enemies_map1.clear()
    enemies_map2.clear()
    enemies_map3.clear()
    enemies_map4.clear()
    enemies_map5.clear()

    hearts = hearts_map1
    swords = swords_map1
    enemies = enemies_map1

    # Spawn enemies for each map
    spawn_enemies_for_map1()
    spawn_enemies_for_map2()
    spawn_enemies_for_map3()
    spawn_enemies_for_map4()
    spawn_enemies_for_map5()

#title
title = Actor("sa_title")
title.center = (WIDTH // 2, HEIGHT // 2 - 240)
title_anim_dir = 1  # 1 for down, -1 for up
title_anim_speed = 0.3  # Adjust for slower/faster animation
title_anim_range = 10   # How many pixels up and down
title_anim_base_y = title.y
win_text = Actor("win_text")
lose_text = Actor("lose_text")
end_text_anim_y = 80
end_text_anim_dir = 1
end_text_anim_speed = 0.8  # Adjust for faster/slower animation
end_text_anim_range = 20   # How many pixels up and down
end_text_anim_base_y = 80

#Protagonis
char1 = Actor('sans_right')
char1.top = bg.height
char1.left = bg.width
char1.health = 100
char1.attack = 5
char1_direction = "right"  # Possible values: "right", "left", "up", "down"

#chest
chest_closed = Actor("chest_closed")
chest_opened = Actor("chest_opened")

health_bars = [
    "health_bar_0", "health_bar_1", "health_bar_2", "health_bar_3", "health_bar_4", "health_bar_5",
    "health_bar_6", "health_bar_7", "health_bar_8", "health_bar_9", "health_bar_10"
]
#bonus
hearts = []
swords = []

hearts_map1 = []
hearts_map2 = []
hearts_map3 = []
hearts_map4 = []
hearts_map5 = []

swords_map1 = []
swords_map2 = []
swords_map3 = []
swords_map4 = []
swords_map5 = []
hearts = hearts_map1
swords = swords_map1

#membangkitkan musuh
enemies_map1 = []
enemies_map2 = []
enemies_map3 = []
enemies_map4 = []
enemies_map5 = []
tutorial_enemies_map1 = []
tutorial_enemies_map2 = []
enemies = enemies_map1
used_positions = set()

maps = [my_map1, my_map2, my_map3, my_map4, my_map5]
enemies_maps = [enemies_map1, enemies_map2, enemies_map3, enemies_map4, enemies_map5]  # Expand if you add more
hearts_maps = [hearts_map1, hearts_map2, hearts_map3, hearts_map4, hearts_map5,]     # Expand if you add more
swords_maps = [swords_map1, swords_map2, swords_map3, swords_map4, swords_map5,]     # Expand if you add more

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
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        enemy1.health = 10
        enemy1.attack = random.randint(5, 10)
        enemy1.bonus = random.randint(0, 2)
        enemies_map1.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        enemy2.health = 20
        enemy2.attack = random.randint(5, 10)
        enemy2.bonus = random.randint(0, 2)
        enemies_map1.append(enemy2)

def spawn_enemies_for_map2():
    global enemies_map3
    enemies_map3.clear()
    used_positions = set()
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        enemy1.health = 10
        enemy1.attack = random.randint(5, 10)
        enemy1.bonus = random.randint(0, 2)
        enemies_map2.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        enemy2.health = 20
        enemy2.attack = random.randint(5, 10)
        enemy2.bonus = random.randint(0, 2)
        enemies_map2.append(enemy2)

def spawn_enemies_for_map3():
    global enemies_map3
    enemies_map3.clear()
    used_positions = set()
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        enemy1.health = 10
        enemy1.attack = random.randint(5, 10)
        enemy1.bonus = random.randint(0, 2)
        enemies_map3.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        enemy2.health = 20
        enemy2.attack = random.randint(5, 10)
        enemy2.bonus = random.randint(0, 2)
        enemies_map3.append(enemy2)

def spawn_enemies_for_map4():
    global enemies_map4
    enemies_map4.clear()
    used_positions = set()
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        enemy1.health = 10
        enemy1.attack = random.randint(5, 10)
        enemy1.bonus = random.randint(0, 2)
        enemies_map4.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        enemy2.health = 20
        enemy2.attack = random.randint(5, 10)
        enemy2.bonus = random.randint(0, 2)
        enemies_map4.append(enemy2)

def spawn_enemies_for_map5():
    global enemies_map5
    enemies_map5.clear()
    used_positions = set()
    for dx in range(2):
        for dy in range(2):
            used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))
    for i in range(3):
        # Spawn knight
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy1 = Actor("knight", topleft = (x, y))
        enemy1.health = 10
        enemy1.attack = random.randint(5, 10)
        enemy1.bonus = random.randint(0, 2)
        enemies_map5.append(enemy1)
        # Spawn juggernaut
        while True:
            x = random.randint(1, 8) * bg.width
            y = random.randint(1, 8) * bg.height
            pos = (x, y)
            if pos not in used_positions:
                used_positions.add(pos)
                break
        enemy2 = Actor("juggernaut", topleft = (x, y))
        enemy2.health = 20
        enemy2.attack = random.randint(5, 10)
        enemy2.bonus = random.randint(0, 2)
        enemies_map5.append(enemy2)

def draw():
    global menu_playing, ingame_bsound_playing
    if mode == "menu":
        screen.fill("#000000")
        menu.center = (WIDTH // 2, HEIGHT // 2)
        menu.draw()
        title.draw()
        play_button.center = (WIDTH // 2, HEIGHT // 2 + 120)
        play_button.draw()
        tutorial_button.center = (WIDTH // 2, HEIGHT // 2 + 200)
        tutorial_button.draw()
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
            "Tutorial:\n\n- Use WASD or Arrow keys to move\n- Press F to attack in the direction you are facing\n- Collect hearts and knives for bonuses\n- press Spacebar Use doors to move between rooms\n\nPress ESC to return to menu.",
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

    if mode == "game":
        map_draw()
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
        for i in range(len(enemies)):
            enemies[i].draw()
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        
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
    global mode, win, enemies_map1, enemies_map2
    if mode == "game":
        # Win if all enemies from both maps are dead and player is alive
        if not enemies_map1 and not enemies_map2 and char1.health > 0:
            mode = "end"
            win = 1
        elif char1.health <= 0:
            mode = "end"
            win = -1

def on_mouse_down(pos):
    global mode, menu_playing
    if mode == "menu":
        if play_button.collidepoint(pos):
            mode = "game"
            reset_game()
            if menu_playing:
                sounds.menu.stop()
                menu_playing = False
        elif tutorial_button.collidepoint(pos):
            mode = "tutorial"
            spawn_tutorial_enemies_map1()
            spawn_tutorial_enemies_map2()
            # Optionally stop menu music or play a different sound here
    elif mode == "end":
        if menu_button.collidepoint(pos):
            mode = "menu"
            reset_game()
            sounds.lose.stop()   # <-- Add this line
            sounds.win.stop()    # <-- And this line
            if not menu_playing:
                sounds.menu.set_volume(0.5)
                sounds.menu.play(-1)
                menu_playing = True
        elif play_again_button.collidepoint(pos):
            mode = "game"
            reset_game()
            sounds.lose.stop()   # <-- Add this line
            sounds.win.stop()    # <-- And this line

def on_key_down(key):
    global mode, menu_playing, current_map, enemies, hearts, swords, char1_direction, current_tutorial_map, current_enemy_list
    if mode == "tutorial" and key == keys.ESCAPE:
        mode = "menu"
        return
    
    elif mode == "tutorial" and key == keys.SPACE:
        # Door teleport logic for tutorial maps
        grid_x, grid_y = get_player_grid()
        tutorial_map = tutorial_map1 if current_tutorial_map == 1 else tutorial_map2
        tile = tutorial_map[grid_y][grid_x]
        if tile == 8:
            # Find the other tutorial map and the position of door 8
            if current_tutorial_map == 1:
                # Find door 8 in tutorial_map2
                for y in range(len(tutorial_map2)):
                    for x in range(len(tutorial_map2[0])):
                        if tutorial_map2[y][x] == 8:
                            current_tutorial_map = 2
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
            else:
                # Find door 8 in tutorial_map1
                for y in range(len(tutorial_map1)):
                    for x in range(len(tutorial_map1[0])):
                        if tutorial_map1[y][x] == 8:
                            current_tutorial_map = 1
                            char1.x = bg.width * (x + 0.5)
                            char1.y = bg.height * (y + 0.5)
                            return
        return

    elif key == keys.SPACE:
        # Toggle between tutorial maps
        current_tutorial_map = 2 if current_tutorial_map == 1 else 1
        return

    old_x = char1.x
    old_y = char1.y

    # Always use the current map from the maps list
    my_map = maps[current_map - 1]
    grid_x, grid_y = get_player_grid()
    
    # Determine which map to use
    if mode == "tutorial":
        current_map_data = tutorial_map1 if current_tutorial_map == 1 else tutorial_map2
        current_enemy_list = tutorial_enemies_map1 if current_tutorial_map == 1 else tutorial_enemies_map2
    else:
        current_map_data = maps[current_map - 1]
        current_enemy_list = enemies

    # Movement logic: allow walking on doors (3,4,5,6,8) and non-wall tiles (not 0)
    if (keyboard.right or keyboard.d):
        char1.image = 'sans_right'
        char1_direction = "right"
        nx, ny = grid_x + 1, grid_y
        if nx < len(current_map_data[0]) and (current_map_data[ny][nx] != 0 or current_map_data[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.x += bg.width

    elif (keyboard.left or keyboard.a):
        char1.image = 'sans_left'
        char1_direction = "left"
        nx, ny = grid_x - 1, grid_y
        if nx >= 0 and (current_map_data[ny][nx] != 0 or current_map_data[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.x -= bg.width

    elif (keyboard.down or keyboard.s):
        char1.image = 'sans_down'
        char1_direction = "down"
        nx, ny = grid_x, grid_y + 1
        if ny < len(current_map_data) and (current_map_data[ny][nx] != 0 or current_map_data[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
            char1.y += bg.height

    elif (keyboard.up or keyboard.w):
        char1.image = 'sans_up'
        char1_direction = "up"
        nx, ny = grid_x, grid_y - 1
        if ny >= 0 and (current_map_data[ny][nx] != 0 or current_map_data[ny][nx] in [3,4,5,6,8]) and not is_enemy_at(nx, ny, current_enemy_list):
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
        else:
            current_enemy_list = enemies

        # Check for enemy in that tile
        for idx, enemy in enumerate(current_enemy_list):
            enemy_grid_x = int((enemy.x - bg.width // 2) // bg.width)
            enemy_grid_y = int((enemy.y - bg.height // 2) // bg.height)
            if enemy_grid_x == atk_x and enemy_grid_y == atk_y:
                sounds.slash.play()
                enemy.health -= char1.attack
                char1.health -= enemy.attack
                if enemy.health <= 0:
                    # No bonus drops in tutorial, but you can add if you want
                    current_enemy_list.pop(idx)
                break  # Only attack one enemy per press

# --- DOOR TELEPORT LOGIC ---
    if key == keys.SPACE:
        my_map = maps[current_map - 1]
        grid_x, grid_y = get_player_grid()
        tile = my_map[grid_y][grid_x]
        # Check if standing on a door (number 3, 4, 5, 6, ...)
        if tile in [3, 4, 5, 6]:
            for i, m in enumerate(maps):
                if i != (current_map - 1):  # Only check other maps
                    for y in range(len(m)):
                        for x in range(len(m[0])):
                            if m[y][x] == tile:
                                # Only teleport if not already at this position
                                current_map = i + 1
                                enemies = enemies_maps[i]
                                hearts = hearts_maps[i]
                                swords = swords_maps[i]
                                char1.x = bg.width * (x + 0.5)
                                char1.y = bg.height * (y + 0.5)
                                return
                    
    enemy_index = char1.collidelist(enemies)
    if enemy_index != -1:
        sounds.slash.play()
        char1.x = old_x
        char1.y = old_y
        enemy = enemies[enemy_index]
        enemy.health -= char1.attack
        char1.health -= enemy.attack
        if enemy.health <= 0:
            if enemy.bonus == 1:
                heart = Actor("heart")
                heart.pos = enemy.pos
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor("knive")
                sword.pos = enemy.pos
                swords.append(sword)
            enemies.pop(enemy_index)

def update(dt):
    global title_anim_dir, title_anim_base_y, end_text_anim_y, end_text_anim_dir, end_text_anim_base_y, hearts, swords
    victory()
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
    for i in range(len(hearts)):
        if char1.colliderect(hearts[i]):
            char1.health += 5
            hearts.pop(i)
            break
    for i in range(len(swords)):
        if char1.colliderect(swords[i]):
            char1.attack += 5
            swords.pop(i)
            break




















pgzrun.go()
