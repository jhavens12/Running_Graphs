import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

def graph_per_month_total(master_dict,choice_dict):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input2 = 'distance_miles'

    graph_dict = {}
    for choice in choice_dict:
        graph_dict[choice] = calc.monthly_daily_totals(master_dict.copy(),choice_dict[choice],input2) #calculates monthly totals for number of months chosen
        #returns dictionary of all computed values - keys eliminated in the monthly_daily_totals function
    for date_range,choice in zip(graph_dict,choice_dict): #for each month, graph values. Choice dict used for labels
        plt.plot(list(graph_dict[date_range].keys()),list(graph_dict[date_range].values()),label=(get_time.what_month(get_time.FOM(choice_dict[choice]).month)+" "+str(get_time.FOM(choice_dict[choice]).year)))

    plt.style.use('dark_background')
    plt.rcParams['lines.linewidth'] = 1
    plt.ylim(ymin=0)
    plt.title('Monthly Totals - '+' Unit: ' + input2)
    plt.legend()
    plt.show()

def graph_per_month_running(master_dict,choice_dict):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input1 = 7
    input2 = 'distance_miles'

    graph_dict = {}
    for choice in choice_dict:
        graph_dict[choice] = calc.full_running_totals(master_dict.copy(),input1,input2) #duplicates data dictionary into number of months given

    for date_range,choice in zip(graph_dict,choice_dict):
        for key in list(graph_dict[date_range].keys()):
            if key < get_time.FOM(choice_dict[choice]) or key > get_time.LOM(choice_dict[choice]):  #
                del graph_dict[date_range][key] #eliminates keys older or newer than specified for each month

        y_list = []
        for key in sorted(graph_dict[date_range].keys()):
            y_list.append(graph_dict[date_range][key]) #gets y values
        x_list = list(range(1,len(list(graph_dict[date_range].keys()))+1)) #calculates x values based on y values

        plt.plot(x_list,y_list,label=(get_time.what_month(get_time.FOM(choice_dict[choice]).month)+" "+str(get_time.FOM(choice_dict[choice]).year)))

    plt.style.use('dark_background')
    plt.rcParams['lines.linewidth'] = 1
    plt.ylim(ymin=0)
    plt.title('Running Total - ' + str(input1) + ' days, Unit: ' + input2)
    plt.legend()
    plt.show()

list1 = list(range(0,15)) #past 15 months
list2 = []
for x in list1:
    list2.append(str(get_time.what_month(get_time.FOM(x).month)) +" "+str(get_time.FOM(x).year)) #generates month and years

for x,y in zip(list1,list2):
    print(str(x)+" - "+str(y)) #prints out nice list

q1 = int(input("How many months would you like to graph? "))
q2 = int(input("Running Graph or Total? \n 1 - Total \n 2 - Running \n"))

choice_dict = {}
for q in list(range(1,q1+1)):
    choice_dict[q] = int(input("What is the number "+str(q)+" month number? "))
if q2 == 1: #total choice
    graph_per_month_total(master_dict,choice_dict)
if q2 == 2: #running choice
    graph_per_month_running(master_dict,choice_dict)
