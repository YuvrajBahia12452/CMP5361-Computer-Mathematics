# Option 1: Convert (decimal -> hex and binary) + SIGNED16
# Spec: HEX, BIN(16) must be 16 bits, SIGNED16 uses two's complement

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
    
def Convert(): # Convert (decimal → hex and binary)
    """Output line for Option 1
    """
    n = require_u16(n)
    print(f"HEX = {hex_u16(n)}\nBIN(16) = {bin16(n)}\nSIGNED16 = {signed16(n)}")

def Littleendian(): # Little-endian pack/unpack (16-bit) + memory write/read
    pass

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
            print(' 2- Little-endian pack/unpack (16-bit) + memory write/read')
            print(' 3- ASCII memory dump + null terminator + length scan')
            print(' 4- Array addressing + dereference (read/write one element)')
            print(' 5- Stack frame (simplified bp offsets) + register-style view')
            print(' 6- Quit')
        

        # get the option
            op = input('Option: ')

            if op == '1':
            # 1 -  Convert (decimal → hex and binary)
                Convert()
         

            elif op == '2':
            # 2 - Little-endian pack/unpack (16-bit) + memory write/read
                Littleendian()
        
            elif op == '3':
            # 3 - ASCII memory dump + null terminator + length scan
                ASCII()

            elif op == '4':
            # 4 - Array addressing + dereference (read/write one element)
                ArrayAdressing()

            elif op == '5':
            # 5 - Stack frame (simplified bp offsets) + register-style view
                StackFrame()
            
            elif op == '6':
                running = False
            # Quits the program
            
            else:
            # the user did not enter an option that exists in the menu
                print('Invalid option. Try again')

if __name__ == '__main__':
    main()

