import pygame
import sys
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 600
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60
TILE_SIZE = 50

FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

LEVEL_MAP = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

scroll = vec(0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.standing = pygame.transform.scale(pygame.image.load("textures/cat/cat1standing1.png"), (50, 50))
            self.walking1 = pygame.transform.scale(pygame.image.load("textures/cat/cat1walking1.png"), (50, 50))
            self.walking2 = pygame.transform.scale(pygame.image.load("textures/cat/cat1walking2.png"), (50, 50))
        except FileNotFoundError:
            self.standing = pygame.Surface((50, 50))
            self.standing.fill((255, 0, 0))
            self.walking1 = self.standing
            self.walking2 = self.standing

        self.images = [self.standing, self.walking1, self.standing, self.walking2]
        self.index = 0
        self.counter = 0
        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect()
        self.pos = vec((100, 300))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.midbottom = self.pos

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_d]:
            self.acc.x = ACC 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if abs(self.vel.x) > 0.2:
            self.counter += 1
            if self.counter >= 10:
                self.index = (self.index + 1) % len(self.images)
                self.surf = self.images[self.index]
                self.counter = 0
        else:
            self.surf = self.standing
            self.index = 0
    
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:        
            if hits:
                lowest_block = hits[0] 
                if self.pos.y < lowest_block.rect.bottom:      
                    self.pos.y = lowest_block.rect.top + 1
                    self.vel.y = 0
                    self.rect.midbottom = self.pos
    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -12

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type_id):
        super().__init__()
        self.type_id = type_id
        if self.type_id == 1:
            try:
                img = pygame.image.load("textures/terrain/1.png")
                self.surf = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            except FileNotFoundError:
                self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.surf.fill((0, 255, 0))
        else:
             self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
             self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)

platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
P1 = Player()
all_sprites.add(P1)

def load_level(level_data):
    platforms.empty()
    for s in all_sprites:
        if isinstance(s, Block):
            s.kill()
    for row_idx, row in enumerate(level_data):
        for col_idx, tile_id in enumerate(row):
            if tile_id != 0:
                b = Block(col_idx * TILE_SIZE, row_idx * TILE_SIZE, tile_id)
                platforms.add(b)
                all_sprites.add(b)

load_level(LEVEL_MAP)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                P1.jump()

    displaysurface.fill((0,0,0))
    P1.move()
    P1.update()

    target_x = P1.rect.centerx - WIDTH // 2
    target_y = P1.rect.centery - HEIGHT // 2
    scroll.x += (target_x - scroll.x) * 0.1
    scroll.y += (target_y - scroll.y) * 0.1

    for entity in all_sprites:
        displaysurface.blit(entity.surf, (entity.rect.x - scroll.x, entity.rect.y - scroll.y))

    pygame.display.update()
    FramePerSec.tick(FPS)
