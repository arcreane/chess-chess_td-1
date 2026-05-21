import unittest
from src.board import Board
from src.position import Position


class TestMovements(unittest.TestCase):
    def test_pawn_first_double_move(self):
        board = Board()
        pawn = board.getPiece(Position.from_string("e2"))
        self.assertTrue(pawn.isValidMove(Position.from_string("e4"), board))

    def test_rook_blocked_initially(self):
        board = Board()
        rook = board.getPiece(Position.from_string("a1"))
        self.assertFalse(rook.isValidMove(Position.from_string("a4"), board))

    def test_knight_can_jump(self):
        board = Board()
        knight = board.getPiece(Position.from_string("b1"))
        self.assertTrue(knight.isValidMove(Position.from_string("c3"), board))

    def test_bishop_blocked_initially(self):
        board = Board()
        bishop = board.getPiece(Position.from_string("c1"))
        self.assertFalse(bishop.isValidMove(Position.from_string("h6"), board))


if __name__ == "__main__":
    unittest.main()
