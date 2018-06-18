#! PyTetris Blocks and shapes
# Error with L and I shapes not wanting to rotate around near the left side of the game space.


import pygame
from pygame.locals import *


windowWidth = 800
windowHeight = 800
gameWindowWidth = windowWidth/2
gameWindowHeight = windowHeight - 40
Scale = int(gameWindowWidth/10)

Row = []
for i in range(int(gameWindowHeight / Scale)):
    Row.append([])

nextShapeSurf = pygame.Surface((Scale * 5, Scale * 6))
gameSpace = pygame.Surface((gameWindowWidth, gameWindowHeight))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
GREEN = (0, 100, 0)
ORANGE = (200, 100, 0)
BLUE = (0, 0, 100)
PURPLE = (100, 0, 100)
YELLOW = (100, 100, 0)
RED = (255, 0, 0)

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
