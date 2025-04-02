from minmaxagent import MinMaxAgent


class AlphaBetaAgent(MinMaxAgent):
    def __init__(self, my_token='o'):
        super().__init__(my_token)

    def minmax_decide(self, connect4):
        new_board = [row[:] for row in connect4.board]
        possible_moves = self.possible_drops(new_board, connect4.width)
        alfa = float('-inf')
        v = float('-inf')
        best_move = None
        d = 6
        for possible_move in possible_moves:
            n_row = 0
            while n_row + 1 < connect4.height and new_board[n_row + 1][possible_move] == '_':
                n_row += 1
            new_board[n_row][possible_move] = self.my_token
            tmp = self.alfabeta(new_board, 0, d - 1, alfa, float('inf'), connect4)
            new_board[n_row][possible_move] = '_'
            if tmp > v:
                v = tmp
                best_move = possible_move
            alfa = max(alfa, v)
        return best_move

    def alfabeta(self, board, x, d, alfa, beta, connect4):
        if d == 0:
            return self.h(board, connect4)
        end_game = self._check_game_over(board, connect4)
        if end_game is not None:
            return end_game

        possible_moves = self.possible_drops(board, connect4.width)
        new_x = int(not x)
        if x == 1:
            v = float('-inf')
            for possible_move in possible_moves:
                n_row = 0
                while n_row + 1 < connect4.height and board[n_row + 1][possible_move] == '_':
                    n_row += 1
                board[n_row][possible_move] = self.my_token
                v = max(v, self.minmax(board, new_x, d - 1, connect4))
                alfa = max(alfa, v)
                board[n_row][possible_move] = '_'
                if v >= beta:
                    break
        else:
            v = float('inf')
            for possible_move in possible_moves:
                n_row = 0
                while n_row + 1 < connect4.height and board[n_row + 1][possible_move] == '_':
                    n_row += 1
                board[n_row][possible_move] = self.enemy_token
                v = min(v, self.minmax(board, new_x, d - 1, connect4))
                beta = min(beta, v)
                board[n_row][possible_move] = '_'
                if v <= alfa:
                    break
        return v
