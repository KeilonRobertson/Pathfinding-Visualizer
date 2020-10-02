# Pathfinding Visualizer #

Pygame application for visualizing pathfinding algorithms on randomly generated weighted graphs <br />

### How to get set up? ###

- Install  [Python 3](https://www.python.org).
- Install these modules:
```
pip install pygame
pip install playsound
```

- Run Visualizer.py file.

### Files / Directories ###

 - **/images** : Contains the images used in the program
 - **/sounds** : Contains the sounds used in the program
 - **Vertex.py** : Has the Vertex class, where each object represents a node in the graph.
 - **Grid.py** : Contains the Grid class to generate the graph for the application
 - **Visualizer.py** : Main game loop and contains the algorithms for pathfinding
 - **Colours.py** : Stores the colours used in the app


### How it works? ###

1. This program displays a weighted graph where the user can input the source and destination, and draw obstacles.
2. The user can choose from 5 algorithms to find a path between the source and destination; BFS, Dijkstra's, A* Search, Bi-directional BFS, Bi-directional Dijkstra's.
3. Two destinations can be selected to find a path between the source and the two endpoints.
4. More information on how to use the app can be found by selecting the "How to Use" button on the main menu

### Authors ###

* **Keilon Robertson** 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.