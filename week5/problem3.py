def insertion_sort(arr):
    """
    插入排序算法
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# 接受输入端的数组
array = list(map(int, input("请输入待排序的数组:").split()))

# 使用插入排序进行排序
insertion_sort(array)

# 输出排序后的结果
print("排序后的结果：", array)