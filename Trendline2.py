import matplotlib.pyplot as plt
import pandas as pd
from random import randint
from sklearn.linear_model import LinearRegression
from time import mktime
import get_time
import get_data
import calc
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np
import datetime

master_dict = get_data.my_filtered_activities()
diff = datetime.datetime.now() - datetime.datetime(2017, 1, 1)
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
        for activity in week_dict[week]:
            mile_list.append(float(week_dict[week][activity]['distance_miles']))
        miles_dict[get_time.LM(week)] = sum(mile_list)
    else:
        miles_dict[get_time.LM(week)] = 0


x_list = []
y_list = []
for month in miles_dict:
    x_list.append(month)
    y_list.append(miles_dict[month])

def trend_line(x_list,y_list):
    df = pd.DataFrame()
    df['dates'] = x_list
    df['miles'] = y_list
    df['seconds'] = df.dates.apply(lambda x: mktime(x.timetuple()))
    model = LinearRegression().fit(df.seconds.values.reshape(-1,1), df.miles)
    df['y_trend'] = model.predict(df.seconds.values.reshape(-1,1))

    return df

ax1df = trend_line(x_list,y_list)


fig, ax = plt.subplots(figsize=(13,8))
ax.bar(x_list,y_list,align='center',width=6)
ax.plot_date(ax1df.dates, ax1df.y_trend, 'red', ls='solid', marker='None')
#ax.plot_date(df.dates, df.y_trend, 'red', ls='solid', marker='None')
ax.grid()
plt.show()
