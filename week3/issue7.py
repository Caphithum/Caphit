def get_integer_input(prompt):
    """
    通用函数：获取用户输入的整数
    """
    while True:
        try:
            value = int(input(prompt))
            break
        except ValueError:
            print("请输入整数！")
    return value

# 输入两个整数
a = get_integer_input("请输入第一个整数：")
b = get_integer_input("请输入第二个整数：")

# 选择较小的数作为公共因子的初始值
common_divisor = min(a, b)

# 从大到小循环查找公共因子
for i in range(common_divisor, 0, -1):
    if a % i == 0 and b % i == 0:
        print("%d和%d的最大公约数为%d" % (a, b, i))
        break
else:
    print("没有找到%d和%d的公约数！" % (a, b))