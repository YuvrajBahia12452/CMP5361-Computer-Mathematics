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


class TestOption3(unittest.TestCase):

    def test_normal_string_hello(self):
        result = ProgramA.ascii_dump_lines("HELLO")
        expected = [
            "0x1000 : 0x48",
            "0x1001 : 0x45",
            "0x1002 : 0x4C",
            "0x1003 : 0x4C",
            "0x1004 : 0x4F",
            "0x1005 : 0x00",
            "LENGTH (until 0x00) = 5"
        ]
        self.assertEqual(result, expected)

    def test_single_character(self):
        result = ProgramA.ascii_dump_lines("A")
        expected = [
            "0x1000 : 0x41",
            "0x1001 : 0x00",
            "LENGTH (until 0x00) = 1"
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        result = ProgramA.ascii_dump_lines("")
        expected = [
            "0x1000 : 0x00",
            "LENGTH (until 0x00) = 0"
        ]
        self.assertEqual(result, expected)

    def test_maximum_length_10_characters(self):
        result = ProgramA.ascii_dump_lines("ABCDEFGHIJ")
        expected = [
            "0x1000 : 0x41",
            "0x1001 : 0x42",
            "0x1002 : 0x43",
            "0x1003 : 0x44",
            "0x1004 : 0x45",
            "0x1005 : 0x46",
            "0x1006 : 0x47",
            "0x1007 : 0x48",
            "0x1008 : 0x49",
            "0x1009 : 0x4A",
            "0x100A : 0x00",
            "LENGTH (until 0x00) = 10"
        ]
        self.assertEqual(result, expected)

    def test_more_than_10_characters_raises_value_error(self):
        with self.assertRaises(ValueError):
            ProgramA.ascii_dump_lines("ABCDEFGHIJK")

    def test_addresses_increase_by_one(self):
        result = ProgramA.ascii_dump_lines("ABC")
        self.assertEqual(result[0], "0x1000 : 0x41")
        self.assertEqual(result[1], "0x1001 : 0x42")
        self.assertEqual(result[2], "0x1002 : 0x43")
        self.assertEqual(result[3], "0x1003 : 0x00")

    def test_null_terminator_added_after_last_character(self):
        result = ProgramA.ascii_dump_lines("CAT")
        self.assertEqual(result[3], "0x1003 : 0x00")

    def test_length_output_for_three_character_string(self):
        result = ProgramA.ascii_dump_lines("DOG")
        self.assertEqual(result[-1], "LENGTH (until 0x00) = 3")

    def test_digits_string(self):
        result = ProgramA.ascii_dump_lines("123")
        expected = [
            "0x1000 : 0x31",
            "0x1001 : 0x32",
            "0x1002 : 0x33",
            "0x1003 : 0x00",
            "LENGTH (until 0x00) = 3"
        ]
        self.assertEqual(result, expected)

    def test_string_with_space(self):
        result = ProgramA.ascii_dump_lines("A B")
        expected = [
            "0x1000 : 0x41",
            "0x1001 : 0x20",
            "0x1002 : 0x42",
            "0x1003 : 0x00",
            "LENGTH (until 0x00) = 3"
        ]
        self.assertEqual(result, expected)


class TestOption4(unittest.TestCase):

    def test_array_address_calculation(self):
        # The brief asked that the testing base=1000, index=3, size=2 -> 1006
        address = ProgramA.get_address(1000, 3, 2)
        self.assertEqual(address, 1006)

    def test_memory_write_and_read_1_byte(self):
        # Test is storing a simple value in 1 byte
        test_addr = 0x1000
        ProgramA.write_mem(test_addr, 1, 200)
        
        # it will read it back and check if it matches
        result = ProgramA.read_mem(test_addr, 1)
        self.assertEqual(result, 200)

    def test_memory_write_and_read_2_bytes_little_endian(self):
        # Test iswriting a 2 byte value (like 1000) to memory and reading back
        test_addr = 0x3004
        ProgramA.write_mem(test_addr, 2, 1000)
        
        # Read it back to ensure the little endian rebuilding works
        result = ProgramA.read_mem(test_addr, 2)
        self.assertEqual(result, 1000)

if __name__ == "__main__":
    unittest.main(verbosity=2)
