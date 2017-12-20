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
waypoint_info = pd.read_csv("find_nearest_station/training_with_nearest.csv")
number_of_flights = waypoint_info['received'].count()

#Support function. We're going to sort values in waypoint_info dataframe in order of received time.
#Some time notes are in format 'dd.mm.yyyy h.mm' and this function convert them to the format 'dd.mm.yyyy hh.mm' (with leading null in hours) to sort correctly
def prepare_flighttime(datetime_array):
	for i in range(number_of_flights):
		if datetime_array[i][12] == ":":
			datetime_array[i] = datetime_array[i][:11] + '0' + datetime_array[i][11:]
	return datetime_array

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
weather_info = pd.read_csv("weather_data/full_stations_weather_info.csv")
number_of_forecasts = weather_info['weather_station_code'].count()

#Correct format of received values in waypoint_info
received_array = np.array(waypoint_info['received'])
received_array = prepare_flighttime(received_array)
waypoint_info['received'] = received_array

#Sort values in the waypoint_info and fix indexes
waypoint_info = waypoint_info.sort_values(['nearest_station_name', 'received'])
waypoint_info.index = np.array(range(number_of_flights))

#Sort values in the weather_info and fix indexes
weather_info = weather_info.sort_values(['weather_station_code', 'date_time_issued'])
weather_info.index = np.array(range(number_of_forecasts))

#Create arrays for time values when the information about plane and forecast were received
received_flight = np.array(waypoint_info['received'])
received_forecast = np.array(weather_info['date_time_issued'])

#Create arrays with station names (we will compare name of the nearest station and station name from weather_info to get forecast from right station)
waypoint_nearest_array = np.array(waypoint_info['nearest_station_name'])
station_codes_array = np.array(weather_info['weather_station_code'])

#Create arrays with forecast params
stat_wind_dir = np.array(weather_info['wind_direction'])
stat_wind_speed = np.array(weather_info['wind_speed'])
stat_wind_gust = np.array(weather_info['wind_gusts'])
stat_visib = np.array(weather_info['visibility'])

#Write data to the received_info file
f = open('find_forecast/received_info', 'w')

for i in range(number_of_flights):
	f.write(prepare_datetime(received_flight[i]))

for i in range(number_of_forecasts):
	f.write(prepare_datetime(received_forecast[i]))

for i in range(number_of_forecasts):
	f.write(station_codes_array[i] + " ")

for i in range(number_of_flights):
	f.write(waypoint_nearest_array[i] + " ")

for i in range(number_of_forecasts):
	f.write(str(stat_wind_dir[i]) + " ")
	f.write(str(stat_wind_speed[i]) + " ")
	f.write(str(stat_wind_gust[i]) + " ")
	f.write(str(stat_visib[i]) + " ")

f.close()