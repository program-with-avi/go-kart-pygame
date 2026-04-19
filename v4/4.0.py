import pygame
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1100, 700))
clock = pygame.time.Clock()

arial_font = pygame.font.SysFont("Arial", 28, bold=1)

x, y = 1250, 300 # Initial world position
vel_x = 0
vel_y = 0
angle = 0
current_speed = 0
target_max = 15.0
max_speed = 15.0  # Increased for the larger scale
acceleration = 0.2
friction = 0.98  # Keep 98% of velocity each frame
grip = 0.05       # Driftiness (Lower = more slide)
steering = 2
S = 3             # Track Scale
click = False
collision_map = pygame.Surface((5000, 5000)) 
collision_map.fill((0, 255, 0))
game_state = "CAR_SELECT"  # Start with car selection
selected_car = 0  # 0=Red, 1=Blue
cars = ["Red", "Blue"]
is_paused = False
click = False
last_collision_check = None  # Cache for collision detection
grass_tex = pygame.image.load("grass_tex.png").convert()
road_tex = pygame.image.load("asphalt.jfif").convert()

# If your images are small, we can scale them up
grass_tex = pygame.transform.scale(grass_tex, (200, 200))
road_tex = pygame.transform.scale(road_tex, (300, 300))

# Load kart images
red_kart = pygame.image.load("red_car.png").convert_alpha()
red_kart = pygame.transform.scale(red_kart, (200,137))
blue_kart = pygame.image.load("blue_car.png").convert_alpha()
blue_kart = pygame.transform.scale(blue_kart, (200,137))
kart_images = [red_kart, blue_kart]  # 0=Red, 1=Blue
# Load textures

#variables
running = True
skid_marks = [] 
debug_print = False  # Control debug output

# Pre-cache texture sizes for performance
grass_w, grass_h = grass_tex.get_size()
road_w, road_h = road_tex.get_size()

# Left ellipse - efficient creation with mask
t1_left_ellipse = pygame.Surface((300*S, 600*S), pygame.SRCALPHA)
for tx in range(0, 300*S, road_w):
    for ty in range(0, 600*S, road_h):
        t1_left_ellipse.blit(road_tex, (tx, ty))
# Create and apply ellipse mask
mask_left = pygame.Surface((300*S, 600*S), pygame.SRCALPHA)
mask_left.fill((0, 0, 0, 0))
pygame.draw.ellipse(mask_left, (255, 255, 255, 255), (0, 0, 300*S, 600*S))
t1_left_ellipse.blit(mask_left, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# Right ellipse
t1_right_ellipse = pygame.Surface((300*S, 600*S), pygame.SRCALPHA)
for tx in range(0, 300*S, road_w):
    for ty in range(0, 600*S, road_h):
        t1_right_ellipse.blit(road_tex, (tx, ty))
mask_right = pygame.Surface((300*S, 600*S), pygame.SRCALPHA)
mask_right.fill((0, 0, 0, 0))
pygame.draw.ellipse(mask_right, (255, 255, 255, 255), (0, 0, 300*S, 600*S))
t1_right_ellipse.blit(mask_right, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# Track 1 infield grass texture
t1_infield = pygame.Surface((700*S, 400*S))
for gx in range(0, 700*S, grass_w):
    for gy in range(0, 400*S, grass_h):
        t1_infield.blit(grass_tex, (gx, gy))

# Track 2 outer ellipse textured
t2_outer_ellipse = pygame.Surface((1100*S, 900*S), pygame.SRCALPHA)
for tx in range(0, 1100*S, road_w):
    for ty in range(0, 900*S, road_h):
        t2_outer_ellipse.blit(road_tex, (tx, ty))
# Create and apply ellipse mask for track 2
mask_t2_outer = pygame.Surface((1100*S, 900*S), pygame.SRCALPHA)
mask_t2_outer.fill((0, 0, 0, 0))
pygame.draw.ellipse(mask_t2_outer, (255, 255, 255, 255), (0, 0, 1100*S, 900*S))
t2_outer_ellipse.blit(mask_t2_outer, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

# Track 2 infield ellipse grass texture
t2_infield = pygame.Surface((800*S, 500*S), pygame.SRCALPHA)
for gx in range(0, 800*S, grass_w):
    for gy in range(0, 500*S, grass_h):
        t2_infield.blit(grass_tex, (gx, gy))
# Create and apply ellipse mask for infield
mask_t2_infield = pygame.Surface((800*S, 500*S), pygame.SRCALPHA)
mask_t2_infield.fill((0, 0, 0, 0))
pygame.draw.ellipse(mask_t2_infield, (255, 255, 255, 255), (0, 0, 800*S, 500*S))
t2_infield.blit(mask_t2_infield, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False
    
    # === MENU STATES ===
    if game_state == "MENU" or game_state == "CAR_SELECT" or not click:
        screen.fill((50,150,50))
        
        # CAR SELECTION SCREEN
        if game_state == "CAR_SELECT":
            title_font = pygame.font.SysFont("Arial", 40, bold=True)
            title = title_font.render("SELECT YOUR CAR", True, (255, 255, 0))
            screen.blit(title, (250, 50))
            
            car_colors = [(255, 0, 0), (0, 0, 255)]  # Red, Blue
            
            for i, car_name in enumerate(cars):
                x_pos = 200 + i * 400
                y_pos = 250
                
                # Draw car rectangle
                rect = pygame.Rect(x_pos, y_pos, 200, 150)
                pygame.draw.rect(screen, car_colors[i], rect)
                if i == selected_car:
                    pygame.draw.rect(screen, (255, 255, 0), rect, 5)  # Yellow border if selected
                
                # Draw car name
                car_text = arial_font.render(car_name, True, (255, 255, 255))
                screen.blit(car_text, (x_pos + 50, y_pos + 60))
            
            # Navigation
            if keys[pygame.K_a]:
                selected_car = (selected_car - 1) % len(cars)
                pygame.time.delay(200)
            if keys[pygame.K_d]:
                selected_car = (selected_car + 1) % len(cars)
                pygame.time.delay(200)
            
            # Select car and go to track selection
            if keys[pygame.K_w]:
                game_state = "MENU"
                pygame.time.delay(200)
            
            # Instructions
            instr = arial_font.render("A/D to select | W to confirm", True, (255, 255, 255))
            screen.blit(instr, (150, 600))
        
        # MAIN MENU SCREEN (Track Selection)
        elif game_state == "MENU":
            title_font = pygame.font.SysFont("Arial", 40, bold=True)
            title = title_font.render("SELECT TRACK", True, (255, 255, 0))
            screen.blit(title, (300, 50))
            
            # 1. Define the button area
            button_rect = pygame.Rect(300, 250, 150, 50)
            button2 = pygame.Rect(600, 250, 150, 50)
            t1_font = arial_font.render("Track1", True, (255, 255, 0))
            t2_font = arial_font.render("Track2", True, (255, 255, 0))
                   
            # 2. Get mouse data
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            # 3. Logic: Is the mouse hovering?
            if button_rect.collidepoint(mouse_pos):
                color = (200, 0, 0) # Lighter red on hover
                if mouse_click[0]: # 0 is Left Click
                    click = True
                    x, y = 1250, 300
                    game_state = "RACE_TRACK1"
                    collision_map.fill((0, 255, 0)) # Reset to all grass
                    # Draw the track shapes in a different color (like Grey)
                    pygame.draw.ellipse(collision_map, (100, 100, 100), (8*S, 50*S, 300*S, 600*S))
                    pygame.draw.rect(collision_map, (100, 100, 100), (145*S, 50*S, 800*S, 100*S))
                    pygame.draw.rect(collision_map, (100, 100, 100), (145*S, 550*S, 800*S, 100*S))    
                    pygame.draw.ellipse(collision_map, (100, 100, 100), (795*S, 50*S, 300*S, 600*S))
                    # Draw the infield grass back on
                    pygame.draw.rect(collision_map, (0, 255, 0), (190*S, 150*S, 700*S, 400*S))
                    debug_print = False
                
            else:         
                color = (150, 0, 0) # Dark red
            pygame.draw.rect(screen, color, button_rect)
            screen.blit(t1_font, t1_font.get_rect(center=button_rect.center))
            if button2.collidepoint(mouse_pos):
                color2 = (0,0,200)
                if mouse_click[0]:
                    click = True
                    x, y = 1550, 350
                    game_state = "RACE_TRACK2"
                    collision_map.fill((0, 255, 0)) 
                    pygame.draw.ellipse(collision_map, (100, 100, 100), (0, 0, 1100*S, 900*S))
                    pygame.draw.ellipse(collision_map, (0, 255, 0), (150*S, 200*S, 800*S, 500*S))
                    debug_print = True
            else:
                color2 = (0,0,150)
            pygame.draw.rect(screen, color2, button2 )
            screen.blit(t2_font,t2_font.get_rect(center=button2.center))
        
        pygame.display.flip()
        clock.tick(60)
        continue
    
    # === RACING STATE ===
    
    # ESC to return to track selection
    if keys[pygame.K_ESCAPE]:
        click = False
        game_state = "MENU"
        is_paused = False
        vel_x = 0
        vel_y = 0
        pygame.time.delay(300)
        continue
    
    # P to toggle pause
    if keys[pygame.K_p]:
        is_paused = not is_paused
        pygame.time.delay(300)
    
    # If paused, show pause screen
    if is_paused:
        screen.fill((0, 0, 0))
        pause_title = pygame.font.SysFont("Arial", 60, bold=True)
        pause_text = pause_title.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (350, 250))
        
        instr_font = pygame.font.SysFont("Arial", 32)
        instr1 = instr_font.render("P - Resume", True, (255, 255, 255))
        instr2 = instr_font.render("ESC - Change Track", True, (255, 255, 255))
        screen.blit(instr1, (350, 350))
        screen.blit(instr2, (300, 400))
        
        pygame.display.flip()
        clock.tick(60)
        continue
    
    S = 3 # Your Scale
    cam_x = x - (1100 / 2)
    cam_y = y - (700 / 2)
    radians = math.radians(angle)
    forward_x = math.cos(math.radians(angle))
    forward_y = -math.sin(math.radians(angle))
    if click and "RACE_TRACK2" in game_state:
    # 1. Tile Grass (Always first) - optimized
        start_tx = int(cam_x // grass_w) * grass_w - grass_w
        start_ty = int(cam_y // grass_h) * grass_h - grass_h
        for tx in range(start_tx, start_tx + 1100 + grass_w * 2, grass_w):
            for ty in range(start_ty, start_ty + 700 + grass_h * 2, grass_h):
                screen.blit(grass_tex, (tx - cam_x, ty - cam_y))
            
        # 2. Draw Track 2 Asphalt Ellipse with texture
        screen.blit(t2_outer_ellipse, (0 - cam_x, 0 - cam_y))
        pygame.draw.ellipse(screen, (200, 200, 200), (0 - cam_x, 0 - cam_y, 1100*S, 900*S), 3)  # Border
    
        # 3. Draw Track 2 Infield (Grass) with proper ellipse
        screen.blit(t2_infield, (150*S - cam_x, 200*S - cam_y))
        pygame.draw.ellipse(screen, (200, 200, 200), (150*S - cam_x, 200*S - cam_y, 800*S, 500*S), 3)  # Border
    elif click and "RACE_TRACK1" in game_state:
    # 1. Tile Grass - optimized
        start_x = int(cam_x // grass_w) * grass_w - grass_w
        start_y = int(cam_y // grass_h) * grass_h - grass_h
        for tx in range(start_x, start_x + 1100 + grass_w * 2, grass_w):
            for ty in range(start_y, start_y + 700 + grass_h * 2, grass_h):
                screen.blit(grass_tex, (tx - cam_x, ty - cam_y))

        # 2. Draw Road Ellipses (Curves) with pre-rendered textures
        screen.blit(t1_left_ellipse, (8*S - cam_x, 50*S - cam_y))
        pygame.draw.ellipse(screen, (200, 200, 200), (8*S - cam_x, 50*S - cam_y, 300*S, 600*S), 3)  # Border

        screen.blit(t1_right_ellipse, (795*S - cam_x, 50*S - cam_y))
        pygame.draw.ellipse(screen, (200, 200, 200), (795*S - cam_x, 50*S - cam_y, 300*S, 600*S), 3)  # Border
        
        # 3. Tile Road Rectangles (Straightaways) - only draw if visible
        if 50*S - cam_y > -road_h and 50*S - cam_y < 700:
            for rx in range(int(145*S), int(945*S), road_w):
                screen.blit(road_tex, (rx - cam_x, 50*S - cam_y))
        if 550*S - cam_y > -road_h and 550*S - cam_y < 700:
            for rx in range(int(145*S), int(945*S), road_w):
                screen.blit(road_tex, (rx - cam_x, 550*S - cam_y))

        # 4. Draw Infield with grass texture
        screen.blit(t1_infield, (190*S - cam_x, 150*S - cam_y))
        pygame.draw.rect(screen, (255, 255, 255), (400*S - cam_x, 50*S - cam_y, 40*S, 100*S))
    # Debug circles removed for performance
    # === COLLISION CHECK (OPTIMIZED) ===
    try:
        kart_x_int = int(x)
        kart_y_int = int(y)
        if 0 <= kart_x_int < 5000 and 0 <= kart_y_int < 5000:
            ground_type = collision_map.get_at((kart_x_int, kart_y_int))
            # Grass has high green (>100), low red/blue
            is_grass = ground_type[1] > ground_type[0] + 50 and ground_type[1] > ground_type[2] + 50
            
            if is_grass:
                target_max = 3.0  # Slow on grass
                if current_speed > target_max:
                    vel_x *= 0.92
                    vel_y *= 0.92
            else:
                target_max = 15.0
        else:
            target_max = 3.0
    except (IndexError, ValueError):
        target_max = 3.0

    # Only add marks if we are moving fast and turning/drifting (limited to 200 marks for performance)
    is_drifting = abs(vel_x * math.sin(radians) + vel_y * math.cos(radians)) > 2.0
    if is_drifting and current_speed > 4.5 and len(skid_marks) < 200:
        skid_marks.append([x, y, angle, 255]) 

    # Draw and Fade Skids
        # Use Trigonometry to move in the direction the kart is facing
    # 1. Update Angle (Heading)
    if keys[pygame.K_a] and (abs(vel_x) > 0.1 or abs(vel_y) > 0.1):
        angle += steering
        current_speed *=0.97
    if keys[pygame.K_d] and (abs(vel_x) > 0.1 or abs(vel_y) > 0.1):
        angle -= steering
        current_speed *=0.97

# 2. Acceleration
# We calculate "Forward" based on where the nose is pointing
    forward_x = math.cos(math.radians(angle))
    forward_y = -math.sin(math.radians(angle))

    # --- REPLACE YOUR ENTIRE PHYSICS BLOCK (From Acceleration to Drift) ---
    if keys[pygame.K_w]:
        if current_speed < target_max:
            vel_x += forward_x * acceleration
            vel_y += forward_y * acceleration
    elif keys[pygame.K_s]:
        vel_x -= forward_x * (acceleration / 2)
        vel_y -= forward_y * (acceleration / 2)

    # APPLY FRICTION ONLY ONCE HERE
    vel_x *= friction
    vel_y *= friction
    current_speed = math.sqrt(vel_x**2 + vel_y**2)

    x += vel_x
    y += vel_y
    screen_x = x - cam_x
    screen_y = y - cam_y

    for mark in skid_marks[:]:
        mark[3] -= 3  # Faster fade for performance
        if mark[3] <= 0:
            skid_marks.remove(mark)
            continue
        # Draw smaller skid marks at lower alpha for better performance
        skid_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        skid_surf.set_alpha(int(mark[3]))
        skid_surf.fill((123, 127, 133))
        screen.blit(skid_surf, (mark[0] - cam_x - 5, mark[1] - cam_y - 5))
    rotated_kart = pygame.transform.rotate(kart_images[selected_car], angle)
    new_rect = rotated_kart.get_rect(center=(550, 350))
    screen.blit(rotated_kart, new_rect.topleft)
    display_speed = current_speed
        #speedmeter
    display_speed = int(math.sqrt(vel_x**2 + vel_y**2) * 20)
    speed_text = arial_font.render(f"{display_speed} KPH", True, (255, 255, 0))
    screen.blit(speed_text, (10, 50))
    
    # Display car info
    car_text = arial_font.render(f"Car: {cars[selected_car]}", True, (255, 255, 255))
    screen.blit(car_text, (10, 10))
    
    # Display pause instructions
    small_font = pygame.font.SysFont("Arial", 16)
    pause_instr = small_font.render("P=Pause  ESC=Change Track", True, (200, 200, 200))
    screen.blit(pause_instr, (10, 90))
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
