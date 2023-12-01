"""
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998
Controlls the spawning of the agents
"""

import boardMan as LocalBoard

fps = 200

data = {
    "drawer": True,
    "map": "../ejemplo/2023.txt",
    "spawn_rate": 0,
}

board, drawer = LocalBoard.createBoard(data)

board.specialValues["draw_framerate"] = 1 / fps

drawer.run()

