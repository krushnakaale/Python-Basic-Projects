import unittest
from calculator_logic import calculate

class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(calculate('2+3*4'), '14')
        self.assertEqual(calculate('(10+5)×2'), '30')
        self.assertEqual(calculate('10%3'), '1')
        self.assertEqual(calculate('sqrt(81)'), '9')
        self.assertEqual(calculate('5**2'), '25')

    def test_errors(self):
        for expression in ['1/0', '__import__("os")', '2+']:
            with self.assertRaises(ValueError):
                calculate(expression)

if __name__ == '__main__':
    unittest.main()
