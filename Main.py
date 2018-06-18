#! IMPORTANT
# The player having 1 frame to move the center block
# by updating the Shape before letting it get "groudned" a variable within the shapes/blocks
# still needs further testing to see if the issue has been completly resolved.
#
# The player could move the object into the wall, causing the shape to return near the screen.
# to counter act this, I've added a if statement within several parts of the rotate function,
# not allowing it to rotate if there is the wall and a object that is thinner than the total width
# of the shape.

import pygame, sys, random, time
from pygame.locals import *

windowWidth = 800
windowHeight = 800
gameWindowWidth = windowWidth/2
gameWindowHeight = windowHeight - 40
Scale = int(gameWindowWidth/10)

pygame.init()

# Colour schemes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
GREEN = (0, 100, 0)
ORANGE = (200, 100, 0)
BLUE = (0, 0, 100)
PURPLE = (100, 0, 100)
YELLOW = (100, 100, 0)
RED = (255, 0, 0)

# This variable holds the Row numbers for later scoring system.
Row = []
for i in range(int(gameWindowHeight/Scale)):
    Row.append([])

# some essential variables for the player and others
playing = False
pause = False
displayNext = True

ROD = 30    # Rate of drop, slowly decreases each incremented level
RODcounter = 0
lvl = 0
score = 0
Turn = True
DROPFAST = False
LEFT = False
RIGHT = False
ROTATE = False
currentShape = random.randint(0, 4) # generates an number which will be associated with a shape.
#0 = Triangle
#1 = Square
#2 = L
#3 = reverse L
#4 = Line

# Set up the fonts
font = pygame.font.SysFont('Arial', int(windowWidth/15))

#<editor-fold desc="Game Font">
lvlFont = font.render("Level: " + str(lvl), False, WHITE, BLACK)
lvlRect = lvlFont.get_rect()
lvlRect.top = windowHeight/10 + Scale
lvlRect.left = windowWidth - Scale * 9

scoreFont = font.render("Score: " + str(score), False, WHITE, BLACK)
scoreRect = scoreFont.get_rect()
scoreRect.top = int(windowHeight/10) + Scale * 3
scoreRect.left = windowWidth - Scale * 9
#</editor-fold>

#<editor-fold desc="Start Screen font">
tFont = pygame.font.SysFont('Arial', int(windowWidth/7))
titleFont = tFont.render("Python Tetris", False, (0,0,255),ORANGE)
titleRect = titleFont.get_rect()
titleRect.top = Scale*6
titleRect.centerx = windowWidth/2

buttonFont = font.render("Press 'Space' to start the game", False, (0,0,255),ORANGE)
buttonRect = buttonFont.get_rect()
buttonRect.top = titleRect.bottom
buttonRect.centerx = windowWidth/2
#</editor-fold>

#<editor-fold desc="Instructions font">
insFont = pygame.font.SysFont('Arial', int(windowWidth/Scale))
instFont = []
instRect = []
instFont.append(insFont.render("                    How to play                     ", False, WHITE,  BLACK))
instFont.append(insFont.render("Press W or up key to rotate shape        ", False, WHITE, BLACK))
instFont.append(insFont.render("Press A or left to move shape left          ", False, WHITE, BLACK))
instFont.append(insFont.render("Press D or right key to move shape right", False, WHITE, BLACK))
instFont.append(insFont.render("Press S or down key to go down quicker", False, WHITE, BLACK))
instFont.append(insFont.render("Press P to Pause the game                   ", False, WHITE, BLACK))
instFont.append(insFont.render("Press shift to toggle display next Shape ", False, WHITE, BLACK))

for i in range(len(instFont)):
    instRect.append(instFont[i].get_rect())
    instRect[i].top = windowHeight/3 + Scale/2 * (11 + i) + i*4 + Scale
    instRect[i].left = windowWidth - Scale * 9
    instRect[i].width = 400
#</editor-fold>

#<editor-fold desc="Pause font">
pauseFont = font.render("PAUSED", False, WHITE)
pauseRect = pauseFont.get_rect()
pauseRect.top = gameWindowHeight/2 - Scale*6
pauseRect.centerx = gameWindowWidth/2

pFont = pygame.font.SysFont('Arial', Scale)
pauseinstFont = pFont.render("Press 'P' to resume", False, WHITE)
pauseinstRect = pauseFont.get_rect()
pauseinstRect.top = gameWindowHeight/2 - Scale*2
pauseinstRect.left = Scale
#</editor-fold>

# Setting the surfaces which to draw Objects to
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Python Tetris")
gameSpace = pygame.Surface((gameWindowWidth, gameWindowHeight))
pauseSurf = pygame.Surface((gameWindowWidth, gameWindowHeight))
pauseSurf.set_alpha(100)
nextShapeSurf = pygame.Surface((Scale*5, Scale*6))
mainClock = pygame.time.Clock()

# the structor of the shapes
class block():
    def __init__(self, colour):
        self.scale = Scale
        self.x = self.scale * 5
        self.y = self.scale
        self.rect = pygame.Rect(0, 0, self.scale, self.scale)
        self.colourRect = pygame.Rect(0, 0, self.scale-self.scale/5, self.scale-self.scale/5)
        self.grounded = False
        self.colour = colour

    def show(self, display=False):
        if display:
            pygame.draw.rect(nextShapeSurf, BLACK, self.rect)
            pygame.draw.rect(nextShapeSurf, self.colour, self.colourRect)
        else:
            pygame.draw.rect(gameSpace, BLACK, self.rect)
            pygame.draw.rect(gameSpace, self.colour, self.colourRect)

    def update(self):
        self.rect.top = self.y
        self.rect.left = self.x
        self.colourRect.top = self.rect.top + (self.scale/10)
        self.colourRect.left = self.rect.left + (self.scale / 10)

    def drop(self):
        if self.y + self.scale < gameWindowHeight and not self.grounded:
            self.y += self.scale
        else:
            return self.get_y()

    def get_y(self):
        return self.y/self.scale

    def set_y(self, y):
        self.y = y * self.scale

    def get_x(self):
        return self.x/self.scale

    def set_x(self, x):
        self.x = x * self.scale

    def Direction(self, LEFT, RIGHT):
        if LEFT and not self.grounded:
            self.x -= self.scale
        if RIGHT and not self.grounded:
            self.x += self.scale

    def setGrounded(self, grounded):
        self.grounded = grounded

# properties for the triangle shape
class triangleBlock():
    def __init__(self):
        self.Blocks = [block(GREEN), block(GREEN), block(GREEN), block(GREEN)]
        self.Blocks[0].set_x((int(gameWindowWidth/Scale)) / 2)
        self.orientation = 0
        self.grounded = False

    def update(self):
        if not self.grounded:
            if self.orientation == 0:
                self.Blocks[1].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() - 1)
            if self.orientation == 1:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[3].set_y(self.Blocks[0].get_y())
            if self.orientation == 2:
                self.Blocks[1].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() + 1)
            if self.orientation == 3:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[3].set_y(self.Blocks[0].get_y())

        for boxes in self.Blocks:
            boxes.update()

    def show(self, display=False):
        for boxes in self.Blocks:
            if display:
                self.Blocks[0].set_x(2)
                self.Blocks[0].set_y(3)
                self.update()
            boxes.show(display)
            #print boxes.get_x()

    def drop(self):
        #if self.get_bottom() + 1 == int(gameWindowHeight/Scale):
            #self.set_grounded("Drop event")
            #return True
        #else:
        return self.Blocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.Blocks)):
            #print self.Blocks[i].get_y()
            Row[int(self.Blocks[i].get_y())].append(self.Blocks[i])
            self.Blocks[i].setGrounded(True)
        #print len(Row[17])

    def Direction(self, LEFT, RIGHT):
        self.Blocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_orientation(self):
        return self.orientation, "triangle"

    def get_left(self):
        if self.orientation == 0:
            return self.Blocks[1].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[3].get_x()
        if self.orientation == 3:
            return self.Blocks[0].get_x()

    def get_right(self):
        if self.orientation == 0:
            return self.Blocks[2].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[3].get_x()
        if self.orientation == 3:
            return self.Blocks[2].get_x()

    def get_top(self):
        if self.orientation == 0:
            return self.Blocks[3].get_y()
        if self.orientation == 1:
            return self.Blocks[1].get_y()
        if self.orientation == 2:
            return self.Blocks[0].get_y()
        if self.orientation == 3:
            return self.Blocks[2].get_y()

    def get_bottom(self):
        if self.orientation == 0:
            return self.Blocks[0].get_y()
        if self.orientation == 1:
            return self.Blocks[2].get_y()
        if self.orientation == 2:
            return self.Blocks[3].get_y()
        if self.orientation == 3:
            return self.Blocks[1].get_y()

    def get_middley(self):
        return self.Blocks[0].get_y()

    def get_middlex(self):
        return self.Blocks[0].get_x()

    def get_tooth(self):
        if self.orientation == 0:
            return False
        if self.orientation == 1:
            return [self.Blocks[3].get_x(), self.Blocks[3].get_y(), 1, 'Triangle']
        if self.orientation == 2:
            return [self.Blocks[2].get_x(), self.Blocks[0].get_y(), self.Blocks[1].get_x(), 2, 'Triangle']
        if self.orientation == 3:
            return [self.Blocks[3].get_x(), self.Blocks[3].get_y(), 3, 'Triangle']

    def get_grounded(self):
        return self.grounded

# properties for the L shape
class LBlock():
    def __init__(self):
        self.Blocks = [block(RED), block(RED), block(RED), block(RED)]
        self.Blocks[0].set_x((int(gameWindowWidth/Scale)) / 2)
        self.orientation = 0
        self.grounded = False

    def update(self):
        if not self.grounded:
            if self.orientation == 0:
                self.Blocks[1].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() - 2)
            if self.orientation == 1:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() + 2)
                self.Blocks[3].set_y(self.Blocks[0].get_y())
            if self.orientation == 2:
                self.Blocks[1].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() + 2)
            if self.orientation == 3:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() - 2)
                self.Blocks[3].set_y(self.Blocks[0].get_y())

        for boxes in self.Blocks:
            boxes.update()

    def show(self, display=False):
        for boxes in self.Blocks:
            if display:
                self.Blocks[0].set_x(2)
                self.Blocks[0].set_y(3.5)
                self.update()
            boxes.show(display)

    def drop(self):
        return self.Blocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.Blocks)):
            Row[int(self.Blocks[i].get_y())].append(self.Blocks[i])
            self.Blocks[i].setGrounded(True)

    def Direction(self, LEFT, RIGHT):
        self.Blocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_orientation(self):
        return self.orientation, "line"

    def get_left(self):
        if self.orientation == 0:
            return self.Blocks[0].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[0].get_x()
        if self.orientation == 3:
            return self.Blocks[3].get_x()

    def get_right(self):
        if self.orientation == 0:
            return self.Blocks[1].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[0].get_x()
        if self.orientation == 3:
            return self.Blocks[0].get_x()

    def get_top(self):
        if self.orientation == 0:
            return self.Blocks[3].get_y()
        if self.orientation == 1:
            return self.Blocks[0].get_y()
        if self.orientation == 2:
            return self.Blocks[0].get_y()
        if self.orientation == 3:
            return self.Blocks[1].get_y()

    def get_bottom(self):
        if self.orientation == 0:
            return self.Blocks[0].get_y()
        if self.orientation == 1:
            return self.Blocks[1].get_y()
        if self.orientation == 2:
            return self.Blocks[3].get_y()
        if self.orientation == 3:
            return self.Blocks[0].get_y()

    def get_middley(self):
        return self.Blocks[0].get_y()

    def get_middlex(self):
        return self.Blocks[0].get_x()

    def get_tooth(self):
        if self.orientation == 0:
            return False
        if self.orientation == 1:
            return [self.Blocks[3].get_x(), self.Blocks[3].get_y(), 1, 'L']
        if self.orientation == 2:
            return [self.Blocks[1].get_x(), self.Blocks[1].get_y(), 2, 'L']
        if self.orientation == 3:
            return False

    def get_grounded(self):
        return self.grounded

# properties for the reverseL shape
class reverseLBlock():
    def __init__(self):
        self.Blocks = [block(BLUE), block(BLUE), block(BLUE), block(BLUE)]
        self.Blocks[0].set_x((int(gameWindowWidth/Scale)) / 2)
        self.orientation = 0
        self.grounded = False

    def update(self):
        if not self.grounded:
            if self.orientation == 0:
                self.Blocks[1].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() - 2)
            if self.orientation == 1:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() + 2)
                self.Blocks[3].set_y(self.Blocks[0].get_y())
            if self.orientation == 2:
                self.Blocks[1].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() + 2)
            if self.orientation == 3:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() - 2)
                self.Blocks[3].set_y(self.Blocks[0].get_y())

        for boxes in self.Blocks:
            boxes.update()

    def show(self, display=False):
        for boxes in self.Blocks:
            if display:
                self.Blocks[0].set_x(2)
                self.Blocks[0].set_y(3.5)
                self.update()
            boxes.show(display)

    def drop(self):
        return self.Blocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.Blocks)):
            Row[int(self.Blocks[i].get_y())].append(self.Blocks[i])
            self.Blocks[i].setGrounded(True)

    def Direction(self, LEFT, RIGHT):
        self.Blocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_orientation(self):
        return self.orientation, "reverseL"

    def get_left(self):
        if self.orientation == 0:
            return self.Blocks[1].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[3].get_x()
        if self.orientation == 3:
            return self.Blocks[0].get_x()

    def get_right(self):
        if self.orientation == 0:
            return self.Blocks[0].get_x()
        if self.orientation == 1:
            return self.Blocks[3].get_x()
        if self.orientation == 2:
            return self.Blocks[0].get_x()
        if self.orientation == 3:
            return self.Blocks[0].get_x()

    def get_top(self):
        if self.orientation == 0:
            return self.Blocks[3].get_y()
        if self.orientation == 1:
            return self.Blocks[0].get_y()
        if self.orientation == 2:
            return self.Blocks[0].get_y()
        if self.orientation == 3:
            return self.Blocks[1].get_y()

    def get_bottom(self):
        if self.orientation == 0:
            return self.Blocks[0].get_y()
        if self.orientation == 1:
            return self.Blocks[0].get_y()
        if self.orientation == 2:
            return self.Blocks[3].get_y()
        if self.orientation == 3:
            return self.Blocks[1].get_y()

    def get_middley(self):
        return self.Blocks[0].get_y()

    def get_middlex(self):
        return self.Blocks[0].get_x()

    def get_tooth(self):
        if self.orientation == 0:
            return False
        if self.orientation == 1:
            return False
        if self.orientation == 2:
            return [self.Blocks[1].get_x(), self.Blocks[1].get_y(), 2, 'reverseL']
        if self.orientation == 3:
            return [self.Blocks[3].get_x(), self.Blocks[3].get_y(), 3, 'reverseL']

    def get_grounded(self):
        return self.grounded

# properties for the square shape
class squareBlock():
    def __init__(self):
        self.Blocks = [block(YELLOW), block(YELLOW), block(YELLOW), block(YELLOW)]
        self.Blocks[0].set_x((int(gameWindowWidth/Scale)) / 2)
        self.orientation = 0
        self.grounded = False

    def update(self):
        if not self.grounded:
            self.Blocks[1].set_x(self.Blocks[0].get_x() + 1)
            self.Blocks[1].set_y(self.Blocks[0].get_y())
            self.Blocks[2].set_x(self.Blocks[0].get_x())
            self.Blocks[2].set_y(self.Blocks[0].get_y() + 1)
            self.Blocks[3].set_x(self.Blocks[0].get_x() + 1)
            self.Blocks[3].set_y(self.Blocks[0].get_y() + 1)

        for boxes in self.Blocks:
            boxes.update()

    def show(self, display=False):
        for boxes in self.Blocks:
            if display:
                self.Blocks[0].set_x(1.5)
                self.Blocks[0].set_y(2)
                self.update()
            boxes.show(display)

    def drop(self):
        return self.Blocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.Blocks)):
            Row[int(self.Blocks[i].get_y())].append(self.Blocks[i])
            self.Blocks[i].setGrounded(True)

    def Direction(self, LEFT, RIGHT):
        self.Blocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_orientation(self):
        return self.orientation, "Square"

    def get_left(self):
        return self.Blocks[0].get_x()


    def get_right(self):
        return self.Blocks[1].get_x()

    def get_top(self):
        return self.Blocks[0].get_y()

    def get_bottom(self):
        return self.Blocks[3].get_y()

    def get_middley(self):
        return self.Blocks[0].get_y()

    def get_middlex(self):
        return self.Blocks[0].get_x()

    def get_tooth(self):
        return False

    def get_grounded(self):
        return self.grounded

# properties for the line shape
class lineBlock():
    def __init__(self):
        self.Blocks = [block(PURPLE), block(PURPLE), block(PURPLE), block(PURPLE)]
        self.Blocks[0].set_x((int(gameWindowWidth/Scale)) / 2)
        self.orientation = 0
        self.grounded = False


    def update(self):
        if not self.grounded:
            if self.orientation == 0:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() - 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() - 2)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() - 3)
            if self.orientation == 1:
                self.Blocks[1].set_x(self.Blocks[0].get_x() + 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x() + 2)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() + 3)
                self.Blocks[3].set_y(self.Blocks[0].get_y())
            if self.orientation == 2:
                self.Blocks[1].set_x(self.Blocks[0].get_x())
                self.Blocks[1].set_y(self.Blocks[0].get_y() + 1)
                self.Blocks[2].set_x(self.Blocks[0].get_x())
                self.Blocks[2].set_y(self.Blocks[0].get_y() + 2)
                self.Blocks[3].set_x(self.Blocks[0].get_x())
                self.Blocks[3].set_y(self.Blocks[0].get_y() + 3)
            if self.orientation == 3:
                self.Blocks[1].set_x(self.Blocks[0].get_x() - 1)
                self.Blocks[1].set_y(self.Blocks[0].get_y())
                self.Blocks[2].set_x(self.Blocks[0].get_x() - 2)
                self.Blocks[2].set_y(self.Blocks[0].get_y())
                self.Blocks[3].set_x(self.Blocks[0].get_x() - 3)
                self.Blocks[3].set_y(self.Blocks[0].get_y())

        for boxes in self.Blocks:
            boxes.update()

    def show(self, display=False):
        for boxes in self.Blocks:
            if display:
                self.Blocks[0].set_x(2)
                self.Blocks[0].set_y(4)
                self.update()
            boxes.show(display)

    def drop(self):
        return self.Blocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.Blocks)):
            Row[int(self.Blocks[i].get_y())].append(self.Blocks[i])
            self.Blocks[i].setGrounded(True)

    def Direction(self, LEFT, RIGHT):
        self.Blocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_orientation(self):
        return self.orientation, "line"

    def get_left(self):
        if self.orientation == 0:
            return self.Blocks[0].get_x()
        if self.orientation == 1:
            return self.Blocks[0].get_x()
        if self.orientation == 2:
            return self.Blocks[0].get_x()
        if self.orientation == 3:
            return self.Blocks[3].get_x()

    def get_right(self):
        if self.orientation == 0:
            return self.Blocks[0].get_x()
        if self.orientation == 1:
            return self.Blocks[3].get_x()
        if self.orientation == 2:
            return self.Blocks[0].get_x()
        if self.orientation == 3:
            return self.Blocks[0].get_x()

    def get_top(self):
        if self.orientation == 0:
            return self.Blocks[3].get_y()
        if self.orientation == 1:
            return self.Blocks[0].get_y()
        if self.orientation == 2:
            return self.Blocks[0].get_y()
        if self.orientation == 3:
            return self.Blocks[0].get_y()

    def get_bottom(self):
        if self.orientation == 0:
            return self.Blocks[0].get_y()
        if self.orientation == 1:
            return self.Blocks[0].get_y()
        if self.orientation == 2:
            return self.Blocks[3].get_y()
        if self.orientation == 3:
            return self.Blocks[0].get_y()

    def get_middley(self):
        return self.Blocks[0].get_y()

    def get_middlex(self):
        return self.Blocks[0].get_x()

    def get_tooth(self):
        return False

    def get_grounded(self):
        return self.grounded

def nextShape():
    global currentShape, activeShape

    if currentShape == 0:
        activeShape = triangleBlock()
    if currentShape == 1:
        activeShape = squareBlock()
    if currentShape == 2:
        activeShape = LBlock()
    if currentShape == 3:
        activeShape = reverseLBlock()
    if currentShape == 4:
        activeShape = lineBlock()
    currentShape = random.randint(0, 4)

nextShape()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w and playing:
                ROTATE = True
            if event.key == K_DOWN or event.key == K_s and playing:
                DROPFAST = True
            if event.key == K_LEFT or event.key == K_a and playing:
                RIGHT = False
                LEFT = True
            if event.key == K_RIGHT or event.key == K_d and playing:
                LEFT = False
                RIGHT = True
            if event.key == K_SPACE:
                playing = True
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                displayNext = not displayNext
            if event.key == K_p:
                pause = not pause

        if event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_s:
                DROPFAST = False

    if playing:
        if not pause:
            # This variable keeps the blocks within the game space. accepting the tooth as an extension of the shape
            blocksTooth = activeShape.get_tooth()
            if blocksTooth:
                if blocksTooth[len(blocksTooth)-1] == 'Triangle':
                    if len(blocksTooth) > 4:
                        blocksLx = blocksTooth[0]
                        blocksRx = blocksTooth[2]
                    else:
                        if blocksTooth[2] == 1:
                            blocksLx = activeShape.get_left()
                            blocksRx = blocksTooth[0]
                        if blocksTooth[2] == 3:
                            blocksRx = activeShape.get_right()
                            blocksLx = blocksTooth[0]

                if blocksTooth[len(blocksTooth)-1] == "L":
                    if blocksTooth[2] == 1:
                        blocksLx = activeShape.get_left()
                        blocksRx = blocksTooth[0]
                    if blocksTooth[2] == 2:
                        blocksRx = activeShape.get_right()
                        blocksLx = blocksTooth[0]
                if blocksTooth[len(blocksTooth)-1] == "reverseL":
                    if blocksTooth[2] == 3:
                        blocksLx = blocksTooth[0]
                        blocksRx = activeShape.get_right()
                    if blocksTooth[2] == 2:
                        blocksRx = blocksTooth[0]
                        blocksLx = activeShape.get_right()
            else:
                blocksLx = activeShape.get_left()
                blocksRx = activeShape.get_right()

            #If the player tries to clip out of game space it pushes them back in.
            if blocksLx < 0:
                activeShape.Direction(False, True)
            if blocksRx > gameWindowWidth / Scale - 1:
                activeShape.Direction(True, False)

            # this controls the shape to not intersect with the blocks that have been grounded.
            for y in range(len(Row)):
                for x in range(len(Row[y])):
                    checkColx = Row[y][x].get_x()
                    checkColy = Row[y][x].get_y()
                    if blocksTooth:
                        if blocksTooth[len(blocksTooth)-1] == "Triangle":
                            if activeShape.get_top() == checkColy and blocksTooth[3] == 2:
                                if blocksLx - 1 == checkColx:
                                    LEFT = False
                                if blocksRx + 1 == checkColx:
                                    RIGHT = False
                            elif activeShape.get_middley() == checkColy and (blocksTooth[2] == 1 or blocksTooth[2] == 3):
                                if blocksLx - 1 == checkColx:
                                    LEFT = False
                                if blocksRx + 1 == checkColx:
                                    RIGHT = False
                        if blocksTooth[len(blocksTooth) - 1] == "L":
                            if activeShape.get_middley() == checkColy and blocksTooth[2] == 1:
                                if blocksLx - 1 == checkColx:
                                    LEFT = False
                                if blocksRx + 1 == checkColx:
                                    RIGHT = False
                            elif activeShape.get_middley() == checkColy and blocksTooth[2] == 2:
                                if blocksLx - 2 == checkColx:
                                    LEFT = False
                                if blocksRx + 1 == checkColx:
                                    RIGHT = False
                        if blocksTooth[len(blocksTooth) - 1] == "reverseL":
                            if activeShape.get_middley() == checkColy and blocksTooth[2] == 3:
                                if blocksLx - 1 == checkColx:
                                    LEFT = False
                                if blocksRx + 1 == checkColx:
                                    RIGHT = False
                            elif activeShape.get_middley() == checkColy and blocksTooth[2] == 2:
                                if blocksLx - 1 == checkColx:
                                    LEFT = False
                                if blocksRx + 2 == checkColx:
                                    RIGHT = False
                        if activeShape.get_left() - 1 == checkColx and activeShape.get_middley() == checkColy:
                            LEFT = False
                        if activeShape.get_right() + 1 == checkColx and activeShape.get_middley() == checkColy:
                            RIGHT = False
                    else:
                        if activeShape.get_left() - 1 == checkColx:
                            for i in range(int(activeShape.get_top()), int(activeShape.get_bottom())):
                                if i == checkColy:
                                    LEFT = False
                        if activeShape.get_right() + 1 == checkColx:
                            for i in range(int(activeShape.get_top()), int(activeShape.get_bottom())):
                                if i == checkColy:
                                    RIGHT = False
                    if activeShape.get_left() - 1 == checkColx and activeShape.get_middley() == checkColy:
                            LEFT = False
                    if activeShape.get_right() + 1 == checkColx and activeShape.get_middley() == checkColy:
                            RIGHT = False


            #Move the Shape left or right within limits
            if RIGHT or LEFT and not activeShape.get_grounded():
                if blocksLx <= 0:
                    LEFT = False
                if blocksRx >= int(gameWindowWidth/Scale) - 1:
                    RIGHT = False

                activeShape.Direction(LEFT, RIGHT)
                LEFT = False
                RIGHT = False
            activeShape.update()

            # Rotate the current shape,
            if ROTATE:
                orientation = activeShape.get_orientation()
                #Rules for the rotation, stops the shape rotating into another shape.
                for y in range((len(Row))):
                    for x in range((len(Row[y]))):
                        if orientation[1] == 'line':
                            for l in range(1,4):
                                if orientation[0] == 0:
                                    if activeShape.get_middlex() + l == windowWidth and activeShape.get_middlex() - l == Row[y][x].get_x():
                                        Turn = False
                                    if activeShape.get_middlex() + l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                if orientation[0] == 1:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + l == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middley() >= windowHeight/Scale - 4:
                                        Turn = False
                                if orientation[0] == 2:
                                    if activeShape.get_middlex() - l == 0 and activeShape.get_middlex() + l == Row[y][x].get_x():
                                        Turn = False
                                    if activeShape.get_middlex() - l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                if orientation[0] == 3:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - l == Row[y][x].get_y():
                                        Turn = False
                        for l in range(1,3):
                            if orientation[1] == 'L':
                                if orientation[0] == 0:
                                    if activeShape.get_middlex() + l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + 1 == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middley()+ 1 > windowHeight/Scale:
                                        Turn = False
                                    if activeShape.get_middlex() + l == windowWidth and activeShape.get_middlex() - l == Row[y][x].get_x():
                                        Turn = False
                                if orientation[0] == 1:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + l == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() - 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middley()+ 2 > windowHeight/Scale:
                                        Turn = False
                                if orientation[0] == 2:
                                    if activeShape.get_left() - l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - 1 == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() - l == 0 and activeShape.get_middlex() + l == Row[y][x].get_x():
                                        Turn = False
                                if orientation[0] == 3:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - l == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() + 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                            if orientation[1] == 'reverseL':
                                if orientation[0] == 0:
                                    if activeShape.get_middlex() + l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - 1 == Row[y][x].get_y():
                                            Turn = False
                                    if activeShape.get_middlex() + l == windowWidth and activeShape.get_middlex() - l == Row[y][x].get_x():
                                        Turn = False
                                if orientation[0] == 1:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + l == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() + 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middley()+ 2 > windowHeight/Scale:
                                        Turn = False
                                if orientation[0] == 2:
                                    if activeShape.get_left() - l == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + 1 == Row[y][x].get_y():
                                        Turn = False
                                if orientation[0] == 3:
                                    if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - l == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_left() - 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                        Turn = False
                                    if activeShape.get_middley() + 1 > windowHeight / Scale:
                                        Turn = False
                        if orientation[1] == 'triangle':
                            if orientation[0] == 0:
                                if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() + 1 == Row[y][x].get_y():
                                    Turn = False
                            if orientation[0] == 1:
                                if activeShape.get_left() - 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                    Turn = False
                                if activeShape.get_middlex() - 1 == 0 and activeShape.get_middlex() + 1 == Row[y][x].get_x():
                                    Turn = False
                            if orientation[0] == 2:
                                if activeShape.get_middlex() == Row[y][x].get_x() and activeShape.get_middley() - 1 == Row[y][x].get_y():
                                    Turn = False
                            if orientation[0] == 3:
                                if activeShape.get_middlex() + 1 == Row[y][x].get_x() and activeShape.get_middley() == Row[y][x].get_y():
                                    Turn = False
                                if activeShape.get_middlex() + 1 == 0 and activeShape.get_middlex() - 1 == Row[y][x].get_x():
                                    Turn = False

                if Turn:
                    activeShape.Rotate()
                ROTATE = False
                Turn = True
            # The rate of drop counter, keeping the game going at a decent pace.
            if RODcounter > ROD - lvl or DROPFAST:
                activeShape.drop()
                activeShape.update()
                if activeShape.get_bottom() + 1 == int(gameWindowHeight/Scale):
                    activeShape.set_grounded("Drop")
                    nextShape()
                RODcounter = 0
            RODcounter += lvl*0.1+1

            # This loop goes through each block that is stationary, compares with the active block('s) and grounds them
            for i in range(len(Row)):
                for x in range(len(Row[i])):
                    checkColy = activeShape.get_bottom()
                    checkColLx = activeShape.get_left()
                    checkColRx = activeShape.get_right()
                    checkColTooth = activeShape.get_tooth()
                    if checkColTooth:
                        if checkColTooth[len(checkColTooth)-1] == 'Triangle':
                            if len(checkColTooth) > 4:
                                checkColTLx = checkColTooth[0]
                                checkColTy = checkColTooth[1]
                                checkColTRx = checkColTooth[2]
                                if checkColTy + 1 == Row[i][x].get_y() and checkColTLx <= Row[i][x].get_x() and checkColTRx >= Row[i][x].get_x():
                                    activeShape.set_grounded("Checking two tooth")
                                    nextShape()
                            else:
                                checkColTx = checkColTooth[0]
                                checkColTy = checkColTooth[1]
                                if checkColTy + 1 == Row[i][x].get_y() and checkColTx == Row[i][x].get_x():
                                    activeShape.set_grounded("Checking one tooth")
                                    nextShape()

                        if checkColTooth[len(checkColTooth) - 1] == 'L':
                            checkColTx = checkColTooth[0]
                            checkColTy = checkColTooth[1]
                            if checkColTy + 1 == Row[i][x].get_y() and checkColTx == Row[i][x].get_x():
                                activeShape.set_grounded("Checking one tooth")
                                nextShape()

                        if checkColTooth[len(checkColTooth) - 1] == 'reverseL':
                            checkColTx = checkColTooth[0]
                            checkColTy = checkColTooth[1]
                            if checkColTy + 1 == Row[i][x].get_y() and checkColTx == Row[i][x].get_x():
                                activeShape.set_grounded("Checking one tooth")
                                nextShape()

                    if checkColy + 1 == Row[i][x].get_y() and checkColLx <= Row[i][x].get_x() and checkColRx >= Row[i][x].get_x() or checkColy + 1 == int(gameWindowHeight/Scale):
                        activeShape.set_grounded("Checking without a tooth")
                        nextShape()

            # This is the scoring system which deletes a row if it has a length of 10.
            cleared = 0
            for r in range(-len(Row) + 1, 1):
                if len(Row[-r]) == 10:
                    cleared += 1
                    score += 100
                    for x in range(-len(Row[-r])+1, 1):
                        Row[-r].pop(-x)
            if cleared > 0:
                for y in range(-len(Row)+2, 1):
                    for i in range(-len(Row[-y])+1, 1):
                        Row[-y][-i].set_y(-y+cleared)
                        Row[-y+cleared].append(Row[-y][-i])
                        Row[-y].pop(-i)




            # update objects
            activeShape.update()
            lvlFont = font.render("Level: " + str(lvl), False, WHITE, BLACK)
            scoreFont = font.render("Score: " + str(score), False, WHITE, BLACK)
            lvl = int(score/1000)

            for y in range(len(Row)):
                for i in range(len(Row[y])):
                    Row[y][i].update()



        # The draw events for objects
        windowSurface.fill(ORANGE)
        for x in range(Scale, windowWidth, Scale):
            for y in range(Scale, windowHeight, Scale):
                pygame.draw.line(windowSurface, BLACK, (0, y), (windowWidth, y), 3)
            pygame.draw.line(windowSurface, BLACK, (x, 0), (x, windowHeight), 3)

        windowSurface.blit(lvlFont, lvlRect)
        windowSurface.blit(scoreFont, scoreRect)

        for i in range(len(instFont)):
            windowSurface.blit(instFont[i], instRect[i])


        gameSpace.fill(GREY)

        for i in range(len(Row)):
            for x in range(len(Row[i])):
                Row[i][x].show()

        #activeBlock.show()
        activeShape.show()

        #This block is the display for the next shape
        nextShapeSurf.fill(BLACK)
        if displayNext:
            if currentShape == 0:
                triangleBlock.show(triangleBlock(), True)
            if currentShape == 1:
                squareBlock.show(squareBlock(), True)
            if currentShape == 2:
                LBlock.show(LBlock(), True)
            if currentShape == 3:
                reverseLBlock.show(reverseLBlock(), True)
            if currentShape == 4:
                lineBlock.show(lineBlock(), True)

        #The game over sequence
        if len(Row[0]) > 0:
            for y in range(len(Row)):
                for x in range(-len(Row[y])+1, 1):
                    Row[y].pop(-x)
            score = 0
            currentShape = random.randint(0,4)
            nextShape()
            playing = False
        if pause:
            pauseSurf.fill(BLACK)
            gameSpace.blit(pauseFont, pauseRect)
            gameSpace.blit(pauseinstFont, pauseinstRect)
            gameSpace.blit(pauseSurf, (0, 0))

        windowSurface.blit(nextShapeSurf, ((windowWidth/2) + Scale * 2, windowHeight/10 + Scale * 5))
        windowSurface.blit(gameSpace, (windowWidth/Scale, windowHeight/Scale))
    else:
        windowSurface.fill(ORANGE)
        for x in range(Scale, windowWidth, Scale):
            for y in range(Scale, windowHeight, Scale):
                pygame.draw.line(windowSurface, BLACK, (0, y), (windowWidth, y), 3)
            pygame.draw.line(windowSurface, BLACK, (x, 0), (x, windowHeight), 3)
        windowSurface.blit(titleFont, titleRect)
        windowSurface.blit(buttonFont, buttonRect)

    pygame.display.update()
    mainClock.tick(60)