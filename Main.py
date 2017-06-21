import pygame, sys, random, time
from pygame.locals import *

windowWidth = 800
windowHeight = 800
gameWindowWidth = windowWidth/2
gameWindowHeight = windowHeight - 40
Scale = gameWindowWidth/10

pygame.init()

# Colour schemes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
GREEN = (0, 100, 0)
ORANGE = (200, 100, 0)
PURPLE = (100, 0, 100)

# This variable holds the Row numbers for later scoring system.
Row = []
for i in range(gameWindowHeight/Scale):
    Row.append([])

# some essential variables for the player and others
ROD = 30    # Rate of drop, slowly decreases each incremented level
RODcounter = 0
lvl = 0
score = 0
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
font = pygame.font.SysFont('Arial', windowWidth/15)

lvlFont = font.render("Level: " + str(lvl), False, WHITE, BLACK)
lvlRect = lvlFont.get_rect()
lvlRect.top = windowHeight/10
lvlRect.left = windowWidth - (windowWidth/2) + Scale

scoreFont = font.render("Score: " + str(score), False, WHITE, BLACK)
scoreRect = scoreFont.get_rect()
scoreRect.top = windowHeight/10 * 2
scoreRect.left = windowWidth - (windowWidth/2) + Scale

# Setting the surfaces which to draw Objects onto
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
gameSpace = pygame.Surface((gameWindowWidth, gameWindowHeight))
mainClock = pygame.time.Clock()

# Setting up the object for tetris blocks
class block():
    def __init__(self):
        self.scale = Scale
        self.x = self.scale * 5
        self.y = self.scale
        self.rect = pygame.Rect(0, 0, self.scale, self.scale)
        self.grounded = False

    def show(self):
        pygame.draw.rect(gameSpace, GREEN, self.rect)

    def update(self):
        self.rect.top = self.y
        self.rect.left = self.x

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

class triangleBlock():
    def __init__(self):
        self.triBlocks = [block(), block(), block(), block()]
        self.triBlocks[0].set_x((gameWindowWidth/Scale) / 2)
        self.orientation = 0
        self.grounded = False

    def update(self):
        if not self.grounded:
            if self.orientation == 0:
                self.triBlocks[1].set_x(self.triBlocks[0].get_x() - 1)
                self.triBlocks[1].set_y(self.triBlocks[0].get_y())
                self.triBlocks[2].set_x(self.triBlocks[0].get_x() + 1)
                self.triBlocks[2].set_y(self.triBlocks[0].get_y())
                self.triBlocks[3].set_x(self.triBlocks[0].get_x())
                self.triBlocks[3].set_y(self.triBlocks[0].get_y() - 1)
            if self.orientation == 1:
                self.triBlocks[1].set_x(self.triBlocks[0].get_x())
                self.triBlocks[1].set_y(self.triBlocks[0].get_y() - 1)
                self.triBlocks[2].set_x(self.triBlocks[0].get_x())
                self.triBlocks[2].set_y(self.triBlocks[0].get_y() + 1)
                self.triBlocks[3].set_x(self.triBlocks[0].get_x() + 1)
                self.triBlocks[3].set_y(self.triBlocks[0].get_y())
            if self.orientation == 2:
                self.triBlocks[1].set_x(self.triBlocks[0].get_x() + 1)
                self.triBlocks[1].set_y(self.triBlocks[0].get_y())
                self.triBlocks[2].set_x(self.triBlocks[0].get_x() - 1)
                self.triBlocks[2].set_y(self.triBlocks[0].get_y())
                self.triBlocks[3].set_x(self.triBlocks[0].get_x())
                self.triBlocks[3].set_y(self.triBlocks[0].get_y() + 1)
            if self.orientation == 3:
                self.triBlocks[1].set_x(self.triBlocks[0].get_x())
                self.triBlocks[1].set_y(self.triBlocks[0].get_y() + 1)
                self.triBlocks[2].set_x(self.triBlocks[0].get_x())
                self.triBlocks[2].set_y(self.triBlocks[0].get_y() - 1)
                self.triBlocks[3].set_x(self.triBlocks[0].get_x() - 1)
                self.triBlocks[3].set_y(self.triBlocks[0].get_y())

        for boxes in self.triBlocks:
            boxes.update()

    def show(self):
        for boxes in self.triBlocks:
            boxes.show()
            #print boxes.get_x()

    def drop(self):
        #if self.get_bottom() + 1 == gameWindowHeight/Scale:
            #self.set_grounded("Drop event")
            #return True
        #else:
        return self.triBlocks[0].drop()


    def set_grounded(self, callFrom):
        self.grounded = True
        #print callFrom
        for i in range(len(self.triBlocks)):
            #print self.triBlocks[i].get_y()
            Row[self.triBlocks[i].get_y()].append(self.triBlocks[i])
            self.triBlocks[i].setGrounded(True)
        #print len(Row[17])

    def Direction(self, LEFT, RIGHT):
        self.triBlocks[0].Direction(LEFT, RIGHT)

    def Rotate(self):
        self.orientation +=1
        if self.orientation > 3:
            self.orientation = 0

    def get_left(self):
        if self.orientation == 0:
            return self.triBlocks[1].get_x()
        if self.orientation == 1:
            return self.triBlocks[0].get_x()
        if self.orientation == 2:
            return self.triBlocks[3].get_x()
        if self.orientation == 3:
            return self.triBlocks[0].get_x()

    def get_right(self):
        if self.orientation == 0:
            return self.triBlocks[2].get_x()
        if self.orientation == 1:
            return self.triBlocks[2].get_x()
        if self.orientation == 2:
            return self.triBlocks[3].get_x()
        if self.orientation == 3:
            return self.triBlocks[2].get_x()

    def get_top(self):
        if self.orientation == 0:
            return self.triBlocks[3].get_y()
        if self.orientation == 1:
            return self.triBlocks[1].get_y()
        if self.orientation == 2:
            return self.triBlocks[0].get_y()
        if self.orientation == 3:
            return self.triBlocks[2].get_y()

    def get_bottom(self):
        if self.orientation == 0:
            return self.triBlocks[0].get_y()
        if self.orientation == 1:
            return self.triBlocks[2].get_y()
        if self.orientation == 2:
            return self.triBlocks[3].get_y()
        if self.orientation == 3:
            return self.triBlocks[1].get_y()

    def get_middley(self):
        return self.triBlocks[0].get_y()

    def get_middlex(self):
        return self.triBlocks[0].get_x()

    #def get_middle(self):
    #    return self.triBlocks[0].get_x()
    def get_tooth(self):
        if self.orientation == 0:
            return False
        if self.orientation == 1:
            return [self.triBlocks[3].get_x(), self.triBlocks[3].get_y(), 1, 'Triangle']
        if self.orientation == 2:
            return [self.triBlocks[2].get_x(), self.triBlocks[0].get_y(), self.triBlocks[1].get_x(), 2, 'Triangle']
        if self.orientation == 3:
            return [self.triBlocks[3].get_x(), self.triBlocks[3].get_y(), 3, 'Triangle']




activeShape = triangleBlock()
#activeBlock = block()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                ROTATE = True
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

    # This variable keeps the blocks within the game space. accepting the tooth as an extention of the shape
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
    else:
        blocksLx = activeShape.get_left()
        blocksRx = activeShape.get_right()

    #If the player tries to clip out of game space it pushes them back in.
    if blocksLx < 0:
        activeShape.Direction(False, True)
    if blocksRx > gameWindowWidth / Scale - 1:
        activeShape.Direction(True, False)

    # this controls the shape to not intersect with the blocks that have been grounded.
    if blocksTooth:
        for y in range(len(Row)):
            for x in range(len(Row[y])):
                checkColx = Row[y][x].get_x()
                checkColy = Row[y][x].get_y()
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


    #Move the Shape left or right within limits
    if RIGHT or LEFT:
        if blocksLx <= 0:
            LEFT = False
        if blocksRx >= gameWindowWidth/Scale - 1:
            RIGHT = False

        activeShape.Direction(LEFT, RIGHT)
        LEFT = False
        RIGHT = False

    # Rotate the current shape,
    if ROTATE:
        activeShape.Rotate()
        ROTATE = False

    # The rate of drop counter, keeping the game going at a decent pace.
    if RODcounter > ROD - score or DROPFAST:
        activeShape.drop()
        activeShape.update()
        if activeShape.get_bottom() + 1 == gameWindowHeight/Scale:
            activeShape.set_grounded("Drop")
            activeShape = triangleBlock()
        RODcounter = 0
    RODcounter += 1

    # This loop goes through each block that is stationary, compares with the active block('s) and grounds them
    for i in range(len(Row)):
        for x in range(len(Row[i])):
            checkColy = activeShape.get_bottom()
            checkColLx = activeShape.get_left()
            checkColRx = activeShape.get_right()
            checkColTooth = activeShape.get_tooth()
            #if checkColTooth[len(checkColTooth) - 1] == 'Triangle':
            if checkColTooth:
                if checkColTooth[len(checkColTooth)-1] == 'Triangle':
                    if len(checkColTooth) > 4:
                        checkColTLx = checkColTooth[0]
                        checkColTy = checkColTooth[1]
                        checkColTRx = checkColTooth[2]
                        if checkColTy + 1 == Row[i][x].get_y() and checkColTLx <= Row[i][x].get_x() and checkColTRx >= Row[i][x].get_x():
                            activeShape.set_grounded("Checking two tooth")
                            activeShape = triangleBlock()
                    else:
                        checkColTx = checkColTooth[0]
                        checkColTy = checkColTooth[1]
                        if checkColTy + 1 == Row[i][x].get_y() and checkColTx == Row[i][x].get_x():
                            activeShape.set_grounded("Checking one tooth")
                            activeShape = triangleBlock()

            if checkColy + 1 == Row[i][x].get_y() and checkColLx <= Row[i][x].get_x() and checkColRx >= Row[i][x].get_x() or checkColy + 1 == gameWindowHeight/Scale:
                activeShape.set_grounded("Checking without a tooth")
                activeShape = triangleBlock()

    # This is the scoring system which deletes a row if it has a length of 10.
    for r in range(len(Row)):
        if len(Row[r]) == 10:
            score += 100
            for x in range(-len(Row[r])+1, 1):
                Row[r].pop(-x)
            for y in range(-len(Row)+1, 1):
                for i in range(-len(Row[-y])+1, 1):
                    Row[-y][-i].set_y(-y+1)
                    Row[-y+1].append(Row[-y][-i])
                    Row[-y].pop(-i)



    # update objects
    activeShape.update()
    lvlFont = font.render("Level: " + str(lvl), False, WHITE, BLACK)
    scoreFont = font.render("Score: " + str(score), False, WHITE, BLACK)
    lvl = score/1000

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

    gameSpace.fill(GREY)

    for i in range(len(Row)):
        for x in range(len(Row[i])):
            Row[i][x].show()

    #activeBlock.show()
    activeShape.show()

    windowSurface.blit(gameSpace, (windowWidth/Scale, windowHeight/Scale))
    pygame.display.update()
    mainClock.tick(60)