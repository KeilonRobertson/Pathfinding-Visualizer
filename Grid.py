from Vertex import Vertex
import pygame
from Colours import Colours

class Grid:
    def createGrid(self, rows, width):
        grid = []
        space = width // rows
        for x in range(rows):
            grid.append([])
            for i in range(rows):
                vertex = Vertex(space, rows, x, i)
                grid[x].append(vertex)
        return grid

    def generateGrid(self, width, rows, window):
        space = width // rows
        for x in range(rows):
            pygame.draw.line(window, Colours.BLACK, (0, x * space), (width, x * space))
            for i in range(rows):
                pygame.draw.line(window, Colours.BLACK, (i * space, 0), (i * space, width))

    def colour(self, window, grid, rows, width):
        window.fill(Colours.WHITE)
        for row in grid:
            for vertex in row:
                vertex.createVertex(window)

        self.generateGrid(width, rows, window)
        pygame.display.update()

    def getClicked(self, position, rows, width):
        space = width // rows
        y, x = position

        column = x // space
        row = y // space

        return row, column
