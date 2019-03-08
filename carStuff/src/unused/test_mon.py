import performance
perf = performance.Performance()


RAM_stats = perf.getRAMinfo()
RAM_total = round(int(RAM_stats[0]) / 1000,1)
RAM_used = round(int(RAM_stats[1]) / 1000,1)
RAM_free = round(int(RAM_stats[2]) / 1000,1) 
print (RAM_total)
print (RAM_used)
print (RAM_free)
