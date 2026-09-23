import os
import sys
import unittest

# Чтобы импорт работал из корня проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from triangle import (  # noqa: E402
    check_triangle,
    EQUILATERAL,
    ISOSCELES,
    SCALENE,
    NOT_TRIANGLE,
    INVALID,
    ERR_NUMERIC,
    ERR_NON_NUMERIC,
)


class TestTriangle(unittest.TestCase):

    def test_equilateral(self):
        kind, coords = check_triangle("3", "3", "3")
        self.assertEqual(kind, EQUILATERAL)
        self.assertEqual(len(coords), 3)
        for x, y in coords:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(x, 100)
            self.assertLessEqual(y, 100)

    def test_isosceles(self):
        kind, _ = check_triangle("5", "5", "8")
        self.assertEqual(kind, ISOSCELES)

    def test_scalene(self):
        kind, _ = check_triangle("3", "4", "5")
        self.assertEqual(kind, SCALENE)

    def test_not_triangle(self):
        kind, coords = check_triangle("1", "2", "10")
        self.assertEqual(kind, NOT_TRIANGLE)
        self.assertEqual(coords, [ERR_NUMERIC] * 3)

    def test_zero_side(self):
        kind, coords = check_triangle("0", "4", "5")
        self.assertEqual(kind, NOT_TRIANGLE)
        self.assertEqual(coords, [ERR_NUMERIC] * 3)

    def test_negative_side(self):
        kind, coords = check_triangle("-3", "4", "5")
        self.assertEqual(kind, NOT_TRIANGLE)
        self.assertEqual(coords, [ERR_NUMERIC] * 3)

    def test_non_numeric(self):
        kind, coords = check_triangle("abc", "4", "5")
        self.assertEqual(kind, INVALID)
        self.assertEqual(coords, [ERR_NON_NUMERIC] * 3)

    def test_empty_strings(self):
        kind, coords = check_triangle("", "", "")
        self.assertEqual(kind, INVALID)
        self.assertEqual(coords, [ERR_NON_NUMERIC] * 3)

    def test_float_sides(self):
        kind, coords = check_triangle("3.5", "4.5", "5.5")
        self.assertEqual(kind, SCALENE)
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)


if __name__ == "__main__":
    unittest.main()