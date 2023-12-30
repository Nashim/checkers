import numpy as np

BOARD_SIZE = 8
EMPTY = 0
BLACK = -1
WHITE = 1

class Game:
    def __init__(self):
        self.reset()
        self.current_player = WHITE

    def __str__(self):
        return str(self.board)
    
    def reset(self):
        self.board = EMPTY*np.ones((BOARD_SIZE, BOARD_SIZE), dtype=int)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i+j)%2 == 1:
                    if i < 3:
                        self.board[i, j] = WHITE
                    elif i > 4:
                        self.board[i, j] = BLACK

    def move(self, player, move):
        if player != self.current_player:
            print("Wrong player")
            return
        self.current_player = -self.current_player
        if move.size == 0:
            if self.legal_moves(player).size != 0:
                print("Wrong move: move available")
            return
        if np.abs(move[0][0] - move[1][0]) == 2:
            self.board[(move[0][0] + move[1][0])//2, (move[0][1] + move[1][1])//2] = EMPTY
        else:
            if self.legal_jump_moves(player).size != 0:
                print("Wrong move: can take a piece")
                return
        self.board[tuple(move[0])] = EMPTY
        self.board[tuple(move[1])] = player
        

    
    def legal_moves(self, player):
        moves = np.empty((0, 2, 2), dtype=int)
        moves = np.append(moves, self.legal_jump_moves(player), axis=0)
        print(moves)
        if moves.size == 0:
            moves = np.append(moves, self.legal_free_moves(player), axis=0)
        return moves
    
    def legal_jump_moves(self, player):
        moves = np.empty((0, 2, 2), dtype=int)
        for piece in np.argwhere(self.board == player):
            moves = np.append(moves, self.legal_jump_moves_for_piece(piece), axis=0)
        return moves
    
    def legal_jump_moves_for_piece(self, piece):
        moves = np.empty((0, 2, 2), dtype=int)
        player = self.board[tuple(piece)]
        if player != EMPTY:
            next_row = piece[0] + player
            land_row = next_row + player
            if land_row < BOARD_SIZE and land_row >= 0:
                if piece[1] + 2 < BOARD_SIZE and piece[1] + 2 >= 0:
                    if self.board[land_row, piece[1] + 2] == EMPTY and self.board[next_row, piece[1] + 1] == -player:
                        moves = np.append(moves, [(tuple(piece), (land_row, piece[1] + 2))], axis=0)
                if piece[1] - 2 < BOARD_SIZE and piece[1] - 2 >= 0:
                    if self.board[land_row, piece[1] - 2] == EMPTY and self.board[next_row, piece[1] - 1] == -player:
                        moves = np.append(moves, [(tuple(piece), (land_row, piece[1] - 2))], axis=0)
        return moves
    
    def legal_free_moves(self, player):
        moves = np.empty((0, 2, 2), dtype=int)
        for piece in np.argwhere(self.board == player):
            moves = np.append(moves, self.legal_free_moves_for_piece(piece), axis=0)
        return moves
    
    def legal_free_moves_for_piece(self, piece):
        moves = np.empty((0, 2, 2), dtype=int)
        player = self.board[tuple(piece)]
        if player != EMPTY:
            next_row = piece[0] + player
            if next_row < BOARD_SIZE and next_row >= 0:
                if piece[1] + 1 < BOARD_SIZE and piece[1] + 1 >= 0:
                    if self.board[next_row, piece[1] + 1] == EMPTY:
                        moves = np.append(moves, [(tuple(piece), (next_row, piece[1] + 1))], axis=0)
                if piece[1] - 1 < BOARD_SIZE and piece[1] - 1 >= 0:
                    if self.board[next_row, piece[1] - 1] == EMPTY:
                        moves = np.append(moves, [(tuple(piece), (next_row, piece[1] - 1))], axis=0)
        return moves
    
    def winner(self):
        if np.sum(self.board == BLACK) == 0:
            return WHITE
        if np.sum(self.board == WHITE) == 0:
            return BLACK
        return EMPTY
    
    def end(self):
        if self.winner() == EMPTY:
            return False
        return True
    
    