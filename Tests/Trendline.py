import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import numpy as np
from pprint import pprint
import datetime

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

input1 = 90 #Blue
input4 = 365 #Red
input2 = 'distance_miles'
input3 = 12 #months back to graph

graph_dict_1 = {}

graph_dict = calc.full_running_totals(master_dict.copy(),input1,input2)

for key in list(graph_dict.keys()):
    if key < get_time.FOM(input3):
        del graph_dict[key]

graph_dict_2 = {}

graph_dict_2 = calc.full_running_totals(master_dict.copy(),input4,input2)

for key in list(graph_dict_2.keys()):
    if key < get_time.FOM(input3):
        del graph_dict_2[key]

######
def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

x = list(graph_dict.keys())
y = list(graph_dict.values())

x2 = []
for value in x:
    x2.append(datetime_to_float(value))

plt.plot(x, y)

#plt.style.use('dark_background')
#plt.rcParams['lines.linewidth'] = 1
#plt.ylim(ymin=0)
#plt.title('Running '+str(input1)+' Day Total Over '+str(input3)+' Months, Unit: ' + input2)

fit = np.polyfit(x2, y, deg=1)
plt.plot(x2, fit[0] * x2 + fit[1], color='red')


plt.legend()
plt.subplots_adjust(left=.05, right=.95, bottom=.05, top=.95)
plt.show()
