import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
    def __init__(self, x, y, w, h, image_url):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_url = pygame.image.load(image_url)
    
    def isTile(self):
        return False
    
    def isLink(self):
        return False
    
    def isBoomerang(self):
        return False
    
    def isPot(self):
        return False 
    
    def draw(self, screen, roomPosX, roomPos):
          pass

class Tile(Sprite):
    def __init__(self, x, y, w, h, image_url):
         super().__init__(x, y, w, h, image_url)
         self.w = 50
         self.h = 50
         self.image = pygame.image.load(image_url)
         
    def update(self):
        return True

    def draw(self, screen, roomPosX, roomPosY):
        screen.blit(self.image,(self.x - roomPosX, self.y - roomPosY))

    def isTile(self):
        return True

class Link(Sprite):
    def __init__(self, x, y, w, h, image_url):
        super().__init__(x, y, w, h, image_url)
        self.w = 50
        self.h = 50
        self.direction = 0
        self.speed = 30
        self.prevX = 0
        self.prevY = 0
        self.speed = 8
        self.currentImage = 0
        self.MAX_IMAGES = 13
        self.images = []
        
        self.imageNum = 0

        for i in range(50):
            image = pygame.image.load("link_images/link" + str(i+1) + ".png")
            self.images.append(image)
        
    def updateImage(self, dir):
        self.direction = dir
        self.currentImage += 1
        if self.currentImage >= self.MAX_IMAGES:
            self.currentImage = 0
        if self.currentImage + self.direction * self.MAX_IMAGES >= 50:
            self.currentImage = 0

    def draw(self, screen, roomPosX, roomPosY):
        screen.blit(self.images[self.currentImage + self.direction * self.MAX_IMAGES], (self.x - roomPosX, self.y - roomPosY))

    def setPrevCoordinates(self):
        self.prevX = self.x
        self.prevY = self.y

    def leaveTile(self, t):
        if (self.x + self.w >= t.x) and (self.prevX + self.w <= t.x): #Left Collision
            self.x = t.x - self.w
        elif (self.x <= t.x + self.w) and (self.prevX >= t.x + t.w): #Right Collision
            self.x = t.x + t.w
        elif (self.y + self.h >= t.y) and (self.prevY + self.h <= t.y):#From top collision
            self.y = t.y - self.h
        elif (self.y <= t.x + t.h) and (self.prevY >= t.y + t.h): #bottom Collision
            self.y = t.y + t.h

    def update(self):
        return True

    def isLink(self):
        return True

    def toString(self):
        return "Link (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.width) + ", h = " + str(self.height)

class Boomerang(Sprite):
	def __init__(self, x, y, w, h, direction):
		super().__init__(x, y, w, h, "boomerang_images/boomerang1.png")
		self.w = 5
		self.h = 5
		self.dir = direction
		self.speed = 30
		self.images = []
		self.NUM_IMAGES = 4
		for i in range(self.NUM_IMAGES):
			image = pygame.image.load("boomerang_images/boomerang" + str(i+1) + ".png")
			self.images.append(image)
    
	def draw(self, g, roomPosX, roomPosY):
		g.blit(self.images[self.dir], (self.x - roomPosX, self.y - roomPosY))
        
	def toString(self):
		return "Boomerang (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.width) + ", h = " + str(self.height)
        
	def isBoomerang(self):
		return True
        
	def update(self):
		if self.dir == 0: #down
			self.y += self.speed
		if self.dir == 1: #left
			self.x -= self.speed
		if self.dir == 2: #right
			self.x += self.speed
		if self.dir == 3: #up
			self.y -= self.speed
		return True

class Pots(Sprite):
	goodPot = None
	badPot = None
	def __init__(self, x, y, w, h, image_url):
		super().__init__(x, y, w, h, image_url)
		self.w = 50
		self.h = 50
		self.speed = 30
		self.dir = -1
		self.isBroken = False
		self.timer = 5
		if Pots.goodPot == None:
			Pots.goodPot = pygame.image.load("pot.png")
		if Pots.badPot == None:
			Pots.badPot = pygame.image.load("pot_broken.png")

	def draw(self, g, roomPosX, roomPosY):
		if not self.isBroken:
			g.blit(Pots.goodPot, (self.x - roomPosX, self.y - roomPosY))
		else:
			g.blit(Pots.badPot, (self.x - roomPosX, self.y - roomPosY))

	def update(self):
		if self.isBroken:
			self.timer -= 1
		if self.timer == 0:
			return False

		if self.dir == 0 and not self.isBroken: #down
			self.y += self.speed
		if self.dir == 1 and not self.isBroken: #left
			self.x -= self.speed
		if self.dir == 2 and not self.isBroken: #right
			self.x += self.speed
		if self.dir == 3 and not self.isBroken: #up
			self.y -= self.speed

		return True

	def isPots(self):
		return True

	def __str__(self):
		return "Pots (x,y) = (" + str(self.x) + ", " + str(self.y) + "), w = " + str(self.w) + ", h = " + str(self.h)

class Model():
	def __init__(self):
		self.sprites = []
		self.sprites.append(Tile(0, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(200, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(300, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(400, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(450, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(250, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(650, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(600, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(550, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 200, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 300, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 350, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 450, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 500, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 600, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 650, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 700, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(200, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(250, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(300, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(400, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(450, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(550, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(600, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(650, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(700, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(800, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(900, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(950, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1000, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1150, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1100, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1200, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 950, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 700, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 650, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 600, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 500, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 450, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 350, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 200, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 300, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1350, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1200, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1150, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1000, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1100, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(950, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(900, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(800, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(700, 0, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1200, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 50, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1200, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1250, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1300, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(50, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(100, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(0, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(550, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(600, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(650, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 450, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 500, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(550, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(600, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(650, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(700, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(800, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 500, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(700, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(800, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(850, 450, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 350, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(200, 350, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(200, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 400, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(450, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(400, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(550, 100, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1150, 300, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1150, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1100, 300, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 200, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1100, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 200, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(800, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(750, 250, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(950, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(950, 700, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 700, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1000, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(900, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1050, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(950, 850, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(300, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(250, 700, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(450, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(250, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 750, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(400, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 800, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 900, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(350, 650, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(150, 550, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(500, 150, 50, 50, "tile.jpg"))
		self.sprites.append(Tile(1100, 200, 50, 50, "tile.jpg"))
		self.link = Link(300,100,50,50, "link_images/link1.png")
		self.sprites.append(self.link)
		self.sprites.append(Pots(200,200,50,50, "pot.png"))
		self.sprites.append(Pots(250,230,50,50, "pot.png"))
	
	def isColliding(self, a, b):
		if a.x + a.w < b.x:
			# print("colliding left")
			return False
		if a.x > b.x + b.w:
			# print("colliding right")
			return False
		if a.y + a.h < b.y:
			# print("colliding down")
			return False
		if a.y > b.y + b.h:
			# print("colliding up")
			return False
		return True

	def update(self):
		for sprite1 in self.sprites:
			if not sprite1.update():
				self.sprites.remove(sprite1)
				continue
				
			for sprite2 in self.sprites:
				if sprite1 == sprite2:
					continue
					
				if self.isColliding(sprite1, sprite2):
					if isinstance(sprite1, Link) and isinstance(sprite2, Tile):
						sprite1.leaveTile(sprite2)
						
					elif isinstance(sprite1, Boomerang) and isinstance(sprite2, Tile):
						self.sprites.remove(sprite1)
						
					elif isinstance(sprite1, Link) and isinstance(sprite2, Pots):
							sprite2.dir = sprite1.direction
						
					elif isinstance(sprite1, Pots) and isinstance(sprite2, Tile):
						sprite1.isBroken = True
						sprite1.dir = -1
						
					elif isinstance(sprite1, Boomerang) and isinstance(sprite2, Pots):
						sprite2.isBroken = True
						self.sprites.remove(sprite1)						
					break

	def throwBoomerang(self):
		boomerang = Boomerang(self.link.x, self.link.y, 10, 10, self.link.direction)
		self.sprites.append(boomerang)


class View():
	def __init__(self, model):
		screen_size = (700,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.posX = 0
		self.posY = 0
		self.model = model
		

	def update(self):
		self.screen.fill([0,200,100])
		for sprite in self.model.sprites:
			sprite.draw(self.screen, self.posX, self.posY)
		pygame.display.flip()
    
        

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			
		keys = pygame.key.get_pressed()
        
		self.model.link.setPrevCoordinates()
		self.x = 0
		self.y = 0
		if keys[K_RIGHT]:
			self.model.link.x += self.model.link.speed
			self.model.link.updateImage(2)
		if keys[K_LEFT]:
			self.model.link.x -= self.model.link.speed
			self.model.link.updateImage(1)
		if keys[K_UP]:
			self.model.link.y -= self.model.link.speed
			self.model.link.updateImage(3)
		if keys[K_DOWN]:
			self.model.link.y += self.model.link.speed
			self.model.link.updateImage(0)
		if keys[K_LCTRL]:
			self.model.throwBoomerang()
        
		if self.model.link.x > 700 and self.view.posX == 0:
			self.view.posX = 700
		if self.model.link.x < 700 and self.view.posX == 700:
			self.view.posX = 0
		if self.model.link.y > 500 and self.view.posY == 0:
			self.view.posY = 500
		if self.model.link.y < 500 and self.view.posY == 500:
			self.view.posY = 0

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")