#Just prints a list of mondays and their corresponding run amounts for M-S
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

diff = datetime.datetime.now() - datetime.datetime(2017, 1, 1)

weeks_back = int(diff.days/7) + 1
weeks_to_calculate = list(range(0,weeks_back)) #calculate 0 to 17

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

for week in week_dict:
    if week_dict[week]: #check to see if any activites exist in the given week
        mile_list = []
        count_list = []
        for activity in week_dict[week]:
            count_list.append(1)
            mile_list.append(float(week_dict[week][activity]['distance_miles']))
        miles_dict[get_time.LM(week)] = sum(mile_list)

pprint(miles_dict)
