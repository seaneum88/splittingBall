import os
import pygame

#######################################################################################################
# initialization
pygame.init()

# screen setting
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

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
character_y_pos = screen_height - character_height - stage_height # bottom position of the screen

# character position
character_to_x = 0

# character speed
character_speed = 5

# making weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# weapon can be fired multiple times
weapons = []

# bullet speed
weapon_speed = 10

# making balls
ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# each ball's speed
ball_speed_y = [-18, -15, -12, -9]

# balls
balls = []

# add first ball
balls.append({
    "pos_x" : 50, # x position of ball
    "pos_y" : 50, # y position of ball
    "img_idx" : 0, # image index of ball
    "to_x" : 3, # x direction of ball
    "to_y" : -6, # y direction of ball
    "init_spd_y" : ball_speed_y[0] # initial speed of ball 
})

# collided balls and bullets
bullet_to_remove = -1
ball_to_remove = -1

# font
game_font = pygame.font.Font(None, 40) # create font

# play time
total_time = 10

# start time
start_ticks = pygame.time.get_ticks() # getting tick

# event loop
running = True
while running:
    dt = clock.tick(30) # setting in game frame per second

    # 2. handling event (keyboard, mouse..)
    for event in pygame.event.get(): # recognizing event
        if event.type == pygame.QUIT: # when user click exit button
            running = False

        if event.type == pygame.KEYDOWN: # check if key is down
            if event.key == pygame.K_LEFT: # check if left key is working
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: # check if right key is working
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # using weapon
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP: # check if key is up
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. character position
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # bullet position (should go up as it's fired)
    # (100, 200 -> 180, 160, 140....)
    # (500, 200 -> 180, 160, 140.....)
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ]

    # make bullet disappear when it hit the top screen
    weapons = [ [w[0], w[1]] for w in weapons if w[1]  > 0 ]

    # position of ball
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # change ball direction when it hit the wall
        if ball_pos_x < 0 or ball_pos_x > (screen_width - ball_width):
            ball_val["to_x"] = ball_val["to_x"] * -1

        # y position of ball
        # intial speed when it starts to bounce up
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. handling collision

    # character rect info
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos 

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # ball rect info
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # collision between ball and character
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # collision between ball and bullets
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # bullet rect info
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # collision logic
            if weapon_rect.colliderect(ball_rect):
                bullet_to_remove = weapon_idx # setting which bullet to remove
                ball_to_remove = ball_idx # setting which ball to remove

                # ball should be splited if it's not the smallest one
                if ball_img_idx < 3:
                    # current ball's size
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # splited ball
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # the left ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x position of left ball
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y position of left ball
                        "img_idx" : ball_img_idx + 1, # image index of left ball
                        "to_x" : -3, # x direction of left ball
                        "to_y" : -6, # y direction of left ball
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # initial speed of left ball 
                    })
                    
                    # the right ball
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # x position of left ball
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # y position of left ball
                        "img_idx" : ball_img_idx + 1, # image index of left ball
                        "to_x" : 3, # x direction of left ball
                        "to_y" : -6, # y direction of left ball
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # initial speed of left ball 
                    })
                break

    # remove collided ball or bullet
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if bullet_to_remove > -1:
        del weapons[bullet_to_remove]
        bullet_to_remove = -1

    # 5. display
    screen.blit(background, (0, 0)) # adding background image from variable

    for weapon_x_pos, weapon_y_pos in weapons: # adding bullet image from variable
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height)) # adding background image from variable
    screen.blit(character, (character_x_pos, character_y_pos)) #adding character image from variable

    pygame.display.update() # re-displaying game screen

# delay before exit
pygame.time.delay(2000) # 2 second delay before exit

# exit pygame
pygame.quit()