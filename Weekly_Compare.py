import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint

master_dict = get_data.my_filtered_activities()

#calculate weekly totals for the year
#ex {1:15.4, 2:16.5}
#How to bridge across years?

#Create dictionary, a copy for each week I need
#go through and limit each dictionary
#keys are weeks in the year
#could do weeks back from today?

#  _____ _   _ _____  _    _ _______
# |_   _| \ | |  __ \| |  | |__   __|
#   | | |  \| | |__) | |  | |  | |
#   | | | . ` |  ___/| |  | |  | |
#  _| |_| |\  | |    | |__| |  | |
# |_____|_| \_|_|     \____/   |_|

x_list = []
y_list = []

time_input = 0
unit_input = 'distance_miles'

weeks_to_calculate = list(range(0,17))
week_dict = {}
for week in weeks_to_calculate:
    week_dict[week] = master_dict.copy()

x_labels = []
for week in week_dict:
    x_labels.append(str(get_time.LM(week+1).year)+" - "+str(get_time.LM(week+1).isocalendar()[1]))
    for key in list(week_dict[week]):
        if key < get_time.LM(week+1): #if older than last monday (0 is 1, 1 is 2,2 mondays ago)
            del week_dict[week][key]
    for key in list(week_dict[week]):
       if key > get_time.LS(week): #if newer than last sunday (0 is 1)
           del week_dict[week][key]

final_dict = {}
for week in week_dict:
    if week_dict[week]: #check to see if any activites exist in the given week
        mile_list = []
        for activity in week_dict[week]:
            mile_list.append(float(week_dict[week][activity][unit_input]))
        final_dict[week] = sum(mile_list)
    else:
        final_dict[week] = 0

pprint(final_dict)
for month in sorted(final_dict.keys()):
    x_list.append(month)
    y_list.append(final_dict[month])

plt.bar(list(final_dict.keys()),list(final_dict.values()))
plt.style.use('dark_background')
plt.rcParams['lines.linewidth'] = 1
plt.ylim(ymin=0)
plt.xticks(list(final_dict.keys()),x_labels)
#plt.title('Running Total - ' + str(input1) + ' days, Unit: ' + input2)
plt.legend()
plt.show()
