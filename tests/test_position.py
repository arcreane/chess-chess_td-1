import unittest
from src.position import Position


class TestPosition(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Position("e", 4)), "e4")

    def test_invalid_position(self):
        with self.assertRaises(ValueError):
            Position("z", 9)


if __name__ == "__main__":
    unittest.main()
