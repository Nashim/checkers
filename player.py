import numpy as np
from copy import deepcopy

from game import Game, BLACK, WHITE


class Player(Game):
    def __init__(self, player):
        self.player = player

    def play(self, board):
        self.board = deepcopy(board)
        moves = self.legal_moves(self.player)
        if moves.size == 0:
            return np.array([])
        return moves[np.random.randint(len(moves))]