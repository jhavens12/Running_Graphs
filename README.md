# Running_Graphs
Python scripts used to map previous runs using Strava API

# Month_Compare_Total.py
Script that combines all of my previous scripts for mapping out month by month
Can show totals for month compared on a graph

Or shows the "running totals" (inspired by Smashrun) for the past x days

It should be noted that the running totals will include previous days at start of month

Meaning - If you just look for Jan 2017 - the first days will carry over data from Dec 2016 in the totals

This value can be adjusted - currently set to 7 days as on Smashrun


# Requires:
pandas
sklearn
ktinker
yagmail
matplotlib
scipy

import matplotlib
matplotlib.use('Agg')

Make dir named "temp"

Needs python 3.6 to work correctly

curl https://bootstrap.pypa.io/get-pip.py | sudo python3.6
