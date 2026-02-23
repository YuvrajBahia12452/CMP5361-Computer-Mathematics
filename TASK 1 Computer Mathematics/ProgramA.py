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
                pass
         

            elif op == '2':
            # 2 - Little-endian pack/unpack (16-bit) + memory write/read
                pass
        
            elif op == '3':
            # 3 - ASCII memory dump + null terminator + length scan
                pass

            elif op == '4':
            # 4 - Array addressing + dereference (read/write one element)
                pass

            elif op == '5':
            # 5 - Stack frame (simplified bp offsets) + register-style view
                pass
            
            elif op == '6':
                running = False
            # Quits the program
            
            else:
            # the user did not enter an option that exists in the menu
                print('Invalid option. Try again')

if __name__ == '__main__':
    main()
