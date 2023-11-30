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

