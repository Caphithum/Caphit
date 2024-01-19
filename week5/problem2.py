import time

# 记录开始时间
start_time = time.perf_counter()

# 在此处放置你想要测量执行时间的代码
# 例如，执行一些计算密集型的任务
result = sum(i * i for i in range(1000000))

# 记录结束时间
end_time = time.perf_counter()

# 计算并打印执行时间
execution_time = end_time - start_time
print(f"程序执行时间: {execution_time} 秒")
