"""Interface graphique Tkinter simple pour le jeu d'échecs."""

import os
import tkinter as tk
from PIL import Image, ImageTk

from src.chess import Chess
from src.position import Position
from src.pieces import WHITE


SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


class ChessGUI:
    """Interface graphique permettant de déplacer les pièces à la souris."""

    def __init__(self):
        self.game = Chess()
        self.game.players = []  # joueurs sans saisie console
        from src.player import Player
        self.game.players = [Player("Blanc", 0), Player("Noir", 1)]
        self.game.currentPlayer = self.game.players[0]

        self.selected_position = None
        self.images = {}

        self.root = tk.Tk()
        self.root.title("Projet I1 - Jeu d'échecs")
        self.status = tk.Label(self.root, text="Tour des blancs", font=("Arial", 14))
        self.status.pack()
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.load_images()
        self.draw_board()

    def load_images(self):
        """Charge les images une seule fois pour éviter qu'elles disparaissent."""
        for filename in os.listdir(ASSET_DIR):
            if filename.endswith(".png"):
                key = filename.replace(".png", "")
                image = Image.open(os.path.join(ASSET_DIR, filename)).resize((SQUARE_SIZE, SQUARE_SIZE))
                self.images[key] = ImageTk.PhotoImage(image)

    def position_to_xy(self, position: Position):
        """Convertit une position échiquier en coordonnées canvas."""
        col, row = position.to_indices()
        x = col * SQUARE_SIZE
        y = (7 - row) * SQUARE_SIZE
        return x, y

    def xy_to_position(self, x: int, y: int):
        """Convertit des coordonnées canvas en position échiquier."""
        col_index = x // SQUARE_SIZE
        row = 8 - (y // SQUARE_SIZE)
        return Position(Position.COLUMNS[col_index], row)

    def draw_board(self):
        """Dessine le plateau et les pièces."""
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        if self.selected_position:
            x, y = self.position_to_xy(self.selected_position)
            self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, outline="yellow", width=4)

        for piece in self.game.board.grid.values():
            x, y = self.position_to_xy(piece.position)
            image = self.images.get(piece.get_image_key())
            if image:
                self.canvas.create_image(x, y, image=image, anchor="nw")
            else:
                self.canvas.create_text(x + 40, y + 40, text=str(piece), font=("Arial", 28))

    def on_click(self, event):
        """Gère la sélection puis le déplacement d'une pièce."""
        clicked = self.xy_to_position(event.x, event.y)
        piece = self.game.board.getPiece(clicked)

        if self.selected_position is None:
            if piece is not None and piece.color == self.game.currentPlayer.color:
                self.selected_position = clicked
                self.draw_board()
            return

        selected_piece = self.game.board.getPiece(self.selected_position)
        move = f"{selected_piece.symbol}{self.selected_position} {clicked}"

        if self.game.isValidMove(move):
            self.game.updateBoard(move)
            self.game.switchPlayer()
            player_name = "blancs" if self.game.currentPlayer.color == WHITE else "noirs"
            self.status.config(text=f"Tour des {player_name}")
        else:
            self.status.config(text="Coup invalide")

        self.selected_position = None
        self.draw_board()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ChessGUI().run()
