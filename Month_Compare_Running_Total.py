import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
#graphs running total for 2 months

master_dict = get_data.my_filtered_activities()

def graph(master_dict,input3,input4):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input1 = 7
    input2 = 'distance_miles'

    x_list = []
    y_list = []

    x2_list = []
    y2_list = []

    ####

    #creates "running total" dictionary based on unit and number of days to total up
    #each day has a value which is calculated on the running total sum
    graph_dict = calc.full_running_totals(master_dict,input1,input2)
    graph_dict1 = graph_dict.copy()
    graph_dict2 = graph_dict.copy()

    #removes keys older and newer than specified
    for key in list(graph_dict1):
        if key < get_time.FOM(input3) or key > get_time.LOM(input3):  #fom0 is 1/1/18 lom8 is
            del graph_dict1[key]

    #create graphing dictionary
    for key in sorted(graph_dict1.keys()):
        y_list.append(graph_dict1[key])
    len_x = len(y_list) + 1
    x_list = range(1,len_x)

    #removes keys older and newer than specified
    for key in list(graph_dict2):
        if key < get_time.FOM(input4) or key > get_time.LOM(input4):  #fom0 is 1/1/18 lom8 is
            del graph_dict2[key]

    #create graphing dictionary
    for key in sorted(graph_dict2.keys()):
        y2_list.append(graph_dict2[key])
    len_x2 = len(y2_list) + 1
    x2_list = range(1,len_x2)

    plt.style.use('dark_background')
    #plt.axis('off')
    plt.rcParams['lines.linewidth'] = 1
    plt.plot(x_list,y_list, color='red')
    plt.plot(x2_list,y2_list, color='blue')
    plt.ylim(ymin=0)
    plt.title('Running Total - ' + str(input1) + ' days, Unit: ' + input2)


    #print(plt.style.available)
    plt.legend([get_time.what_month(get_time.FOM(input3).month)+" "+str(get_time.FOM(input3).year), get_time.what_month(get_time.FOM(input4).month)+" "+str(get_time.FOM(input4).year)], loc='best')
    plt.show()

list1 = list(range(0,15))
list2 = []
for x in list1:
    list2.append(str(get_time.what_month(get_time.FOM(x).month)) +" "+str(get_time.FOM(x).year))

for x,y in zip(list1,list2):
    print(str(x)+" - "+str(y))

input3 = int(input("What is the first month number? "))
input4 = int(input("What is the second month number? "))

graph(master_dict,input3,input4)
