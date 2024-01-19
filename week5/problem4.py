def shell_sort(arr):
    """
    希尔排序算法
    """
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
        print(array)

# 调用示例
array = list(map(int, input("请输入待排序的数组:").split()))
shell_sort(array)
print("排序结果：", array)