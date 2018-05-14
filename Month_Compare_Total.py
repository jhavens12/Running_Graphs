import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

pprint(master_dict)

def graph_per_month_total(master_dict,choice_dict,unit_dict):
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

def graph_per_month_running(master_dict,choice_dict,unit_dict,days_total):
    input1 = days_total
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

unit_dict = {1:'distance_miles', 2:'elapsed_time', 3:'average_speed', 4:'kudos_count', 5:'max_heartrate', 6:'average_heartrate', 7:'max_speed', 8:'pace_dec', 9:'total_elevation_gain', \
    10:'athlete_count', 11:'average_temp', 12:'achivement_count'}

list1 = list(range(0,15)) #past 15 months
list2 = []
for x in list1:
    list2.append(str(get_time.what_month(get_time.FOM(x).month)) +" "+str(get_time.FOM(x).year)) #generates month and years

for x,y in zip(list1,list2):
    print(str(x)+" - "+str(y)) #prints out nice list

q2 = int(input("Running Graph or Total? \n 1 - Total \n 2 - Running \n"))
q1 = int(input("How many months would you like to graph? "))

#for option in unit_dict:
    #print(str(option)+" - "+unit_dict[option])
choice_dict = {}
full_choice_dict = {1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14}
chosen_unit_dict = {}

if q1 == 15:
    if q2 == 1: #total choice
        graph_per_month_total(master_dict,full_choice_dict,chosen_unit_dict)
    if q2 == 2: #running choice
        graph_per_month_running(master_dict,full_choice_dict,chosen_unit_dict)
else:
    for q in list(range(1,q1+1)):
        choice_dict[q] = int(input("What is the number "+str(q)+" month number? "))
        #chosen_unit_dict[q] = unit_dict[int(input("What unit should be graphed? "))]

    if q2 == 1: #total choice
        graph_per_month_total(master_dict,choice_dict,chosen_unit_dict)
    if q2 == 2: #running choice
        q3 = int(input("How many running total days? "))
        graph_per_month_running(master_dict,choice_dict,chosen_unit_dict,q3)
