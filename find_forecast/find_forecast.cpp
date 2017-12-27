#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>

/**
 * This file contains algorythm for finding id of the last suitable forecast from the nearest station.
 * Forecast is suitable if it was received before we get information about flight. 
 * Best forecast is a last suitable forecast.
 **/

const int FLIGHT_SIZE = 332338;
const int FORECASTS_SIZE = 79709;

//Vectors with date_time values for flight and forecast
std::vector<std::string> received_flight(FLIGHT_SIZE);
std::vector<std::string> received_forecast(FORECASTS_SIZE);

//Vectors with station codes values (we will compare name of the nearest station and station name from weather_info to get forecast from right station)
std::vector<std::string> station_codes_array(FORECASTS_SIZE);
std::vector<std::string> waypoint_nearest_array(FLIGHT_SIZE);

//Vectors with date_time parameters: day, hour and minute for forecasts
std::vector<int> forecast_day(FORECASTS_SIZE);
std::vector<int> forecast_hour(FORECASTS_SIZE);
std::vector<int> forecast_minute(FORECASTS_SIZE);

//Vectors with date_time parameters: day, hour and minute for flights
std::vector<int> flight_day(FLIGHT_SIZE);
std::vector<int> flight_hour(FLIGHT_SIZE);
std::vector<int> flight_minute(FLIGHT_SIZE);

//Vectors with forecasts parameters: wind direction, speed, gusts, visibility
std::vector<double> stat_wind_dir(FORECASTS_SIZE);
std::vector<double> stat_wind_speed(FORECASTS_SIZE);
std::vector<double> stat_wind_gust(FORECASTS_SIZE);
std::vector<double> stat_visib(FORECASTS_SIZE);

//Vector for result
std::vector<int> forecast_for_flight(FLIGHT_SIZE);

//Vectors for the forecast parameters from the weather_info
std::vector<double> wind_dir(FLIGHT_SIZE);
std::vector<double> wind_speed(FLIGHT_SIZE);
std::vector<double> wind_gust(FLIGHT_SIZE);
std::vector<double> visib(FLIGHT_SIZE);

//Functions to get date and time parameters from date_time string in dataframes
std::string get_day_for_flight(std::string date_time_str){
	std::string result = "";
	result += date_time_str[0];
	result += date_time_str[1];
	return result;
}

std::string get_day_for_forecast(std::string date_time_str){
	std::string result = "";
	result += date_time_str[8];
	result += date_time_str[9];
	return result;
}

std::string get_hour_from_str(std::string date_time_str){
	std::string delimeter = "";
	delimeter += date_time_str[11];
	if (delimeter == ":"){
		std::string result = "";
		result += date_time_str[10];
		return result;
	}
	std::string result = "";
	result += date_time_str[10];
	result += date_time_str[11];
	return result;
}

std::string get_minute_from_str(std::string date_time_str){
	std::string delimeter = "";
	delimeter += date_time_str[11];
	if (delimeter == ":"){
		std::string result = "";
		result += date_time_str[12];
		result += date_time_str[13];
		return result;
	}
	std::string result = "";
	result += date_time_str[13];
	result += date_time_str[14];
	return result;
}

int main() {
	//We use ifstream to read string values correctly and simply
	std::ifstream file("received_info");

    if (file.is_open()){
		for (int i = 0; i < FLIGHT_SIZE; i++){
            std::string tmp;
            file >> tmp;

            flight_day[i] = atoi(get_day_for_flight(tmp).c_str());
			flight_hour[i] = atoi(get_hour_from_str(tmp).c_str());
			flight_minute[i] = atoi(get_minute_from_str(tmp).c_str()); 
        }

        for (int i = 0; i < FORECASTS_SIZE; i++){
            std::string tmp;
            file >> tmp;
            
            forecast_day[i] = atoi(get_day_for_forecast(tmp).c_str());
			forecast_hour[i] = atoi(get_hour_from_str(tmp).c_str());
			forecast_minute[i] = atoi(get_minute_from_str(tmp).c_str());
        }

        for (int i = 0; i < FORECASTS_SIZE; i++){
            file >> station_codes_array[i];
        }

        for (int i = 0; i < FLIGHT_SIZE; i++){
            file >> waypoint_nearest_array[i];
        }

        for (int i = 0; i < FORECASTS_SIZE; i++){
        	file >> stat_wind_dir[i];
        	file >> stat_wind_speed[i];
        	file >> stat_wind_gust[i];
        	file >> stat_visib[i];
        }
    }

    file.close();

	//Open file to write result
    freopen("forecast", "w", stdout);
    
    for (int i = 0; i < FLIGHT_SIZE; i++){
		int nearest_forecast = -1;

		for (int j = 0; j < FORECASTS_SIZE; j++){
			if (station_codes_array[j] == waypoint_nearest_array[i]){
				//Move to the next j while we get suitable forecasts and remember last j as nearest_forecast variable
				if ((flight_day[i] > forecast_day[j]) || 
					((flight_day[i] == forecast_day[j]) && (flight_hour[i] > forecast_hour[j])) || 
					((flight_day[i] == forecast_day[j]) && (flight_hour[i] == forecast_hour[j]) && (flight_minute[i] >= forecast_minute[j]))){
					nearest_forecast = j;
					continue;
				}
				//At this point we get first unsuitable forecast, so we can say that last forecast (nearest_forecast) was optimal
				forecast_for_flight[i] = nearest_forecast;
				wind_dir[i] = stat_wind_dir[nearest_forecast];
				wind_speed[i] = stat_wind_speed[nearest_forecast];
				wind_gust[i] = stat_wind_gust[nearest_forecast];
				visib[i] = stat_visib[nearest_forecast];
				break;
			} else {
				//We can have a situation when all forecasts from our nearest station are suitable, so we should use last forecast from our station as optimal
				if (nearest_forecast != -1) {
					forecast_for_flight[i] = nearest_forecast;
					wind_dir[i] = stat_wind_dir[nearest_forecast];
					wind_speed[i] = stat_wind_speed[nearest_forecast];
					wind_gust[i] = stat_wind_gust[nearest_forecast];
					visib[i] = stat_visib[nearest_forecast];
				}
			}
		}
	}

	for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%d ", forecast_for_flight[i]);
	}
	fclose(stdout);

	//Open file to write wind_dir
    freopen("wind_dir", "w", stdout);
    for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%lf ", wind_dir[i]);
	}
	fclose(stdout);

	//Open file to write wind_speed
    freopen("wind_speed", "w", stdout);
    for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%lf ", wind_speed[i]);
	}
	fclose(stdout);

	//Open file to write wind_gusts
    freopen("wind_gust", "w", stdout);
    for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%lf ", wind_gust[i]);
	}
	fclose(stdout);

	//Open file to write visibility
    freopen("visib", "w", stdout);
    for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%lf ", visib[i]);
	}
	fclose(stdout);
}