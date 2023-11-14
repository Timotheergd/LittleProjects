from chessgame import Game

g = Game()

import datetime
now = datetime.datetime.now()

import os
position = (0, 0)
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    