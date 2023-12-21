import psutil

cpu = psutil.cpu_percent(None)
print(cpu)