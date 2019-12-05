"""
Add heuristics here
"""
from chess import *
from typing import Dict, List
import collections


def piece_value_heuristic(board: Board, color: bool, max_turn) -> int:
    score = 0
    opponent = not color
    board_size: int = 64

    for tile in range(0, board_size):
        current_piece = board.piece_at(tile)
        score = score + get_piece_value(current_piece, color)

    return score


def get_piece_value(piece: Piece, color: bool) -> int:
    if piece is None:
        return 0

    piece_values: Dict[str, int] = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 100}

    value = 0

    value = piece_values[piece.symbol().upper()]

    if piece.color != color:
        value = value * -1

    return value


def general_mobility(board: Board, max_turn: bool) -> int:
    piece_mobility_values = {PAWN: 4, KNIGHT: 8, BISHOP: 8, ROOK: 5, QUEEN: 3, KING: 2}
    moves = [move.from_square for move in board.legal_moves]
    move_count = collections.Counter(moves)
    mobility_score = 0
    for move in move_count.keys():
        piece = board.piece_at(move)
        num_moves = move_count[move]
        mobility_score += num_moves * piece_mobility_values[piece.piece_type]

    if not max_turn:
        mobility_score = mobility_score * -1

    return mobility_score


# Find potential victims -> then for each victim find least valuable aggressor
def mvvlva(board: Board, color: bool):
    pieces = PIECE_TYPES[:-1]
    mvv_locations = []
    moves = []
    # Victim cycle -> find MVV
    for piece in pieces[::-1]:
        # Get the location(s) of the given piece type for the opponent
        location = board.pieces(piece, not color)
        attackers = []
        if len(location) > 0:
            # Check to see that mvv can be attacked
            for l in location:
                attkr_locations = board.attackers(color, l)
                attackers += list(attkr_locations)
            if len(attackers) > 0:
                mvv_locations = location
                break

    if len(attackers) > 0:
        # Aggressor Cycle -> find the least valuable aggressor for the victim
        for l in mvv_locations:
            piece_to_location = [{"piece": board.piece_at(x), "from_square": x, "to_square": l} for x in attackers]
            sorted_pieces = sorted(piece_to_location, key=lambda x: x['piece'].piece_type)
            for x in sorted_pieces:
                m = Move(x['from_square'], x['to_square'])
                if board.is_legal(m):
                    moves.append(m)
    return moves


def combined(board: Board, color: bool, max_turn: bool) -> int:
    score = piece_value_heuristic(board, color, max_turn) + general_mobility(board, max_turn)
    return score


def sort_non_captures(history, turn, moves, board):
    # sort moves by hh:
    moves_to_values = []
    for m in moves:
        p = board.piece_at(m.from_square).piece_type
        val = history[turn][p][m.to_square]
        moves_to_values.append({'move': m, 'val': val})

    sorted_non_caps = sorted(moves_to_values, key=lambda x: x['val'], reverse=True)
    return [m['move'] for m in sorted_non_caps]


def get_possible_moves(board, turn, history=None):
    """
    returns a list of possible moves that can be made by the agent
    uses mvvlva and history table for move ordering
    :param board: the current board
    :param turn: bool
    :param history: history_table for agent
    :return: list of move objects
    """
    #TODO add in PV and Trans-table stuff to happen before captures

    # Get sorted capture moves:
    captures = mvvlva(board, turn)

    # get non-captures:
    non_captures = [move for move in board.legal_moves if move not in captures]

    # sort non_captures with HH:
    sorted_non_caps = sort_non_captures(history, turn, non_captures, board)

    move_list = captures + sorted_non_caps

    return move_list


