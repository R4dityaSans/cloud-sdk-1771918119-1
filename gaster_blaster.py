import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
import pgzrun
import random
import math

WIDTH = 640
HEIGHT = 640
TILE_SIZE = 64

# Actor for classic sans
start_tile_x = 5
start_tile_y = 5
char1 = Actor("classic_sans_down", (start_tile_x * TILE_SIZE + TILE_SIZE // 2, start_tile_y * TILE_SIZE + TILE_SIZE // 2))
char1_direction = "down"
move_hold_dir = None
move_hold_timer = 0
MOVE_HOLD_DELAY = 0.15  # seconds between steps when holding
# Gaster blaster beams: each is a dict with x, y, angle, timer
beams = []
blasters = []
BEAM_DURATION = 2.0  # seconds
SUMMON_DURATION = 0.5
FIRE_DURATION = 2.0
FADEOUT_DURATION = 0.5

# Boss setup
boss_timer = 0
BOSS_BLASTER_INTERVAL = 3.0  # seconds
boss_attack_mode = "random"  # "random" or "line"
boss_blaster_count = 0
boss_line_shots = 0
ground_bone_attacks = []  # Each is {"tiles": [(tx, ty)], "timer": 0, "state": "warn"}
spin_attack_timer = 0
spin_blaster_timer = 0
spin_positions = []
spin_shots = 0
spin_index = 0
SPIN_BLASTER_INTERVAL = 0.2  # seconds
spin_initialized = False

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
        "actor": Actor("gblaster_idle", (bx, by))
    }
    blaster["actor"].angle = -math.degrees(angle) + 90
    blasters.append(blaster)
    sounds.gaster_blaster_sound.play()
    boss_blaster_count += 1
    if boss_blaster_count >= 5:
        boss_attack_mode = "line"
        boss_blaster_count = 0
        boss_line_shots = 0

def boss_attack_line():
    global boss_line_shots, boss_attack_mode, boss_blaster_count
    rows = HEIGHT // TILE_SIZE
    cols = WIDTH // TILE_SIZE
    if boss_line_shots % 2 == 0:
        chosen_rows = random.sample(range(rows), 3)
        for row in chosen_rows:
            if row < rows // 2:
                bx = row * TILE_SIZE + TILE_SIZE // 2
                by = TILE_SIZE // 2
                angle = math.pi / 2
            else:
                bx = row * TILE_SIZE + TILE_SIZE // 2
                by = HEIGHT - TILE_SIZE // 2
                angle = -math.pi / 2
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
    else:
        chosen_cols = random.sample(range(cols), 3)
        for col in chosen_cols:
            if col < cols // 2:
                bx = TILE_SIZE // 2
                by = col * TILE_SIZE + TILE_SIZE // 2
                angle = 0
            else:
                bx = WIDTH - TILE_SIZE // 2
                by = col * TILE_SIZE + TILE_SIZE // 2
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
    if boss_line_shots >= 3:
        boss_attack_mode = "ground_bone"
        boss_line_shots = 0
        boss_blaster_count = 0

def boss_attack_ground_bone():
    global boss_blaster_count, boss_attack_mode, spin_shots, spin_index, boss_timer, spin_initialized
    tiles_x = WIDTH // TILE_SIZE
    tiles_y = HEIGHT // TILE_SIZE
    used_tiles = set()
    bone_tiles = []
    for _ in range(10):
        while True:
            tx = random.randint(0, tiles_x - 1)
            ty = random.randint(0, tiles_y - 1)
            if (tx, ty) not in used_tiles:
                used_tiles.add((tx, ty))
                bone_tiles.append((tx, ty))
                break
    ground_bone_attacks.append({"tiles": bone_tiles, "timer": 0, "state": "warn"})
    boss_blaster_count += 1
    if boss_blaster_count >= 5:
        boss_attack_mode = "spin"
        boss_blaster_count = 0
        spin_shots = 0
        spin_index = 0
        boss_timer = 0
        spin_initialized = False

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

    if spin_shots < 50:
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
            "actor": Actor("gblaster_idle", (x, y))
        }
        blaster["actor"].angle = -math.degrees(angle) + 90
        blasters.append(blaster)
        sounds.gaster_blaster_sound.play()
        spin_index = (spin_index + 1) % len(spin_positions)
        spin_shots += 1
    else:
        boss_attack_mode = "random"
        spin_shots = 0
        spin_index = 0
        spin_positions = []
        spin_initialized = False

def draw():
    screen.fill("black")
    char1.draw()
    max_thickness = 32
    min_thickness = 8
    amp = 0.3
    osc_speed = 6

    for attack in ground_bone_attacks:
        for tx, ty in attack["tiles"]:
            gx = tx * TILE_SIZE + TILE_SIZE // 2
            gy = ty * TILE_SIZE + TILE_SIZE // 2
            if attack["state"] == "warn":
                # Draw warning rect (red, semi-transparent)
                screen.draw.filled_rect(Rect((gx - TILE_SIZE // 2, gy - TILE_SIZE // 2), (TILE_SIZE, TILE_SIZE)), (255, 0, 0, 100))
                screen.draw.rect(Rect((gx - TILE_SIZE // 2, gy - TILE_SIZE // 2), (TILE_SIZE, TILE_SIZE)), (255, 0, 0))
            elif attack["state"] == "fadein":
                # Fade in bone (0 to 255 alpha over 0.5s)
                alpha = int(255 * (attack["timer"] / 0.5))
                bone = Actor("virus_sans_groundbones", (gx, gy))
                bone._surf.set_alpha(alpha)
                bone.draw()
            elif attack["state"] == "stay":
                # Fully visible bone
                bone = Actor("virus_sans_groundbones", (gx, gy))
                bone._surf.set_alpha(255)
                bone.draw()
            elif attack["state"] == "fadeout":
                # Fade out bone (255 to 0 alpha over 0.5s)
                alpha = int(255 * (1 - attack["timer"] / 0.5))
                bone = Actor("virus_sans_groundbones", (gx, gy))
                bone._surf.set_alpha(alpha)
                bone.draw()
    # Draw blasters
    for blaster in blasters:
        angle_deg = math.degrees(blaster["angle"])
        blaster["actor"].angle = -angle_deg + 90  # Only this line for correct facing!
        blaster["actor"].flip_x = False           # Always False, never mirror
        blaster["actor"]._surf.set_alpha(int(blaster["alpha"]))
        blaster["actor"].draw()
    # Draw beams
    for beam in beams:
        x, y = beam["x"], beam["y"]
        angle = beam["angle"]
        t = 1.0 - (beam["timer"] / (FIRE_DURATION + FADEOUT_DURATION))
        # Animate thickness: grow, oscillate, shrink
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

        # Calculate end point for the beam (extend far outside the screen)
        length = 1000
        end_x = x + math.cos(angle) * length
        end_y = y + math.sin(angle) * length

        # Draw the thick beam as a series of filled circles
        steps = 100
        for i in range(steps):
            px = x + (end_x - x) * i / steps
            py = y + (end_y - y) * i / steps
            screen.draw.filled_circle((px, py), thickness // 2, "white")

mouse_pos = (WIDTH // 2, HEIGHT // 2)  # Track mouse position manually

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

def on_key_down(key):
    global char1_direction
    if key == keys.F:
        mx, my = mouse_pos
        tx = int(char1.x // TILE_SIZE)
        ty = int(char1.y // TILE_SIZE)
        x = tx * TILE_SIZE + TILE_SIZE // 2
        y = ty * TILE_SIZE + TILE_SIZE // 2
        # Spawn 4 blasters at 0, 90, 180, 270 degrees relative to mouse direction
        base_angle = math.atan2(my - y, mx - x)
        for i in range(4):
            angle = base_angle + i * (math.pi / 2)  # 0, 90, 180, 270 degrees
            blaster = {
                "x": x,
                "y": y,
                "angle": angle,
                "state": "summon",  # "summon", "fire", "fadeout"
                "timer": 0,
                "alpha": 0,
                "actor": Actor("gblaster_idle", (x, y))
            }
            blaster["actor"].angle = -math.degrees(angle) + 90
            blasters.append(blaster)
            sounds.gaster_blaster_sound.play()
        return

def update(dt):
    global boss_timer, boss_attack_mode, boss_blaster_count, boss_line_shots, spin_attack_timer, spin_blaster_timer, spin_attack_timer, spin_blaster_timer, spin_positions, spin_index
    global spin_positions, spin_shots, spin_index, spin_initialized
    # --- Gaster Blaster state machine ---
    for blaster in blasters[:]:
        if blaster["state"] == "summon":
            blaster["timer"] += dt
            blaster["alpha"] = min(255, int(255 * (blaster["timer"] / SUMMON_DURATION)))
            if blaster["timer"] >= SUMMON_DURATION:
                blaster["state"] = "fire"
                blaster["timer"] = 0
                blaster["alpha"] = 255
                blaster["actor"].image = "gblaster_shoot"
                # Add beam when firing starts
                beams.append({
                    "x": blaster["x"],
                    "y": blaster["y"],
                    "angle": blaster["angle"],
                    "timer": FIRE_DURATION + FADEOUT_DURATION  # Beam lasts through fire+fadeout
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
    # Update all beams and remove expired ones

    for b in beams:
        b["timer"] -= dt
    beams[:] = [b for b in beams if b["timer"] > 0]

    # --- Tile-based movement with hold-to-repeat ---
    global move_hold_dir, move_hold_timer, char1_direction
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
            move_sans_tile(direction)
        else:
            move_hold_timer -= dt
            if move_hold_timer <= 0:
                move_sans_tile(direction)
                move_hold_timer = MOVE_HOLD_DELAY
    else:
        move_hold_dir = None
        move_hold_timer = 0

    # --- Boss logic: summon blaster every 3 seconds ---
    boss_timer += dt
    if boss_attack_mode == "spin":
        interval = SPIN_BLASTER_INTERVAL
    else:
        interval = BOSS_BLASTER_INTERVAL

    if boss_timer >= interval:
        boss_timer = 0
        if boss_attack_mode == "random":
            boss_attack_random()
        elif boss_attack_mode == "line":
            boss_attack_line()
        elif boss_attack_mode == "ground_bone":
            boss_attack_ground_bone()
        elif boss_attack_mode == "spin":
            boss_attack_spin()


def move_sans_tile(direction):
    global char1_direction
    dx, dy = 0, 0
    if direction == "right":
        char1_direction = "right"
        dx = TILE_SIZE
    elif direction == "left":
        char1_direction = "left"
        dx = -TILE_SIZE
    elif direction == "up":
        char1_direction = "up"
        dy = -TILE_SIZE
    elif direction == "down":
        char1_direction = "down"
        dy = TILE_SIZE

    new_x = char1.x + dx
    new_y = char1.y + dy
    if TILE_SIZE // 2 <= new_x <= WIDTH - TILE_SIZE // 2 and TILE_SIZE // 2 <= new_y <= HEIGHT - TILE_SIZE // 2:
        char1.x = new_x
        char1.y = new_y
    char1.image = f"classic_sans_{char1_direction}"

pgzrun.go()

