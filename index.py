import pygame 
import math
import random
pygame.init()

clock = pygame.time.Clock()
FPS = 60

#SCREEN SETTINGS
screen_width = 620
screen_height = 780
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Garage Genius')

background = pygame.image.load('Road.png').convert()
background_height = background.get_height()

#CHARACTER SETTINGS
pinkcar = pygame.image.load('PinkCar.png')
pinkcar_x = 620
pinkcar_y = -130
pinkcar_speed = 5
pinkcar_rect = pinkcar.get_rect(topleft=(pinkcar_x, pinkcar_y))

#POTHOLE SETTINGS
obstacle_speed = 7
num_obstacles = 3
obstacles = []

for i in range(num_obstacles):
    obs_type = random.randint(0, 2)  
    obs_x = random.randrange(0, 620)
    obs_y = 780 + random.randint(100, 200)  
    obstacles.append({'x': obs_x, 'y': obs_y, 'type': obs_type})

def get_obstacle_image(obs_type):
    if obs_type == 0:
        return pygame.image.load('SmPothole.png')
    elif obs_type == 1:
        return pygame.image.load('MdPothole.png')
    elif obs_type == 2:
        return pygame.image.load('LgPothole.png')

def get_obstacle_height(obs_type):
    if obs_type == 0:
        return 56  
    elif obs_type == 1:
        return 125  
    elif obs_type == 2:
        return 125

#GAME VARIABLES
scroll = 0
tiles = math.ceil(screen_height / background_height) + 1

#LOOP
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(tiles):
        screen.blit(background, (0, i * background_height - scroll))

    scroll += 7
    if scroll >= background_height:
        scroll = 0

#CHARACTER MOVEMENT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pinkcar_x -= pinkcar_speed  # Move left
    if keys[pygame.K_RIGHT]:
        pinkcar_x += pinkcar_speed  # Move right

    if pinkcar_x < -150:
        pinkcar_x = -150 
    if pinkcar_x > screen_width + 150 - pinkcar.get_width():
        pinkcar_x = screen_width + 150 - pinkcar.get_width()

    pinkcar_rect.topleft = (pinkcar_x, pinkcar_y)

#POTHOLE MOVEMENT
    for obs in obstacles:
        obs['y'] -= obstacle_speed 

        obs_height = get_obstacle_height(obs['type'])

        if obs['y'] < -obs_height:  
            obs['y'] = screen_height + random.randint(100, 300) 
            obs['x'] = random.randrange(0, screen_width - 50)

#COLLISION
        pothole_rect = pygame.Rect(obs['x'], obs['y'],
                                get_obstacle_image(obs['type']).get_width(),
                                obs_height)

        if pinkcar_rect.colliderect(pothole_rect) and obs ['y'] > pinkcar_y - 80:
            print('Collision detected! GAME OVER.')
            running = False

#END
        screen.blit(get_obstacle_image(obs['type']), (obs['x'], obs['y']))

    screen.blit(pinkcar, pinkcar_rect.topleft)

    pygame.display.update()

pygame.quit()