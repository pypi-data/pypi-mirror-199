import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_add(self): # test the addition

        calc = Calculator()
        calc.add(2)
        self.assertEqual(calc.memory, 2)
        
    def test_subtract(self): # test the subtraction
        calc = Calculator()
        calc.subtract(2)
        self.assertEqual(calc.memory, -2)
        
    def test_multiply(self): # test the multiplication
        calc = Calculator()
        calc.multiply(2)
        self.assertEqual(calc.memory, 0)
        
    def test_divide(self): # test the divide
        calc = Calculator()
        calc.divide(2)
        self.assertEqual(calc.memory, 0)
        with self.assertRaises(ValueError): # with the case of the denominator being 0
            calc.divide(0)
        
    def test_root(self): # test the root
        calc = Calculator()
        calc.root(2)
        self.assertEqual(calc.memory, 0)
        
    def test_reset(self): # test the reset
        calc = Calculator()
        calc.add(2)
        calc.reset()
        self.assertEqual(calc.memory, 0)


if __name__ == '__main__':
    unittest.main()