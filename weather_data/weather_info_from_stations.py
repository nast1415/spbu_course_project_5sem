import numpy as np
import pandas as pd

'''
This part contains getting information about the weather from different sources and creating weather_info dataframe
'''

'''
Read weather info to the dataframe 'weather_info'
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
'''

weather_info = pd.read_csv("primary_data/train/weather_from_stations.csv")
number_of_forecasts = weather_info['weather_station_code'].count()

#Delete forecasts with nan value of the wind_speed, wind_direction, visibility
weather_info = weather_info.dropna(subset=['wind_speed', 'wind_direction', 'visibility'])
number_of_forecasts = weather_info['weather_station_code'].count()
weather_info.index = np.array(range(number_of_forecasts))


'''
First we need to fill empty values of the altimeter column with the average value and wind_gusts column with wind_speed values if wind_gust value is empty
Next we need to add to the weather_info values about station elevation
'''

#Fill altimeter column
weather_info['altimeter'] = weather_info['altimeter'].interpolate()

#Fill wind_gusts column
gusts_array = np.array(weather_info['wind_gusts'])
isnull_array = weather_info['wind_gusts'].isnull()

for i in range(number_of_forecasts):
	if isnull_array[i] == True:
		gusts_array[i] = weather_info['wind_speed'][i]

weather_info['wind_gusts'] = gusts_array

#Sort values in the weather_info dataframe (in order of station names) and fix indexes
weather_info = weather_info.sort_values('weather_station_code')
weather_info.index = np.array(range(number_of_forecasts))

#This dataframe contains name of the station and it's elevation
#We add to the weather_info dataframe column 'elevation' with data from stationinfo.csv about stations' elevation 
station_elevation = pd.read_csv("primary_data/stationelev.csv")
number_of_stations = station_elevation['station_name'].count()

#Sort values in the station_elevation (in order of station names) and fix indexes
station_elevation = station_elevation.sort_values('station_name')
station_elevation.index = np.array(range(number_of_stations))

#The we're going to add information about elevtion to the weather_info dataframe
#Create two numpy arrays for two columns of station_elevation dataframe
stations_name_array = np.array(station_elevation['station_name'])
stations_elev_array = np.array(station_elevation['elevation'])

#Create numpy array for column of weather_info dataframe
weather_station_array = np.array(weather_info['weather_station_code'])

#Create null array for future values of stations' elevation
elev_array = np.zeros(number_of_forecasts)

print "Start getting elevation"
#Get elevation from stationinfo.csv and fill elev_array 
for i in range(number_of_forecasts):
	for j in range(number_of_stations):
		if stations_name_array[j] == weather_station_array[i]:
			elev_array[i] = stations_elev_array[j]
			break

#Create new column 'elevation' in the weather_info dataframe and fill it with the values from elev_array
weather_info['elevation'] = elev_array

weather_info.to_csv("weather_data/full_stations_weather_info.csv")