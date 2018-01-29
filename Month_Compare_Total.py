import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
#calculates the total per month, given the option to graph multiple months

master_dict = get_data.my_filtered_activities()

def graph_per_month_total(master_dict,choice_dict):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input2 = 'distance_miles'

    graph_dict = {}
    for choice in choice_dict:
        graph_dict[choice] = calc.monthly_daily_totals(master_dict.copy(),choice_dict[choice],input2)

    for date_range,choice in zip(graph_dict,choice_dict):
        plt.plot(list(graph_dict[date_range].keys()),list(graph_dict[date_range].values()),label=(get_time.what_month(get_time.FOM(choice_dict[choice]).month)+" "+str(get_time.FOM(choice_dict[choice]).year)))

    plt.style.use('dark_background')
    plt.rcParams['lines.linewidth'] = 1
    plt.ylim(ymin=0)
    plt.title('Monthly Totals - '+' Unit: ' + input2)
    plt.legend()
    plt.show()

list1 = list(range(0,15)) #past 15 months
list2 = []
for x in list1:
    list2.append(str(get_time.what_month(get_time.FOM(x).month)) +" "+str(get_time.FOM(x).year))

for x,y in zip(list1,list2):
    print(str(x)+" - "+str(y))

q1 = int(input("How many months would you like to graph? "))

choice_dict = {}
for q in list(range(1,q1+1)):
    choice_dict[q] = int(input("What is the number "+str(q)+" month number? "))

pprint(choice_dict)
graph_per_month_total(master_dict,choice_dict)
