
def Convert(): # Convert (decimal → hex and binary)
    pass

def Littleendian(n, addr): # Little-endian pack/unpack (16-bit) + memory write/read
    # Convert address if hex string
    if isinstance(addr, str):
        addr = int(addr, 0)  # auto-detects 0x prefix

    # Simulated memory (64KB)
    MEMO = bytearray(65536)

    # Compute bytes (little-endian)
    LOW  = n & 0xFF
    HIGH = (n >> 8) & 0xFF

    # Write to memory
    MEMO[addr]     = LOW
    MEMO[addr+1] = HIGH

    # Read back
    rLOW  = MEMO[addr]
    rHIGH = MEMO[addr+1]

    # Reconstruct (unpack)
    UNPACKED = rLOW | (rHIGH << 8)

    # Output
    print(f"low byte  = {LOW}")
    print(f"high byte = {HIGH}")
    print(f"unpacked  = {UNPACKED}")

    print(f"MEM[0x{addr:04X}] = 0x{LOW:02X}")
    print(f"MEM[0x{addr+1:04X}] = 0x{HIGH:02X}")

    print(f"READ MEM[0x{addr:04X}] = 0x{rLOW:02X}")
    print(f"READ MEM[0x{addr+1:04X}] = 0x{rHIGH:02X}")


def ASCII(): # ASCII memory dump + null terminator + length scan
    pass

def ArrayAdressing(): # Array addressing + dereference (read/write one element)
    pass

def StackFrame(): # Stack frame (simplified bp offsets) + register-style view
    pass


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
                    if 0 <= n < 65535:
                        addr = input("Input a memory address (decimal or hex number e.g. 0x2000): ")
                        Littleendian(n, addr)

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
