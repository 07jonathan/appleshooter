import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Warna yang sering digunakan
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot the Fruit")

# Kelas untuk menangani buah
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('apple.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # Ensure self.rect.width is less than SCREEN_WIDTH
        max_x = SCREEN_WIDTH - self.rect.width
        if max_x > 0:
            self.rect.x = random.randrange(max_x)
        else:
            self.rect.x = 0  # Fallback to 0 if width is too large

        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT + 10:
            # Reset position if fruit goes off screen
            max_x = SCREEN_WIDTH - self.rect.width
            if max_x > 0:
                self.rect.x = random.randrange(max_x)
            else:
                self.rect.x = 0  # Fallback to 0 if width is too large
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 5)


# Kelas untuk menangani peluru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Load gambar buah
fruit_img = pygame.image.load('apple.png').convert()
fruit_img.set_colorkey(BLACK)

# Inisialisasi grup sprite
all_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Membuat buah
for i in range(8):
    fruit = Fruit()
    all_sprites.add(fruit)
    fruits.add(fruit)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(*event.pos)
            all_sprites.add(bullet)
            bullets.add(bullet)

    # Update
    all_sprites.update()

    # Cek tabrakan antara peluru dan buah
    hits = pygame.sprite.groupcollide(fruits, bullets, True, True)
    for hit in hits:
        fruit = Fruit()
        all_sprites.add(fruit)
        fruits.add(fruit)

    # Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Delay
    pygame.time.delay(30)

pygame.quit()
sys.exit()
