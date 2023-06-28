import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("./UltimatePygameIntro-main/graphics/Player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("./chars/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("./UltimatePygameIntro-main/graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,200))
        self.gravity = 0
    
        self.jump_sound = pygame.mixer.Sound("./UltimatePygameIntro-main/audio/jump.mp3")
        self.jump_sound.set_volume(.25)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 200:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 200:
            self.rect.bottom = 200
        
    def animation_state(self):
        if self.rect.bottom < 200:
            self.image = self.player_jump
        else:
            self.player_index += 0.1    #'''len(self.player_walk)'''
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load("./UltimatePygameIntro-main/graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("./UltimatePygameIntro-main/graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 100
        else:
            snail_1 = pygame.image.load("./UltimatePygameIntro-main/graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("./chars/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 200
        
        self.animation_index = 0    
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6  
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render('Score: {}'.format(current_time), False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for rect in obstacle_list:
            rect.x -= 5
            
            if rect.bottom == 100:
                screen.blit(fly_surf,rect)
            else:
                screen.blit(snail_surf,rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:   return []
    
def collisions(player, obstacles):
    if obstacles:
        for rect in obstacles:
            if player.colliderect(rect):
                return False
    return True
    
def collision_sprite():   
    if pygame.sprite.spritecollide(player.sprite,obstacle,False):
        obstacle.empty()
        return False
    return True
    
def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 200:    #jump
        player_surf = player_jump
    else:                       #walk
        player_index += 0.1
        if player_index >= len(player_walk): 
            player_index = 0
        player_surf = player_walk[int(player_index)]
     
    
pygame.init()       # Initialises game
screen = pygame.display.set_mode((800,400))     # Main screen

# Sets a caption "title" on the game window
pygame.display.set_caption("Runner") # --> "title"

clock = pygame.time.Clock() # Clock object (Main timer)
test_font = pygame.font.Font("./UltimatePygameIntro-main/font/Pixeltype.ttf", 50)

# Game state
game_active = False
start_time = 0
score = 0

# BKG music
bk_music = pygame.mixer.Sound("./UltimatePygameIntro-main/audio/music.wav")
bk_music.set_volume(0.25)
bk_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

    # obstacle group
obstacle = pygame.sprite.Group()

test_surface = pygame.image.load("./graphics/Layer_0002_7.png").convert_alpha()
background = pygame.image.load("./graphics/Layer_0011_0.png").convert_alpha()

#text_surface = test_font.render("My game", False, (64,64,64))
#text_rect = text_surface.get_rect(center = (400,50))

# Obstacles + animation
snail_frame1 = pygame.image.load("./UltimatePygameIntro-main/graphics/snail/snail1.png").convert_alpha()
snail_frame2 = pygame.image.load("./chars/snail2.png").convert_alpha()
snail_index = 0
snail_frames = [snail_frame1, snail_frame2]
snail_surf = snail_frames[snail_index]

fly_frame1 = pygame.image.load("./UltimatePygameIntro-main/graphics/Fly/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("./UltimatePygameIntro-main/graphics/Fly/Fly2.png").convert_alpha()
fly_index = 0
fly_frames = [fly_frame1, fly_frame2]
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

# Player animation
player_walk1 = pygame.image.load("./UltimatePygameIntro-main/graphics/Player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("./chars/player_walk_2.png").convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load("./UltimatePygameIntro-main/graphics/Player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (50,200))

# Game over screen
player_stand = pygame.image.load("./UltimatePygameIntro-main/graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

text_over = test_font.render("Pixel Runner", False, (234, 234, 234))
text_over_rect = text_over.get_rect(center = (400,80))

text_confirm = test_font.render("Press space to Run", False, (234,234,234))
text_confirm_rect = text_confirm.get_rect(center = (400,325))

# Gravity
player_gravity = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1800)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                start_time = pygame.time.get_ticks()
        if game_active:
            # Obstacles timer
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(['fly','snail', 'snail', 'snail'])))
                #if randint(0,2):
                #    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 200)))
                #else:
                #   obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100), 100)))
             # Snail animation timer
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surf = snail_frames[snail_index]
            # Fly animation timer
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]
    
    if game_active:  
        ''' Active game '''
        # Places surface object on screen (width, height)
        screen.blit(background, (0,0))   
        screen.blit(test_surface, (0,0))  
        #pygame.draw.rect(screen, "#54697f",text_rect)    # Draws a rectangle (around
        #pygame.draw.rect(screen, "#54697f",text_rect,10) # the text in this case)
        #screen.blit(text_surface,text_rect)  
        score = display_score()        
            
        # This is the way to move objects using rectangles
        ###
        
        # Player movement
        """ player_gravity += 1
        player_rect.y += player_gravity
        
        if player_rect.bottom >= 200:
            player_rect.bottom = 200
        player_animation()
         """#screen.blit(player_surf,player_rect)  
        player.draw(screen)
        player.update()
        
        obstacle.draw(screen)
        obstacle.update()
        
        # Obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collision_sprite()
        #game_active = collisions(player_rect,obstacle_rect_list)
    else:
        ''' Non active (menu, game over)'''
        screen.fill((94,129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(text_over,text_over_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (50,200)
        player_gravity = 0
        
        text_score = test_font.render(f"Score: {score}", False, (234,234,234))
        text_score_rect = text_score.get_rect(center = (400,325))
        
        if score == 0:
            screen.blit(text_confirm,text_confirm_rect)
        else:
            screen.blit(text_score,text_score_rect)
            
    pygame.display.update()   # Necesary to place here
    clock.tick(60)            # Framerate (60fps)
        