"""Module contenant Player et AIPlayer."""

import random
from .position import Position


class Player:
    """Représente un joueur humain.

    Attributes:
        name (str): nom du joueur.
        color (int): 0 pour blanc, 1 pour noir.
    """

    def __init__(self, name: str, color: int):
        self.name = name
        self.color = color

    def askMove(self) -> str:
        """Demande au joueur son prochain coup."""
        return input(f"{self.name}, entre ton coup : ").strip()


class AIPlayer(Player):
    """Joueur IA simple générant un déplacement aléatoire."""

    def askMove(self, board=None) -> str:
        """Génère un coup aléatoire parmi les coups pseudo-valides."""
        if board is None:
            return super().askMove()

        own_pieces = [piece for piece in board.grid.values() if piece.color == self.color]
        random.shuffle(own_pieces)

        all_positions = [Position(col, row) for col in Position.COLUMNS for row in range(1, 9)]
        random.shuffle(all_positions)

        for piece in own_pieces:
            for target in all_positions:
                if piece.isValidMove(target, board):
                    return f"{piece.symbol}{piece.position} {target}"

        return "quit"


if __name__ == "__main__":
    p = Player("Alice", 0)
    print(f"Joueur créé : {p.name}, couleur : {p.color}")
    print("Tests Player OK !")
