import matplotlib
matplotlib.use('Agg')

import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np
import datetime
import pandas as pd
from random import randint
from sklearn.linear_model import LinearRegression
from time import mktime
import yagmail
import io
import credentials
#####

global mass_figsize
mass_figsize=(15,10)

#####
gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP( gmail_user, gmail_password)

global graph_list
graph_list = []

master_dict = get_data.my_filtered_activities()

def append_image(graph_name,plt):
    name = './temp/'+graph_name+'.png'
    plt.savefig(name)
    graph_list.append(name)

def send_mail():
    timestamp = str(datetime.datetime.now())
    yag.send('jhavens12@gmail.com', 'Running Graphs', contents=[timestamp,graph_list])

def format_number(number):
    return str("{0:.2f}".format(number))

def trend_line(x_list,y_list):
    df = pd.DataFrame()
    df['dates'] = x_list
    df['miles'] = y_list
    df['seconds'] = df.dates.apply(lambda x: mktime(x.timetuple()))
    model = LinearRegression().fit(df.seconds.values.reshape(-1,1), df.miles)
    df['y_trend'] = model.predict(df.seconds.values.reshape(-1,1))

    return df

def weekly_compare():

    diff = datetime.datetime.now() - datetime.datetime(2018, 1, 1)

    weeks_back = int(diff.days/7)
    weeks_to_calculate = list(range(0,weeks_back)) #calculate 0 to 17

    week_dict = {}
    for week in weeks_to_calculate:
        week_dict[week] = master_dict.copy() #make a master dict for each week to calculate

    for week in week_dict:

        for key in list(week_dict[week]): #for each key in each master dictionary
            if key < get_time.LM(week): #if older than last monday (0 is 1, 1 is 2,2 mondays ago)
                del week_dict[week][key]
        for key in list(week_dict[week]):
           if key > get_time.LS(week-1): #if newer than last sunday (0 is 1)
               del week_dict[week][key]

    #Mileage
    miles_dict = {}
    pace_dict = {}
    hr_dict = {}
    ele_dict = {}
    tred_dict = {}
    count_dict = {}

    for week in week_dict:
        if week_dict[week]: #check to see if any activites exist in the given week
            mile_list = []
            pace_list = []
            hr_list = []
            ele_list = []
            tred_list = []
            count_list = []
            for activity in week_dict[week]:
                count_list.append(1)
                mile_list.append(float(week_dict[week][activity]['distance_miles']))
                pace_list.append(float(week_dict[week][activity]['pace_dec']))
                hr_list.append(float(week_dict[week][activity]['average_heartrate']))
                #print(week_dict[week][activity]['average_heartrate'])
                if 'total_elevation_feet' in week_dict[week][activity]:
                    ele_list.append(float(week_dict[week][activity]['total_elevation_feet']))
                    ele_dict[get_time.LM(week)] = sum(ele_list)#/len(ele_list)
                else:
                    ele_dict[get_time.LM(week)] = 0
                if 'treadmill_flagged' in week_dict[week][activity]:
                    if week_dict[week][activity]['treadmill_flagged'] == 'yes':
                        tred_list.append(1)
                else:
                    tred_list.append(0)
            hr_dict[get_time.LM(week)] = sum(hr_list)/len(hr_list)
            miles_dict[get_time.LM(week)] = sum(mile_list)
            pace_dict[get_time.LM(week)] = sum(pace_list)/len(pace_list)
            tred_dict[get_time.LM(week)] = sum(tred_list)
            count_dict[get_time.LM(week)] = sum(count_list)
        else:
            miles_dict[get_time.LM(week)] = 0
            pace_dict[get_time.LM(week)] = 0
            hr_dict[get_time.LM(week)] = 0
            count_dict[get_time.LM(week)] = 0

    x_list = []
    y_list = []
    for month in miles_dict:
        x_list.append(month)
        y_list.append(miles_dict[month])

    x2_list = []
    y2_list = []
    for month in pace_dict:
        x2_list.append(month)
        y2_list.append(pace_dict[month])

    x3_list = []
    y3_list = []
    for month in hr_dict:
        x3_list.append(month)
        y3_list.append(hr_dict[month])

    x4_list = []
    y4_list = []
    for month in ele_dict:
        x4_list.append(month)
        y4_list.append(ele_dict[month])

    x5_list = []
    y5_list = []
    for month in tred_dict:
        x5_list.append(month)
        y5_list.append(tred_dict[month])

    x6_list = []
    y6_list = []
    for month in count_dict:
        x6_list.append(month)
        y6_list.append(count_dict[month])

    fig, (ax1,ax2,ax4,ax5) = plt.subplots(nrows=4, figsize=mass_figsize) #figsize sets window


    myFmt = mdates.DateFormatter('%m/%d')

    ax1df = trend_line(x_list, y_list)
    ax1.bar(x_list, y_list, align='center', width=6)
    ax1slope = format_number(float(ax1df['y_trend'].iloc[0]) - float(ax1df['y_trend'].iloc[-1]))
    ax1.plot_date(ax1df.dates, ax1df.y_trend, 'red', ls='--', marker='None',label=ax1slope)
    ax1.set_ylabel('Miles Ran', color='b')
    ax1.set_yticks(range(int(max(y_list))+1),3)
    ax1.tick_params('y', colors='b')
    ax1.yaxis.grid(True)
    ax1.legend()
    ax1.set_xticks(x_list)
    ax1.xaxis.set_major_formatter(myFmt)

    ax2.plot(x2_list,y2_list, color='g', label='Pace', linewidth=2)
    ax2.set_ylabel('Pace (Decimal)', color='g')
    ax2.tick_params('y', colors='g')
    ax2.yaxis.grid(True)
    ax3 = ax2.twinx()
    ax3.plot(x3_list,y3_list, color='r', label='Avg HR')
    ax3.set_ylabel('Avg of Avg HR', color='r')
    ax3.tick_params('y', colors='r')
    ax2.set_xticks(x2_list)
    ax2.xaxis.set_major_formatter(myFmt)

    ax4.bar(x6_list,y6_list, align='center', width=6, color='b', label='Outdoor') #total runs
    ax4.bar(x5_list,y5_list, align='center', width=6, color='#fc5e02', label='Treadmill') #treadmill runs
    ax4.set_ylabel('Runs Per Week', color='b')
    ax4.set_yticks(range(max(y6_list)+1))
    ax4.tick_params('y', colors='b')
    ax4.yaxis.grid(True)
    ax4.legend()
    ax4.set_xticks(x5_list)
    ax4.xaxis.set_major_formatter(myFmt)

    ax5.plot(x4_list,y4_list, label='Total')
    ax5.set_ylabel('Total Elevation (Feet)')
    #ax5.set_yticks(range(int(max(y4_list)+1)),20)
    ax5.yaxis.grid(True)
    ax5.legend()
    ax5.set_xticks(x4_list)
    ax5.xaxis.set_major_formatter(myFmt)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3)
    #plt.show()

    append_image("Weekly_Compare",plt)

    ####

def monthly_compare():

    weeks_to_calculate = list(range(0,14))

    week_dict = {}

    for week in weeks_to_calculate:
        week_dict[week] = master_dict.copy() #make a master dict for each week to calculate

    for week in week_dict:

        for key in list(week_dict[week]): #for each key in each master dictionary
            if key < get_time.FOM(week):
                del week_dict[week][key]
        for key in list(week_dict[week]):
           if key > get_time.LOM(week):
               del week_dict[week][key]

    #Mileage
    miles_dict = {}
    pace_dict = {}
    hr_dict = {}
    ele_dict = {}
    tred_dict = {}
    count_dict = {}

    for week in week_dict:
        if week_dict[week]: #check to see if any activites exist in the given week
            mile_list = []
            pace_list = []
            hr_list = []
            ele_list = []
            tred_list = []
            count_list = []
            for activity in week_dict[week]:
                count_list.append(1)
                mile_list.append(float(week_dict[week][activity]['distance_miles']))
                pace_list.append(float(week_dict[week][activity]['pace_dec']))
                hr_list.append(float(week_dict[week][activity]['average_heartrate']))
                #print(week_dict[week][activity]['average_heartrate'])
                if 'total_elevation_feet' in week_dict[week][activity]:
                    ele_list.append(float(week_dict[week][activity]['total_elevation_feet']))
                    ele_dict[get_time.FOM(week)] = sum(ele_list)#/len(ele_list)
                else:
                    ele_dict[get_time.FOM(week)] = 0
                if 'treadmill_flagged' in week_dict[week][activity]:
                    if week_dict[week][activity]['treadmill_flagged'] == 'yes':
                        tred_list.append(1)
                else:
                    tred_list.append(0)
            hr_dict[get_time.FOM(week)] = sum(hr_list)/len(hr_list)
            miles_dict[get_time.FOM(week)] = sum(mile_list)
            pace_dict[get_time.FOM(week)] = sum(pace_list)/len(pace_list)
            tred_dict[get_time.FOM(week)] = sum(tred_list)
            count_dict[get_time.FOM(week)] = sum(count_list)
        else:
            miles_dict[get_time.FOM(week)] = 0
            pace_dict[get_time.FOM(week)] = 0
            hr_dict[get_time.FOM(week)] = 0
            count_dict[get_time.FOM(week)] = 0

    x_list = []
    y_list = []
    for month in miles_dict:
        x_list.append(month)
        y_list.append(miles_dict[month])

    x2_list = []
    y2_list = []
    for month in pace_dict:
        x2_list.append(month)
        y2_list.append(pace_dict[month])

    x3_list = []
    y3_list = []
    for month in hr_dict:
        x3_list.append(month)
        y3_list.append(hr_dict[month])

    x4_list = []
    y4_list = []
    for month in ele_dict:
        x4_list.append(month)
        y4_list.append(ele_dict[month])

    x5_list = []
    y5_list = []
    for month in tred_dict:
        x5_list.append(month)
        y5_list.append(tred_dict[month])

    x6_list = []
    y6_list = []
    for month in count_dict:
        x6_list.append(month)
        y6_list.append(count_dict[month])

    ########
    fig, (ax1,ax2,ax4,ax5) = plt.subplots(nrows=4, figsize=mass_figsize) #figsize sets window

    myFmt = mdates.DateFormatter('%m/%y')

    ax1df = trend_line(x_list, y_list)
    ax1.bar(x_list, y_list, align='center', width=25)
    ax1slope = format_number(float(ax1df['y_trend'].iloc[0]) - float(ax1df['y_trend'].iloc[-1]))
    ax1.plot_date(ax1df.dates, ax1df.y_trend, 'red', ls='--', marker='None',label=ax1slope)
    ax1.set_ylabel('Miles Ran', color='b')
    ax1.set_yticks(range(int(max(y_list))+1),3)
    ax1.tick_params('y', colors='b')
    ax1.yaxis.grid(True)
    ax1.legend()
    ax1.set_xticks(x_list)
    ax1.xaxis.set_major_formatter(myFmt)

    ax2.plot(x2_list,y2_list, color='g', label='Pace', linewidth=2)
    ax2.set_ylabel('Pace (Decimal)', color='g')
    ax2.tick_params('y', colors='g')
    ax2.yaxis.grid(True)
    ax3 = ax2.twinx()
    ax3.plot(x3_list,y3_list, color='r', label='Avg HR')
    ax3.set_ylabel('Avg of Avg HR', color='r')
    ax3.tick_params('y', colors='r')
    ax2.set_xticks(x2_list)
    ax2.xaxis.set_major_formatter(myFmt)

    ax4.bar(x6_list,y6_list, align='center', width=25, color='b', label='Outdoor') #total runs
    ax4.bar(x5_list,y5_list, align='center', width=25, color='#fc5e02', label='Treadmill') #treadmill runs
    ax4.set_ylabel('Runs Per Week', color='b')
    ax4.set_yticks(range(max(y6_list)+1))
    ax4.tick_params('y', colors='b')
    ax4.yaxis.grid(True)
    ax4.legend()
    ax4.set_xticks(x5_list)
    ax4.xaxis.set_major_formatter(myFmt)

    ax5.plot(x4_list,y4_list, label='Total')
    ax5.set_ylabel('Total Elevation (Feet)')
    #ax5.set_yticks(range(int(max(y4_list)+1)),20)
    ax5.yaxis.grid(True)
    ax5.legend()
    ax5.set_xticks(x4_list)
    ax5.xaxis.set_major_formatter(myFmt)

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3)

    append_image("Monthly_Compare",plt)

def yearly_compare():
    year_linewidth = 3
    linewidth = year_linewidth
    single_dict = {}

    for event in master_dict:
        if master_dict[event]['athlete_count'] == 1:
            if master_dict[event]['treadmill_flagged'] == 'no':
                single_dict[event] = master_dict[event]

    single_yearly_dict = calc.yearly_totals(single_dict.copy(),0) #this year
    single_yearly_dict_2 = calc.yearly_totals(single_dict.copy(),1) #last year

    yearly_dict = calc.yearly_totals(master_dict.copy(),0) #current year
    yearly_dict2 = calc.yearly_totals(master_dict.copy(),1) #last year

    fig, (ax1,ax2) = plt.subplots(nrows=2, figsize=mass_figsize)

    ax1.plot(list(yearly_dict.keys()),list(yearly_dict.values()),label=('This Year'),color='green', linewidth = year_linewidth)
    ax1.plot(list(yearly_dict2.keys()),list(yearly_dict2.values()),label=('Last Year'), linewidth = year_linewidth)

    def graph(formula, x_range,title,plot_number,color):
        x = np.array(x_range)
        y = eval(formula)
        plot_number.plot(x, y, color, label=title, linestyle=':', linewidth = year_linewidth)

    def format_number(number):
        return str("{0:.2f}".format(number))

    graph('x*(600/365)', range(0,366),"600 Miles",ax1,'r')
    graph('x*(365/365)', range(0,366),"365 Miles",ax1,'b')
    ax1.set_title('Yearly Totals')
    ax1.legend()

    #ax2 setup
    x_list = []
    y_list = []
    x2_list = []
    y2_list = []

    todays_number = datetime.datetime.now().timetuple().tm_yday #finds number of year
    month_ago_number = todays_number - 30 #number to filter entires out from since not datetime objects

    for event in yearly_dict:
        x_list.append(event)
        y_list.append(yearly_dict[event])
        if event > month_ago_number:
            x2_list.append(event)
            y2_list.append(yearly_dict[event])

    def extended_prediction(x_list,y_list,end_day):
        extended_range = list(range(x_list[0],end_day))
        model = np.polyfit(x_list, y_list, 1)
        predicted = np.polyval(model, extended_range)
        return extended_range, predicted

    extended_range, predicted = extended_prediction(x_list, y_list, 365)
    extended_range_30, predicted_30 = extended_prediction(x2_list, y2_list, 365)

    label1 = "30 Days: "+format_number(predicted_30[-1])
    label2 = "2018: "+format_number(predicted[-1])

    graph('x*(600/365)', range(0,366),"600 Miles",ax2,'r')
    ax2.plot(extended_range, predicted, label=label2, linestyle='--', linewidth = year_linewidth)
    ax2.plot(extended_range_30, predicted_30, label=label1, linestyle='--', linewidth = year_linewidth)
    ax2.plot(list(yearly_dict.keys()),list(yearly_dict.values()),label=('This Year'),color='green', linewidth = year_linewidth)
    ax2.legend()

    fig.tight_layout()
    fig.subplots_adjust(hspace=0.3)
    #plt.show()
    append_image("Yearly_Compare",plt)

def running_totals():
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

    fig, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(nrows=6, figsize=mass_figsize) #figsize sets window

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
    append_image("Running_Totals",plt)

####
weekly_compare()
monthly_compare()
yearly_compare()
running_totals()



send_mail()
