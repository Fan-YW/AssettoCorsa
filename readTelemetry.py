import struct
import pandas as pd
from matplotlib import pyplot as plt

def bytesToFloat(h1,h2,h3,h4):
    ba = bytearray()
    ba.append(h1)
    ba.append(h2)
    ba.append(h3)
    ba.append(h4)
    return struct.unpack("<f",ba)[0]

def floatToBytes(f):
    bs = struct.pack("f",f)
    return (bs[3],bs[2],bs[1],bs[0])

with open(r"D:\\Documents\Assetto Corsa\\ctelemetry\\player\\RedSt0ne_bahrain_2020_gp_rss_formula_hybrid_x_evo.tc", mode="rb") as f:
    filesize=len(f.read())
    print(filesize)

    gear = []
    distance0=[]
    speed=[]
    throttle=[]
    brake=[]
    for i in range(3999):
        f.seek(filesize-79980+i*20)
        a = f.read(1)
        gear.append(a[0]-1)

        f.seek(filesize-79976+i*20)
        a = f.read(4)
        distance0.append(bytesToFloat(a[0],a[1],a[2],a[3]))
        
        f.seek(filesize-79972+i*20)
        a = f.read(4)
        speed.append(bytesToFloat(a[0],a[1],a[2],a[3]))

        f.seek(filesize-79968+i*20)
        a = f.read(4)
        throttle.append(100*bytesToFloat(a[0],a[1],a[2],a[3]))

        f.seek(filesize-79964+i*20)
        a = f.read(4)
        brake.append(bytesToFloat(a[0],a[1],a[2],a[3]))

fig, axes = plt.subplots(4, 1, figsize=(10,15), dpi=192, facecolor='w', sharex=True, gridspec_kw={'height_ratios': [1.5, 1, 0.8, 0.2]}) #画图
axes[0].plot(distance0, speed   , color='#000000', linewidth=3, linestyle='-')
axes[1].plot(distance0, gear    , color='#000000', linewidth=3, linestyle='-')
axes[2].plot(distance0, throttle, color='#000000', linewidth=3, linestyle='-')
axes[3].plot(distance0, brake   , color='#000000', linewidth=3, linestyle='-')

#保存图片
plt.subplots_adjust(left=0.13, bottom=0.07, right=0.97, top=0.95, hspace=0.1)
filename = 'D:/telemetry.png'
plt.savefig(filename, dpi=192, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,  format='png', transparent=False)
