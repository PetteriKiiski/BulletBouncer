import pygame, sys, time, random
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((400, 660))
PlayerRight = pygame.image.load("MoveRight.png")
PlayerLeft = pygame.image.load("MoveLeft.png")
PaddleImg = pygame.image.load("Paddle.png")
class Player:
    #Defining some basic variables needed later
    def __init__(self):
        self.rect = pygame.Rect(0, 550, 23, 30)
        self.rect.bottom = 660
        self.imgs = [PlayerRight, PlayerLeft]
        self.img = self.imgs[0]
        self.movex = 0
        self.neg = 1
        self.jumpcount = 10
        self.jumping = False
    #next 3 functions for changing x position
    def right(self):
        if self.jumping:
            return
        self.movex = 6
        self.img = self.imgs[0]
    def left(self):
        if self.jumping:
            return
        self.movex = -6
        self.img = self.imgs[1]
    def stop(self):
        if self.jumping:
            return
        self.movex = 0
    #next 2 functions for changing y position
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
        if (self.rect.right >= 400 and self.movex == 6) or (self.rect.left <= 0 and self.movex == -6):
            self.movex = 0
        self.rect.right += self.movex 
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jumpcount = 10
    #displays player given the canvas
    def display(self, canvas):
        canvas.blit(self.img, self.rect)
class Bullet:
    pass
class Paddle:
    def __init__(self):
        self.img = PaddleImg
        xOptions = [-150, 410]
        option = random.choice(xOptions)
        self.movex = 0
        if option == -150:
            self.movex = 3
        else:
            self.movex = -3
        self.rect = pygame.Rect(random.choice(xOptions), random.randint(0, 615), 150, 15)
    def move(self):
            self.rect.right += self.movex
    def display(self, canvas):
        canvas.blit(self.img, self.rect)
class Paddles:
    def __init__(self):
        self.paddles = [Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle(), Paddle()]
    def move(self):
        for paddle in self.paddles:
            paddle.move()
    def display(self, canvas):
        for paddle in self.paddles:
            paddle.display(canvas)
class Lazer:
    pass
player = Player()
paddles = Paddles()
#MAIN LOOP
while True:
    #reset canvas and adjust
    canvas.fill((255, 255, 255))
    player.move()
    player.display(canvas)
    paddles.move()
    paddles.display(canvas)
    #react to events
    for event in pygame.event.get():
        #quit if requested
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #move around based on keys
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump()
            if event.key == K_RIGHT:
                player.right()
            if event.key == K_LEFT:
                player.left()
            if event.key == K_DOWN:
                player.stop()
    pygame.display.update()
    time.sleep(0.02)
