#冒泡排序算法
arr = [7,1,4,3,99,5,96,2,]
# for i in range(1,len(arr)):
#     print(arr,"@@@@")
#     for j in range(0, len(arr) - i):
#         if arr[j] > arr[j + 1]:
#             arr[j], arr[j + 1] = arr[j + 1], arr[j]
# print(arr)
#排序算法
for i in range(len(arr) - 1):
        # 记录最小数的索引
        minIndex = i
        print(arr,"@@")
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        # i 不是最小数时，将 i 和最小数进行交换
        if i != minIndex:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
print(arr)