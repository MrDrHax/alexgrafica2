import boardMan as LocalBoard
from fastautomata import APIAttachment

board_width = 21
board_height = 21

fps = 100

data = {
    "drawer": False,
    "map": "../ejemplo/2022_base.txt",
}

board = LocalBoard.createBoard(data)

drawer = APIAttachment(board)

board.specialValues["draw_framerate"] = 1 / fps

drawer.run()
