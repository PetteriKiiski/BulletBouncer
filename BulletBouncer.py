import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
canvas = pygame.display.set_mode((400, 660))
pygame.display.set_caption("Bullet Bouncer")
LazerImg = pygame.image.load("Lazer.png")
BulletImg = pygame.image.load("Bullet.png")
PlayerRight = pygame.image.load("MoveRight.png")
PlayerLeft = pygame.image.load("MoveLeft.png")
PaddleImg = pygame.image.load("Paddle.png")
Boing = pygame.mixer.Sound("boing.wav")
LazerSound = pygame.mixer.Sound("lazer.wav")
class Player:
    #Defining some basic variables needed later
    def __init__(self):
        self.rect = pygame.Rect(0, 550, 23, 30)
        self.rect.bottom = 660
        self.imgs = [PlayerRight, PlayerLeft]
        self.img = self.imgs[0]
        self.movex = 0
        self.neg = 1
        self.falling = False
        self.jumpcount = 10
        self.jumping = False
        self.alt = True
    #next 3 functions for changing x position
    def alter(self):
        self.alt = not self.alt
        if self.movex != 0:
            self.movex /= abs(self.movex)
            self.movex *= 3 * (int(self.alt) + 1)
    def update(self):
        if self.rect.bottom < 660 and not self.falling:
            self.falling = True
    def right(self):
        if self.jumping:
            return
        self.movex = (int(self.alt) + 1) * 3
        self.img = self.imgs[0]
    def left(self):
        if self.jumping:
            return
        self.movex = (int(self.alt) + 1) * -3
        self.img = self.imgs[1]
    def on_paddles(self, paddles):
        for paddle in paddles.paddles:
            if self.rect.colliderect(paddle.rect) and self.rect.bottom >= paddle.rect.top and self.rect.bottom <= paddle.rect.bottom:
                return True
        return False
    def stop(self):
        if self.jumping:
            return
        self.movex = 0
    #next 2 functions for changing y position
    def move(self, paddles):
        if (self.rect.right >= 400 and self.movex > 0) or (self.rect.left <= 0 and self.movex < 0):
            self.movex = 0
        self.rect.right += self.movex        
        if self.jumping or self.falling:
            if not self.rect.bottom > 660:
                self.neg = 1
                if self.jumpcount < 0:
                    self.neg = -1
                    if self.on_paddles(paddles):
                        self.jumpcount = 0
                        self.jumping = False
                        self.falling = True
                        return
                self.rect.bottom -= int((self.jumpcount**2) * 0.25 * self.neg) #replace 0.5(default) for change in height that is desired.
                self.jumpcount -= 1
            else:
                self.rect.bottom = 660
                self.jumping = False
                self.falling = False
                self.jumpcount = 10
    def jump(self, paddles):
        if self.rect.bottom >= 660 or self.on_paddles(paddles):
            Boing.play()
            self.jumping = True
            self.jumpcount = 10
    #displays player given the canvas
    def display(self, canvas):
        canvas.blit(self.img, self.rect)
class Bullet:
    def __init__(self, x, y):
        self.img = BulletImg
        self.rect = pygame.Rect(x, y, 10, 10)
        self.counter = 0
        self.dist = 0
        self.xc = 0
        self.yc = 0
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.SPEED = 1
        self.AFTERSPEED = 3
    def move(self, player):
        x_delta = player.rect.centerx - self.x
        y_delta = player.rect.centery - self.y
        if self.counter < 50:
            self.counter += 1
            dist = math.sqrt(x_delta ** 2 + y_delta ** 2)
            self.x += x_delta * (self.SPEED / dist)
            self.y += y_delta * (self.SPEED / dist)
            self.rect.centerx = int(self.x)
            self.rect.centery = int(self.y)
            self.dist = dist
            self.xc = x_delta
            self.yc = y_delta
            return
        self.x += self.xc * (self.AFTERSPEED / self.dist)
        self.y += self.yc * (self.AFTERSPEED / self.dist)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
    def display(self, canvas):
        canvas.blit(self.img, self.rect)
class Bullets:
    def __init__(self):
        self.bullets = [Bullet(0, 330), Bullet(360, 330), Bullet(200, 0), Bullet(200, 610)]
    def move(self, player):
        for bullet in self.bullets:
            bullet.move(player)
    def display(self, canvas):
        for bullet in self.bullets:
            bullet.display(canvas)
    def update(self):
        counter = 0
        for bullet in self.bullets:
            if bullet.rect.left > 400 or bullet.rect.right < 0 or bullet.rect.top > 660 or bullet.rect.bottom < 0:
                counter += 1
        if counter == len(self.bullets):
            self.bullets = [Bullet(0, 330), Bullet(360, 330), Bullet(200, 0), Bullet(200, 610)]           
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
        self.paddles = []
        for i in range(20):
            self.paddles += [Paddle()]
    def update(self):
        counter = 0
        for paddle in self.paddles:
            if paddle.rect.left > 400 and paddle.movex == 3:
                counter += 1
            if paddle.rect.right < 0 and paddle.movex == -3:
                counter += 1
        if counter == len(self.paddles):
            print ("yupadoodle")
            self.paddles = []
            for i in range(20):
                self.paddles += [Paddle()]
    def move(self):
        for paddle in self.paddles:
            paddle.move()
    def display(self, canvas):
        for paddle in self.paddles:
            paddle.display(canvas)
class Lazer:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 500, 30)
        self.img = LazerImg
        self.launching = False
        self.launch_t = time.time()
        self.wait_t = time.time()
    def update(self, player):
        if not self.launching:
            if time.time() - self.wait_t >= 5:
                LazerSound.play(maxtime=5000)
                self.launching = True
                self.launch_t = time.time()
        else:
            if time.time() - self.launch_t >= 5:
                self.launching = False
                self.wait_t = time.time()
                self.rect.top = player.rect.top
    def display(self, canvas):
        if self.launching:
            canvas.blit(self.img, self.rect)
player = Player()
paddles = Paddles()
lazer = Lazer()
bullets = Bullets()
#MAIN LOOP
while True:
    #reset canvas and adjust
    canvas.fill((255, 255, 255))
    player.move(paddles)
    player.display(canvas)
    player.update()
    paddles.update()
    paddles.move()
    paddles.display(canvas)
    lazer.update(player)
    lazer.display(canvas)
    bullets.update()
    bullets.move(player)
    bullets.display(canvas)
    dead = False
    for bullet in bullets.bullets:
        if bullet.rect.colliderect(player.rect):
            dead = True
    if dead or (player.rect.colliderect(lazer.rect) and lazer.launching):
        lazer.update(player)
        lazer.display(canvas)
        pygame.mixer.fadeout(3000)
        while True:
            print ("You LOSE >:)")
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.display.update()
    #react to events
    for event in pygame.event.get():
        #quit if requested
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #move around based on keys
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.jump(paddles)
                if player.falling:
                    player.falling = False
            if event.key == K_RIGHT:
                player.right()
            if event.key == K_LEFT:
                player.left()
            if event.key == K_DOWN:
                player.stop()
        #ALTer the player speed
            if event.key in [K_RALT, K_LALT]:
                player.alter()
    pygame.display.update()
    time.sleep(0.02)
