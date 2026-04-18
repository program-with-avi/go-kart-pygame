import pygame
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1100, 700))
clock = pygame.time.Clock()

arial_font = pygame.font.SysFont("Arial", 28, bold=1)

click = False
game_state = "MENU"
menu = (True if "MENU" in game_state else(False))
while menu:
    screen.fill((50,150,50))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            menu = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        menu = False
    if game_state == "MENU" or "MENU" in game_state:
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
                menu  = False
                x, y = 1250, 300
                game_state = "RACE_TRACK1"
            
        else:         
            color = (150, 0, 0) # Dark red
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(t1_font, t1_font.get_rect(center=button_rect.center))
        if button2.collidepoint(mouse_pos):
            color2 = (0,0,200)
            if mouse_click[0]:
                click = True
                menu  = False
                x, y = 1550, 225
                game_state = "RACE_TRACK2"
        else:
            color2 = (0,0,150)
        pygame.draw.rect(screen, color2, button2 )
        screen.blit(t2_font,t2_font.get_rect(center=button2.center))

    pygame.display.flip()
    clock.tick(60)
# Kart 
kart_img = pygame.Surface((40, 20), pygame.SRCALPHA)
pygame.draw.rect(kart_img, (255, 0, 0), (0, 0, 40, 20)) # Red Kart
# kartimg
# Load your image
#kart_img = pygame.image.load("kart.png").convert_alpha()
#kart_img = pygame.transform.scale(screen, (40,20))

#variables
x, y = 1250, 300 # Initial world position
vel_x = 0
vel_y = 0
angle = 0
current_speed = 0
max_speed = 15.0  # Increased for the larger scale
acceleration = 0.2
friction = 0.98  # Keep 98% of velocity each frame
grip = 0.05       # Driftiness (Lower = more slide)
steering = 2
S = 3             # Track Scale
running = True
skid_marks = [] 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False
    S = 3 # Your Scale
    cam_x = x - (1100 / 2)
    cam_y = y - (700 / 2)
    if click and "RACE_TRACK2" in game_state:
        # Define a central anchor for the whole track in the World
        track_origin_x = 0
        track_origin_y = 0
        screen.fill((50, 150, 50))
        pygame.draw.ellipse(screen, (100, 100, 100),(track_origin_x - cam_x, track_origin_y - cam_y, 1100*S, 600*S))
        pygame.draw.ellipse(screen, (50, 150, 50),((track_origin_x + 150*S) - cam_x, (track_origin_y + 150*S) - cam_y, 800*S, 300*S))
        pygame.draw.rect(screen, (255, 255, 255),((track_origin_x + 500*S) - cam_x, track_origin_y - cam_y, 40*S, 150*S))
    elif click and "RACE_TRACK1" in game_state:
        screen.fill((50, 150, 50)) 
        pygame.draw.ellipse(screen, (100, 100, 100), (8*S - cam_x, 50*S - cam_y, 300*S, 600*S))
        pygame.draw.rect(screen, (100, 100, 100), (145*S - cam_x, 50*S - cam_y, 800*S, 100*S))
        pygame.draw.rect(screen, (100, 100, 100), (145*S - cam_x, 550*S - cam_y, 800*S, 100*S))    
        pygame.draw.ellipse(screen, (100, 100, 100), (795*S - cam_x, 50*S - cam_y, 300*S, 600*S))    
        pygame.draw.rect(screen, (50, 150, 50), (190*S - cam_x, 150*S - cam_y, 700*S, 400*S))    
        pygame.draw.rect(screen, (255, 255, 255), (400*S - cam_x, 50*S - cam_y, 40*S, 100*S))
    for i in range(10):
        # This draws dots at (100, 100), (200, 200), etc. in the WORLD
        pygame.draw.circle(screen, (40, 120, 40), (i*200 - cam_x, i*200 - cam_y), 5)
        # Use Trigonometry to move in the direction the kart is facing
    radians = math.radians(angle)
    forward_x = math.cos(math.radians(angle))
    forward_y = -math.sin(math.radians(angle))
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

    if keys[pygame.K_w]:
        vel_x += forward_x * acceleration
        vel_y += forward_y * acceleration
    elif keys[pygame.K_s]:
        vel_x -= forward_x * (acceleration / 2)
        vel_y -= forward_y * (acceleration / 2)
    else:
        # Apply friction
        if current_speed > 0: current_speed -= friction
        if current_speed < 0: current_speed += friction

    vel_x *= friction
    vel_y *= friction
    current_speed = math.sqrt(vel_x**2 + vel_y**2)
    if current_speed > 0.1:
    # Blend current velocity with the forward direction
    # Higher 0.1 = more grip (boring), Lower 0.02 = more drift (fun!)
        grip = 0.02 
        vel_x = (vel_x * (1 - grip)) + (forward_x * current_speed * grip)
        vel_y = (vel_y * (1 - grip)) + (forward_y * current_speed * grip)
    x += vel_x
    y += vel_y
    screen_x = x - cam_x
    screen_y = y - cam_y
    try:
        sensor_x = 550 + 25 * math.cos(radians)
        sensor_y = 350 - 25 * math.sin(radians)
        current_color = screen.get_at((int(sensor_x), int(sensor_y)))
        if current_color[1] > current_color[0] + 20: 
            max_speed = 4.0 
        else:
            max_speed = 15.0
    except IndexError:
        x,y = 400, 100
        current_speed=0

    # Only add marks if we are moving fast and turning/drifting
    is_drifting = abs(vel_x * math.sin(radians) + vel_y * math.cos(radians)) > 2.0
    if is_drifting and current_speed > 5:
        skid_marks.append([x, y, angle, 255]) 

    # Draw and Fade Skids
    for mark in skid_marks[:]:
        mark[3] -= 2 
        if mark[3] <= 0:
            skid_marks.remove(mark)
            continue
        skid_surf = pygame.Surface((5, 5))
        skid_surf.set_alpha(mark[3])
        skid_surf.fill((30, 30, 30))
        screen.blit(skid_surf, (mark[0] - cam_x, mark[1] - cam_y))

    rotated_kart = pygame.transform.rotate(kart_img, angle)
    new_rect = rotated_kart.get_rect(center=(550, 350))
    screen.blit(rotated_kart, new_rect.topleft)
    display_speed = current_speed
        #speedmeter
    display_speed = int(math.sqrt(vel_x**2 + vel_y**2) * 20)
    speed_text = arial_font.render(f"{display_speed} KPH", True, (255, 255, 0))
    screen.blit(speed_text, (10, 50))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
