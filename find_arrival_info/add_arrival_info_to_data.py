import numpy as np
import pandas as pd


'''
This file contains code for addinf arrival info to the data
'''

#Support function. We're going to sort values in arriving_info and waypoint_info dataframes in order of received time.
#Some time notes are in format 'dd.mm.yyyy h.mm' and this function convert them to the format 'dd.mm.yyyy hh.mm' (with leading null in hours) to sort correctly
def prepare_flighttime(datetime_array, amount_of_notes):
	for i in range(amount_of_notes):
		if datetime_array[i][12] == ":":
			datetime_array[i] = datetime_array[i][:11] + '0' + datetime_array[i][11:]
	return datetime_array

'''
Read main information about flight to the dataframe 'waypoint_info'
This dataframe includes columns:
	-received
	-callsign
	-altitude
	-groundspeed
	-latitudedegrees
	-longitudedegrees
	-flighthistoryid
	-action
'''
waypoint_info = pd.read_csv("../pressure/training_with_pressure.csv")
number_of_flights = waypoint_info['received'].count()


#Correct format of received values in waypoint_info
received_array = np.array(waypoint_info['received'])
received_array = prepare_flighttime(received_array, number_of_flights)
waypoint_info['received'] = received_array

#Sort values in the waypoint_info and fix indexes
waypoint_info = waypoint_info.sort_values(['flighthistoryid', 'received'])
waypoint_info.index = np.array(range(number_of_flights))

#Read information about forecasts to the array
with open('remaining_time') as inp:
    remaining_time_array = inp.read().split()
with open('remaining_distance') as inp2:
    remaining_distance_array = inp2.read().split()
    print(len(remaining_distance_array))
with open('speed_indicator') as inp3:
    is_avg_speed_bigger_array = inp3.read().split()    

waypoint_info['remaining_time'] = remaining_time_array
waypoint_info['remaining_distance'] = remaining_distance_array
waypoint_info['is_avg_speed_bigger'] = is_avg_speed_bigger_array

waypoint_info.to_csv("full_waypoint_info.csv")
