def is_prime(a):
    if a <= 1:
        return False
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True

# 测试示例
num = int(input("请输入一个数字："))
if is_prime(num):
    print(num, "是质数")
else:
    print(num, "不是质数")