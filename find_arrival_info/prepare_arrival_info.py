import numpy as np
import pandas as pd


'''
This file contains code for preparing data to get arrival info: remaining distance, remaining time
'''

#Supporting function. All date_time values in our data have one of two formats: 'dd.mm.yyyy h(hh).mm' or 'yyyy-mm-dd hh.mm+hh.mm'
#This function cut date_time string after hh.mm and delete space between date and time to simplify work with this attribute in future
def prepare_datetime(datetime):
	datetime = datetime[:10] + datetime[11:16]
	datetime = datetime + " "
	return datetime

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


'''
Read information about arriving parameters to the dataframe 'arriving_info'
This dataframe includes columns:
	- updatetimeutc (time when this information was updated)
	- flighthistoryid (related to the flighthistoryid column from the waypoint_info)
	- departureairport (IATA or ICAO code of the departure airport)
	- arrivalairport (IATA or ICAO code of the arrival airport)
	- arrival_lat
	- arrival_long (geographic coordinates of arrival airport)
	- departure
	- arrival (estimated times of departure and arrival)
'''
arriving_info = pd.read_csv("../primary_data/arrival_info.csv")
number_of_notes = arriving_info['flighthistoryid'].count()


#Correct format of received values in waypoint_info
received_array = np.array(waypoint_info['received'])
received_array = prepare_flighttime(received_array, number_of_flights)
waypoint_info['received'] = received_array

#Sort values in the waypoint_info and fix indexes
waypoint_info = waypoint_info.sort_values(['flighthistoryid', 'received'])
waypoint_info.index = np.array(range(number_of_flights))

#Correct format of received values in arriving_info
updated_array = np.array(arriving_info['updatetimeutc'])
updated_array = prepare_flighttime(updated_array, number_of_notes)
arriving_info['updatetimeutc'] = updated_array

#Sort values in the arriving_info and fix indexes
arriving_info = arriving_info.sort_values(['flighthistoryid', 'updatetimeutc'])
arriving_info.index = np.array(range(number_of_notes))

#Array for estimated arrival time from flightplans
arrival_time_array = np.array(arriving_info['arrival'])

#Arrays for historyid for flight and flightplan
waypoint_historyid_array = np.array(waypoint_info['flighthistoryid'])
flightplan_historyid_array = np.array(arriving_info['flighthistoryid'])

#Arrays with date time parameters for flight (when we get information about flight) and for flightplan (when it was updated)
received_flight = np.array(waypoint_info['received'])
received_flightplan = np.array(arriving_info['updatetimeutc'])

#Array with geographic coordinates of plane and arrival airport
waypoint_lat_array = np.array(waypoint_info['latitudedegrees']).astype(float)
waypoint_long_array = np.array(waypoint_info['longitudedegrees']).astype(float)

arriving_lat_array = np.array(arriving_info['arrival_lat']).astype(float)
arriving_long_array = np.array(arriving_info['arrival_long']).astype(float)

#Array with speed value of plane
speed_array = np.array(waypoint_info['groundspeed']).astype(float)

#Open file to write prepared data to it
f = open('arrival_info', 'w')

for i in range(number_of_flights):
	f.write(str(waypoint_historyid_array[i]) + " ")

for i in range(number_of_notes):
	f.write(str(flightplan_historyid_array[i]) + " ")

for i in range(number_of_notes):
	f.write(prepare_datetime(arrival_time_array[i]))

for i in range(number_of_flights):
	f.write(prepare_datetime(received_flight[i]))

for i in range(number_of_notes):
	f.write(prepare_datetime(received_flightplan[i]))

f.close()
f2 = open('arrival_info2', 'w')

for i in range(number_of_flights):
	f2.write(str(waypoint_lat_array[i]) + " ")
	f2.write(str(waypoint_long_array[i]) + " ")

for i in range(number_of_notes):
	f2.write(str(arriving_lat_array[i]) + " ")
	f2.write(str(arriving_long_array[i]) + " ")

for i in range(number_of_flights):
	f2.write(str(speed_array[i]) + " ")
f2.close()