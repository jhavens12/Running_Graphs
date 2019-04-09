#compares this current year to last years efforts

import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from time import mktime
import datetime

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information
single_dict = {}

for event in master_dict:
    if master_dict[event]['athlete_count'] == 1:
        if master_dict[event]['treadmill_flagged'] == 'no':
            single_dict[event] = master_dict[event]

single_yearly_dict = calc.yearly_totals(single_dict.copy(),0) #this year
single_yearly_dict_2 = calc.yearly_totals(single_dict.copy(),1) #last year

print("This year:")
print(len(single_yearly_dict))

print("last year:")
print(len(single_yearly_dict_2))
####********

yearly_dict = calc.yearly_totals(master_dict.copy(),0) #current year
yearly_dict2 = calc.yearly_totals(master_dict.copy(),1) #last year
#pprint(yearly_dict2)

fig, (ax1,ax2) = plt.subplots(nrows=2, figsize=(13,8))

ax1.plot(list(yearly_dict.keys()),list(yearly_dict.values()),label=('This Year'),color='green')
ax1.plot(list(yearly_dict2.keys()),list(yearly_dict2.values()),label=('Last Year'))

def graph(formula, x_range,title,plot_number,color):
    x = np.array(x_range)
    y = eval(formula)
    plot_number.plot(x, y, color, label=title, linestyle=':')

def format_number(number):
    return str("{0:.2f}".format(number))

graph('x*(600/365)', range(0,366),"600 Miles",ax1,'r')
graph('x*(365/365)', range(0,366),"365 Miles",ax1,'b')
ax1.set_title('Yearly Totals')
ax1.legend()

#ax2 setup
x_list = []
y_list = []
x2_list = []
y2_list = []

todays_number = datetime.datetime.now().timetuple().tm_yday #finds number of year
month_ago_number = todays_number - 30 #number to filter entires out from since not datetime objects


for event in yearly_dict:
    x_list.append(event)
    y_list.append(yearly_dict[event])
    if event > month_ago_number:
        x2_list.append(event)
        y2_list.append(yearly_dict[event])

def extended_prediction(x_list,y_list,end_day):
    extended_range = list(range(x_list[0],end_day))
    model = np.polyfit(x_list, y_list, 1)
    predicted = np.polyval(model, extended_range)
    return extended_range, predicted

extended_range, predicted = extended_prediction(x_list, y_list, 365)
extended_range_30, predicted_30 = extended_prediction(x2_list, y2_list, 365)

# ######
# the_list = []
# for x,y in zip(extended_range_30,predicted_30):
#     if y > 600:
#         the_list.append(x)
# print()
# print(the_list)
# goal_day = the_list[0]
# #day_of_year = datetime.now().timetuple().tm_yday
# timestamp = datetime.datetime.now()
# goal_day_nice = datetime.datetime(timestamp.year, 1, 1) + datetime.timedelta(goal_day - 1)
# print(str(goal_day_nice)+" is the day we will hit 600 miles based on the past 30 days")

####

label1 = "30 Days: "+format_number(predicted_30[-1])
label2 = "2018: "+format_number(predicted[-1])

graph('x*(600/365)', range(0,366),"600 Miles",ax2,'r')
ax2.plot(extended_range, predicted, label=label2, linestyle='--')
ax2.plot(extended_range_30, predicted_30, label=label1, linestyle='--')
ax2.plot(list(yearly_dict.keys()),list(yearly_dict.values()),label=('This Year'),color='green',lw='1')
ax2.legend()

fig.tight_layout()
fig.subplots_adjust(hspace=0.3)
plt.show()
