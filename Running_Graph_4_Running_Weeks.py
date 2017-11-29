import get_time
import get_data
import calc
import graph
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates

master_dict = get_data.my_filtered_activities()

def graph(master_dict,unit):
    #elapsed_time, distance_miles, average_speed, kudos_count, max_heartrate, average_heartrate, max_speed, pace_dec, total_elevation_gain,
    #athlete_count, average_temp, achivement_count
    input1 = 8
    input2 = 'distance_miles'

    x_list = []
    y_list = []
    x2_list = []
    y2_list = []
    x3_list = []
    y3_list = []
    x4_list = []
    y4_list = []

    graph_dict = calc.full_running_totals(master_dict,input1,input2)
    graph_dict1 = graph_dict.copy()
    graph_dict2 = graph_dict.copy()
    graph_dict3 = graph_dict.copy()
    graph_dict4 = graph_dict.copy()

    for key in list(graph_dict1):
        if key < get_time.running_week(0): #if time is greater than now
            del graph_dict1[key]
    # for key in list(graph_dict1):
    #    if key > get_time.running_week(0):
    #        del graph_dict1[key]

    for key in sorted(graph_dict1.keys()):
        x_list.append(key)
        y_list.append(graph_dict1[key])
    len_x = len(x_list)
    x_list2 = range(len_x)

    for key in list(graph_dict2):
        if key < get_time.running_week(1):
            del graph_dict2[key]
    for key in list(graph_dict2):
       if key > get_time.running_week(0):
           del graph_dict2[key]

    for key in sorted(graph_dict2.keys()):
        x2_list.append(key)
        y2_list.append(graph_dict2[key])
    len_x2 = len(x2_list)
    x2_list2 = range(len_x2)

    for key in list(graph_dict3):
        if key < get_time.running_week(2):
            del graph_dict3[key]
    for key in list(graph_dict3):
       if key > get_time.running_week(1):
           del graph_dict3[key]
    for key in sorted(graph_dict3.keys()):
        x3_list.append(key)
        y3_list.append(graph_dict3[key])
    len_x3 = len(x3_list)
    x3_list2 = range(len_x3)

    for key in list(graph_dict4):
        if key < get_time.running_week(3):
            del graph_dict4[key]
    for key in list(graph_dict4):
       if key > get_time.running_week(2):
           del graph_dict4[key]
    for key in sorted(graph_dict4.keys()):
        x4_list.append(key)
        y4_list.append(graph_dict4[key])
    len_x4 = len(x4_list)
    x4_list2 = range(len_x4)

    plt.style.use('dark_background')
    #plt.axis('off')
    plt.rcParams['lines.linewidth'] = 1
    plt.plot(x_list2,y_list, color='red')
    plt.plot(x2_list2,y2_list, color='blue')
    plt.plot(x3_list2,y3_list, color='green')
    plt.plot(x4_list2,y4_list, color='yellow')
    plt.title('Previous 4 Running Weeks - ' + str(input1) + ' days total, Unit: ' + input2)
    #plt.ylim(ymin=0)

    label1 = calc.month_day(get_time.running_week(0))+" - "+calc.month_day(get_time.running_week(-1))
    label2 = calc.month_day(get_time.running_week(1))+" - "+calc.month_day(get_time.running_week(0))
    label3 = calc.month_day(get_time.running_week(2))+" - "+calc.month_day(get_time.running_week(1))
    label4 = calc.month_day(get_time.running_week(3))+" - "+calc.month_day(get_time.running_week(2))

    #print(plt.style.available)
    plt.legend([label1, label2, label3, label4], loc='best')
    plt.show()

graph(master_dict,"nothing")
