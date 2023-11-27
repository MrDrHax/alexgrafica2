from fastautomata import Board, Agents, fastautomata_clib
from fastautomata.LocalDraw import LocalDraw
from fastautomata.ClassTypes import Pos
import agents as LocalAgents
import random, hashlib

from jsonChache import JsonSave

hash = ""

def createBoard(data: dict) -> Board.SimulatedBoard:
    '''
    Create a new board with the data provided.

    Parameters:
        data (dict): The data to create the board with. Must contain the following required parameters:
            - board_width (int): The width of the board.
            - board_height (int): The height of the board.

    Returns:
        Board.SimulatedBoard: The newly created board.
    '''

    global hash

    with open(data["map"], "r") as f:
        map = f.readlines()
        data["board_width"] = len(map[0])
        data["board_height"] = len(map)
        hash = hashlib.md5(str(map).encode()).hexdigest()

    board = Board.SimulatedBoard(data["board_width"] - 1, data["board_height"], 3)

    # collisions: map, car, stoplights

    Agents.initialize_agents(board)

    if "drawer" not in data:
        data["drawer"] = False

    if data["drawer"]:
        drawer = LocalDraw(board, 800, 800)

    # Layers: food, obstacles, bases, roomba

    # add types
    board.addColor("Road", (50, 50, 50))
    board.addColor("Building", (150, 255, 30))
    board.addColor("Stoplight_go", (0, 255, 0))
    board.addColor("Stoplight_stop", (255, 0, 0))
    board.addColor("Car", (0, 0, 255))
    board.addColor("Destination", (255, 255, 0))

    # add board variables
    board.specialValues["map"] = data["map"]
    board.specialValues["spawn_rate"] = 1

    # collisions
    # car to stoplight
    board.layer_collisions.addCollision(fastautomata_clib.CollisionType.TRIGGER, 1, 2)
    # car to map
    board.layer_collisions.addCollision(fastautomata_clib.CollisionType.TRIGGER, 1, 0)

    # add agents
    board.append_on_reset(addAgents)

    # add the car summoner
    board.step_instructions_add(spawnCar)

    if data["drawer"]:
        return board, drawer
    return board


def addAgents(board: Board.SimulatedBoard):
    '''
    Add the agents to the board.
    '''
    global hash
    with open(board.specialValues["map"], "r") as f:
        mapB = f.readlines()

        for row in range(len(mapB)):
            for col in range(len(mapB[row])):
                pos = Pos(col, board.getHeight() - row - 1)
                match mapB[row][col]:
                    case "#":
                        LocalAgents.Building(board, pos)
                    case "D":
                        LocalAgents.Destination(board, pos)
                    case "S" | "s":
                        LocalAgents.Stoplight(board, pos) # FIXME stoplight with s is vertical, and S is horizontal
                        LocalAgents.Road(board, pos, "O")
                    case "<" | ">" | "^" | "v":
                        LocalAgents.Road(board, pos, mapB[row][col])
    
    # Calculate the road paths (where they can go and where they can't)
    for road in LocalAgents.roadsList:
        road.convertCrazyToRoad()

    for road in LocalAgents.roadsList:
        road.calculateRoads()

    cachedRoutes = JsonSave(f"cache/{hash}.json")

    print("Cooking routes... This might take a while.")
    print("calculating \r(x, y)", end="")
    for road in LocalAgents.roadsList:
        print(f"\r({road.pos.x}, {road.pos.y})..........", end="")
        road.cookRoutes(cachedRoutes)

    print("\nDone! Saving routes...")

    cachedRoutes.save()

    spawnCar(board)

count = 0

def spawnCar(board: Board.SimulatedBoard):
    global count
    count += 1
    if count > board.specialValues["spawn_rate"]:
        try:
            LocalAgents.Car(board)
            count = 0
        except:
            print("No more cars can be spawned. (crash!)")
            board.simulated = False