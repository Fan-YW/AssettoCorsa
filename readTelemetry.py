from dis import dis
from re import T
from tkinter import font
from turtle import color, left
from matplotlib.font_manager import FontProperties
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator 
import numpy as np
import fastf1
from fastf1 import plotting
import math
import struct

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

fastf1.plotting.setup_mpl()
fastf1.Cache.enable_cache('D:/Onedrive/Docs/F1/doc_cache')

year = 2020 
# track = ['Australia', 0, [5278, 1750, 3163, 375, 1100, 1880, 3325, 4150, 4420, 4660], ['\nFL', '\nS1', '\nS2', '1', '3', '6', '11', '13', '14', '15']]
track = ['Belgium', 0, [7004, 2262, 5077, 380, 1100, 2440, 3080, 3280, 3900, 4550, 4940, 6760], ['\nFL', '\nS1', '\nS2', '1', '3', '5', '8', '9', '10', '12', '14', '19']]
# track = ['Emilia Romagna', 0.044, [4909, 1780, 3390, 920, 1640, 1940, 2565, 3080, 3615, 4370], ['\nFL', '\nS1', '\nS2', 'T3', 'T6', 'T7', 'T9', 'T12', 'T14', 'T17']]

gp = track[0]
sess = 'Qualifying'
lapLength = track[2][0]
session = fastf1.get_session(year, gp, sess)
session.load()
driver = ['44','16'] #想对比的车手
myTime = 100.966 #自己的时间，秒
telemetryFile = "D:\\Documents\Assetto Corsa\\ctelemetry\\player\\Fan_spa__rss_formula_hybrid_2020.tc" #遥测文件位置

#F1字体文件
tickFont   = FontProperties(fname="D:/OneDrive/Docs/F1/font/Formula1-Regular.ttf", size=18)
labelFont  = FontProperties(fname="D:/OneDrive/Docs/F1/font/Formula1-Bold.ttf", size=20)
titleFont  = FontProperties(fname="D:/OneDrive/Docs/F1/font/Formula1-Bold.ttf", size=22)
legendFont = FontProperties(fname="D:/OneDrive/Docs/F1/font/Formula1-Regular.ttf", size=12)

fig, axes = plt.subplots(4, 1, figsize=(10,12), dpi=192, facecolor='w', sharex=True, gridspec_kw={'height_ratios': [1.5, 1, 0.8, 0.2]})
existTeam = {''}

with open(telemetryFile, mode="rb") as f:
    filesize=len(f.read())
    print(filesize)

    gear = []
    distance=[]
    speed=[]
    throttle=[]
    brake=[]
    for i in range(3999):
        f.seek(filesize-79980+i*20)
        a = f.read(1)
        gear.append(a[0]-1)

        f.seek(filesize-79976+i*20)
        a = f.read(4)
        distance.append(bytesToFloat(a[0],a[1],a[2],a[3])*track[2][0])
        
        f.seek(filesize-79972+i*20)
        a = f.read(4)
        speed.append(bytesToFloat(a[0],a[1],a[2],a[3]))

        f.seek(filesize-79968+i*20)
        a = f.read(4)
        throttle.append(100*bytesToFloat(a[0],a[1],a[2],a[3]))

        f.seek(filesize-79964+i*20)
        a = f.read(4)
        brake.append(bytesToFloat(a[0],a[1],a[2],a[3]))

    axes[0].plot(distance, speed   , label='FAN '+('%1.0f' % (myTime//60)) + (':%06.3f' % (myTime%60)), color='#000000', linewidth=3, linestyle='-')
    axes[1].plot(distance, gear    , label='FAN '+('%1.0f' % (myTime//60)) + (':%06.3f' % (myTime%60)), color='#000000', linewidth=3, linestyle='-')
    axes[2].plot(distance, throttle, label='FAN '+('%1.0f' % (myTime//60)) + (':%06.3f' % (myTime%60)), color='#000000', linewidth=3, linestyle='-')
    axes[3].plot(distance, brake   , label='FAN '+('%1.0f' % (myTime//60)) + (':%06.3f' % (myTime%60)), color='#000000', linewidth=3, linestyle='-')

for i in range(len(driver)):
    if session.results.loc[driver[i]].TeamName in existTeam:
        linestyle = '-.'
        linewidth = 3
    else:
        linestyle = '-'
        linewidth = 3
        existTeam.add(session.results.loc[driver[i]].TeamName)

    currentLap = session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest()

    car_data = currentLap.get_car_data()
    
    lapTime = car_data['Time']
    lapTime = (lapTime/np.timedelta64(1, 's')).astype(float)
    time = [0]
    time.extend(lapTime)
    time.append(currentLap.LapTime/np.timedelta64(1, 's'))
    speed = []
    speed.append(car_data['Speed'].iloc[0])
    speed.extend(car_data['Speed'])
    speed.append(currentLap.SpeedFL)
    gear = []
    gear.append(car_data['nGear'].iloc[0])
    gear.extend(car_data['nGear'])
    gear.append(gear[len(gear)-1])
    throttle = []
    throttle.append(car_data['Throttle'].iloc[0])
    throttle.extend(car_data['Throttle'])
    throttle.append(throttle[len(throttle)-1])
    brake = []
    brake.append(car_data['Brake'].iloc[0])
    brake.extend(car_data['Brake'])
    brake.append(brake[len(brake)-1])
    distance = [0]

    for j in range(1,len(time)):
        distance.append(distance[j-1] + (time[j] - time[j-1]) * (speed[j] + speed[j-1]) / 7.2)

    actrualLapLen = distance[len(distance)-1]

    for j in range(len(time)):
        distance[j] = distance[j] / actrualLapLen * lapLength
        
    axes[0].plot(distance, speed   , label=session.results.loc[driver[i]].Abbreviation+' '+('%1.0f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()//60)) + (':%06.3f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()%60)), color='#' + session.results.loc[driver[i]].TeamColor, linewidth=linewidth, linestyle=linestyle)
    axes[1].plot(distance, gear    , label=session.results.loc[driver[i]].Abbreviation+' '+('%1.0f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()//60)) + (':%06.3f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()%60)), color='#' + session.results.loc[driver[i]].TeamColor, linewidth=linewidth, linestyle=linestyle)
    axes[2].plot(distance, throttle, label=session.results.loc[driver[i]].Abbreviation+' '+('%1.0f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()//60)) + (':%06.3f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()%60)), color='#' + session.results.loc[driver[i]].TeamColor, linewidth=linewidth, linestyle=linestyle)
    axes[3].plot(distance, brake   , label=session.results.loc[driver[i]].Abbreviation+' '+('%1.0f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()//60)) + (':%06.3f' % (session.laps[session.laps.DriverNumber.eq(driver[i]) & session.laps.IsAccurate.eq(True)].pick_fastest().LapTime.total_seconds()%60)), color='#' + session.results.loc[driver[i]].TeamColor, linewidth=linewidth, linestyle=linestyle)

# SPEED
axes[0].set_title(str(year) +' '+ session.event.EventName, color='black', fontproperties=titleFont)
axes[0].set_xlim(0,lapLength)
axes[0].set_ylim(60,360)
axes[0].yaxis.set_major_locator(MultipleLocator(60)) 
axes[0].yaxis.set_minor_locator(MultipleLocator(10))  
axes[0].xaxis.set_minor_locator(MultipleLocator(10000))
axes[0].set_xticks(track[2])
axes[0].yaxis.set_ticklabels(['',60,120,180,240,300,360], color='black', fontproperties=tickFont)
axes[0].set_ylabel('Speed (kph)', color='black', fontproperties=labelFont)
axes[0].legend(prop=legendFont)

# GEAR
axes[1].set_ylim(0.8,8.2)
axes[1].yaxis.set_major_locator(MultipleLocator(1)) 
axes[1].yaxis.set_minor_locator(MultipleLocator(1))
axes[1].yaxis.set_ticklabels(['','',2,'',4,'',6,'',8], color='black', fontproperties=tickFont)
axes[1].set_ylabel('Gear', color='black', fontproperties=labelFont)

# THROTTLE
axes[2].set_ylim(0,100)
axes[2].yaxis.set_major_locator(MultipleLocator(50)) 
axes[2].yaxis.set_minor_locator(MultipleLocator(10))  
axes[2].yaxis.set_ticklabels(['',0,50,100], color='black', fontproperties=tickFont)
axes[2].set_ylabel('Throttle (%)', color='black', fontproperties=labelFont)

# BRAKE
axes[3].set_ylim(-0.1,1.1)
axes[3].yaxis.set_major_locator(MultipleLocator(1))
axes[3].yaxis.set_minor_locator(MultipleLocator(1)) 
axes[3].yaxis.set_ticklabels(['','N','Y'], color='black', fontproperties=tickFont)
axes[3].xaxis.set_ticklabels(track[3], color='black', fontproperties=tickFont)
axes[3].set_ylabel('Brake', color='black', fontproperties=labelFont)

for i in range(4):
    axes[i].set_facecolor("white")
    axes[i].grid(ls='--')
    axes[i].axvline(track[2][1])
    axes[i].axvline(track[2][2])
axes[3].yaxis.grid(True, which='major') 

plt.subplots_adjust(left=0.13, bottom=0.07, right=0.97, top=0.95, hspace=0.1)
filename = 'D:/Onedrive/Docs/F1/fig/'+str(year)+'_'+gp+'_'+sess+'_telemetry.png'
plt.savefig(filename, dpi=192, facecolor='w', edgecolor='w', orientation='portrait', papertype=None,  format='png', transparent=False)
