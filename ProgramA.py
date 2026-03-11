U16_MAX = 0xFFFF
U16_SIGN_BIT = 0x8000

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





def ASCII(): # ASCII memory dump + null terminator + length scan
    pass

def ArrayAdressing(): # Array addressing + dereference (read/write one element)
    pass

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
                ArrayAdressing()

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
