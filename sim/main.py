import boardMan as LocalBoard

board_width = 21
board_height = 21

fps = 20

data = {
    "drawer": True,
    "map": "../ejemplo/2022_base.txt",
}

board, drawer = LocalBoard.createBoard(data)

board.specialValues["draw_framerate"] = 1 / fps

drawer.run()

