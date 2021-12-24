import pygame, sys, time
import RealJump as rj
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((400, 660))
PlayerRight = pygame.image.load("MoveRight.png")
PlayerLeft = pygame.image.load("MoveLeft.png")
class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 550, 23, 30)
        self.rect.bottom = 660
        self.imgs = [PlayerRight, PlayerLeft]
        self.img = self.imgs[0]
        self.movex = 0
        self.jumping = False
        self.jumpt = 0
        self.jumpVel = 0
    def right(self):
        self.movex = 5
        self.img = self.imgs[0]
    def left(self):
        self.movex = 5
        self.img = self.imgs[1]
    def move(self):
        if self.rect.right >= 660 and self.rect.left <= 0:
            self.rect.left += self.movex
        if self.jumping:
            oldrectbottom = self.rect.bottom
            move = rj.MoveY((time.time() - self.jumpt), -9.81, 0, self.jumpVel)
            self.rect.bottom += move[0]
            self.jumpVel = move[1]
            print (move)

#            print (self.rect.bottom)
            self.jumpt = time.time()
            if self.rect.bottom >= 660:
                self.jumpVel = 0
                self.jumping = False
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jumpt = time.time()
            self.jumpVel = -2
    def display(self, canvas):
        canvas.blit(self.img, self.rect)
class Bullet:
    pass
class Paddles:
    pass
class Lazer:
    pass
player = Player()
while True:
    canvas.fill((255, 255, 255))
    player.move()
    player.display(canvas)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
    pygame.display.update()
