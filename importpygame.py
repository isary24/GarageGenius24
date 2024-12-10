import pygame
import random
import sys

pygame.init()

# Set up display
WIDTH, HEIGHT = 620, 780
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Garage Genius")

# Define colors (for text)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define car and pothole properties
CAR_WIDTH, CAR_HEIGHT = 250, 300
POTHOLE_WIDTH, POTHOLE_HEIGHT = 250, 220
CAR_SPEED = 5
POTHOLE_SPEED = 5

# Images and masks
car_image = pygame.image.load("PinkCar.png").convert_alpha()
car_mask = pygame.mask.from_surface(car_image)

pothole_image = pygame.image.load("SmPothole.png").convert_alpha()
pothole_mask = pygame.mask.from_surface(pothole_image)

background_image = pygame.image.load("Road.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Resetting the game
def reset_game():
    global car_x, car_y, potholes, score
    car_x = WIDTH // 2 - CAR_WIDTH // 2
    car_y = HEIGHT - CAR_HEIGHT - 10
    potholes = []
    score = 0

# Pothole class
class Pothole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = POTHOLE_WIDTH
        self.height = POTHOLE_HEIGHT
        self.mask = pygame.mask.from_surface(pothole_image)

    def move(self):
        self.y += POTHOLE_SPEED
        if self.y > HEIGHT:
            self.y = random.randint(-150, -50)
            self.x = random.randint(0, WIDTH - self.width)

    def draw(self):
        screen.blit(pothole_image, (self.x, self.y))

# Main game loop
def game_loop():
    global car_x, car_y, potholes, score

    # Game variables
    car_x = WIDTH // 2 - CAR_WIDTH // 2
    car_y = HEIGHT - CAR_HEIGHT - 10
    potholes = []
    score = 0
    game_over = False

    # Pothole generation timer
    pothole_timer = 0
    pothole_frequency = 30  # Every 30 frames, spawn a new pothole

    clock = pygame.time.Clock()

    while not game_over:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle car movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= CAR_SPEED
        if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
            car_x += CAR_SPEED

        # Generate potholes
        pothole_timer += 1
        if pothole_timer >= pothole_frequency:
            pothole_timer = 0
            potholes.append(Pothole(random.randint(0, WIDTH - POTHOLE_WIDTH), random.randint(-150, -50)))

        # Move potholes and check collision
        for pothole in potholes:
            pothole.move()
            pothole.draw()

            # Check for pixel-perfect collision
            offset_x = pothole.x - car_x
            offset_y = pothole.y - car_y
            if car_mask.overlap(pothole.mask, (offset_x, offset_y)):
                game_over = True

        # Draw car
        screen.blit(car_image, (car_x, car_y))

        # Update score
        score += 1
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Display Game Over screen
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()

            # Wait for restart key (R)
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            game_loop()
                            waiting_for_restart = False

        # Update the display
        pygame.display.flip()

# Start the game
reset_game()
game_loop()
