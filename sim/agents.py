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

    def cookRoutes(self):
        # TODO @Alex-Barr0n agrega aquí tu A*
        # has que valla a cualquier Destination (para que no tenga que calcular el a* cada vez que se mueva) 
        # puedes usar el destinationList e iterar en el
        pass 

    def getRoute(self, destination: 'Destination') -> list[Pos]:
        # TODO @Alex-Barr0n agrega aquí la lectura de tu A*
        pass

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