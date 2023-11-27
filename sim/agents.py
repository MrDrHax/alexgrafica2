from typing import Any
from fastautomata import Agents
from fastautomata.Board import SimulatedBoard as Board
from fastautomata.ClassTypes import Pos
from fastautomata.fastautomata_clib import BaseAgent
import random
from enum import Enum
from jsonChache import JsonSave

# TODO hacer que todos los agentes se pongan juntos de un jalon

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    FUCKING_CRAZY = "O"

class Neighbors(Enum):
    Top_Left        = 0
    Top_Center      = 1
    Top_Right       = 2
    Middle_Left     = 3
    Middle_Center   = 4
    Middle_Right    = 5
    Bottom_Left     = 6
    Bottom_Center   = 7
    Bottom_Right    = 8
    

destinationsList: list['Destination'] = []
roadsList: list['Road'] = []

class Road(Agents.SimulatedAgent):
    roads: list['Road'] = []
    direction: str

    routes: dict[Pos, list[Pos]]

    def __init__(self, board: Board, pos: Pos, direction: str):
        super().__init__(board, pos, "Road", 0, False)
        self.direction = direction
        roadsList.append(self)
        self.roads = []
        self.routes = {}
    
    def step(self) -> None:
        pass

    def convertCrazyToRoad(self):
        if self.direction == Direction.FUCKING_CRAZY.value:
            neighbors : list[Road] = self.get_neighbors(1, False, -1)
            # check if there is road up
            stoplights = self.get_neighbors(1, False, 2)
            if (neighbors[Neighbors.Top_Center.value] is not None 
                and isinstance(neighbors[Neighbors.Top_Center.value], Road)
                and neighbors[Neighbors.Top_Center.value].direction == Direction.DOWN.value
                and stoplights[Neighbors.Top_Center.value] is None):
                self.direction = Direction.DOWN.value

            elif (neighbors[Neighbors.Middle_Right.value] is not None 
                and isinstance(neighbors[Neighbors.Middle_Right.value], Road)
                and neighbors[Neighbors.Middle_Right.value].direction == Direction.LEFT.value
                and stoplights[Neighbors.Middle_Right.value] is None):
                self.direction = Direction.LEFT.value

            elif (neighbors[Neighbors.Bottom_Center.value] is not None 
                and isinstance(neighbors[Neighbors.Bottom_Center.value], Road)
                and neighbors[Neighbors.Bottom_Center.value].direction == Direction.UP.value
                and stoplights[Neighbors.Bottom_Center.value] is None):
                self.direction = Direction.UP.value

            elif (neighbors[Neighbors.Middle_Left.value] is not None 
                and isinstance(neighbors[Neighbors.Middle_Left.value], Road)
                and neighbors[Neighbors.Middle_Left.value].direction == Direction.RIGHT.value
                and stoplights[Neighbors.Middle_Left.value] is None):
                self.direction = Direction.RIGHT.value

            else:
                self.direction = Direction.LEFT.value

    def calculateRoads(self):
        neighbors : list[Road] = self.get_neighbors(1, False, -1)
        options: list[BaseAgent] = []

        match self.direction:
            # si queremos agregar en un futuro que no solo sea diagonal... se puede aqui
            case Direction.UP.value:
                # it can move to a road that is pointing outwards (not inwards)
                if (neighbors[Neighbors.Top_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Left.value], Destination) or 
                    neighbors[Neighbors.Top_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Top_Left.value].direction == Direction.UP.value)):

                    options.append(neighbors[Neighbors.Top_Left.value])

                if (neighbors[Neighbors.Top_Center.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Center.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Center.value], Destination) or 
                    neighbors[Neighbors.Top_Center.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Top_Center.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Top_Center.value].direction == Direction.LEFT.value)):

                    options.append(neighbors[Neighbors.Top_Center.value])

                if (neighbors[Neighbors.Top_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Right.value], Destination) or
                    neighbors[Neighbors.Top_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Top_Right.value].direction == Direction.UP.value)):

                    options.append(neighbors[Neighbors.Top_Right.value])

            case Direction.LEFT.value:

                if (neighbors[Neighbors.Top_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Left.value], Destination) or 
                    neighbors[Neighbors.Top_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Top_Left.value].direction == Direction.UP.value)):

                    options.append(neighbors[Neighbors.Top_Left.value])

                if (neighbors[Neighbors.Middle_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Middle_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Middle_Left.value], Destination) or 
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.LEFT.value or 
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Middle_Left.value])

                if (neighbors[Neighbors.Bottom_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Left.value], Destination) or
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Bottom_Left.value])

            case Direction.RIGHT.value:

                if (neighbors[Neighbors.Bottom_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Right.value], Destination) or 
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Bottom_Right.value])

                if (neighbors[Neighbors.Middle_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Middle_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Middle_Right.value], Destination) or 
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Middle_Right.value])

                if (neighbors[Neighbors.Top_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Right.value], Destination) or
                    neighbors[Neighbors.Top_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Top_Right.value].direction == Direction.UP.value)):

                    options.append(neighbors[Neighbors.Top_Right.value])
                
            case Direction.DOWN.value:

                if (neighbors[Neighbors.Bottom_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Left.value], Destination) or
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Bottom_Left.value])

                if (neighbors[Neighbors.Bottom_Center.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Center.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Center.value], Destination) or 
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Bottom_Center.value])

                if (neighbors[Neighbors.Bottom_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Right.value], Destination) or 
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.DOWN.value)):

                    options.append(neighbors[Neighbors.Bottom_Right.value])

            

        self.roads = options

    def cookRoutes(self, cache: JsonSave):

        start = self

        for destination in destinationsList:
            cachedRoute = cache.getRoute(self.pos, destination.pos)
            if cachedRoute is not None:
                self.routes[destination.pos.toString()] = cachedRoute
                continue

            # Future cells is a priority queue (road, priority)
            future_cells: list[tuple[Road, int]] = []
            future_cells.append((start, 0))
            past_cells: dict[Road, Road] = {} # dictionary of (current, come_from)
            cost_so_far = {start: 0}

            while len(future_cells) != 0:
                current_packed = future_cells.pop()
                current = current_packed[0]
                
                if current.pos == destination.pos:
                    break

                if isinstance(current, Destination):
                    continue # ignore destinations

                for next in current.roads:
                    new_cost = cost_so_far[current] + 1

                    if not (next.pos.x == current.pos.x or next.pos.y == current.pos.y):
                        new_cost = cost_so_far[current] + 1.75 # if it is not in the same axis, add a diagonal cost

                    if next not in past_cells.keys() or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + (abs(destination.pos.x - next.pos.x) + abs(destination.pos.y - next.pos.y))
                        past_cells[next] = current
                        future_cells.append((next, priority))

            route: list[Pos] = [destination.pos]
            actual = destination
            while actual != start:
                last_cell = past_cells[actual]
                route.insert(0, last_cell.pos)
                actual = last_cell
            
            route.pop(0) # remove starting pos

            # return track
            self.routes[destination.pos.toString()] = route

            cache.addRoute(self.pos, destination.pos, route)
            
    def getRoute(self, destination: 'Destination') -> list[Pos]:
        if isinstance(destination, Destination):
            return self.routes[destination.pos.toString()]
        else:
            raise TypeError("The destination is not a destination.")

class Destination(Agents.StaticAgent):
    def __init__(self, board: Board, pos: Pos):
        super().__init__(board, pos, "Destination", 0, False)
        destinationsList.append(self)

class Building(Agents.StaticAgent):
    def __init__(self, board: Board, pos: Pos):
        super().__init__(board, pos, "Building", 0, False)

class Stoplight(Agents.SimulatedAgent):
    def __init__(self, board: Board, pos: Pos):
        super().__init__(board, pos, "Stoplight_go", 2, False)

    def step(self):
        pass

class Car(Agents.SimulatedAgent):
    destination: Destination

    path: list[Pos] = []

    lastPos: Pos

    desperation: int = 0

    def __init__(self, board: Board):
        choices = [
            # corners of the map
            Pos(0, 0),
            Pos(0, board.getHeight() - 1),
            Pos(board.getWidth() - 1, 0),
            Pos(board.getWidth() - 1, board.getHeight() - 1)
        ]
        spawnIn = random.choice(choices)

        for i in range(4):
            spawnIn = random.choice(choices)
            if board.agent_get(spawnIn, 1, False) is None:
                break
            choices.remove(spawnIn)

        super().__init__(board, spawnIn, "Car", 1, False)

        self.destination = random.choice(destinationsList)

        self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination)

        self.lastPos = self.pos

        self.desperation = 0

    def step(self):
        if isinstance(self.board.agent_get(self.pos, 0, False), Destination):
            self.kill()
            return

        if self.lastPos != self.pos: # if this runs, then it means someone got in their way
            self.lastPos = self.pos
            self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination)

        if len(self.path) == 0 or not (self.pos.x - 1 <= self.path[0].x <= self.pos.x + 1 and self.pos.y - 1 <= self.path[0].y <= self.pos.y + 1):
            self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination)

            if len(self.path) == 0 or not (self.pos.x - 1 <= self.path[0].x <= self.pos.x + 1 and self.pos.y - 1 <= self.path[0].y <= self.pos.y + 1):
                self.path.append(random.choice(self.board.agent_get(self.pos, 0, False).roads).pos)

        if self.desperation > 3:
            self.path = [random.choice(self.board.agent_get(self.pos, 0, False).roads).pos] # just move brute force

        self.desperation += 1

        nextPos = self.path[0]

        if nextPos == self.pos:
            self.path.pop(0)
            self.step()
            return

        if self.board.agent_get(nextPos, 1, False) is None:
            self.pos = self.path.pop(0)
            self.lastPos = nextPos
            self.desperation = 0
            