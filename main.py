import numpy as np
from copy import deepcopy

from game import Game, BLACK, WHITE
from player import Player

game = Game()
print(game.legal_moves(BLACK))

players = [Player(WHITE), Player(BLACK)]
last_move = np.array([])
running = True
while running:
    for player in players:
        print(game)
        input()
        move = player.play(game.board)
        print("Player:", player.player, "Move:", move)
        game_response = game.move(player.player, move)
        
        if game_response != 0:
            if game_response == BLACK:
                print("Black wins")
            elif game_response == WHITE:
                print("White wins")
            running = False
            break
        if move.size == 0 and last_move.size == 0:
            print("Draw")
            running = False
            break
        if game.end():
            print("Winner:", game.winner())
            running = False
            break
        last_move = move
        
    