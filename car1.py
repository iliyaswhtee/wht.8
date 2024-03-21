# import the modules
import pygame
import sys
from pygame.locals import *
import random
import time

# Initialize pygame
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Open the display screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  # Initialize the coin count

# Fonts that we need
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("C:\pp2 lab 8\sup.jpg")

# Set the display
DISPLAYSURF = pygame.display.set_mode((600, 800))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Traffic Race")


# We open classes for each features like coin, player or enemy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\pp2 lab 8\images.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 650)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.move_ip(-SPEED, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(SPEED, 0)
        if keys[K_UP]:
            self.rect.move_ip(0, -SPEED)
        if keys[K_DOWN]:
            self.rect.move_ip(0, SPEED)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\pp2 lab 8\kollil.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:\pp2 lab 8\lkjjj.png")  # Load the coin image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

P1 = Player()
E1 = Enemy()
C1 = Coin()  # Create a coin instance
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()  # Group for coins
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)  # Add the coin sprite to all_sprites

# Speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)  # Display the score
    coins_collected = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)  # Display collected coins
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_collected, (400, 10))  # Display collected coins in the top right corner

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

# This is sound if we collide with enemy car
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("C:\pp2 lab 8\katja-lel-mojj-marmeladnyjj.mp3").play()
        time.sleep(0)
        DISPLAYSURF.fill(GREEN)
        DISPLAYSURF.blit(game_over, (130, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    # Check for collision with coins
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1  # Increment the coin count
        for coin in coins:  # Reset the coin position
            coin.rect.top = 0
            coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    pygame.display.update()
    FramePerSec.tick(FPS)