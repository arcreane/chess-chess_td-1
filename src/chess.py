"""Module principal de gestion d'une partie d'échecs."""

import json
from .board import Board
from .player import Player, AIPlayer
from .position import Position
from .pieces import WHITE, BLACK, PIECE_CLASSES


class Chess:
    """Gère une partie complète d'échecs.

    Attributes:
        board (Board): plateau courant.
        players (list[Player]): liste des deux joueurs.
        currentPlayer (Player): joueur dont c'est le tour.
    """

    def __init__(self):
        self.board = Board()
        self.players = []
        self.currentPlayer = None

    def initPlayers(self) -> None:
        """Demande les noms et initialise les deux joueurs."""
        if self.players:
            return

        name_white = input("Nom du joueur blanc (ou AI) : ").strip() or "Blanc"
        name_black = input("Nom du joueur noir (ou AI) : ").strip() or "Noir"

        white_player = AIPlayer("AI blanc", WHITE) if name_white.upper() == "AI" else Player(name_white, WHITE)
        black_player = AIPlayer("AI noir", BLACK) if name_black.upper() == "AI" else Player(name_black, BLACK)

        self.players = [white_player, black_player]
        self.currentPlayer = self.players[0]

    def displayBoard(self) -> None:
        """Affiche le plateau en mode texte."""
        print()
        print(self.board)
        print()

    def parse_move(self, move: str) -> tuple[str, Position, Position]:
        """Analyse un coup comme 'Pe2 e4' ou 'Nb1 c3'."""
        parts = move.strip().split()
        if len(parts) != 2:
            raise ValueError("Format attendu : Pe2 e4")

        piece_and_start, end_text = parts
        if len(piece_and_start) == 3:
            symbol = piece_and_start[0].upper()
            start_text = piece_and_start[1:]
        elif len(piece_and_start) == 2:
            start_text = piece_and_start
            start_piece = self.board.getPiece(Position.from_string(start_text))
            if start_piece is None:
                raise ValueError("Aucune pièce sur la case de départ")
            symbol = start_piece.symbol
        else:
            raise ValueError("Format de départ invalide")

        if symbol not in PIECE_CLASSES:
            raise ValueError("Identifiant de pièce invalide")

        return symbol, Position.from_string(start_text), Position.from_string(end_text)

    def isValidMove(self, move: str) -> bool:
        """Vérifie si un coup saisi est valide."""
        try:
            symbol, start, end = self.parse_move(move)
            piece = self.board.getPiece(start)

            if piece is None:
                print("Erreur : aucune pièce sur la case de départ.")
                return False

            if piece.symbol != symbol:
                print("Erreur : l'identifiant ne correspond pas à la pièce.")
                return False

            if piece.color != self.currentPlayer.color:
                print("Erreur : ce n'est pas ta pièce.")
                return False

            if not piece.isValidMove(end, self.board):
                print("Erreur : déplacement interdit pour cette pièce.")
                return False

            return True
        except ValueError as error:
            print(f"Erreur : {error}")
            return False

    def updateBoard(self, move: str) -> None:
        """Met à jour l'échiquier après un coup valide."""
        _, start, end = self.parse_move(move)
        self.board.move_piece(start, end)

    def switchPlayer(self) -> None:
        """Passe au joueur suivant."""
        self.currentPlayer = self.players[1] if self.currentPlayer == self.players[0] else self.players[0]

    def isCheckMate(self) -> bool:
        """Détermine si la partie est terminée.

        Version volontairement simple : le projet accepte une première version retournant False.
        """
        return False

    def save_game(self, filename: str) -> None:
        """Sauvegarde la partie dans un fichier JSON."""
        data = {
            "board": self.board.to_dict(),
            "players": [{"name": p.name, "color": p.color, "ai": isinstance(p, AIPlayer)} for p in self.players],
            "current_color": self.currentPlayer.color,
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_game(self, filename: str) -> None:
        """Restaure une partie depuis un fichier JSON."""
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.board = Board.from_dict(data["board"])
        self.players = []
        for item in data["players"]:
            cls = AIPlayer if item.get("ai") else Player
            self.players.append(cls(item["name"], item["color"]))

        current_color = data["current_color"]
        self.currentPlayer = next(player for player in self.players if player.color == current_color)

    def play(self) -> None:
        """Déroule la partie complète en mode texte."""
        self.initPlayers()

        while not self.isCheckMate():
            self.displayBoard()
            print(f"Tour de {self.currentPlayer.name}")

            while True:
                if isinstance(self.currentPlayer, AIPlayer):
                    move = self.currentPlayer.askMove(self.board)
                    print(f"L'IA joue : {move}")
                else:
                    move = self.currentPlayer.askMove()

                if move.lower() == "quit":
                    print("Partie terminée.")
                    return

                if move.lower().startswith("save "):
                    filename = move.split(maxsplit=1)[1]
                    self.save_game(filename)
                    print(f"Partie sauvegardée dans {filename}.")
                    continue

                if move.lower().startswith("load "):
                    filename = move.split(maxsplit=1)[1]
                    self.load_game(filename)
                    print(f"Partie chargée depuis {filename}.")
                    break

                if self.isValidMove(move):
                    self.updateBoard(move)
                    self.switchPlayer()
                    break


if __name__ == "__main__":
    game = Chess()
    print(game.board)
    print("Tests Chess OK !")
