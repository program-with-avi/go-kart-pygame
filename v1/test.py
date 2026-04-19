import pygame
pygame.init()
screen = pygame.display.set_mode((1100,700))
clock = pygame.time.Clock()
t_img = pygame.image.load("track.png").convert_alpha()
running = True
click = False
game_state = "MENU"
while running:

    screen.fill((0,0,0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False
    if game_state == "MENU":
        # 1. Define the button area
        button_rect = pygame.Rect(300, 250, 200, 50)
        # 2. Get mouse data
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 3. Logic: Is the mouse hovering?
        if button_rect.collidepoint(mouse_pos):
         color = (200, 0, 0) # Lighter red on hover
         if mouse_click[0]: # 0 is Left Click
             click = True
        else:
         
         color = (150, 0, 0) # Dark red

    if click:
        screen.blit(t_img)
        game_state = "RACE"
    elif game_state == "RACE":
        race = "race"
    pygame.draw.rect(screen, color, button_rect)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

