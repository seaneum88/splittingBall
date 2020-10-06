import os
import pygame

#######################################################################################################
# initialization
pygame.init()

# screen setting
screen_width = 640
screen_heigth = 480
screen = pygame.display.set_mode((screen_width, screen_heigth))

# set title screen
pygame.display.set_caption("Shawn's Game") # game name

# FPS
clock = pygame.time.Clock()
#######################################################################################################

# 1. game setting (background, game image, position, speed, font...)
current_path = os.path.dirname(__file__) # current file location
image_path = os.path.join(current_path, "images") # images file location

# getting background image
background = pygame.image.load(os.path.join(image_path, "background.png"))

# making stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))

stage_size = stage.get_rect().size
stage_height = stage_size[1] # putting character on specific stage loaction

# making character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # getting image size
character_width = character_size[0] # width size of character
character_height = character_size[1] # height size of character
character_x_pos = (screen_width / 2) - (character_width / 2) # half size of the screen - half of the character size
character_y_pos = screen_heigth - character_height - stage_height # bottom position of the screen

# character position
to_x = 0
to_y = 0

# character speed
character_speed = 0.6

# event loop
running = True
while running:
    dt = clock.tick(30) # setting in game frame per second

    # 2. handling event (keyboard, mouse..)
    for event in pygame.event.get(): # recognizing event
        if event.type == pygame.QUIT: # when user click exit button
            running = False

        if event.type == pygame.KEYDOWN: # check if key is down
            if event.key == pygame.K_LEFT: # check if left key is pressed
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # check if right key is pressed
                to_x += character_speed
            elif event.key == pygame.K_UP: # check if up key is pressed
                to_y -= character_speed
            elif event.key == pygame.K_DOWN: # check if down key is pressed
                to_y += character_speed

        if event.type == pygame.KEYUP: # check if key is up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    # 4. handling collision

    # 5. display
    screen.blit(background, (0, 0)) # adding background image from variable
    screen.blit(stage, (0, screen_heigth - stage_height)) # adding background image from variable
    screen.blit(character, (character_x_pos, character_y_pos)) #adding character image from variable

    pygame.display.update() # re-displaying game screen

# delay before exit
pygame.time.delay(2000) # 2 second delay before exit

# exit pygame
pygame.quit()