Problem Statement
-----------------
Create a Pac-Man game that implements the A* path finding algorithm to help
the ghosts catch Pac-Man. This specific implementation uses the Manhattan
Distance for heuristic calculations.


A* Algorithm
____________
  def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

  def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    return came_from


Order of Time Complexity
------------------------
The primary comparison if-statement is in a for loop, nested within a
while loop. Therefore the Order of Complexity is O(n^2)


Description of How to Play
--------------------------
To initiate the program, either load the folder in Visual Studio Code, open the
'run.py' file and press the play button in the top right corner of VSC.
or
open a terminal window, go to the folder path and type the command
'python3 run.py' and press enter.
Once the game has loaded, you can press the space bar to start the game.
(Pressing the space bar again will pause the game at any time)
During game play, you can use either the arrow keys or W,A,S,D to control
the movement of Pac-Man. You have 5 lives to last as many levels as you can.
There are 2 different mazes that will alternate levels.
