import unittest
from programA import decimal_to_hex, decimal_to_binary16

class MyTests(unittest.TestCase):

    def test_hex_values(self):
        self.assertEqual(decimal_to_hex(10), '0xa')

    def test_binary(self):
        self.assertEqual(decimal_to_hex(30), '0x1e')

if __name__ == '__main__':
    unittest.main()
