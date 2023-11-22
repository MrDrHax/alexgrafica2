import boardMan as LocalBoard

board_width = 21
board_height = 21

fps = 10

data = {
    "board_width": board_width,
    "board_height": board_height,
    "drawer": True
}

board, drawer = LocalBoard.createBoard(data)

board.specialValues["draw_framerate"] = 1 / fps

drawer.run()

