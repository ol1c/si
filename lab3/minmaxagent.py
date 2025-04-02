from exceptions import AgentException


class MinMaxAgent :
    def __init__(self, my_token='o'):
        self.my_token = my_token
        if my_token == 'o':
            self.enemy_token = 'x'
        else:
            self.enemy_token = 'o'

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return self.minmax_decide(connect4)

    def possible_drops(self, board, width):
        return [n_column for n_column in range(width) if board[0][n_column] == '_']

    def iter_fours(self, board, width, height):
        # horizontal
        for n_row in range(height):
            for start_column in range(width - 3):
                yield board[n_row][start_column:start_column + 4]

        # vertical
        for n_column in range(width):
            for start_row in range(height - 3):
                yield [board[n_row][n_column] for n_row in range(start_row, start_row + 4)]

        # diagonal
        for n_row in range(height - 3):
            for n_column in range(width - 3):
                yield [board[n_row + i][n_column + i] for i in range(4)]  # decreasing
                yield [board[n_row + i][width - 1 - n_column - i] for i in range(4)]  # increasing

    def _check_game_over(self, board, connect4):
        if not self.possible_drops(board, connect4.width):
            return 0  # tie
        wins = '_'
        for four in self.iter_fours(board, connect4.width, connect4.height):
            if four == ['o', 'o', 'o', 'o']:
                wins = 'o'
                break
            elif four == ['x', 'x', 'x', 'x']:
                wins = 'x'
                break

        if wins == self.my_token:
            return 1
        elif wins == self.enemy_token:
            return -1
        return None

    def _update_h(self, token, my_best, enemy_best, x):
        if token == self.my_token:
            if my_best < x:
                my_best = x
        elif token == self.enemy_token:
            if enemy_best < x:
                enemy_best = x
        return my_best, enemy_best, 0

    def h(self, board, connect4):
        token = '_'
        my_best = 0
        enemy_best = 0
        tmp = 0

        for n_row in range(connect4.height):
            for n_column in range(connect4.width):
                if token != board[n_row][n_column]:
                    my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)
                    token = board[n_row][n_column]
                tmp += 1
            my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)

        for n_column in range(connect4.width):
            for n_row in range(connect4.height):
                if token != board[n_row][n_column]:
                    my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)
                    token = board[n_row][n_column]
                tmp += 1
            my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)

        for n_row in range(connect4.height - 3):
            for n_column in range(connect4.width - 3):
                for i in range(4):
                    if token != board[n_row + i][n_column + i]:
                        my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)
                        token = board[n_row][n_column]
                    tmp += 1
                my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)
                for i in range(4):
                    if token != board[n_row + i][connect4.width - 1 - n_column - i]:
                        my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)
                        token = board[n_row][n_column]
                    tmp += 1
                my_best, enemy_best, tmp = self._update_h(token, my_best, enemy_best, tmp)

        my_h = my_best/4.0
        enemy_h = enemy_best/4.0
        if my_h >= enemy_h:
            return my_h
        elif enemy_h > my_h:
            return -enemy_h

    def draw_board(self, board):
        for row in board:
            print(' '.join(row))
        print("+++")

    def minmax(self, board, x, d, connect4):
        if d == 0:
            return self.h(board, connect4)
        end_game = self._check_game_over(board, connect4)
        if end_game is not None:
            return end_game

        new_x = int(not x)
        if x == 1:
            token = self.my_token
        else:
            token = self.enemy_token
        possible_moves = self.possible_drops(board, connect4.width)
        args = []
        for possible_move in possible_moves:
            n_row = 0
            while n_row + 1 < connect4.height and board[n_row + 1][possible_move] == '_':
                n_row += 1
            board[n_row][possible_move] = token
            args.append(self.minmax(board, new_x, d-1, connect4))
            board[n_row][possible_move] = '_'

        if x == 1:
            return max(args)
        else:
            return min(args)

    def minmax_decide(self, connect4):
        new_board = [row[:] for row in connect4.board]
        possible_moves = self.possible_drops(new_board, connect4.width)
        v = float('-inf')
        best_move = None
        d = 6
        for possible_move in possible_moves:
            n_row = 0
            while n_row + 1 < connect4.height and new_board[n_row + 1][possible_move] == '_':
                n_row += 1
            new_board[n_row][possible_move] = self.my_token
            tmp = self.minmax(new_board, 0, d-1, connect4)
            new_board[n_row][possible_move] = '_'
            if tmp > v:
                v = tmp
                best_move = possible_move
        return best_move
