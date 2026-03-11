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

    
class TestOption2(unittest.TestCase):
    def check_output(self, n, addr, expected_LOW, expected_HIGH, expected_UNPACKED):
        output = ProgramA.Littleendian(n, addr)
        # Convert all lines to a single string for testing
        full_output = "\n".join(output)

        self.assertIn(f"LOW = {expected_LOW}", full_output)
        self.assertIn(f"HIGH = {expected_HIGH}", full_output)
        self.assertIn(f"UNPACKED = {expected_UNPACKED}", full_output)
        self.assertIn(f"MEM[0x{addr:04X}] = 0x{expected_LOW:02X}", full_output)
        self.assertIn(f"MEM[0x{addr+1:04X}] = 0x{expected_HIGH:02X}", full_output)
        self.assertIn(f"READ MEM[0x{addr:04X}] = 0x{expected_LOW:02X}", full_output)
        self.assertIn(f"READ MEM[0x{addr+1:04X}] = 0x{expected_HIGH:02X}", full_output)

    def test_0(self):
        self.check_output(0, 0x2000, 0, 0, 0)

    def test_1(self):
        self.check_output(1, 0x2000, 1, 0, 1)

    def test_255(self):
        self.check_output(255, 0x2000, 255, 0, 255)

    def test_256(self):
        self.check_output(256, 0x2000, 0, 1, 256)

    def test_65535(self):
        self.check_output(65535, 0x2000, 255, 255, 65535)

if __name__ == "__main__":
    unittest.main()