from fastautomata import Board, Agents, fastautomata_clib
from fastautomata.LocalDraw import LocalDraw
from fastautomata.ClassTypes import Pos
import agents as LocalAgents
import random

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

    # TODO leer desde el mapa

    # data["board_width"] = 
    # data["board_height"] = 

    board = Board.SimulatedBoard(data["board_width"], data["board_height"], 3)

    # collisions: map, car, stoplights

    Agents.initialize_agents(board)

    if "drawer" not in data:
        data["drawer"] = False

    if data["drawer"]:
        drawer = LocalDraw(board, 800, 800)

    # Layers: food, obstacles, bases, roomba

    # add types
    board.addColor("Road", (50, 50, 50))

    # add board variables
    obstacles = int(data["board_height"] * data["board_width"] * data["obstacles"])

    board.specialValues["obstacles"] = obstacles
    board.specialValues["FinishState"] = "None"

    # collisions
    # car to stoplight
    board.layer_collisions.addCollision(fastautomata_clib.CollisionType.SOLID, 1, 2)
    # car to map
    board.layer_collisions.addCollision(fastautomata_clib.CollisionType.TRIGGER, 1, 0)

    # add agents
    board.append_on_reset(addAgents)

    if data["drawer"]:
        return board, drawer
    return board


def addAgents(board: Board.SimulatedBoard):
    '''
    Add the agents to the board.
    '''

    # TODO leer el mapa