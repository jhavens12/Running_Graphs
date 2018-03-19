import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np
import datetime
import pandas as pd
from random import randint
from sklearn.linear_model import LinearRegression
from time import mktime

master_dict = get_data.my_filtered_activities()

#Setup

def trend_line(x_list,y_list):
    df = pd.DataFrame()
    df['dates'] = x_list
    df['miles'] = y_list
    df['seconds'] = df.dates.apply(lambda x: mktime(x.timetuple()))
    model = LinearRegression().fit(df.seconds.values.reshape(-1,1), df.miles)
    df['y_trend'] = model.predict(df.seconds.values.reshape(-1,1))

    return df
print("1 - 2017")
print("2 - 2018")
q1 = int(input("How far back to graph? "))

if q1 == 1:
    diff = datetime.datetime.now() - datetime.datetime(2017, 1, 1)
if q1 == 2:
    diff = datetime.datetime.now() - datetime.datetime(2018, 1, 1)

weeks_back = int(diff.days/7)
weeks_to_calculate = list(range(1,weeks_back)) #calculate 0 to 17

week_dict = {}
for week in weeks_to_calculate:
    week_dict[week] = master_dict.copy() #make a master dict for each week to calculate

for week in week_dict:

    for key in list(week_dict[week]): #for each key in each master dictionary
        if key < get_time.LM(week): #if older than last monday (0 is 1, 1 is 2,2 mondays ago)
            del week_dict[week][key]
    for key in list(week_dict[week]):
       if key > get_time.LS(week-1): #if newer than last sunday (0 is 1)
           del week_dict[week][key]

#Mileage
miles_dict = {}
pace_dict = {}
hr_dict = {}
cad_dict = {}
tred_dict = {}
count_dict = {}

for week in week_dict:
    if week_dict[week]: #check to see if any activites exist in the given week
        mile_list = []
        pace_list = []
        hr_list = []
        cad_list = []
        tred_list = []
        count_list = []
        for activity in week_dict[week]:
            count_list.append(1)
            mile_list.append(float(week_dict[week][activity]['distance_miles']))
            pace_list.append(float(week_dict[week][activity]['pace_dec']))
            hr_list.append(float(week_dict[week][activity]['average_heartrate']))
            if 'average_cadence' in week_dict[week][activity]:
                cad_list.append(float(week_dict[week][activity]['average_cadence']))
                cad_dict[get_time.LM(week)] = sum(cad_list)/len(cad_list)
            else:
                cad_dict[get_time.LM(week)] = 0
            if 'treadmill_flagged' in week_dict[week][activity]:
                if week_dict[week][activity]['treadmill_flagged'] == 'yes':
                    tred_list.append(1)
            else:
                tred_list.append(0)
        hr_dict[get_time.LM(week)] = sum(hr_list)/len(hr_list)
        miles_dict[get_time.LM(week)] = sum(mile_list)
        pace_dict[get_time.LM(week)] = sum(pace_list)/len(pace_list)
        tred_dict[get_time.LM(week)] = sum(tred_list)
        count_dict[get_time.LM(week)] = sum(count_list)
    else:
        miles_dict[get_time.LM(week)] = 0
        pace_dict[get_time.LM(week)] = 0
        hr_dict[get_time.LM(week)] = 0
        count_dict[get_time.LM(week)] = 0

x_list = []
y_list = []
for month in miles_dict:
    x_list.append(month)
    y_list.append(miles_dict[month])

x2_list = []
y2_list = []
for month in pace_dict:
    x2_list.append(month)
    y2_list.append(pace_dict[month])

x3_list = []
y3_list = []
for month in hr_dict:
    x3_list.append(month)
    y3_list.append(hr_dict[month])

x4_list = []
y4_list = []
for month in cad_dict:
    x4_list.append(month)
    y4_list.append(cad_dict[month])

x5_list = []
y5_list = []
for month in tred_dict:
    x5_list.append(month)
    y5_list.append(tred_dict[month])

x6_list = []
y6_list = []
for month in count_dict:
    x6_list.append(month)
    y6_list.append(count_dict[month])


########
fig, (ax1,ax2,ax4) = plt.subplots(nrows=3, figsize=(13,8)) #figsize sets window

ax1df = trend_line(x_list,y_list)
#plots top plot with shared x but different scale Y
#ax1.set_title("Weekly Mileage")
ax1.bar(x_list,y_list,align='center',width=6)
ax1slope = str(float(ax1df['y_trend'].iloc[0]) - float(ax1df['y_trend'].iloc[-1]))
ax1.plot_date(ax1df.dates, ax1df.y_trend, 'red', ls='solid', marker='None',label=ax1slope)


#ax1.set_xlabel('Week Start', color='b')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Miles Ran', color='b')
ax1.tick_params('y', colors='b')
ax1.grid(True)
ax1.legend()

#ax2.set_title("Weekly Pace - Averages of Averages")
ax2.plot(x2_list,y2_list,'r',label='Pace')
#ax2.set_xlabel('Week Start', color='r')
ax2.set_ylabel('Pace (Decimal)', color='r')
ax2.tick_params('y', colors='r')
ax2.grid(True)

ax3 = ax2.twinx()
ax3.plot(x3_list,y3_list,'g',label='Avg HR')
ax3.set_ylabel('Avg of Avg HR', color='g')
ax3.tick_params('y', colors='g')

ax4.bar(x6_list,y6_list,align='center',width=6,color='b') #total runs
ax4.bar(x5_list,y5_list,align='center',width=6,color='r') #treadmill runs
ax4.set_ylabel('Runs Per Week', color='b')
ax4.set_yticks(range(max(y6_list)+1))
ax4.tick_params('y', colors='b')
ax4.grid(True)

#ax5 = ax4.twinx()
#ax5.bar(x6_list,y6_list,color='r')
#ax5.set_ylabel('Runs', color='r')
#ax5.tick_params('y', colors='r')

fig.tight_layout()
fig.subplots_adjust(hspace=0.3)
plt.show()

print("Need to fix so dates are consistent, possibly show every date instead of letting it choose")
