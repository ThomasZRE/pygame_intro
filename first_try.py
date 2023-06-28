import pygame
from sys import exit

# Initialises game
pygame.init()

# Main screen
screen = pygame.display.set_mode((800,400))

# Sets a caption "title" on the game window
pygame.display.set_caption("Runner") # --> "title"

# Clock object (Main timer)
clock = pygame.time.Clock()

'''
 surface object (width, height)
    # test_surface = pygame.Surface((50,150))
    # test_surface.fill('Green')    # fills it with color
'''

# Font object for text ppts: ("string", bool: Antialiasing (AA), "string: color")
test_font = pygame.font.Font("./fonts/Debrosee-ALPnL.ttf", 50)

# Game state
game_active = True

# objects for the game (surface, background, text, etc.)
test_surface = pygame.image.load("./graphics/Layer_0002_7.png").convert_alpha()
background = pygame.image.load("./graphics/Layer_0011_0.png").convert_alpha()

# Font renders
text_surface = test_font.render("My game", False, (64,64,64))

# Sprite for a character
char_surface = pygame.image.load("./chars/snail2.png").convert_alpha()
    # char_x_pos = -10        # x position of an object (char position)

# Creates a rectangle around the surface of the object.
# It can be used to manipulate placement and movment of the object
char_rect = char_surface.get_rect(midbottom = (0, 200))
text_rect = text_surface.get_rect(center = (400,50))

# Surface and rectangle of the playable character
player_surf = pygame.image.load("./chars/player_walk_2.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (700,200))

# Gravity
player_gravity = 0

while True:
    # Event loop
    # Loop for exiting window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Quit: exit button
            pygame.quit()
            exit()
        if game_active:    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 200: 
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 200:
                    player_gravity = -20
        else:  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True 
                char_rect.left = 0
                
        '''       
        if event.type == pygame.MOUSEMOTION:  # Detects mouse motion
           print(event.pos)                  # prints mouse position
        if event.type == pygame.MOUSEBUTTONDOWN:  # Detects button pressed
           print("Mouse Down")                   # prints if pressed
        if event.type == pygame.MOUSEBUTTONUP:  # Detects button released after pressed
           print("Mouse up")                   # prints if button released
        '''
        
        '''
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if player_rect.collidepoint(pos):
                print("collision")      
        '''
        
    if game_active:  
        ''' Active game '''
        # Places surface object on screen (width, height)
        screen.blit(background, (0,0))   
        screen.blit(test_surface, (0,0))  
        pygame.draw.rect(screen, "#54697f",text_rect)    # Draws a rectangle (around
        pygame.draw.rect(screen, "#54697f",text_rect,10) # the text in this case)
        screen.blit(text_surface,text_rect)  
        
        # Changes the x position simulating movement
            # char_x_pos += 1
        # Replaces the object back once it reaches a certain point
            # if char_x_pos > 700:
                # char_x_pos = -600
        
        # This is the way to move objects using rectangles
        char_rect.right += 3
        if char_rect.left >= 800: char_rect.right = 0
        screen.blit(char_surface,char_rect) 
        
        # Player movement
        player_gravity += 1
        player_rect.y += player_gravity
        
        if player_rect.bottom >= 200:
            player_rect.bottom = 200
        screen.blit(player_surf,player_rect)  

        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
           print("jump")
        if player_rect.colliderect(char_rect):    #checks collision with rectangles
            print("Collision")
        
        Get mouse posisition
            mouse_pos = pygame.mouse.get_pos()
            if player_rect.collidepoint(mouse_pos):     # Check collision with mouse pointer
              print("Collision")                  # Check mouse pressed (L, M, R)
        '''
        
        # Collision
        if char_rect.colliderect(player_rect):
            game_active = False
    else:
        ''' Non active (menu, game over)'''
        screen.fill("Red")
            
    pygame.display.update()   # Necesary to place here
    clock.tick(60)            # Framerate (60fps)
        