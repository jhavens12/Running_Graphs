import matplotlib.pyplot as plt
import pylab
import matplotlib.dates as mdates

def dual_dictionary(dictionary1,dictionary2):
    empty = []
    x1_list = []
    y1_list = []

    x2_list = []
    y2_list = []

    for key in sorted(dictionary1.keys()):
        x1_list.append(key)
        y1_list.append(dictionary1[key])
    len_x1 = len(x1_list)
    x1 = range(len_x1)

    for key in sorted(dictionary2.keys()):
        x2_list.append(key)
        y2_list.append(dictionary2[key])
    len_x2 = len(x2_list)
    x2 = range(len_x2)

    if len_x1 > len_x2:
        x3 = range(len_x1)
    if len_x1 < len_x2:
        x3 = range(len_x2)

    plt.style.use('dark_background')
    plt.axis('off')
    plt.rcParams['lines.linewidth'] = 6
    plt.plot(x1,y1_list, color='red')
    plt.plot(x2,y2_list, color='blue')
    plt.ylim(ymin=0)

    plt.show()

def single_dictionary(dictionary1):
    plt.clf()
    empty = []
    x_list = []
    y_list = []
    for key in sorted(dictionary1.keys()):
        x_list.append(key)
        y_list.append(dictionary1[key])

    n_1 = len(x_list)
    x = range(n_1)

    plt.style.use('dark_background')
    plt.axis('off')
    plt.rcParams['lines.linewidth'] = 6
    plt.plot(x,y_list, color='red')
    plt.ylim(ymin=0)

    plt.show()
