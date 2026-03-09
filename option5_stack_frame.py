# Simple simulation of a stack frame using bp offsets

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
