from typing import Any
from fastautomata import Agents
from fastautomata.Board import SimulatedBoard as Board
from fastautomata.ClassTypes import Pos
from fastautomata.fastautomata_clib import BaseAgent
import random
from enum import Enum
from jsonChache import JsonSave

# TODO hacer que todos los agentes se pongan juntos de un jalon

class Direction(Enum): # this is the direction the road is pointing to
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    NEUTRAL = "O"

class Neighbors(Enum): #Represents neighbor positions around a central point
    Top_Left = 0
    Top_Center = 1
    Top_Right = 2
    Middle_Left = 3
    Middle_Center = 4
    Middle_Right = 5
    Bottom_Left = 6
    Bottom_Center = 7
    Bottom_Right = 8
    

destinationsList: list['Destination'] = [] # list of all destinations for future use
roadsList: list['Road'] = [] # list of all roads for future use

def boardReset(board: Board): # reset the board
    global destinationsList, roadsList
    destinationsList = []
    roadsList = []

class Road(Agents.SimulatedAgent):
    roads: list['Road'] = []
    direction: str

    routes: dict[Pos, list[Pos]]

    def __init__(self, board: Board, pos: Pos, direction: str): # Board, Pos, Direction
        super().__init__(board, pos, "Road", 0, False)
        self.direction = direction # this is the direction the road is pointing to
        roadsList.append(self) # add this road to the list of roads
        self.roads = [] # list of roads this road can go to
        self.routes = {} # waze
    
    def step(self) -> None: # We don't need the road to actually do anything
        pass 

    def convertToRoad(self): # if it is a neutral road, then it can go anywhere
        if self.direction == Direction.NEUTRAL.value:
            neighbors : list[Road] = self.get_neighbors(1, False, -1) # get all neighbors
            stoplights = self.get_neighbors(1, False, 2) # get all stoplights

            if (neighbors[Neighbors.Top_Center.value] is not None 
                and isinstance(neighbors[Neighbors.Top_Center.value], Road)
                and neighbors[Neighbors.Top_Center.value].direction == Direction.DOWN.value
                and stoplights[Neighbors.Top_Center.value] is None):
                # if there is a road pointing somewhere and there is no stoplight
                self.direction = Direction.DOWN.value # then go the opposite direction

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
                # if there is no road pointing in any direction, then go left (default)

    def calculateRoads(self): # Waze-like algorithm
        neighbors : list[Road] = self.get_neighbors(1, False, -1) # get all neighbors
        options: list[BaseAgent] = [] # list of options

        match self.direction: # it can move to a road that is pointing outwards (not inwards)
            case Direction.UP.value: # checks all the "upstairs" roads
                
                if (neighbors[Neighbors.Top_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Left.value], Destination) or 
                    neighbors[Neighbors.Top_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Top_Left.value].direction == Direction.UP.value)):
                    # Top left

                    options.append(neighbors[Neighbors.Top_Left.value]) # add the road to the list of options

                if (neighbors[Neighbors.Top_Center.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Center.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Center.value], Destination) or 
                    neighbors[Neighbors.Top_Center.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Top_Center.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Top_Center.value].direction == Direction.LEFT.value)):
                    # Top center

                    options.append(neighbors[Neighbors.Top_Center.value])

                if (neighbors[Neighbors.Top_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Right.value], Destination) or
                    neighbors[Neighbors.Top_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Top_Right.value].direction == Direction.UP.value)):
                    # Top right

                    options.append(neighbors[Neighbors.Top_Right.value])

            case Direction.LEFT.value: # checks all the left roads

                if (neighbors[Neighbors.Top_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Left.value], Destination) or 
                    neighbors[Neighbors.Top_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Top_Left.value].direction == Direction.UP.value)):
                    # Top left

                    options.append(neighbors[Neighbors.Top_Left.value]) # add the road to the list of options

                if (neighbors[Neighbors.Middle_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Middle_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Middle_Left.value], Destination) or 
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.LEFT.value or 
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Middle_Left.value].direction == Direction.DOWN.value)):
                    # Middle left

                    options.append(neighbors[Neighbors.Middle_Left.value])

                if (neighbors[Neighbors.Bottom_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Left.value], Destination) or
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.DOWN.value)):
                    # Bottom left

                    options.append(neighbors[Neighbors.Bottom_Left.value])

            case Direction.RIGHT.value: # checks all the right roads

                if (neighbors[Neighbors.Top_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Top_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Top_Right.value], Destination) or
                    neighbors[Neighbors.Top_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Top_Right.value].direction == Direction.UP.value)):
                    # Top right

                    options.append(neighbors[Neighbors.Top_Right.value]) # add the road to the list of options

                if (neighbors[Neighbors.Middle_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Middle_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Middle_Right.value], Destination) or 
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.UP.value or  
                    neighbors[Neighbors.Middle_Right.value].direction == Direction.DOWN.value)):
                    # Middle right

                    options.append(neighbors[Neighbors.Middle_Right.value])

                if (neighbors[Neighbors.Bottom_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Right.value], Destination) or 
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.DOWN.value)):
                    # Bottom right

                    options.append(neighbors[Neighbors.Bottom_Right.value])
              
            case Direction.DOWN.value: # checks all the "downstairs" roads

                if (neighbors[Neighbors.Bottom_Left.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Left.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Left.value], Destination) or
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Left.value].direction == Direction.DOWN.value)):
                    # Bottom left

                    options.append(neighbors[Neighbors.Bottom_Left.value]) # add the road to the list of options

                if (neighbors[Neighbors.Bottom_Center.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Center.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Center.value], Destination) or 
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.RIGHT.value or 
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.LEFT.value or  
                    neighbors[Neighbors.Bottom_Center.value].direction == Direction.DOWN.value)):
                    # Bottom center

                    options.append(neighbors[Neighbors.Bottom_Center.value])

                if (neighbors[Neighbors.Bottom_Right.value] is not None and 
                    isinstance(neighbors[Neighbors.Bottom_Right.value], (Destination, Road)) and
                    (isinstance(neighbors[Neighbors.Bottom_Right.value], Destination) or 
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.RIGHT.value or  
                    neighbors[Neighbors.Bottom_Right.value].direction == Direction.DOWN.value)):
                    # Bottom right

                    options.append(neighbors[Neighbors.Bottom_Right.value])

        self.roads = options # set the roads this road can go to

    def cookRoutes(self, cache: JsonSave): # Waze-like algorithm pt.2

        start = self

        for destination in destinationsList: 
            # cache the routes
            cachedRoute = cache.getRoute(self.pos, destination.pos) 
            if cachedRoute is not None: 
                self.routes[destination.pos.toString()] = cachedRoute
                continue

            # Future cells is a priority queue (road, priority)
            future_cells: list[tuple[Road, int]] = []
            future_cells.append((start, 0))
            past_cells: dict[Road, Road] = {} # dictionary of (current, come_from)
            cost_so_far = {start: 0}

            while len(future_cells) != 0: # while there are still cells to check
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

            route: list[Pos] = [destination.pos] # list of positions that make up the route
            actual = destination # the actual cell we are in
            while actual != start: # while we are not in the starting cell
                last_cell = past_cells[actual]
                route.insert(0, last_cell.pos)
                actual = last_cell
            
            route.pop(0) # remove starting pos

            self.routes[destination.pos.toString()] = route # add the route to the list of routes

            cache.addRoute(self.pos, destination.pos, route) # add the route to the cache
            
    def getRoute(self, destination: 'Destination') -> list[Pos]:
        if isinstance(destination, Destination):
            return self.routes[destination.pos.toString()]
        else:
            raise TypeError("The destination is not a destination.")

class Destination(Agents.StaticAgent): # this will work as an appender for the destinations list
    def __init__(self, board: Board, pos: Pos):
        super().__init__(board, pos, "Destination", 0, False)
        destinationsList.append(self)

class Building(Agents.StaticAgent): # set the buildings
    def __init__(self, board: Board, pos: Pos):
        super().__init__(board, pos, "Building", 0, False)

class Stoplight(Agents.SimulatedAgent):
    def __init__(self, board: Board, pos: Pos, state: bool):
        super().__init__(board, pos, "Stoplight_go", 2, False)
        self.counter = 0

        if state:
            self.state = "Stoplight_stop"
        else:
            self.state = "Stoplight_go"

    def step(self):
        self.counter += 1

        # when the couter reaches 5, change the state and reset the counter
        
        if self.counter == 5 and self.state == "Stoplight_stop": 
            self.state = "Stoplight_go" 
            self.counter = 0

        elif self.counter == 5 and self.state == "Stoplight_go":
            self.state = "Stoplight_stop"
            self.counter = 0

class Car(Agents.SimulatedAgent):
    destination: Destination # grab a destination
 
    path: list[Pos] = [] # list of positions that make up the path

    desiredPos: Pos

    desperation: int = 0 # the higher the number the more CDMX-like the driver is

    def __init__(self, board: Board):
        choices = [
            # corners of the map
            Pos(0, 0),
            Pos(0, board.getHeight() - 1),
            Pos(board.getWidth() - 1, 0),
            Pos(board.getWidth() - 1, board.getHeight() - 1)
        ]
        #spawnIn = random.choice(choices)

        for i in range(4): # try to spawn in a corner
            spawnIn = random.choice(choices)
            if board.agent_get(spawnIn, 1, False) is None:
                break
            choices.remove(spawnIn)

        super().__init__(board, spawnIn, "Car", 1, False)

        self.destination = random.choice(destinationsList) # pick a random destination

        self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination) # check Waze
 
        self.desiredPos = self.pos 

        self.desperation = 0 # relax

    def step(self):
        if isinstance(self.board.agent_get(self.pos, 0, False), Destination):
            self.board.specialValues["total_cars_arrived"] += 1
            self.kill() # if the bike is in a destination, then kill it... sorry :(
            return

        if self.desiredPos != self.pos: # if this runs, then it means someone got in their way
            self.desiredPos = self.pos
            self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination) # recalculate just in case
            self.desperation += 1 # GET INTENSE
        else:
            self.desperation = 0 # relax

        if self.desperation > 1:
            choices = []
            for i in self.board.agent_get(self.pos, 0, False).roads:
                if not isinstance(self.board.agent_get(self.pos, 0, False), Destination):
                    choices.append(i.pos)
            self.path = [random.choice(choices)]

        if len(self.path) == 0: # if the next position is not in the path
            self.path = self.board.agent_get(self.pos, 0, False).getRoute(self.destination)

            if len(self.path) == 0: # if the path is still empty
                choices = []
                for i in self.board.agent_get(self.pos, 0, False).roads:
                    if not isinstance(self.board.agent_get(self.pos, 0, False), Destination):
                        choices.append(i.pos)
                self.path = [random.choice(choices)]

        nextPos = self.path[0]

        if nextPos == self.pos: # if the next position is the same as the current one
            self.path.pop(0)
            self.step()
            return
        
        # make sure it can only move by one. 
        if not (self.pos.x - 1 <= nextPos.x <= self.pos.x + 1 and self.pos.y - 1 <= nextPos.y <= self.pos.y + 1):
            choices = []
            for i in self.board.agent_get(self.pos, 0, False).roads:
                if not isinstance(self.board.agent_get(self.pos, 0, False), Destination):
                    choices.append(i.pos)
            nextPos = random.choice(choices)
            self.path = [nextPos] # reset the path and recalculate it
        
        stoplight = self.board.agent_get(nextPos, 2, False)

        if not (stoplight is not None and stoplight.state == "Stoplight_stop"): # if there is no one in the way
            self.pos = self.path.pop(0)
            self.desiredPos = nextPos
            