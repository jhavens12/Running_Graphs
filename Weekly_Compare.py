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
import matplotlib.dates as mdates

master_dict = get_data.my_filtered_activities()
#Setup

def format_number(number):
    return str("{0:.2f}".format(number))

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
print("3 - JUST 2017")
q1 = int(input("How far back to graph? "))

if q1 == 1:
    diff = datetime.datetime.now() - datetime.datetime(2017, 1, 1)

    weeks_back = int(diff.days/7) + 1
    weeks_to_calculate = list(range(0,weeks_back)) #calculate 0 to 17

if q1 == 2:
    diff = datetime.datetime.now() - datetime.datetime(2018, 1, 1)
    weeks_back = int(diff.days/7) + 1
    weeks_to_calculate = list(range(0,weeks_back)) #calculate 0 to 17

if q1 == 3:
    last = datetime.datetime.now() - datetime.datetime(2017, 1, 1)
    this = datetime.datetime.now() - datetime.datetime(2018, 1, 1)
    weeks_back_last = int(last.days/7) + 1
    weeks_back_this = int(this.days/7) + 1
    last_list = list(range(0,weeks_back_last))
    this_list = list(range(0,weeks_back_this))
    weeks_to_calculate = [x for x in last_list if x not in this_list]

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
ele_dict = {}
tred_dict = {}
count_dict = {}
partner_dict = {}

for week in week_dict:
    if week_dict[week]: #check to see if any activites exist in the given week
        mile_list = []
        pace_list = []
        hr_list = []
        ele_list = []
        tred_list = []
        partner_list = []
        count_list = []
        for activity in week_dict[week]:
            count_list.append(1)
            mile_list.append(float(week_dict[week][activity]['distance_miles']))
            pace_list.append(float(week_dict[week][activity]['pace_dec']))
            hr_list.append(float(week_dict[week][activity]['average_heartrate']))
            #print(week_dict[week][activity]['average_heartrate'])
            if 'total_elevation_feet' in week_dict[week][activity]:
                ele_list.append(float(week_dict[week][activity]['total_elevation_feet']))
                ele_dict[get_time.LM(week)] = sum(ele_list)#/len(ele_list)
            # else:
            #     ele_dict[get_time.LM(week)] = 0
            if 'treadmill_flagged' in week_dict[week][activity]:
                if week_dict[week][activity]['treadmill_flagged'] == 'yes':
                    tred_list.append(1)
            if 'athlete_count' in week_dict[week][activity]:
                if week_dict[week][activity]['athlete_count'] > 1:
                    partner_list.append(1)
            # else:
            #     tred_list.append(0)
        hr_dict[get_time.LM(week)] = sum(hr_list)/len(hr_list)
        miles_dict[get_time.LM(week)] = sum(mile_list)
        pace_dict[get_time.LM(week)] = sum(pace_list)/len(pace_list)
        tred_dict[get_time.LM(week)] = sum(tred_list)
        count_dict[get_time.LM(week)] = sum(count_list)
        partner_dict[get_time.LM(week)] = sum(partner_list)
    # else:
    #     miles_dict[get_time.LM(week)] = 0
    #     pace_dict[get_time.LM(week)] = 0
    #     hr_dict[get_time.LM(week)] = 0
    #     count_dict[get_time.LM(week)] = 0

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
for month in ele_dict:
    x4_list.append(month)
    y4_list.append(ele_dict[month])

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

x7_list = []
y7_list = []
for month in partner_dict:
    x7_list.append(month)
    y7_list.append(partner_dict[month])

########
fig, (ax1,ax2,ax4,ax5) = plt.subplots(nrows=4, figsize=(13,8)) #figsize sets window

myFmt = mdates.DateFormatter('%m/%d')

ax1df = trend_line(x_list, y_list)
ax1.bar(x_list, y_list, align='center', width=6, label="Total: "+format_number(sum(y_list)))
ax1slope = format_number(float(ax1df['y_trend'].iloc[0]) - float(ax1df['y_trend'].iloc[-1]))
ax1.plot_date(ax1df.dates, ax1df.y_trend, 'red', ls='--', marker='None',label=ax1slope)
ax1.set_ylabel('Miles Ran', color='b')
ax1.set_yticks(range(int(max(y_list))+1),3)

ax1.set_xticks(x_list)

ax1.tick_params('y', colors='b')
ax1.yaxis.grid(True)
ax1.legend()

labels = ax1.set_xticklabels(x_list)
for i, label in enumerate(labels):
    label.set_y(label.get_position()[1] - (i % 2) * 0.09)

ax1.xaxis.set_major_formatter(myFmt)

####
ax2.plot(x2_list,y2_list, color='g', linewidth=2, label='Pace: '+format_number(sum(y2_list)/len(y2_list)))
ax2.set_ylabel('Pace (Decimal)', color='g')
ax2.tick_params('y', colors='g')
ax2.yaxis.grid(True)
ax2.set_xticks(x2_list)
labels = ax2.set_xticklabels(x2_list)
for i, label in enumerate(labels):
    label.set_y(label.get_position()[1] - (i % 2) * 0.09)
ax2.xaxis.set_major_formatter(myFmt)
ax2.legend()

ax3 = ax2.twinx()
ax3.plot(x3_list,y3_list, color='r', label='Avg HR')
ax3.set_ylabel('Avg of Avg HR', color='r')
ax3.tick_params('y', colors='r')


#Outside/partner/treadmill
ax4.bar(x6_list,y6_list, align='center', width=6, color='b', label='Outdoor') #total runs
ax4.bar(x5_list,y5_list, align='center', width=6, color='#fc5e02', label=('Treadmill: '+str(sum(y5_list)))) #treadmill runs
ax4.bar(x7_list,y7_list, align='center', width=6, color='#f442e2', label=('Partner: '+str(sum(y7_list)))) #treadmill runs
ax4.set_ylabel('Runs Per Week', color='b')
ax4.set_yticks(range(max(y6_list)+1))
ax4.set_xticks(x5_list)
labels = ax4.set_xticklabels(x5_list)
for i, label in enumerate(labels):
    label.set_y(label.get_position()[1] - (i % 2) * 0.09)
ax4.xaxis.set_major_formatter(myFmt)
ax4.tick_params('y', colors='b')
ax4.yaxis.grid(True)
ax4.legend()

#elevation
ax5.plot(x4_list,y4_list, label='Total: '+format_number(sum(y4_list)))
ax5.set_ylabel('Total Elevation (Feet)')
#ax5.set_yticks(range(int(max(y4_list)+1)),20)
ax5.set_xticks(x4_list)
labels = ax5.set_xticklabels(x4_list)
for i, label in enumerate(labels):
    label.set_y(label.get_position()[1] - (i % 2) * 0.09)
ax5.xaxis.set_major_formatter(myFmt)
ax5.yaxis.grid(True)
ax5.legend()

plt.setp(ax1.get_xticklabels(), rotation=0, horizontalalignment='center')
plt.setp(ax2.get_xticklabels(), rotation=0, horizontalalignment='center')
plt.setp(ax4.get_xticklabels(), rotation=0, horizontalalignment='center')
plt.setp(ax5.get_xticklabels(), rotation=0, horizontalalignment='center')

fig.tight_layout()
fig.subplots_adjust(hspace=0.3)
plt.show()
