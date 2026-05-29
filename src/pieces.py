"""Module contenant les classes de pièces d'échecs."""

from __future__ import annotations
from abc import ABC, abstractmethod
from .position import Position


WHITE = 0
BLACK = 1


class Piece(ABC):
    """Classe abstraite représentant une pièce d'échecs.

    Attributes:
        position (Position): position actuelle.
        color (int): 0 pour blanc, 1 pour noir.
    """

    symbol = "?"

    def __init__(self, position: Position, color: int):
        self.position = position
        self.color = color

    def is_enemy_at(self, new_position: Position, board: "Board") -> bool:
        """Retourne True si une pièce adverse est sur la case."""
        target = board.getPiece(new_position)
        return target is not None and target.color != self.color

    def is_own_piece_at(self, new_position: Position, board: "Board") -> bool:
        """Retourne True si une pièce alliée est sur la case."""
        target = board.getPiece(new_position)
        return target is not None and target.color == self.color

    def basic_destination_ok(self, new_position: Position, board: "Board") -> bool:
        """Vérifie qu'on ne reste pas sur place et qu'on ne capture pas une pièce alliée."""
        return self.position != new_position and not self.is_own_piece_at(new_position, board)

    @abstractmethod
    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        """Retourne True si le déplacement respecte les règles de la pièce."""
        raise NotImplementedError

    def get_image_key(self) -> str:
        """Retourne la clé d'image, par exemple Kw, Qb, Pw."""
        color_letter = "w" if self.color == WHITE else "b"
        return self.symbol + color_letter

    def __str__(self) -> str:
        return self.symbol.upper() if self.color == WHITE else self.symbol.lower()


class King(Piece):
    """Roi : se déplace d'une case dans toutes les directions."""

    symbol = "K"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False
        dc, dr = self.position.delta(newPosition)
        return max(abs(dc), abs(dr)) == 1


class Queen(Piece):
    """Reine : se déplace en ligne, colonne ou diagonale."""

    symbol = "Q"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False
        dc, dr = self.position.delta(newPosition)
        straight = dc == 0 or dr == 0
        diagonal = abs(dc) == abs(dr)
        return (straight or diagonal) and board.is_path_clear(self.position, newPosition)


class Bishop(Piece):
    """Fou : se déplace uniquement en diagonale."""

    symbol = "B"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False
        dc, dr = self.position.delta(newPosition)
        return abs(dc) == abs(dr) and board.is_path_clear(self.position, newPosition)


class Knight(Piece):
    """Cavalier : se déplace en L et peut sauter au-dessus des pièces."""

    symbol = "N"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False
        dc, dr = self.position.delta(newPosition)
        return (abs(dc), abs(dr)) in [(1, 2), (2, 1)]


class Rook(Piece):
    """Tour : se déplace horizontalement ou verticalement."""

    symbol = "R"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False
        dc, dr = self.position.delta(newPosition)
        return (dc == 0 or dr == 0) and board.is_path_clear(self.position, newPosition)


class Pawn(Piece):
    """Pion : avance d'une case, deux cases au départ, capture en diagonale.

    Les déplacements spéciaux ne sont pas implémentés : promotion et prise en passant.
    """

    symbol = "P"

    def isValidMove(self, newPosition: Position, board: "Board") -> bool:
        if not self.basic_destination_ok(newPosition, board):
            return False

        dc, dr = self.position.delta(newPosition)
        direction = 1 if self.color == WHITE else -1
        start_row = 2 if self.color == WHITE else 7
        target = board.getPiece(newPosition)

        # Avancer d'une case si la case est vide.
        if dc == 0 and dr == direction and target is None:
            return True

        # Avancer de deux cases depuis la ligne de départ si le chemin est libre.
        if dc == 0 and self.position.row == start_row and dr == 2 * direction and target is None:
            return board.is_path_clear(self.position, newPosition)

        # Capture diagonale.
        if abs(dc) == 1 and dr == direction and target is not None and target.color != self.color:
            return True

        return False


PIECE_CLASSES = {
    "K": King,
    "Q": Queen,
    "B": Bishop,
    "N": Knight,
    "R": Rook,
    "P": Pawn,
}


if __name__ == "__main__":
    from board import Board

    board = Board()
    pawn = board.getPiece(Position.from_string("e2"))
    print(f"Pièce en e2 : {pawn}")  # attendu : P
    print("e2 vers e4 :", pawn.isValidMove(Position.from_string("e4"), board))  # attendu : True
    print("Tests Pieces OK !")
