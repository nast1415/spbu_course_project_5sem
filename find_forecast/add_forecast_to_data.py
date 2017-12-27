import numpy as np
import pandas as pd


'''
This file contains code for preparing data to find forecast id from nearest station for each plane at each moment
'''

#Supporting function. All date_time values in our data have one of two formats: 'dd.mm.yyyy h(hh).mm' or 'yyyy-mm-dd hh.mm+hh.mm'
#This function cut date_time string after hh.mm and delete space between date and time to simplify work with this attribute in future
def prepare_datetime(datetime):
	datetime = datetime[:10] + datetime[11:16]
	datetime = datetime + " "
	return datetime

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
waypoint_info = pd.read_csv("../find_nearest_station/training_with_nearest.csv")
number_of_flights = waypoint_info['received'].count()

#Support function. We're going to sort values in waypoint_info dataframe in order of received time.
#Some time notes are in format 'dd.mm.yyyy h.mm' and this function convert them to the format 'dd.mm.yyyy hh.mm' (with leading null in hours) to sort correctly
def prepare_flighttime(datetime_array):
	for i in range(number_of_flights):
		if datetime_array[i][12] == ":":
			datetime_array[i] = datetime_array[i][:11] + '0' + datetime_array[i][11:]
	return datetime_array

#Correct format of received values in waypoint_info
received_array = np.array(waypoint_info['received'])
received_array = prepare_flighttime(received_array)
waypoint_info['received'] = received_array

#Sort values in the waypoint_info and fix indexes
waypoint_info = waypoint_info.sort_values(['nearest_station_name', 'received'])
waypoint_info.index = np.array(range(number_of_flights))

#Read information about forecasts to the array
with open('forecast') as inp:
	forecast_for_flight = inp.read().split()

with open('wind_dir') as inp:
	wind_dir = inp.read().split()

with open('wind_speed') as inp:
	wind_speed = inp.read().split()

with open('wind_gust') as inp:
	wind_gust = inp.read().split()

with open('visib') as inp:
	visib = inp.read().split()

waypoint_info['forecast'] = forecast_for_flight
waypoint_info['wind_dir'] = wind_dir
waypoint_info['wind_speed'] = wind_speed
waypoint_info['wind_gusts'] = wind_gust
waypoint_info['visib'] = visib
waypoint_info.to_csv("training_with_forecast.csv")