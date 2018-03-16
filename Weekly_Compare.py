import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np

master_dict = get_data.my_filtered_activities()

#Setup

weeks_to_calculate = list(range(1,60)) #calculate 0 to 17

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

week_dict_1 = week_dict_2 = week_dict_3 = week_dict.copy()

#Mileage
miles_dict = {}

for week in week_dict_1:
    if week_dict_1[week]: #check to see if any activites exist in the given week
        mile_list = []
        for activity in week_dict_1[week]:
            mile_list.append(float(week_dict_1[week][activity]['distance_miles']))
        miles_dict[get_time.LM(week)] = sum(mile_list)
    else:
        miles_dict[get_time.LM(week)] = 0

x_list = []
y_list = []
for month in miles_dict:
    x_list.append(month)
    y_list.append(miles_dict[month])

#Pace
pace_dict = {}

for week in week_dict_2:
    if week_dict_2[week]: #check to see if any activites exist in the given week
        pace_list = []
        for activity in week_dict_2[week]:
            pace_list.append(float(week_dict_2[week][activity]['pace_dec']))
        pace_dict[get_time.LM(week)] = sum(pace_list)/len(pace_list)
    else:
        pace_dict[get_time.LM(week)] = 0

x2_list = []
y2_list = []
for month in pace_dict:
    x2_list.append(month)
    y2_list.append(pace_dict[month])

#Average HR


########
fig, (ax1,ax2) = plt.subplots(nrows=2, figsize=(13,9)) #figsize sets window

#plots top plot with shared x but different scale Y
ax1.set_title("Weekly Mileage")
ax1.bar(x_list,y_list,align='center',width=6)
ax1.set_xlabel('Week Start', color='b')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Miles Ran', color='b')
ax1.tick_params('y', colors='b')

ax2.set_title("Weekly Pace - Averages of Averages")
ax2.plot(x2_list,y2_list,'r')
ax2.set_xlabel('Week Start', color='r')
ax2.set_ylabel('Pace (Decimal)', color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()
fig.subplots_adjust(hspace=0.3)
plt.legend()
plt.show()
