def decimal_to_hex(n):
    return hex(n)

def decimal_to_binary16(n):
    return format(n & 0xFFFF, '016b')

def signed16(n):
    if n >= 0:
        return format(n, '016b')
    else:
        return format((1 << 16) + n, '016b')

def menu():
    while True:
        print("\nMenu")
        print("1 - please Convert decimal to HEX and 16-bit binary")
        print("0 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            num = int(input("please Enter decimal number: "))
            print("Hex:", decimal_to_hex(num))
            print("Binary16:", decimal_to_binary16(num))
            print("SIGNED16:", signed16(num))

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
