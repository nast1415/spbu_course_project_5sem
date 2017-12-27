import numpy as np
import pandas as pd


'''
This file contains code for preparing data to find nearest station for each plane at each moment
'''

#Constants for calculating pressure
e = 2.718 #Constant for e number
m = -0.029 #Constant for air density
R = 8.31 #Constant for gas constant
g = 9.81 #Constant for gravitational acceleration
T = 293.15 #Constant for temperature

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
waypoint_info = pd.read_csv("../find_forecast/training_with_forecast.csv")
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

#Array for the result
pressure = np.zeros(number_of_flights)

#Array with values of the nearest stations
nearest_array = np.array(waypoint_info['forecast']).astype(int)
plane_altitude_array = np.array(waypoint_info['altitude']).astype(float)
station_elevation_array = np.array(weather_info['elevation']).astype(float)
station_altimeter_array = np.array(weather_info['altimeter']).astype(float)

for i in range(number_of_flights):
	nearest_station_id = nearest_array[i]
	station_altimeter_in_mmHg = station_altimeter_array[nearest_station_id] / 0.039

	#Convert plane's altitude from feet to metres
	plane_altitude_in_metres = plane_altitude_array[i] * 30.48 / 100
	stat_elevation = station_elevation_array[nearest_station_id]
	h = plane_altitude_in_metres - stat_elevation
	plane_pressure = station_altimeter_in_mmHg * e**(m*g*h/(R*T))
	
	pressure[i] = plane_pressure

#Create special column for real pressure in the height of the plane
waypoint_info['pressure'] = pressure
waypoint_info.to_csv("training_with_pressure.csv")