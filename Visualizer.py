""" Pathfinding Visualizer Made by Keilon Robertson """

import pygame
from tkinter import messagebox, Tk
from queue import PriorityQueue
import os
from Colours import Colours
from Grid import Grid
import pygame_menu
import time
from playsound import playsound

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (350, 50) # open window in the middle of the screen
icon = pygame.image.load('images/location.png')
WIDTH = 600
ROWS = 25

grid = Grid()
colour = Colours()

# Main Visualizer Controller
def visualize(width, ROWS, twoDestinations):

    playsound('sounds/buttonClicked.mp3')
    map = grid.createGrid(ROWS, width)

    pygame.display.set_caption("Pathfinding Visualizer")
    pygame.display.set_icon(icon)

    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.update()

    source = None
    destination = None
    destination2 = None
    exit = False

    while not exit:
        grid.colour(window, map, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = grid.getClicked(position, ROWS, width)
                vertex = map[row][column]

                if not source and vertex != destination:
                    source = vertex
                    source.setSource()

                elif not destination and vertex != source:
                    destination = vertex
                    destination.setDestination()

                elif twoDestinations and not destination2 and vertex != source and vertex != destination:
                    destination2 = vertex
                    destination2.setDestination()

                elif vertex != destination and vertex != source and vertex != destination2:
                    vertex.setObstacle()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                position = pygame.mouse.get_pos()
                row, column = grid.getClicked(position, ROWS, width)
                vertex = map[row][column]
                vertex.clear()

                if vertex == source:
                    source = None

                elif vertex == destination:
                    destination = None

                elif vertex == destination2:
                    destination2 = None

            if event.type == pygame.KEYDOWN:
                if source and destination:
                    if event.key == pygame.K_1:
                        map = setGameBoard(map)
                        grid.colour(window, map, ROWS, width)
                        pygame.display.update()

                        if not twoDestinations:
                            breadthFirstSearch(lambda: grid.colour(window, map, ROWS, width), source, destination, map)

                        elif destination2:
                            twoDestinationBFS(lambda: grid.colour(window, map, ROWS, width), source, destination,
                                              destination2, map)

                    elif event.key == pygame.K_2:
                        map = setGameBoard(map)
                        grid.colour(window, map, ROWS, width)
                        pygame.display.update()
                        if not twoDestinations:
                            dijkstrasAlgorithm(lambda: grid.colour(window, map, ROWS, width), source, destination, map)

                        elif destination2:
                            dijkstraTwoDestinations(lambda: grid.colour(window, map, ROWS, width), source, destination,
                                                    destination2, map)


                    elif event.key == pygame.K_3 and not twoDestinations:
                        map = setGameBoard(map)
                        grid.colour(window, map, ROWS, width)
                        pygame.display.update()
                        AStarAlgorithm(lambda: grid.colour(window, map, ROWS, width), source, destination, map)

                    elif event.key == pygame.K_4 and not twoDestinations:
                        map = setGameBoard(map)
                        grid.colour(window, map, ROWS, width)
                        pygame.display.update()
                        BFSBiDirectional(lambda: grid.colour(window, map, ROWS, width), source, destination, map)

                    elif event.key == pygame.K_5 and not twoDestinations:
                        map = setGameBoard(map)
                        grid.colour(window, map, ROWS, width)
                        pygame.display.update()
                        dijkstraBiDirectional(lambda: grid.colour(window, map, ROWS, width), source, destination, map)


def setGameBoard(map):
    for row in map:
        for vertex in row:
            if not vertex.isSource() and not vertex.isDestination() and not vertex.isObstacle():
                vertex.clear()
            vertex.addConnections(map)
    return map


""" Base Pathfinding Algorithms"""


def breadthFirstSearch(drawing, source, destination, map):
    queue = [source]
    parent = {}
    shortest = {vertex: float("inf") for row in map for vertex in row}
    shortest[source] = 0
    found = False

    startTime = time.time()
    while len(queue) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)

        # Path Found
        if current == destination:
            totalTime = time.time() - startTime
            distanceCovered = reconstructPath(parent, destination, drawing, source)
            destination.setDestination()
            message = "  Speed: {totalTime:.1f}s  Distance Covered:  {distance}"
            Tk().wm_withdraw()
            messagebox.showinfo("Path Found!!", message.format(totalTime=totalTime, distance=distanceCovered))
            return True

        # loop through the current vertex's connections
        for edge in current.connections:
            tempScore = shortest[current] + 1

            if tempScore < shortest[edge]:
                parent[edge] = current
                shortest[edge] = tempScore
                if edge not in queue and edge != source:
                    queue.append(edge)
                    if not edge.isVisited():
                        edge.setInQueue()
        drawing()

        if current != source:
            current.setAsVisited()

    # No Solution Case
    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")


def dijkstrasAlgorithm(drawing, source, destination, map):
    count = 0
    found = False
    queue = PriorityQueue()
    queue.put((0, count, source))
    parent = {}
    gScore = {vertex: float("inf") for row in map for vertex in row} # shortest distance between source and current Node
    gScore[source] = 0

    queueDict = {source}
    startTime = time.time()
    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()[2]
        queueDict.remove(current)

        if current == destination:
            timeTaken = time.time() - startTime
            distanceCovered = reconstructPath(parent, destination, drawing, source)
            destination.setDestination()
            message = "  Speed: {timeTaken:.1f}s  Distance Covered:  {distance}"
            Tk().wm_withdraw()
            messagebox.showinfo("Path Found!!", message.format(timeTaken=timeTaken, distance=distanceCovered))
            return True

        for edge in current.connections:
            temp = gScore[current] + edge.getWeight()

            if temp < gScore[edge]:
                parent[edge] = current
                gScore[edge] = temp
                if edge not in queueDict:
                    count += 1
                    queue.put((gScore[edge], count, edge))
                    queueDict.add(edge)
                    edge.setInQueue()

        drawing()

        if current != source:
            current.setAsVisited()

    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")


def heuristic(currentPosition, destinationPosition): # Estimate distance and position of destination from current vertex
    xAxisSource, yAxisSource = currentPosition
    xAxisDestination, yAxisDestination = destinationPosition
    return abs(xAxisSource - xAxisDestination) + abs(yAxisSource - yAxisDestination)


def AStarAlgorithm(drawing, source, destination, map):
    count = 0
    found = False
    openSet= PriorityQueue()
    openSet.put((0, count, source))
    parent = {}
    gScore = {vertex: float("inf") for row in map for vertex in row} # shortest distance between source and current vertex
    gScore[source] = 0
    fScore = {vertex: float("inf") for row in map for vertex in row} # gScore + heuristic
    fScore[source] = heuristic(source.getPosition(), destination.getPosition())

    openSetHash = {source}
    startTime = time.time()
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == destination:
            timeTaken = time.time() - startTime
            distanceCovered = reconstructPath(parent, destination, drawing, source)
            destination.setDestination()
            message = "  Speed: {timeTaken:.1f}s  Distance Covered:  {distance}"
            Tk().wm_withdraw()
            messagebox.showinfo("Path Found!!", message.format(timeTaken=timeTaken, distance=distanceCovered))
            return True

        for edge in current.connections:
            temp = gScore[current] + edge.getWeight()

            if temp < gScore[edge]:
                parent[edge] = current
                gScore[edge] = temp
                fScore[edge] = temp + heuristic(edge.getPosition(), destination.getPosition())
                if edge not in openSetHash:
                    count += 1
                    openSet.put((fScore[edge], count, edge))
                    openSetHash.add(edge)
                    edge.setInQueue()

        drawing()

        if current != source:
            current.setAsVisited()

    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")


""" Functions for Reconstructing Paths """


# Reconstruct Path
def reconstructPath(parent, vertex, draw, source):
    distanceCovered = 0
    vertex.setDestination()

    # loop through the vertices' parents, making a path from the destination to the source
    while vertex in parent:
        time.sleep(0.025)
        distanceCovered += vertex.getWeight()
        vertex = parent[vertex]
        if vertex.isDestination() or vertex.isSource():
            pass
        else:
            vertex.setPathVertex()
        draw()
        if vertex == source:
            playsound('sounds/success.mp3')
            return distanceCovered


# Reconstruct a Path from bi-directional algorithm
def reconstructdirectionalPath(sourceParent, destParent, sourceCurrent, drawing, source):
    current = sourceCurrent
    distanceCovered = 0

    # loop through the vertices' parents, making a path from the current vertex to the source
    while sourceCurrent in sourceParent:
        distanceCovered += sourceCurrent.getWeight()
        sourceCurrent = sourceParent[sourceCurrent]
        if sourceCurrent.isSource():
            pass
        else:
            sourceCurrent.setPathVertex()
            time.sleep(0.025)
        drawing()
        if sourceCurrent.isDestination():
            sourceCurrent.setDestination()

    current.setPathVertex()

    # loop through the vertices' parents, making a path from the current vertex to the destination
    while current in destParent:
        distanceCovered += current.getWeight()
        current = destParent[current]
        if current.isSource():
            pass
        else:
            time.sleep(0.025)
            if current.isDestination():
                pass
            else:
                current.setPathVertex()
        drawing()
        if current.isDestination():
            current.setDestination()
            source.setSource()
    playsound('sounds/success.mp3')
    return distanceCovered


# Reconstruct a Path with Two destinations
def reconstructRoute(parent1, parent2, vertex, draw, source):
    distanceCovered = 0

    # loop through the vertices' parents, making a path from the current vertex to the destination
    while vertex in parent2:
        distanceCovered += vertex.getWeight()
        vertex = parent2[vertex]
        if vertex.isDestination():
            pass
        else:
            vertex.setPathVertex()
            time.sleep(0.025)
        draw()
        if vertex.isDestination():
            vertex.setDestination()
    time.sleep(0.5)

    # loop through the vertices' parents, making a path from the current vertex to the source
    while vertex in parent1:
        distanceCovered += vertex.getWeight()
        vertex = parent1[vertex]
        if vertex.isSource():
            pass
        else:
            time.sleep(0.025)
            vertex.setPathVertex()
        draw()
        if vertex.isDestination():
            vertex.setDestination()
            source.setSource()

    playsound('sounds/success.mp3')
    message = "  Distance Covered:  {distance}"
    Tk().wm_withdraw()
    messagebox.showinfo("Path Found!!", message.format(distance=distanceCovered))



""" Bi-Directional Algorithms"""


# BFS Biderectional Search
def BFSBiDirectional(drawing, source, destination, map):
    queue = [source]
    destQueue = [destination]
    sourceParent = {}
    destParent = {}
    sourceShortest = {vertex: float("inf") for row in map for vertex in row}
    sourceShortest[source] = 0
    destShortest = {vertex: float("inf") for row in map for vertex in row}
    destShortest[destination] = 0
    found = False

    startTime = time.time()
    while len(queue) != 0 and len(destQueue) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        destCurrent = destQueue.pop(0)
        sourceCurrent = queue.pop(0)

        for edge in sourceCurrent.connections:
            tempScore = sourceShortest[sourceCurrent] + 1

            if tempScore < sourceShortest[edge]:
                sourceParent[edge] = sourceCurrent
                sourceShortest[edge] = tempScore
                if edge not in queue and edge != source:
                    queue.append(edge)
                    if not edge.isVisited():
                        edge.setInQueue()

        for edge in destCurrent.connections:
            tempScore = destShortest[destCurrent] + 1

            if tempScore < destShortest[edge]:
                destParent[edge] = destCurrent
                destShortest[edge] = tempScore
                if edge not in queue and edge != source:
                    destQueue.append(edge)
                    if not edge.isVisited():
                        edge.setInQueue()
        drawing()

        if sourceCurrent != source:
            sourceCurrent.setAsVisited()
        if destCurrent != destination:
            destCurrent.setAsVisited()

        if (sourceCurrent.isVisited() or sourceCurrent.isInQueue()) and sourceCurrent in destParent:
            totalTime = time.time() - startTime
            distanceCovered = reconstructdirectionalPath(sourceParent, destParent, sourceCurrent, drawing, source)
            message = "  Speed: {timeTaken:.1f}s Distance Covered:  {distance}"
            Tk().wm_withdraw()
            messagebox.showinfo("Path Found!!", message.format(distance=distanceCovered, timeTaken=totalTime))
            return True

    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")


# Bi-Directional Dijkstra
def dijkstraBiDirectional(drawing, source, destination, map):
    count = 0
    found = False

    sourceQueue = PriorityQueue() # Vertex Queue starting with the source
    sourceQueue.put((0, count, source))
    destQueue = PriorityQueue() # Vertex Queue starting with the destination
    destQueue.put((0, count, destination))

    destParent = {} # pairs the vertex with it's parent vertex, starting from the destination
    sourceParent = {}# pairs the vertex with it's parent vertex, starting from the source

    sourceGScore = {vertex: float("inf") for row in map for vertex in row}
    sourceGScore[source] = 0

    destGScore = {vertex: float("inf") for row in map for vertex in row}
    destGScore[destination] = 0

    sourceDict = {source}
    destDict = {destination}

    startTime = time.time()

    while not sourceQueue.empty() and not destQueue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        sourceCurrent = sourceQueue.get()[2]
        sourceDict.remove(sourceCurrent)

        destCurrent = destQueue.get()[2]
        destDict.remove(destCurrent)

        # Visit the connections in the current vertex
        for edge in sourceCurrent.connections:
            temp = sourceGScore[sourceCurrent] + edge.getWeight()

            if temp < sourceGScore[edge]:
                sourceParent[edge] = sourceCurrent
                sourceGScore[edge] = temp
                if not edge.isVisited():
                    count += 1
                    sourceQueue.put((sourceGScore[edge], count, edge))
                    sourceDict.add(edge)
                    edge.setInQueue()

        # Visit the connections in the current vertex
        for edge in destCurrent.connections:
            temp = destGScore[destCurrent] + edge.getWeight()

            if temp < destGScore[edge]:
                destParent[edge] = destCurrent
                destGScore[edge] = temp
                if not edge.isVisited():
                    count += 1
                    destQueue.put((destGScore[edge], count, edge))
                    destDict.add(edge)
                    edge.setInQueue()

        drawing()

        if sourceCurrent != source:
            sourceCurrent.setAsVisited()
        if destCurrent != destination:
            destCurrent.setAsVisited()

        if sourceCurrent.isVisited() and sourceCurrent in destParent:
            timeTaken = time.time() - startTime
            distanceCovered = reconstructdirectionalPath(sourceParent, destParent, sourceCurrent, drawing, source)
            message = "  Speed: {timeTaken:.1f}s  Distance Covered:  {distance}"
            Tk().wm_withdraw()
            messagebox.showinfo("Path Found!!", message.format(timeTaken=timeTaken, distance=distanceCovered))
            return True

    # No Solution Case
    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")


""" Two Destination Algorithms """

def dijkstraTwoDestinations(drawing, source, destination, destination2, map):
    def search(drawing, source, destination, destination2, map):
        count = 0
        queue = PriorityQueue()
        queue.put((0, count, source))
        parent = {}
        gScore = {vertex: float("inf") for row in map for vertex in row}
        gScore[source] = 0

        queueDict = {source}
        while not queue.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = queue.get()[2]
            queueDict.remove(current)

            if current == destination:
                return True, True, current, parent

            if current == destination2:
                return True, False, current, parent

            for edge in current.connections:
                temp = gScore[current] + edge.getWeight()

                if temp < gScore[edge]:
                    parent[edge] = current
                    gScore[edge] = temp
                    if edge not in queueDict:
                        count += 1
                        queue.put((gScore[edge], count, edge))
                        queueDict.add(edge)
                        if not edge.isVisited():
                            if edge.isDestination() or edge.isSource():
                                pass
                            else:
                                edge.setInQueue()

            drawing()

            if not current.isSource() and not current.isDestination():
                current.setAsVisited()
        return False, False, None, {}

    found, foundDest1, current, parent1 = search(drawing, source, destination, destination2, map) # find the closest destination
    if foundDest1: # if destination 1 was closest, run bfs on the second destination using destination 1 as the source
        found, foundDest1, current, parent2 = search(drawing, destination, destination2, destination2, map)
    else: # if destination 2 was closest, run bfs on the first destination using destination 2 as the source
        found, foundDest1, current, parent2 = search(drawing, destination2, destination, destination, map)

    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")
    else:
        reconstructRoute(parent1, parent2, current, drawing, source)


def twoDestinationBFS(drawing, source, destination, destination2, map):

    def bfs(parent, drawing, source, destination, destination2, map):
        queue = [source]
        shortest = {vertex: float("inf") for row in map for vertex in row}
        shortest[source] = 0

        while len(queue) != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = queue.pop(0)

            if current == destination:
                return True, True, current, parent

            if current == destination2:
                return True, False, current, parent

            for edge in current.connections:
                tempScore = shortest[current] + 1

                if tempScore < shortest[edge]:
                    parent[edge] = current
                    shortest[edge] = tempScore
                    if edge not in queue and edge != source:
                        queue.append(edge)
                        if not edge.isVisited():
                            if edge.isDestination() or edge.isSource():
                                pass
                            else:
                                edge.setInQueue()

            drawing()

            if not current.isSource() and not current.isDestination():
                current.setAsVisited()

        return False, False, None, {}

    found, foundDest1, current, parent1 = bfs({}, drawing, source, destination, destination2, map) # find the closest destination

    if foundDest1: # if destination 1 was closest, run bfs on the second destination using destination 1 as the source
        found, foundDest1, current, parent2 = bfs({}, drawing, destination, destination2, destination2, map)
    else: # if destination 2 was closest, run bfs on the first destination using destination 2 as the source
        found, foundDest1, current, parent2 = bfs({}, drawing, destination2, destination, destination, map)

    if not found:
        Tk().wm_withdraw()
        messagebox.showinfo("No Solution", "There was no solution")
    else:
        reconstructRoute(parent1, parent2, current, drawing, source)


# Help Option
def helpButton():

    Tk().wm_withdraw()

    messagebox.showinfo("HELP", "When Start button is clicked, you will be greeted with a grid."
                                "\n\nYou can click on the spaces in the grid to set the source, destination or the "
                                "obstacles. "
                                "\n\nThe first click sets the source, the second click sets the destination, then you "
                                "can click and drag to set the obstacles. "
                                "\nYou can also right-click on a selection to undo"
                                "\n\nOnce a source and destination has been set, you can call on different algorithms "
                                "to find the path between the source and the destination between your obstacles. "
                                "\n\nThere are 5 algorithms that can be run at the moment, Breadth First Search ("
                                "BFS), Dijkstra's, and A* Algorithm, the Bi-directional Dijkstra is still in "
                                "development. "
                                "\n\nTo run an algorithm, you can use numbers 1-5 on your keyboard"
                                "\nNo.1 - Breadth First Search\nNo.2 - Dijkstra Algorithm\nNo.3 - A* Search\nNo.4 - "
                                "Bi-Directional BFS\nNo.5 - Bi-Directional Dijkstra's Algorithm"
                                "\n\n NOTE - You can choose to have two destinations on the menu screen but by doing "
                                "this, your second and third clicks will set the first and second destination, "
                                "then you can click and drag to set the obstacles. However, only the Breadth First "
                                "Search and Dijkstra's Algorithms will work with this option.")


def main():
    pygame.init()

    pygame.display.set_caption("Pathfinding Visualizer")
    pygame.display.set_icon(icon)

    MenuWindow = pygame.display.set_mode((600, 600))

    # Menu Initialization
    mainMenuWindow = pygame_menu.Menu(WIDTH, WIDTH, 'Pathfinding Visualizer', theme=pygame_menu.themes.THEME_BLUE)

    # Menu Content
    mainMenuWindow.add_button('START', lambda: visualize(WIDTH, ROWS, False))
    mainMenuWindow.add_button('START - Two Destinations', lambda: visualize(WIDTH, ROWS, True))
    mainMenuWindow.add_button('HOW TO USE', helpButton)
    mainMenuWindow.add_button('QUIT', pygame_menu.events.EXIT)

    mainMenuWindow.mainloop(MenuWindow)

main()

""" Ketastix Production """