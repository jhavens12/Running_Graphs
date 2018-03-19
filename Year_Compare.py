#compares this current year to last years efforts

import get_time
import get_data
import calc
import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates
from pprint import pprint
import numpy as np

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information

yearly_dict = calc.yearly_totals(master_dict.copy(),0) #current year

yearly_dict2 = calc.yearly_totals(master_dict.copy(),1) #last year

plt.plot(list(yearly_dict.keys()),list(yearly_dict.values()),label=('This Year'))
plt.plot(list(yearly_dict2.keys()),list(yearly_dict2.values()),label=('Last Year'))

def graph(formula, x_range,title):
    x = np.array(x_range)
    y = eval(formula)
    plt.plot(x, y, label=(title))
    # for s,l in zip(x,y):
    #     print(s,l)

graph('x*(600/365)', range(0,366),"600 Miles")
graph('x*(365/365)', range(0,366),"365 Miles")


plt.style.use('dark_background')
plt.rcParams['lines.linewidth'] = 1
plt.ylim(ymin=0)
plt.title('Yearly Totals')
plt.legend()
plt.show()
