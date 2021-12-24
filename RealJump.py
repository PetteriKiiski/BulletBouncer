#Planet with PI gravity
import time, pygame, sys
from pygame.locals import *
pygame.init()
def Main():
	canvas = pygame.display.set_mode((500, 500))
	sticky = pygame.image.load("stickman-R1.gif")
	v = 0
	t = 0
	p_time = time.time()
	y = 0
	a = -3140
	x = 15
	xc = 1300
	line = []
	while True:
		t += (time.time() - p_time)
		p_time = time.time()
		canvas.fill((255, 255, 255))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					v += 1000
		print (y)
		y += v * t + 0.5 * a * t ** 2
		v += a * t
		print (y)
		print ("-------------------------------------------------------------")
		if y <= 0:
			v = 0
			y = 0
			t = 0
		if y >= y + a * t ** 2 + 0.5 * a * t ** 2:
			t = 0
		canvas.blit(sticky, (x, int(470 - y)))
		x += xc
		if x > 473:
			sticky = pygame.image.load("stickman-L1.gif")
			xc = -1300
		if x < 0:
			sticky = pygame.image.load("stickman-R1.gif")
			xc = 1300
		pygame.display.update()
def MoveY(t, a, y, v):
	y += v * t + 0.5 * a * t ** 2
	v += a * t
	return [y, v]
