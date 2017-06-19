import pygame, sys, random
from pygame.locals import *

windowWidth = 800
windowHeight = 800
gameWindowWidth = windowWidth/2
gameWindowHeight = windowHeight - 40
Scale = 40

pygame.init()

# Colour schemes
BLACK = (0, 0, 0)
GREY = (155, 155, 155)
GREEN = (0, 100, 0)
ORANGE = (200, 100, 0)
PURPLE = (100, 0, 100)

# This variable holds the Row numbers for later scoring system.
Row = []
for i in range(gameWindowHeight/Scale):
    Row.append([])

# some essential variables for the player and others
ROD = 60    # Rate of drop, slowly decreases each incremented level
DROPFAST = False
LEFT = False
RIGHT = False

# Setting the surfaces which to draw Objects onto
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
gameSpace = pygame.Surface((gameWindowWidth, gameWindowHeight))
mainClock = pygame.time.Clock()

# Setting up the object for tetris blocks
class block():
    def __init__(self):
        self.scale = gameWindowWidth/10
        self.x = self.scale * 5
        self.y = 0
        self.rect = pygame.Rect(0, 0, self.scale, self.scale)
        self.grounded = False

    def show(self):
        pygame.draw.rect(gameSpace, GREEN, self.rect)

    def update(self):
        self.rect.top = self.y
        self.rect.left = self.x

    def drop(self):
        #print self.grounded
        #if grounded:
            #return self.get_y
        if self.y + self.scale < gameWindowHeight and not self.grounded:
            self.y += self.scale
        else:
            return self.get_y()

    def get_y(self):
        return self.y/self.scale

    def get_x(self):
        return self.x/self.scale

    def Direction(self, LEFT, RIGHT):
        if LEFT and not self.grounded:
            self.x -= self.scale
        if RIGHT and not self.grounded:
            self.x += self.scale

    def setGrounded(self, grounded):
        self.grounded = grounded

activeBlock = block()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                print("spin 90")
            if event.key == K_DOWN or event.key == K_s:
                DROPFAST = True
            if event.key == K_LEFT or event.key == K_a:
                RIGHT = False
                LEFT = True
            if event.key == K_RIGHT or event.key == K_d:
                LEFT = False
                RIGHT = True
        if event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_s:
                DROPFAST = False

    blocksx = activeBlock.get_x()
    if RIGHT or LEFT:
        if blocksx <= 0:
            LEFT = False
        if blocksx >= gameWindowWidth/Scale - 1:
            RIGHT = False
        activeBlock.Direction(LEFT, RIGHT)
        LEFT = False
        RIGHT = False

    # This loop goes through each block that is sationary, compares with the active block('s) and grounds them
    for i in range(len(Row)):
        for x in range(len(Row[i])):
            checkColy = activeBlock.get_y()
            checkColx = activeBlock.get_x()
            if checkColy + 1 == Row[i][x].get_y() and checkColx == Row[i][x].get_x():
                activeBlock.setGrounded(True)


    if ROD >30 or DROPFAST:
        gety = activeBlock.drop()
        ROD = 0
        if gety:
            Row[gety].append(activeBlock)
            activeBlock = block()
    ROD += 1

    for r in range(len(Row)):
        if len(Row[r]) == 10:
            for x in range(-len(Row[r])+1, 1):
                Row[r].pop(-x)
            for y in range(len(Row)):
                for i in range(len(Row[y])):
                    Row[y][i].setGrounded(False)

    activeBlock.update()

    for y in range(len(Row)):
        for i in range(len(Row[y])):
            Row[y][i].drop()
            Row[y][i].show()
            Row[y][i].update()



    # The draw events for objects
    windowSurface.fill(ORANGE)
    gameSpace.fill(GREY)

    for i in range(len(Row)):
        for x in range(len(Row[i])):
            Row[i][x].show()

    activeBlock.show()

    windowSurface.blit(gameSpace, (20, 20))
    pygame.display.update()
    mainClock.tick(60)