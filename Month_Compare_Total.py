import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint

master_dict = get_data.my_filtered_activities()

def graph(master_dict,input3,input4):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input2 = 'distance_miles'

    x_list,y_list = calc.monthly_daily_totals(master_dict.copy(),input3,input2)
    x2_list,y2_list = calc.monthly_daily_totals(master_dict.copy(),input4,input2)

    for x,y in zip(x_list,y_list):
        print(str(x)+" "+str(y))

    for x,y in zip(x2_list,y2_list):
        print(str(x)+" "+str(y))

    plt.style.use('dark_background')
    plt.rcParams['lines.linewidth'] = 1
    plt.plot(x_list,y_list, color='red')
    plt.plot(x2_list,y2_list, color='blue')
    plt.ylim(ymin=0)
    plt.title('Monthly Totals - '+' Unit: ' + input2)
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
