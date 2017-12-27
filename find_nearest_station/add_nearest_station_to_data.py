import numpy as np
import pandas as pd
import math as m


'''
This file contains code for preparing data to find nearest station for each plane at each moment
'''

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
waypoint_info = pd.read_csv("../primary_data/delta3_training_matrix.csv")
number_of_flights = waypoint_info['received'].count()

'''
Read information about forecast from weather stations (that we have prepared in the 'weather_info_from_stations.py' module) to the dataframe 'weather_info'
This dataframe includes columns:
	- metar_reports_id
	- weather_station_code
	- latitude (of the station)
	- longtitude (of the station)
	- date_time_issued
	- wind_direction
	- wind_speed
	- wind_gusts
	- visibility
	- altimeter
	- elevation
'''
weather_info = pd.read_csv("../weather_data/full_stations_weather_info.csv")
number_of_forecasts = weather_info['weather_station_code'].count()

#Sort values in the waypoint_info and fix indexes
waypoint_info = waypoint_info.sort_values(['latitudedegrees', 'longitudedegrees'])
waypoint_info.index = np.array(range(number_of_flights))

#Read information about nearest stations to the array
with open('result_nearest') as inp:
    nearest_station_array = inp.read().split()

#Create array for the codes of the nearest stations
nearest_station_name_array = np.chararray(number_of_flights, itemsize=5)

#Create array of stations code names
station_names = np.array(weather_info['weather_station_code'])

#Fill nearest_station_name_array with stations codes
for i in range(number_of_flights):
    id = int(nearest_station_array[i])
    nearest_station_name_array[i] = station_names[id]

#Add two new column with codes of nearest stations to the dataframe
waypoint_info['nearest_station_name'] = nearest_station_name_array
waypoint_info['nearest_station_id'] = nearest_station_array

#Save results to the csv file
waypoint_info.to_csv("training_with_nearest.csv")
