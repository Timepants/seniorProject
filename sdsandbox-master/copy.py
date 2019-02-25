from shutil import copyfile
for n in range(1000):
    copyfile("frame_000008_st_-7_th_90.jpg", "frame_"+str(n + 214).zfill(6)+"_st_-7_th_90.jpg")