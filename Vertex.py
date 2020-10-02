from Colours import Colours
import pygame
import random
import os

colour = Colours()

number1 = pygame.image.load(os.path.join('images', 'number1.png'))
number2 = pygame.image.load(os.path.join('images', 'number2.png'))
number3 = pygame.image.load(os.path.join('images', 'number3.png'))


class Vertex:
    def __init__(self, width, totalRows, row, column):
        self.colour = colour.WHITE
        self.weightToReach = random.randint(1, 3)
        self.width = width
        self.totalRows = totalRows
        self.row = row
        self.column = column
        self.xCoord = row * width
        self.yCoord = column * width
        self.connections = []


    def getWeight(self):
        return self.weightToReach


    def getPosition(self):
        return self.row, self.column


    def isSource(self):
        return self.colour == colour.ORANGE


    def isDestination(self):
        return self.colour == colour.RED


    def isObstacle(self):
        return self.colour == colour.BLACK


    def isVisited(self):
        return self.colour == colour.CYAN


    def isInQueue(self):
        return self.colour == colour.BLUE


    def clear(self):
        self.colour = colour.WHITE


    def setSource(self):
        self.colour = colour.ORANGE


    def setDestination(self):
        self.colour = colour.RED


    def setAsVisited(self):
        self.colour = colour.CYAN


    def setInQueue(self):
        self.colour = colour.BLUE


    def setObstacle(self):
        self.colour = colour.BLACK


    def setPathVertex(self):
        self.colour = colour.GREEN


    def createVertex(self, win):
        pygame.draw.rect(win, self.colour, (self.xCoord, self.yCoord, self.width, self.width))
        if self.weightToReach == 1:
            win.blit(number1, (self.xCoord, self.yCoord, self.width, self.width))
        elif self.weightToReach == 2:
            win.blit(number2, (self.xCoord, self.yCoord, self.width, self.width))
        else:
            win.blit(number3, (self.xCoord, self.yCoord, self.width, self.width))


    def addConnections(self, grid):
        self.connections = []
        # Add connection to the top
        if self.row > 0 and not grid[self.row - 1][self.column].isObstacle():
            self.connections.append(grid[self.row - 1][self.column])

        # Add connection to the bottom
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.column].isObstacle():  # DOWN
            self.connections.append(grid[self.row + 1][self.column])

        # Add connection to the right
        if self.column < self.totalRows - 1 and not grid[self.row][self.column + 1].isObstacle():  # RIGHT
            self.connections.append(grid[self.row][self.column + 1])

        # Add connection to the left
        if self.column > 0 and not grid[self.row][self.column - 1].isObstacle():  # LEFT
            self.connections.append(grid[self.row][self.column - 1])
