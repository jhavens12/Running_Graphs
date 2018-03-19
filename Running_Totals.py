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
input2 = 365 #Red
input3 = 7 #
input4 = 8 #

months_back = 15


graph_dict_1 = {}
graph_dict_1 = calc.full_running_totals(master_dict.copy(),input1,'distance_miles')

for key in list(graph_dict_1.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_1[key]

#
graph_dict_2 = {}
graph_dict_2 = calc.full_running_totals(master_dict.copy(),input2,'distance_miles')

for key in list(graph_dict_2.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_2[key]

#
graph_dict_3 = {}
graph_dict_3 = calc.full_running_totals(master_dict.copy(),input3,'distance_miles')

for key in list(graph_dict_3.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_3[key]

#
graph_dict_4 = {}
graph_dict_4 = calc.full_running_totals(master_dict.copy(),input4,'distance_miles')

for key in list(graph_dict_4.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_4[key]

fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=4, figsize=(17,10)) #figsize sets window

#plots top plot with shared x but different scale Y
ax1.plot(list(graph_dict_1.keys()),list(graph_dict_1.values()),'blue')
ax1.set_title(str(input1)+" Running Days Total")
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel(str(input1), color='blue')
ax1.tick_params('y', colors='blue')
ax1.grid(True)

ax2.plot(list(graph_dict_2.keys()),list(graph_dict_2.values()),'red') #set up third
ax2.set_title(str(input2)+" Running Days Total")
ax2.grid(True)

ax3.plot(list(graph_dict_3.keys()),list(graph_dict_3.values()),'green') #set up fourth graph
ax3.set_title(str(input3)+" Running Days Total")
ax3.grid(True)

ax4.plot(list(graph_dict_4.keys()),list(graph_dict_4.values()),'black') #set up fourth graph
ax4.set_title(str(input4)+" Running Days Total")
ax4.grid(True)

fig.subplots_adjust(hspace=0.3)
#fig.figsize=(12,10)
#fig.set_size_inches(11, 9) #sets actual image size in window
fig.tight_layout()
plt.show()
