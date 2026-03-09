import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import random
import pgzrun

bg = Actor('bg')
bg1 = Actor("wood_a")
bg2 = Actor("wood_b")
door = Actor("door")
menu = Actor("menu")
win_screen = Actor("win_screen")
lose_screen = Actor("lose_screen")
play_button = Actor("play_button")
menu_button = Actor("menu_button")
play_again_button = Actor("play_again_button")
backsound_playing = False
size_w = 10 # Lebar dari bidang dalam sel
size_h = 10 # Tinggi dari bidang dalam sel
WIDTH = bg.width * size_w
HEIGHT = bg.height * size_h
mode = "menu" # Mode permainan
win = 0 # Menang
def get_player_grid():
    # Returns (col, row) of char1's current tile
    return int((char1.x - bg.width // 2) // bg.width), int((char1.y - bg.height // 2) // bg.height)
current_map = 1  # 1 for my_map1, 2 for my_map2
TITLE = "Sans Adventure" # Judul dari jendela permainan
FPS = 30 # Jumlah Frame Per Detik

my_map1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 2, 2, 1, 2, 1, 0], 
          [0, 1, 1, 2, 1, 2, 1, 1, 2, 0], 
          [0, 2, 1, 1, 2, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 1, 1, 2, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 2, 0], 
          [0, 1, 2, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 2, 1, 2, 1, 3, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

my_map2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 2, 1, 1, 1, 1, 1, 0], 
          [0, 1, 2, 1, 2, 2, 1, 2, 1, 0], 
          [0, 1, 1, 2, 1, 2, 2, 1, 2, 0], 
          [0, 2, 1, 1, 2, 1, 1, 2, 1, 0], 
          [0, 1, 2, 1, 1, 1, 2, 1, 1, 0], 
          [0, 2, 1, 1, 2, 1, 2, 1, 2, 0], 
          [0, 1, 2, 1, 1, 1, 1, 1, 1, 0],
          [0, 3, 1, 1, 2, 1, 2, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]


def map_draw():
    if current_map == 1:
        my_map = my_map1
    else:
        my_map = my_map2
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                bg.left = bg.width*j
                bg.top = bg.height*i
                bg.draw()
            elif my_map[i][j] == 1:
                bg1.left = bg.width*j
                bg1.top = bg.height*i
                bg1.draw()
            elif my_map[i][j] == 2:
                bg2.left = bg.width*j
                bg2.top = bg.height*i
                bg2.draw()
            elif my_map[i][j] == 3:
                door.left = bg.width*j
                door.top = bg.height*i
                door.draw()

def reset_game():
    global enemies, hearts, swords, char1, used_positions, enemies_map1, enemies_map2, current_map
    # Reset player
    char1.health = 100
    char1.attack = 5
    char1.x = bg.width * 1.5
    char1.y = bg.height * 1.5
    # Reset lists
    hearts = []
    swords = []
    # Reset and spawn enemies for both maps
    spawn_enemies_for_map1()
    spawn_enemies_for_map2()
    # Set enemies to the correct map
    if current_map == 1:
        enemies = enemies_map1
    else:
        enemies = enemies_map2

#title
title = Actor("sa_title")
title.center = (WIDTH // 2, HEIGHT // 2 - 240)
title_anim_dir = 1  # 1 for down, -1 for up
title_anim_speed = 0.3  # Adjust for slower/faster animation
title_anim_range = 10   # How many pixels up and down
title_anim_base_y = title.y

#Protagonis
char1 = Actor('sans_right')
char1.top = bg.height
char1.left = bg.width
char1.health = 100
char1.attack = 5

health_bars = [
    "health_bar_0", "health_bar_1", "health_bar_2", "health_bar_3", "health_bar_4", "health_bar_5",
    "health_bar_6", "health_bar_7", "health_bar_8", "health_bar_9", "health_bar_10"
]
#bonus
hearts = []
swords = []

#membangkitkan musuh
enemies_map1 = []
enemies_map2 = []
enemies = enemies_map1
used_positions = set()
# Add a 2x2 gap around the player spawn
for dx in range(2):
    for dy in range(2):
        used_positions.add((bg.width * (1 + dx), bg.height * (1 + dy)))

def spawn_enemies_for_map1():
    global enemies_map1
    enemies_map1 = []
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
    global enemies_map2
    enemies_map2 = []
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
def draw():
    global backsound_playing
    if mode == "menu":
        screen.fill("#000000")
        menu.center = (WIDTH // 2, HEIGHT // 2)
        menu.draw()
        title.draw()
        play_button.center = (WIDTH // 2, HEIGHT // 2 + 140)
        play_button.draw()
        if not backsound_playing:
            sounds.backsound.set_volume(0.1)
            sounds.backsound.play(-1)
            backsound_playing = True
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

    elif mode == "end":
        screen.fill("#000000")
        if win == 1:
            win_screen.center = (WIDTH // 2, HEIGHT // 2)
            win_screen.draw()
        else:
            lose_screen.center = (WIDTH // 2, HEIGHT // 2)
            lose_screen.draw()
        # Draw buttons
        menu_button.center = (WIDTH // 2 - 100, HEIGHT // 2 + 120)
        menu_button.draw()
        play_again_button.center = (WIDTH // 2 + 100, HEIGHT // 2 + 120)
        play_again_button.draw()
    else:
        if backsound_playing:
            sounds.backsound.stop()
            backsound_playing = False
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
    global mode, backsound_playing
    if mode == "menu" and play_button.collidepoint(pos):
        mode = "game"
        reset_game()
        if backsound_playing:
            sounds.backsound.stop()
            backsound_playing = False
    elif mode == "end":
        if menu_button.collidepoint(pos):
            mode = "menu"
            reset_game()
            if not backsound_playing:
                sounds.backsound.set_volume(0.1)
                sounds.backsound.play(-1)
                backsound_playing = True
        elif play_again_button.collidepoint(pos):
            mode = "game"
            reset_game()

def on_key_down(key):
    global mode, backsound_playing, current_map, enemies
    if mode == "menu" and key == keys.RETURN:
        mode = "game"
        reset_game()
        if backsound_playing:
            sounds.backsound.stop()
            backsound_playing = False
    
    old_x = char1.x
    old_y = char1.y

    if (keyboard.right or keyboard.d) and char1.x + bg.width < WIDTH - bg.width:
        char1.x += bg.width
        char1.image = 'sans_right'
    elif (keyboard.left or keyboard.a) and char1.x - bg.width > bg.width:
        char1.x -= bg.width
        char1.image = 'sans_left'
    elif (keyboard.down or keyboard.s) and char1.y + bg.height < HEIGHT - bg.height:
        char1.y += bg.height
        char1.image = 'sans_down'
    elif (keyboard.up or keyboard.w) and char1.y - bg.height > bg.height:
        char1.y -= bg.height
        char1.image = 'sans_up'

# --- DOOR TELEPORT LOGIC ---
    if key == keys.SPACE:
        my_map = my_map1 if current_map == 1 else my_map2
        grid_x, grid_y = get_player_grid()
        if my_map[grid_y][grid_x] == 3:
            if current_map == 1:
                current_map = 2
                enemies = enemies_map2
                char1.x = bg.width * 1.5
                char1.y = bg.height * 1.5
            else:
                current_map = 1
                enemies = enemies_map1
                char1.x = bg.width * 1.5
                char1.y = bg.height * 1.5
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
    global title_anim_dir, title_anim_base_y
    victory()
    # Animate title only in menu
    if mode == "menu":
        title.y += title_anim_dir * title_anim_speed
        if abs(title.y - title_anim_base_y) > title_anim_range:
            title_anim_dir *= -1
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
