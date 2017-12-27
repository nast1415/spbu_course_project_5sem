import numpy as np
import pandas as pd


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

#Create id array and new column 'id' in weather_info dataframe to know id of forecast when we drop duplicates
id_array = np.zeros(number_of_forecasts)
for i in range(number_of_forecasts):
	id_array[i] = i

weather_info['id'] = id_array

#Drop duplicates from weather_info dataframe to accelerate finding nearest station
unique_stations = weather_info.drop_duplicates(subset='weather_station_code')
amount_of_unique_stations = unique_stations['weather_station_code'].count()

print(number_of_flights)
print(amount_of_unique_stations)

#Sort values in the unique_stations and fix indexes
unique_stations = unique_stations.sort_values(['latitude', 'longitude'])
unique_stations.index = np.array(range(amount_of_unique_stations))

#Create arrays of geografic coordinates for planes and weather stations
waypoint_lat_array = np.array(waypoint_info['latitudedegrees'])
waypoint_long_array = np.array(waypoint_info['longitudedegrees'])

weather_lat_array = np.array(unique_stations['latitude'])
weather_long_array = np.array(unique_stations['longitude'])

#Create array for forecasts ids
ids_array = np.array(unique_stations['id'])

#To calculate the result faster we use c++ algorithm in 'find_nearest_station.cpp'

#And now we're going to prepare coordinate arrays for this algorithm. We will save values of plane's and station's coordinates to the 'flight_array' file
f = open('flight_array', 'w')

for i in range(amount_of_unique_stations):
	f.write(str(ids_array[i]) + " ")

for i in range(number_of_flights):
	f.write(str(waypoint_lat_array[i]) + " ")
	f.write(str(waypoint_long_array[i]) + " ")

for i in range(amount_of_unique_stations):
	f.write(str(weather_lat_array[i]) + " ")
	f.write(str(weather_long_array[i]) + " ")

f.close()
