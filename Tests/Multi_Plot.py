import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import numpy as np
from pprint import pprint

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

input1 = 90 #Blue
input4 = 365 #Red
input2 = 'distance_miles'
input3 = 12 #months back to graph

graph_dict_1 = {}

graph_dict_1 = calc.full_running_totals(master_dict.copy(),input1,input2)

for key in list(graph_dict_1.keys()):
    if key < get_time.FOM(input3):
        del graph_dict_1[key]

graph_dict_2 = {}

graph_dict_2 = calc.full_running_totals(master_dict.copy(),input4,input2)

for key in list(graph_dict_2.keys()):
    if key < get_time.FOM(input3):
        del graph_dict_2[key]



fig, (ax1,ax3,ax4) = plt.subplots(nrows=3, figsize=(13,9)) #figsize sets window

#plots top plot with shared x but different scale Y
ax1.plot(list(graph_dict_1.keys()),list(graph_dict_1.values()),'b')
ax1.set_xlabel('date')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel(str(input1), color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx() #second data set on plot
ax2.plot(list(graph_dict_2.keys()),list(graph_dict_2.values()),'r')
ax2.set_ylabel(str(input4), color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()

ax3.plot(list(graph_dict_1.keys()),list(graph_dict_1.values()),'b',label=str(input1)) #set up third
ax3.set_title(str(input1)+" Running Days Total")
ax4.plot(list(graph_dict_2.keys()),list(graph_dict_2.values()),'r',label=str(input4)) #set up fourth graph
ax4.set_title(str(input4)+" Running Days Total")
fig.subplots_adjust(hspace=0.3)
#fig.figsize=(12,10)
#fig.set_size_inches(11, 9) #sets actual image size in window
plt.show()
