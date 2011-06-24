import random, pygame

from math import *

class Colony(list):
    def __init__(self,c, n, x, y, w, h, r):
        
        self.food = 10
        self.color=c
        for i in range(n):
            self.append(Ant(self, x, y))
                             
        self.x = x	#X position
        self.y = y	#Y position
        self.w = w	#Screen Width
        self.h = h	#Screen Height
	self.r = r	#Max wander radius
        
    def draw(self, surface):	#Draw our "Hill"
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 12)
        pygame.draw.circle(surface, [0,0,0], (int(self.x), int(self.y)), 4)

class Food:
    def __init__(self, x, y, size):
        self.x = x		#X position
        self.y = y		#Y position
        self.size = size	#Size of food blob

    def draw(self, surface):	#Draw our foods
            pygame.draw.circle(surface, [0,150,0], (int(self.x), int(self.y)), int(self.size))

class Pheromone:
    
    def __init__(self, x, y, r):
        self.x = x		#X position
        self.y = y		#Y position
	self.r = r		#Heading
        self.strength = 1.0	#Streangth of signal
        
    def update(self, d=0.005):	#Degrade over time
        self.strength -= d

    def draw(self, surface):	#Draw using strength as color
	color =[self.strength*255,self.strength*255,self.strength*255]
	y=int(self.y+6*sin(radians(self.r)))
	x=int(self.x+6*cos(radians(self.r)))
        pygame.draw.circle(surface, color , (int(self.x),int(self.y)), 2)
        pygame.draw.line(surface, color, (int(self.x), int(self.y)),(x,y), 1)

class Ant:

    def __init__(self, colony, x, y):
    
        self.colony = colony
    
        self.x = x				#X position
        self.y = y				#Y position
	self.r = int(random.random()*359)	#Initial heading
	self.s = 2.0				#speed
        self.has_food = False			#Do I have food?
        self.wandering = 0			#How far have I wandered
    
    def near(self, obj, radius=10):	#Distance function

        d = (((obj.x-self.x)**2 ) + ((obj.y-self.y)**2))**0.5

        if d < radius:
		return True
        return False
        
    def heading(self, obj): #Set ant's heading twoards a destination
   
        dx = (obj.x-self.x) 
        dy = (obj.y-self.y) 

	angle_rad = atan2(dy,dx)
	self.r= degrees(angle_rad)
        
        self.wandering = 0

    
    def wander(self, d=10.0): 						#Ants must wander to find food.

        self.wandering+=5
        self.r+=((random.random() * d*2)-(d))				#Add random value to heading

        if self.x > self.colony.w: self.heading(self.colony)		#Dont leave the screen
        if self.x < 0: self.heading(self.colony)
        if self.y > self.colony.h: self.heading(self.colony)
        if self.y < 0: self.heading(self.colony)

	if self.wandering > self.colony.r: self.heading(self.colony)	#Dont wander past the wander limit
        if self.near(self.colony): self.wandering = 0
    
    def follow(self, trails):

        if self.has_food == False:	#If we dont have food and we find a trail, follow it!
            for pheromone in trails:
                if self.near(pheromone):
                    if random.random() < pheromone.strength: #Random chance to disregard the trail
                    	self.r=pheromone.r
    
    def harvest(self, foodsource):
        
        for food in foodsource:		#Get food if we find it
            if self.near(food, radius=food.size+2) and self.has_food == False: 
                food.size -= 1
                self.has_food = True
        
    def recall(self, trails, trail=0.08):
        
        if self.has_food:
            self.heading(self.colony)
            if random.random() < trail:
                trails.append(Pheromone(self.x, self.y, (self.r-180)))
        
        if self.near(self.colony) and self.has_food:	#Drop food and start wandering again
            self.has_food = False
            self.colony.food += 1
    
    def update(self, trails, foodsource, speed=3):
        
        self.follow(trails) 		#follow nearby trails to food.
        self.harvest(foodsource)	#harvest nearby food source
        self.recall(trails)		#bring food directly to colony
        self.wander()			#some random wandering is more efficient

        self.y += self.s*sin(radians(self.r))	#Move!
        self.x += self.s*cos(radians(self.r)) 
        
    def draw(self, surface):	#Draw our ant
	y=int(self.y+2*sin(radians(self.r)))
	x=int(self.x+2*cos(radians(self.r)))
        pygame.draw.line(surface, self.colony.color, (int(self.x), int(self.y)),(x,y), 2)


class Text:

    def __init__(self, color, size, pos, text):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft=pos

    def draw(self, surface):
		surface.blit(self.image,self.rect.topleft)
	

