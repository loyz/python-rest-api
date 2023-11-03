"""
Sample Test
"""
from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    """Test calc module"""

    def test_add_numbers(self):
        """Test adding numbers by example"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)

        self.assertEqual(res, -5)
        