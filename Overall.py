#function to show continual running graph across span of months
import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

input1 = 90 #days to total
input2 = 'distance_miles'
input3 = 12 #months back to graph

graph_dict = {}

graph_dict = calc.full_running_totals(master_dict.copy(),input1,input2)

for key in list(graph_dict.keys()):
    if key < get_time.FOM(input3):
        del graph_dict[key]

plt.plot(list(graph_dict.keys()),list(graph_dict.values()))

plt.style.use('dark_background')
plt.rcParams['lines.linewidth'] = 1
plt.ylim(ymin=0)
plt.title('Running '+str(input1)+' Day Total Over '+str(input3)+' Months, Unit: ' + input2)
plt.legend()
plt.subplots_adjust(left=.05, right=.95, bottom=.05, top=.95)
plt.show()
