from typing import Any
from fastautomata import Agents
from fastautomata.Board import SimulatedBoard as Board
from fastautomata.ClassTypes import Pos
from fastautomata.fastautomata_clib import BaseAgent
import random
from enum import Enum

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
    direction: Direction

    def __init__(self, board: Board, pos: Pos, direction: Direction):
        super().__init__(board, pos, "Road", 0, False)
        self.direction = direction
        roadsList.append(self)
    
    def step(self) -> None:
        pass

    def calculateRoads(self):
        neighbors = self.get_neighbors(1, False)
        options: list[BaseAgent] = []

        match self.direction:
            # si queremos agregar en un futuro que no solo sea diagonal... se puede aqui
            case Direction.UP:
                options = [
                    neighbors[Neighbors.Top_Left],
                    neighbors[Neighbors.Top_Center],
                    neighbors[Neighbors.Top_Right],
                ]
            case Direction.LEFT:
                options = [
                    neighbors[Neighbors.Top_Left],
                    neighbors[Neighbors.Middle_Left],
                    neighbors[Neighbors.Bottom_Left],
                ]
            case Direction.RIGHT:
                options = [
                    neighbors[Neighbors.Top_Right],
                    neighbors[Neighbors.Middle_Right],
                    neighbors[Neighbors.Bottom_Right],
                ]
            case Direction.DOWN:
                options = [
                    neighbors[Neighbors.Bottom_Left],
                    neighbors[Neighbors.Bottom_Center],
                    neighbors[Neighbors.Bottom_Right],
                ]
        
        for option in options:
            if option is not None:
                if option.type == "Road":
                    self.roads.append(option)

    def cookRoutes(graph, start, destination, path_empty):

        future_cells = []
        future_cells.push(start, 0)
        past_cells = {start: None}
        cost_so_far = {start: 0}

        while not future_cells.empty():
            current = future_cells.pop()
            
            if current == destination:
                break

            for next in graph.get_neighborhood(current, moore=False, include_center=False):
                if not path_empty(current, next):  # If the path is not clear,
                    continue

                new_cost = cost_so_far[current] + 1

                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + (abs(destination[0] - next[0]) + abs(destination[1] - next[1]))
                    future_cells.push(next, priority)
                    past_cells[next] = current

        track = {}
        actual = destination
        while actual != start:
            if actual in past_cells:
                last_cell = past_cells[actual]
                track[last_cell] = actual
                actual = last_cell
            else:
                return{}
            
        return track


    def getRoute(self, destination: 'Destination') -> list[Pos]:
        # TODO @Alex-Barr0n agrega aquí la lectura de tu A*
        for d in destinationsList:
            self.cookRoutes(self.board, self.pos, d.pos, self.path_empty)

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
    def __init__(self, board: Board):
        choices = [
            # corners of the map
            Pos(0, 0),
            Pos(0, board.specialValues["board_height"] - 1),
            Pos(board.specialValues["board_width"] - 1, 0),
            Pos(board.specialValues["board_width"] - 1, board.specialValues["board_height"] - 1)
        ]
        spawnIn = random.choice(choices)
        super().__init__(board, spawnIn, "Car", 1, False)

        self.destination = random.choice(destinationsList)

    def step(self):
        pass