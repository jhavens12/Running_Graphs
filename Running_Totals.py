import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
import numpy as np
from pprint import pprint

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information
# for x in master_dict:
#     print(master_dict[x]['map']['summary_polyline'])

input1 = 365 #Blue
input2 = 90 #Red
input3 = 30 #
input4 = 8 #
input5 = 7
input6 = 1

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

#
graph_dict_5 = {}
graph_dict_5 = calc.full_running_totals(master_dict.copy(),input5,'distance_miles')

for key in list(graph_dict_5.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_5[key]

#
graph_dict_6 = {}
graph_dict_6 = calc.full_running_totals(master_dict.copy(),input6,'distance_miles')

for key in list(graph_dict_6.keys()):
    if key < get_time.FOM(months_back):
        del graph_dict_6[key]

fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(nrows=6, figsize=(17,10)) #figsize sets window

ax1.plot(list(graph_dict_1.keys()),list(graph_dict_1.values()),'red')
ax1.set_title(str(input1)+" Running Days Total")
ax1.grid(True)

ax2.plot(list(graph_dict_2.keys()),list(graph_dict_2.values()),'blue') #set up third
ax2.set_title(str(input2)+" Running Days Total")
ax2.grid(True)

ax3.plot(list(graph_dict_3.keys()),list(graph_dict_3.values()),'green') #set up fourth graph
ax3.set_title(str(input3)+" Running Days Total")
ax3.grid(True)

ax4.plot(list(graph_dict_4.keys()),list(graph_dict_4.values()),'red') #set up fourth graph
ax4.set_title(str(input4)+" Running Days Total")
ax4.grid(True)

ax5.plot(list(graph_dict_5.keys()),list(graph_dict_5.values()),'blue') #set up fourth graph
ax5.set_title(str(input5)+" Running Days Total")
ax5.grid(True)

ax6.plot(list(graph_dict_6.keys()),list(graph_dict_6.values()),'green') #set up fourth graph
ax6.set_title(str(input6)+" Running Days Total")
ax6.grid(True)

fig.subplots_adjust(hspace=0.3)
fig.tight_layout()
plt.show()
