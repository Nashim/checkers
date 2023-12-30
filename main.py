import numpy as np
from copy import deepcopy

from game import Game, BLACK, WHITE, NO_MOVE
from player import Player

game = Game()

players = [Player(WHITE), Player(BLACK)]
prev_game_response = 0

running = True
print(game)
while running:
    for player in players:
        input()
        move = player.play(game.board)
        print("Player:", player.player, "Move:",)

        game_response = game.move(player.player, move)
        print(game)
        
        if game_response == WHITE:
            print("Black wins")
            running = False
            break
        elif game_response == BLACK:
            print("White wins")
            running = False
            break
        elif game_response == NO_MOVE and prev_game_response == NO_MOVE:
            print("Draw")
            running = False
            break
        
        if game.end():
            print("Winner:", "White" if game.winner() == WHITE else "Black")
            running = False
            break
        prev_game_response = game_response
        
    