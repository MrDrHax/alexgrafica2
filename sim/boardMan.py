"""
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998

Create a new board with the data provided.

    Parameters:
        data (dict): The data to create the board with. Must contain the following required parameters:
            - board_width (int): The width of the board.
            - board_height (int): The height of the board.

    Returns:
        Board.SimulatedBoard: The newly created board.
"""

from fastautomata import Board, Agents, fastautomata_clib
from fastautomata.LocalDraw import LocalDraw
from fastautomata.ClassTypes import Pos
import agents as LocalAgents
import random, hashlib # in case we need it in the future

import requests
import json

from jsonChache import JsonSave

hash = ""


url = "http://52.1.3.19:8585/api/"
endpoint = "attempts"

def createBoard(data: dict) -> Board.SimulatedBoard:

    global hash

    with open(data["map"], "r") as f: #use the map provided
        map = f.readlines()
        data["board_width"] = len(map[0])
        data["board_height"] = len(map)
        hash = hashlib.md5(str(map).encode()).hexdigest()

    board = Board.SimulatedBoard(data["board_width"] - 1, data["board_height"], 3) # separate the layers into 3 layers

    # collisions: map, car, stoplights

    Agents.initialize_agents(board) 

    if "drawer" not in data:
        data["drawer"] = False

    if data["drawer"]:
        drawer = LocalDraw(board, 800, 800)


    # add types
    board.addColor("Road", (30, 30, 30)) # Dark gray
    board.addColor("Building", (180, 100, 255)) # Purple
    board.addColor("Stoplight_go", (0, 200, 0)) # Green
    board.addColor("Stoplight_stop", (255, 50, 50)) # Red
    board.addColor("Car", (40, 140, 240)) # Blue
    board.addColor("Destination", (255, 150, 0)) # Orange


    # add board variables
    board.specialValues["map"] = data["map"]
    board.specialValues["spawn_rate"] = data["spawn_rate"]
    board.specialValues["total_cars_arrived"] = 0

    ### collisions
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
    board.specialValues["total_cars_arrived"] = 0
    LocalAgents.boardReset(board)
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
                        LocalAgents.Stoplight(board, pos, mapB[row][col] == 'S')
                        LocalAgents.Road(board, pos, "O")
                    case "<" | ">" | "^" | "v":
                        LocalAgents.Road(board, pos, mapB[row][col])
    
    # Calculate the road paths (where they can go and where they can't)
    for road in LocalAgents.roadsList:
        road.convertToRoad()

    for road in LocalAgents.roadsList:
        road.calculateRoads()

    cachedRoutes = JsonSave(f"cache/{hash}.json")

    print("Cooking routes... This might take a while.")
    print("calculating \r(x, y)", end="")
    for road in LocalAgents.roadsList:
        print(f"\r({road.pos.x}, {road.pos.y})..........", end="")
        road.cookRoutes(cachedRoutes)

    print("\nDone! Saving routes...")

    # cachedRoutes.save()

    spawnCar(board)

count = 0

def spawnCar(board: Board.SimulatedBoard): 
    # spawn a car every certain steps
    global count
    count += 1
    if count > board.specialValues["spawn_rate"]:
        try:
            count = 0
            LocalAgents.Car(board)
            LocalAgents.Car(board)
            LocalAgents.Car(board)
            LocalAgents.Car(board)
            print(f"Spawned 4 cars! At interval {count}")
        except:
            pass
            # print("No more cars can be spawned. (crash!)")
            # board.simulated = False
    
    # try:
    #     LocalAgents.Car(board)
    # except:
    #     pass

    if board.step_count == 1000:
        board.simulated = False
        print(f"Simulation ended. (1000 steps), total cars arrived: {board.specialValues['total_cars_arrived']}")

    if board.step_count == 1000:

        data = {
            "year" : 2023,
            "classroom" : 301,
            "name" : "Alex² corregido",
            "num_cars": board.specialValues["total_cars_arrived"],
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)

        if not response.status_code == 200:
            print("Error, plz debug api!")