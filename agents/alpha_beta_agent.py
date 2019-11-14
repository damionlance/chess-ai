from agents.base_agent import BaseAgent
from random import shuffle


class AlphaBetaAgent(BaseAgent):
    def __init__(self, color, heuristic, maximum_depth):
        super().__init__(color)
        self.heuristic = heuristic
        self.maximum_depth = maximum_depth

    def get_move(self, board):
        current_depth = 0
        possible_moves = [move for move in board.legal_moves]
        shuffle(possible_moves)
        best_move = None
        best_score = float('-inf')

        for move in possible_moves:
            board.push_uci(move.uci())

            if board.is_checkmate() and board.turn != self.color:
                return move

            score = self.alpha_beta(board, self.heuristic, float('-inf'), float('inf'), False, current_depth + 1, self.maximum_depth)
            board.pop()

            if score > best_score:
                # print(score)
                # print(move)
                best_score = score
                best_move = move

        # print("AlphaBeta:",best_score)
        return best_move

    def alpha_beta(self, board, heuristic, alpha, beta, max_turn, current_depth, maximum_depth):

        if current_depth == maximum_depth or board.is_game_over():
            return heuristic(board, self.color)

        possible_moves = [move for move in board.legal_moves]
        shuffle(possible_moves)

        best_score = float('-inf') if max_turn else float('inf')
        for move in possible_moves:
            board.push_uci(move.uci())
            score = self.alpha_beta(board, heuristic, alpha, beta, not max_turn, current_depth+1, maximum_depth)
            board.pop()

            if max_turn and score > best_score:
                best_score = score
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)

            if not max_turn and score < best_score:
                best_score = score
                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)



        return best_score


    def move_ordering(self, moves, board, max_turn, color):
        move_values = []
        for move in moves:
            board.push_uci(move.uci())
            score = self.heuristic(board, color)
            move_values.append({'move':move, 'value':score})
            board.pop()

        ordered = sorted(move_values, key=lambda x:x['value'], reverse=True if max_turn else False)
        return [x['move'] for x in ordered]
