import numpy as np

BOARD_SIZE = 8
EMPTY = 0
BLACK = -1
WHITE = 1
MAX_STONES = 12
MAX_MOVE_LEN = MAX_STONES+1
MOVE_END = (-1, -1)
NO_MOVE = 2

class Game:
    def __init__(self):
        self.reset()
        self.current_player = WHITE

    def __str__(self):
        return str(self.board)
    
    def reset(self):
        self.board = EMPTY*np.ones((BOARD_SIZE, BOARD_SIZE), dtype=int)
        """
        self.board[1, 2] = WHITE
        self.board[2, 1] = BLACK
        self.board[2, 3] = BLACK
        self.board[4, 3] = BLACK"""
        
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
            return player
        self.current_player = -self.current_player
        legal_moves = self.legal_moves(player)
        
        if move.size == 0:
            if legal_moves != 0:
                print("Wrong move: move available")
                return player
            else:
                return NO_MOVE
        
        if not np.any(np.all(legal_moves == move, axis=(1,2))):
            print("Wrong move: illegal move")
            return player
        if np.all(move[1] == MOVE_END):
            self.board[tuple(move[1])] = player
        else:
            for i in range(0, move.shape[0]):
                if np.all(move[i] == MOVE_END):
                    self.board[tuple(move[i-1])] = player
                    break
                self.board[(move[i][0] + move[i+1][0])//2, (move[i][1] + move[i+1][1])//2] = EMPTY
            
        self.board[tuple(move[0])] = EMPTY
        return 0
        
    def legal_moves(self, player):
        moves = self.legal_jump_moves(player)
        if moves.size == 0:
            moves = self.legal_free_moves(player)
        return moves
    
    def legal_jump_moves(self, player):
        moves = np.empty((0, MAX_MOVE_LEN, 2), dtype=int)
        for piece in np.argwhere(self.board == player):
            moves = np.append(moves, self.legal_jump_moves_for_piece(piece), axis=0)
        return moves
    
    def legal_jump_moves_for_piece(self, piece):
        moves = self.find_next_jump([piece], self.board[tuple(piece)])
        return moves
    
    def find_next_jump(self, move, player):
        moves = np.empty((0, MAX_MOVE_LEN, 2), dtype=int)
        next_row = move[-1][0] + player
        land_row = next_row + player
        next_moves = np.empty((0, MAX_MOVE_LEN, 2), dtype=int)
        if land_row < BOARD_SIZE and land_row >= 0:
            for dir in [-1, 1]:
                if move[-1][1] + dir*2 < BOARD_SIZE and move[-1][1] + dir*2 >= 0:
                    if self.board[land_row, move[-1][1] + dir*2] == EMPTY and self.board[next_row, move[-1][1] + dir] == -player:
                        new_move = np.append(move, [(land_row, move[-1][1] + dir*2)], axis=0)
                        next_moves = self.find_next_jump(new_move, player)
                        if next_moves.size == 0:
                            next_moves = np.array([new_move])
                        next_moves = np.pad(next_moves, ((0, 0), (0, MAX_MOVE_LEN - next_moves.shape[1]), (0, 0)), 'constant', constant_values=MOVE_END)
                        moves = np.append(moves, next_moves, axis=0)
        return moves
    
    def legal_free_moves(self, player):
        moves = np.empty((0, MAX_MOVE_LEN, 2), dtype=int)
        for piece in np.argwhere(self.board == player):
            moves = np.append(moves, self.legal_free_moves_for_piece(piece), axis=0)
        return moves
    
    def legal_free_moves_for_piece(self, piece):
        moves = np.empty((0, MAX_MOVE_LEN, 2), dtype=int)
        player = self.board[tuple(piece)]
        if player != EMPTY:
            next_row = piece[0] + player
            if next_row < BOARD_SIZE and next_row >= 0:
                for dir in [-1, 1]:
                    if piece[1] + dir < BOARD_SIZE and piece[1] + dir >= 0:
                        if self.board[next_row, piece[1] + dir] == EMPTY:
                            move = np.array([(tuple(piece), (next_row, piece[1] + dir))])
                            move = np.pad(move,((0,0), (0, MAX_MOVE_LEN-move.shape[1]), (0, 0)) , 'constant', constant_values=MOVE_END)
                            moves = np.append(moves, move, axis=0)
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
    
    