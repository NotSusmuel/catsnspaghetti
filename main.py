import pygame
import sys
from pygame.locals import *

pygame.init()
vec=pygame.math.Vector2

HEIGHT=600
WIDTH=800
ACC=0.5
FRIC=-0.12
FPS=120

FramePerSec=pygame.time.Clock()

displaysurface=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.standing = pygame.transform.scale(pygame.image.load("textures/cat/cat1standing1.png"), (50, 50))
        self.walking1 = pygame.transform.scale(pygame.image.load("textures/cat/cat1walking1.png"), (50, 50))
        self.walking2 = pygame.transform.scale(pygame.image.load("textures/cat/cat1walking2.png"), (50, 50))
        
        self.images = [self.standing, self.walking1, self.standing, self.walking2]
        self.index = 0
        self.counter = 0

        self.surf = self.images[self.index]
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC 
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
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
        hits = pygame.sprite.spritecollide(P1 ,platforms, False)
        if P1.vel.y > 0:        
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
    
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.vel.y = -10

 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("textures/terrain/1.png")
        img = pygame.transform.scale(img, (50, 50))
        self.surf = pygame.Surface((WIDTH, img.get_height()))
        for x in range(0, WIDTH, img.get_width()):
            self.surf.blit(img, (x, 0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))


PT1=platform()
P1=Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)
 
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                P1.jump()
     
    displaysurface.fill((0,0,0))
 
    P1.move()
    P1.update()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
 
    pygame.display.update()
    FramePerSec.tick(FPS)