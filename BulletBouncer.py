import pygame, sys, time
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
        self.neg = 1
        self.jumpcount = 10
        self.jumping = False
    def right(self):
        self.movex = 5
        self.img = self.imgs[0]
    def left(self):
        self.movex = -5
        self.img = self.imgs[1]
    def move(self):
        if self.jumping:
            if self.jumpcount >= -10:
                self.neg = 1
                if self.jumpcount < 0:
                    self.neg = -1
                self.rect.bottom -= int((self.jumpcount**2) * 0.25 * self.neg) #replace 0.5(default) for change in height that is desired.
                self.jumpcount -= 1
            else:
                self.jumping = False
                self.jumpcount = 10
        if (self.rect.right >= 400 and self.movex == 5) or (self.rect.left <= 0 and self.movex == -5):
            self.movex = 0
        self.rect.right += self.movex 
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
            if event.key == K_RIGHT:
                player.right()
            if event.key == K_LEFT:
                player.left()
    pygame.display.update()
    time.sleep(0.01)
