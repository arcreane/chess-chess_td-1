"""Module contenant la classe Board."""

from .position import Position
from .pieces import WHITE, BLACK, King, Queen, Bishop, Knight, Rook, Pawn, PIECE_CLASSES


class Board:
    """Représente l'état de l'échiquier.

    Attributes:
        grid (dict[str, Piece]): dictionnaire associant une case, par exemple 'e4',
        à une pièce.
    """

    def __init__(self, setup: bool = True):
        self.grid = {}
        if setup:
            self.setup_initial_position()

    def setup_initial_position(self) -> None:
        """Place toutes les pièces à leur position initiale."""
        self.grid.clear()

        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for index, piece_cls in enumerate(order):
            column = Position.COLUMNS[index]
            self.place_piece(piece_cls(Position(column, 1), WHITE))
            self.place_piece(Pawn(Position(column, 2), WHITE))
            self.place_piece(Pawn(Position(column, 7), BLACK))
            self.place_piece(piece_cls(Position(column, 8), BLACK))

    def place_piece(self, piece: "Piece") -> None:
        """Place une pièce sur sa position actuelle."""
        self.grid[str(piece.position)] = piece

    def getPosition(self, piece: "Piece") -> Position | None:
        """Retourne la position d'une pièce ou None si elle est capturée."""
        for current_piece in self.grid.values():
            if current_piece is piece:
                return current_piece.position
        return None

    def getPiece(self, position: Position) -> "Piece | None":
        """Retourne la pièce située sur une case ou None si la case est vide."""
        return self.grid.get(str(position))

    def move_piece(self, start: Position, end: Position) -> None:
        """Déplace une pièce d'une case à une autre, capture comprise."""
        piece = self.getPiece(start)
        if piece is None:
            raise ValueError(f"Aucune pièce en {start}")

        self.grid.pop(str(start))
        captured = self.grid.pop(str(end), None)
        piece.position = end
        self.grid[str(end)] = piece

    def is_path_clear(self, start: Position, end: Position) -> bool:
        """Vérifie qu'aucune pièce ne bloque le chemin entre deux cases.

        Ne vérifie pas la case de départ ni la case d'arrivée.
        """
        dc, dr = start.delta(end)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)
        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)

        c, r = start.to_indices()
        end_c, end_r = end.to_indices()
        c += step_c
        r += step_r

        while (c, r) != (end_c, end_r):
            pos = Position(Position.COLUMNS[c], r + 1)
            if self.getPiece(pos) is not None:
                return False
            c += step_c
            r += step_r

        return True

    def find_king(self, color: int) -> Position | None:
        """Retourne la position du roi d'une couleur."""
        for piece in self.grid.values():
            if isinstance(piece, King) and piece.color == color:
                return piece.position
        return None

    def to_dict(self) -> dict:
        """Convertit le plateau en dictionnaire sérialisable."""
        pieces = []
        for piece in self.grid.values():
            pieces.append({
                "type": piece.symbol,
                "color": piece.color,
                "position": str(piece.position),
            })
        return {"pieces": pieces}

    @classmethod
    def from_dict(cls, data: dict) -> "Board":
        """Reconstruit un plateau depuis un dictionnaire."""
        board = cls(setup=False)
        for item in data.get("pieces", []):
            cls_piece = PIECE_CLASSES[item["type"]]
            piece = cls_piece(Position.from_string(item["position"]), item["color"])
            board.place_piece(piece)
        return board

    def __str__(self) -> str:
        lines = []
        for row in range(8, 0, -1):
            cells = []
            for column in Position.COLUMNS:
                piece = self.getPiece(Position(column, row))
                cells.append(str(piece) if piece else ".")
            lines.append(f"{row} " + " ".join(cells))
        lines.append("  a b c d e f g h")
        return "\n".join(lines)


if __name__ == "__main__":
    board = Board()
    print(board)
    print("Pièce en e1 :", board.getPiece(Position.from_string("e1")))
    print("Tests Board OK !")
