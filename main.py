import pygame
import sys
import random
from math import *

pygame.init()
#the width and height of the screen
width = 700
height = 600

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("MyGame - Balloon Shooter Game") # name of the game
clock = pygame.time.Clock() #to keep track of time
#margin values
margin = 100
lowerBound = 100
#to keep track of the score
score = 0
#store the color and the intensity of each one
white = (240, 240, 240)        
lightBlue = (70, 130, 180)     
red = (255, 0, 0)            
pink = (255, 153, 153)   
darkGray = (52, 73, 94)       
darkBlue = (52, 152, 219)      
green = (0, 204, 0)         
yellow = (255, 255, 0)       
blue = (52, 144, 219)          
purple = (255, 0, 127)        
orange = (255, 128, 0)        

font = pygame.font.SysFont("Arial", 25)

class Balloon:
    def __init__(self, speed): #value of the speed
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90 #angle of the ballon
        self.speed = -speed #speed of the ballon
        self.proPool= [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue]) #list of colors 
#movement of the ballon
    def move(self):
        direct = random.choice(self.proPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()
#display the ballons on the screen 
    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a/2, self.y + self.b), (self.x + self.a/2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a/2 - 5, self.y + self.b - 3, 10, 10))
#check if the balloon is busted or not
    def burst(self):
        global score
        pos = pygame.mouse.get_pos() 
#if the mouse match with the balloon you get a point
        if isonBalloon(self.x, self.y, self.a, self.b, pos):
            score += 1 
            self.reset()
#reset balloons when thet are busted
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.006
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])

balloons = []
noBalloon = 10
for i in range(noBalloon):
    obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    balloons.append(obj)

def isonBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False
#location of the balloons
def pointer():
    pos = pygame.mouse.get_pos()
    r = 30
    l = 32
    color = pink
    for i in range(noBalloon):
        if isonBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)

def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))
#display the score
def showScore():
    scoreText = font.render("Balloons Bursted : " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 50))
#close the game
def close():
    pygame.quit() #deactivate the pygame library
    sys.exit() #close the program without creating any dialogue box
#keep track of events
def game():
    global score
    loop = True

    while loop:
        for event in pygame.event.get(): #to compare the events
            if event.type == pygame.QUIT: #if the user wants to quit
                close()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game()

            if event.type == pygame.MOUSEBUTTONDOWN: # if you try to bust the ballons 
                for i in range(noBalloon):
                    balloons[i].burst()

        display.fill(lightBlue) #fill color in the screen

        for i in range(noBalloon):
            balloons[i].show()

        pointer()

        for i in range(noBalloon):
            balloons[i].move()


        lowerPlatform() #display a rectangle
        showScore() #this will show the scores on that rectangles
        pygame.display.update()
        clock.tick(60)

game() #game function in order to start the game

    