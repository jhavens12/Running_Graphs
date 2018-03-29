import get_time
import get_data
import calc
from pprint import pprint
import datetime

print("These are runs with 1 person in the activity and not treadmill flagged")
print()

master_dict = get_data.my_filtered_activities() #grabs dictionary of strava information
single_dict = {}

for run in master_dict:
    print(str(run)+" - "+str(run + master_dict[run]['elapsed'])+" - "+master_dict[run]['name']+" - "+str(master_dict[run]['distance_miles']))

for event in master_dict:
    if master_dict[event]['athlete_count'] == 1:
        if master_dict[event]['treadmill_flagged'] == 'no':
            single_dict[event] = master_dict[event]

first_of_year = datetime.datetime(2018, 1, 1)

last_year = {}
this_year = {}
for event in single_dict:
    if event > first_of_year:
        if event != datetime.datetime(2018, 2, 4, 8, 13, 21): #this is the FL run which does not have danielle added
            this_year[event] = single_dict[event]
    else:
        last_year[event] = single_dict[event]

###
this_year_miles_list = []
for run in this_year:
    this_year_miles_list.append(float(this_year[run]['distance_miles']))
this_year_miles = sum(this_year_miles_list)

last_year_miles_list = []
for run in last_year:
    last_year_miles_list.append(float(last_year[run]['distance_miles']))
last_year_miles = sum(last_year_miles_list)

###

this_year_pace_list = []
for i in list(sorted(this_year)):
    this_year_pace_list.append(this_year[i]['pace_dec'])
this_year_pace = get_data.convert_dec_time(sum(this_year_pace_list)/len(this_year_pace_list))

last_year_pace_list = []
for i in list(sorted(last_year)):
    last_year_pace_list.append(last_year[i]['pace_dec'])
last_year_pace = get_data.convert_dec_time(sum(last_year_pace_list)/len(last_year_pace_list))







print("Runs: ")
print("This Year:")
print(len(this_year))
print("Last Year:")
print(len(last_year))
print()
print("Distance:")
print("This Year")
print(this_year_miles)
print("Last Year")
print(last_year_miles)
print()
print("Pace:")
print("This Year")
print(this_year_pace)
print("Last Year")
print(last_year_pace)



print()
