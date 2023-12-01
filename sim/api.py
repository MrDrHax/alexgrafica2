"""
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998

Fast-automata's API
"""


import boardMan as LocalBoard
from fastautomata import APIAttachment

data = {
    "drawer": False,
    "map": "../ejemplo/2023.txt",
    "spawn_rate": 2,
}

board = LocalBoard.createBoard(data)

drawer = APIAttachment.API(board)

drawer.run()

