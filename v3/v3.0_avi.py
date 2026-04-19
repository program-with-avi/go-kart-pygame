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
#kart_img = pygame.transform.scale(screen, (50,50))

#variables
x, y = 420, 100
angle = 0
speed = 0
max_speed = 5
acceleration = 0.1
friction = 0.10
steering = 4
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False
    if click and "RACE_TRACK1" in game_state:
        screen.fill((50, 150, 50)) # Grass background

        #track
        pygame.draw.ellipse(screen,(100, 100, 100), (10-2, 50, 300, 600))
        pygame.draw.rect(screen, (100,100,100), (145-2,50, 800,100))
        pygame.draw.rect(screen, (100,100,100), (145-2,550, 800,100))
        pygame.draw.ellipse(screen,(100, 100, 100), (795-3, 50, 300, 600))
        pygame.draw.rect(screen,(50,150,50), (190-7, 150 , 700,400 ))
        #pygame.draw.ellipse(screen, (50, 150, 50), [150, 150, 800, 400])
        pygame.draw.rect(screen, (255, 255, 255), [400, 50, 40, 100])
    elif click and "RACE_TRACK2" in game_state:
        screen.fill((50, 150, 50))
        pygame.draw.ellipse(screen,(100, 100, 100), (50, 50, 900, 500))
        pygame.draw.ellipse(screen, (50, 150, 50), [150, 150, 700, 300])
        pygame.draw.rect(screen, (255, 255, 255), [400, 50, 40, 100])
    # Use Trigonometry to move in the direction the kart is facing
    radians = math.radians(angle)
    x += speed * math.cos(radians)
    y -= speed * math.sin(radians)

    if keys[pygame.K_w]:
        speed = min(speed + acceleration, max_speed)
    elif keys[pygame.K_s]:
        speed = max(speed - acceleration, -max_speed/2)
    else:
        # Apply friction
        if speed > 0: speed -= friction
        if speed < 0: speed += friction

    if keys[pygame.K_a] and abs(speed) > 0.1:
        angle += steering
        speed *=0.97
    if keys[pygame.K_d] and abs(speed) > 0.1:
        angle -= steering
        speed *=0.97
    # Rendering
    rotated_kart = pygame.transform.rotate(kart_img, angle)
    new_rect = rotated_kart.get_rect(center=(x, y))
    screen.blit(rotated_kart, new_rect.topleft)
    display_speed = speed
    # Inside your main loop:
   
    try:
        current_color = screen.get_at((int(x), int(y)))
        if current_color == (50, 150, 50, 255):
            max_speed = 1.5
        else:
            max_speed = 5.0
    except IndexError:
        x, y = 400, 100
        speed = 0
        #speedmeter
    display_speed = int(round(((abs(speed))*20), 2)) 
    speed_text = arial_font.render(f"{display_speed} KPH", True, (255, 255, 0))
    
    screen.blit(speed_text, (10, 50))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
