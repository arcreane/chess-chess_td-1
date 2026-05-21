"""Module contenant la classe Position."""


class Position:
    """Représente une position sur l'échiquier, par exemple e4.

    Attributes:
        column (str): lettre entre 'a' et 'h'.
        row (int): nombre entre 1 et 8.
    """

    COLUMNS = "abcdefgh"

    def __init__(self, column: str, row: int):
        self.column = column.lower()
        self.row = int(row)
        if not self.is_valid():
            raise ValueError(f"Position invalide : {column}{row}")

    @classmethod
    def from_string(cls, text: str) -> "Position":
        """Crée une position depuis une chaîne comme 'e4'."""
        text = text.strip().lower()
        if len(text) != 2:
            raise ValueError(f"Format de position invalide : {text}")
        return cls(text[0], int(text[1]))

    def is_valid(self) -> bool:
        """Retourne True si la position est sur l'échiquier."""
        return self.column in self.COLUMNS and 1 <= self.row <= 8

    def to_indices(self) -> tuple[int, int]:
        """Retourne les indices colonne, ligne entre 0 et 7."""
        return self.COLUMNS.index(self.column), self.row - 1

    def delta(self, other: "Position") -> tuple[int, int]:
        """Retourne le déplacement en colonnes et lignes vers une autre position."""
        c1, r1 = self.to_indices()
        c2, r2 = other.to_indices()
        return c2 - c1, r2 - r1

    def __str__(self) -> str:
        return f"{self.column}{self.row}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Position) and self.column == other.column and self.row == other.row

    def __hash__(self) -> int:
        return hash((self.column, self.row))


if __name__ == "__main__":
    p1 = Position("e", 4)
    print(f"Position créée : {p1}")  # attendu : e4
    p2 = Position.from_string("a1")
    print(f"Position créée : {p2}")  # attendu : a1
    print("Tests Position OK !")
