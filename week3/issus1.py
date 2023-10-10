from decimal import Decimal

def decimal_to_binary(number):
    binary = []
    x = int(number)
    i = 0
    if x == 0:
        binary.append("0")
    while x % (2 ** i) != x:
        i = i + 1
    for j in range(i - 1, -1, -1):
        if x % (2 ** j) != x:
            binary.append("1")
            x = x - 2 ** j
        else:
            binary.append("0")
    binary.append(".")
    y = number - int(number)
    y = float(y)
    if y == 0:
        binary.append("0")
    for k in range(-1, -16, -1):
        if y >= 2 ** k:
            binary.append("1")
            y = y - 2 ** k
        else:
            binary.append("0")
        if y == 0:
            break
    binary_string = "".join(binary)
    return binary_string

print("请输入一个数字")
number = Decimal(input())
binary_string = decimal_to_binary(number)
print(binary_string)