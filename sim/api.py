import boardMan as LocalBoard
from fastautomata import APIAttachment

data = {
    "drawer": False,
    "map": "../ejemplo/2022_base.txt",
    "spawn_rate": 1,
}

board = LocalBoard.createBoard(data)

drawer = APIAttachment.API(board)

drawer.run()

