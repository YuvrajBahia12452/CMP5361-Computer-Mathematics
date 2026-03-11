U16_MAX = 0xFFFF
U16_SIGN_BIT = 0x8000
memory = {}
def require_u16(n: int) -> int:
    """Validate n is a 16-bit unsigned integer (0..65535)."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0 or n > U16_MAX:
        raise ValueError("n must be in range 0..65535")
    return n


def hex_u16(n: int) -> str:
    """
    Return a 16-bit style hex string
    """
    n = require_u16(n)
    return f"{n:04X}"


def bin16(n: int) -> str:
    """
    Return a fixed-width 16-bit binary string.
    """
    n = require_u16(n)
    return format(n, "016b")


def signed16(n: int) -> int:
    """
    Interpret the same 16-bit pattern as a signed two's complement value.
    """
    n = require_u16(n)
    return n if n < U16_SIGN_BIT else n - (U16_MAX + 1)

def option1_lines(n: int) -> list[str]:
    """
    Output lines required for Option 1.
    """
    n = require_u16(n)
    return [
        f"HEX = {hex_u16(n)}",
        f"BIN(16) = {bin16(n)}",
        f"SIGNED16 = {signed16(n)}",
    ]

def Convert(): # Convert (decimal → hex and binary)
    n = int(input("Enter an integer (0..65535): "))
    for line in option1_lines(n):
        print(line)


def WriteMEM(addr, MEMO, LOW, HIGH):
    # Write to memory
    MEMO[addr] = LOW
    MEMO[addr+1] = HIGH
    print_MEMO = [
        f"MEM[0x{addr:04X}] = 0x{LOW:02X}",
        f"MEM[0x{addr+1:04X}] = 0x{HIGH:02X}"
        ]
    return print_MEMO

def ReadMEM(addr, MEMO):
    rLOW  = MEMO[addr]
    rHIGH = MEMO[addr+1]

    print_message = [
        f"READ MEM[0x{addr:04X}] = 0x{rLOW:02X}",
        f"READ MEM[0x{addr+1:04X}] = 0x{rHIGH:02X}"
        ]
    return rLOW, rHIGH, print_message


def Littleendian(n, addr): # Little-endian pack/unpack (16-bit) + memory write/read
    # Convert address if hex string
    if isinstance(addr, str):
        addr = int(addr, 0)  # auto-detects 0x prefix

    # Simulated memory (64KB)
    MEMO = bytearray(65536)

    # Compute bytes (little-endian)
    LOW  = n & 0xFF
    HIGH = (n >> 8) & 0xFF

    # writing the bytes into memory
    WriteMEM(addr, MEMO, LOW, HIGH)

    # getting the rLOW and rHIGH bytes in ReadMEM
    rLOW, rHIGH, print_message = ReadMEM(addr, MEMO)

    # Reconstruct (unpack)
    UNPACKED = rLOW | (rHIGH << 8)

    print_MEMO = WriteMEM(addr, MEMO, LOW, HIGH)
    # Output
    return [
        f"LOW = {LOW}",
        f"HIGH = {HIGH}",
        f"UNPACKED = {UNPACKED}"
    ] + print_message + print_MEMO


def ascii_dump_lines(s: str, base: int = 0x1000) -> list[str]:
    if len(s) > 10:
        raise ValueError("String must be at most 10 characters")

    lines = []

    for i, ch in enumerate(s):
        addr = base + i
        byte = ord(ch)
        lines.append(f"0x{addr:04X} : 0x{byte:02X}")

    null_addr = base + len(s)
    lines.append(f"0x{null_addr:04X} : 0x00")
    lines.append(f"LENGTH (until 0x00) = {len(s)}")

    return lines

def ASCII(): # ASCII memory dump + null terminator + length scan
    try:
        s = input("Enter a string (max 10 characters): ")
        for line in ascii_dump_lines(s):
            print(line)
    except ValueError as e:
        print(e)


def get_address(base, index, size):
    """Computes the exact memory address for an array element."""
    return base + (index * size)

def write_mem(address, size, value):
    """Writes 1 or 2 bytes into the simulated memory dictionary."""
    if size == 1:
        # stores just the lowest 8 bits
        memory[address] = value & 0xFF
    elif size == 2:
        # Little endian: low byte at address, high byte at address + 1
        memory[address] = value & 0xFF
        memory[address + 1] = (value >> 8) & 0xFF

def read_mem(address, size):
    """Reads bytes from memory and reconstructs the integer."""
    if size == 1:
        return memory.get(address, 0)
    elif size == 2:
        # rebuilds from little endian
        low_byte = memory.get(address, 0)
        high_byte = memory.get(address + 1, 0)
        return (high_byte << 8) | low_byte
    

def StackFrame(): # Stack frame (simplified bp offsets) + register-style view
    # asking the user for two numbers
    a = int(input("Input number a: "))
    b = int(input("Input number b: "))

    print("\nSimulated Stack Frame")
    print("----------------")
    print("bp    : RETURN address")
    print("bp+2  : a =", a)
    print("bp+4  : b =", b)

    # register style simulation
    print("\nRegister View")
    print("-------------")

    AX = a
    BX = b

    print("AX =", AX)
    print("BX =", BX)

    # simulate AX + BX
    AX = AX + BX

    print("AX (AX + BX) =", AX)


def main():
    running = True
    while running:
            # print the menu
            print('Choose the operation:')
            print(' 1- Convert (decimal → hex and binary)')
            print(' 2- Little-endian pack/unpack (16-bit)')
            print(' 3- ASCII memory dump')
            print(' 4- Array addressing')
            print(' 5- Stack frame (bp offsets)')
            print(' 0- Exit')
        

        # get the option
            op = input('Option: ')

            if op == '1':
            # 1 -  Convert (decimal → hex and binary)
                Convert()
         

            elif op == '2':
            # 2 - Little-endian pack/unpack (16-bit) + memory write/read
                try:
                    n = int(input("Input a 16-bit number (decimal): "))
                    if 0 <= n <= 65535:
                        addr = input("Input a memory address (decimal or hex number e.g. 0x2000): ")
                        for line in Littleendian(n, addr):
                            print(line)

                    else:
                        print("Error: n must be between 0 and 65535")

                except ValueError:
                    print("Incorrect Value, please enter a valid decimal integer")
            elif op == '3':
            # 3 - ASCII memory dump + null terminator + length scan
                ASCII()

            elif op == '4':
            # 4 - Array addressing + dereference (read/write one element)
                try:
                    base_input = input("Enter base address (e.g., 1000 or 0x3004): ").strip()
                 # It will heck if the user typed a hex string or decimal
                    if base_input.lower().startswith("0x"):
                        base = int(base_input, 16)
                    else:
                        base = int(base_input)
                    
                    index = int(input("Enter index: "))
                    size = int(input("Enter element size (1 or 2): "))
                
                    if size not in [1, 2]:
                        print("Error: Size must be 1 or 2.")
                        continue
                    
                    mode = input("Enter mode (read or write): ").strip().lower()
                    if mode not in ["read", "write"]:
                        print("Error: Invalid mode. Must be 'read' or 'write'.")
                        continue
                    
                    # Calculates the target address
                    address = get_address(base, index, size)
                
                    # then prints the required output formats
                    print("\nADDRESS = base + index*size")
                    print(f"ADDRESS = {hex(address)}")
                
                    if mode == "write":
                        value = int(input("Enter value to write: "))
                        write_mem(address, size, value)
                        print(f"WRITE size={size} value={value} to ADDRESS {hex(address)}")
                    
                    elif mode == "read":
                        val = read_mem(address, size)
                        print(f"READ size={size} from ADDRESS {hex(address)} = {val}")
                    
                except ValueError:
                    #  if user types text instead of numbers
                    print("Error: Invalid number format entered. Returning to menu.")

            elif op == '5':
            # 5 - Stack frame (simplified bp offsets) + register-style view
                StackFrame()
            
            elif op == '0':
                running = False
            # Quits the program
            
            else:
            # the user did not enter an option that exists in the menu
                print('Invalid option. Try again')

if __name__ == '__main__':
    main()
