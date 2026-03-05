import unittest
import ProgramA

class TestOption1(unittest.TestCase):

    def test_hex_u16(self):
        self.assertEqual(ProgramA.hex_u16(10), "000A")
        self.assertEqual(ProgramA.hex_u16(65535), "FFFF")

    def test_bin16_is_16_bits(self):
        self.assertEqual(ProgramA.bin16(5), "0000000000000101")
        self.assertEqual(len(ProgramA.bin16(5)), 16)

    def test_signed16_positive_range(self):
        self.assertEqual(ProgramA.signed16(0), 0)
        self.assertEqual(ProgramA.signed16(32767), 32767)

    def test_signed16_negative_range(self):
        self.assertEqual(ProgramA.signed16(32768), -32768)
        self.assertEqual(ProgramA.signed16(65535), -1)

    def test_option1_lines_format(self):
        lines = ProgramA.option1_lines(65535)
        self.assertEqual(lines[0], "HEX = FFFF")
        self.assertEqual(lines[1], "BIN(16) = 1111111111111111")
        self.assertEqual(lines[2], "SIGNED16 = -1")

    def test_require_u16_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            ProgramA.require_u16(-1)
        with self.assertRaises(ValueError):
            ProgramA.require_u16(65536)

    def test_require_u16_rejects_non_int(self):
        with self.assertRaises(TypeError):
            ProgramA.require_u16("123")  # string not allowed


if __name__ == "__main__":
    unittest.main()
