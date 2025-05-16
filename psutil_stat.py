import psutil
import csv
import datetime

res = []

with open("/home/admin/smart_house/smart_house/data_hot.csv", 'w', newline='') as csvfile:
    fieldnames = ["cpu0", "cpu1", "cpu2", "cpu3", "memory_used", "memory_percent", "timestamp"]
    writer =  csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()
    for _ in range(600):
        cpu = psutil.cpu_percent(interval=1, percpu=True)
        memory = psutil.virtual_memory()
        print("CPU is:")
        print(cpu)
        print("Memory is:")
        print(memory)
        d = {
            "cpu0": cpu[0], "cpu1": cpu[1], "cpu2": cpu[2], "cpu3": cpu[3],
            "memory_used": memory.used, "memory_percent": memory.percent,
            "timestamp": datetime.datetime.now().timestamp()
        }
        res.append(d)

        writer.writerow(d)


with open("/home/admin/smart_house/smart_house/backup.csv", 'w', newline='') as csvfile:
        fieldnames = ["cpu0", "cpu1", "cpu2", "cpu3", "memory_used", "memory_percent", "timestamp"]
        writer =  csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(res)