#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>

/**
 * This file contains algorythm for finding remaining time, distance to the arrival airport (according to flightplan) 
 * and indicator of plane speed - is it bigger than averege remaining speed, or not
 **/

const int FLIGHT_SIZE = 332338;
const int NOTES_SIZE = 285913;
const double earth_radius = 6372797.560856;
const double degrees_to_rad = 0.017453292519943295769236907684886;
const double INF = 1e7;

//Vectors for historyid of the flight and flightplan (we will compare this values to find right flightplan for each flight)
std::vector<std::string> flight_history(FLIGHT_SIZE);
std::vector<std::string> flightplan_history(NOTES_SIZE);

//Vectors for parameters of date time, when flightplan was updated
std::vector<int> flightplan_day(NOTES_SIZE);
std::vector<int> flightplan_hour(NOTES_SIZE);
std::vector<int> flightplan_minute(NOTES_SIZE);

//Vectors for parameters of date time, when information about flight was received
std::vector<int> flight_day(FLIGHT_SIZE);
std::vector<int> flight_hour(FLIGHT_SIZE);
std::vector<int> flight_minute(FLIGHT_SIZE);

//Vectors for parameters of arriving date and time (according to flightplan)
std::vector<int> arrival_day(NOTES_SIZE);
std::vector<int> arrival_hour(NOTES_SIZE);
std::vector<int> arrival_minute(NOTES_SIZE);

//Vectors for geographic coordinates of plane and arrival airport (to find distance)
std::vector< std::pair<double, double> > flight_array(FLIGHT_SIZE);
std::vector< std::pair<double, double> > flightplan_array(NOTES_SIZE);

//Vector for speed value (to calculate indicator's value)
std::vector<double> speed_array(FLIGHT_SIZE);	

//Vectors for the results
std::vector<double> remaining_distance_array(FLIGHT_SIZE);
std::vector<int> remaining_time_array(FLIGHT_SIZE);
std::vector<int> is_avg_speed_bigger_array(FLIGHT_SIZE);

//Function to find distance between two points with geographic coordinates
double getSquareDistance(double lat1, double long1, double lat2, double long2) {
	double d_theta = (lat1 - lat2) * degrees_to_rad;
	double d_lambda = (long1 - long2) * degrees_to_rad;
	double mean_t = (lat1 + lat2) * degrees_to_rad / 2.0;
	double cos_meant = cos(mean_t);

	return (earth_radius * sqrt(d_theta * d_theta + cos_meant * cos_meant * d_lambda * d_lambda));
}

//Functions to get date and time parameters from date_time string in dataframes
std::string get_day_from_str(std::string date_time_str){
	std::string result = "";
	result += date_time_str[0];
	result += date_time_str[1];
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
	//Read prepared information from file 
	std::ifstream file("arrival_info");
    if(file.is_open()){
		for(int i = 0; i < FLIGHT_SIZE; i++){
            file >> flight_history[i];
        }
        
		
		for(int i = 0; i < NOTES_SIZE; i++){
            file >> flightplan_history[i];
        }

        for(int i = 0; i < NOTES_SIZE; i++){
            std::string tmp;
            file >> tmp;

            arrival_day[i] = atoi(get_day_from_str(tmp).c_str());
			arrival_hour[i] = atoi(get_hour_from_str(tmp).c_str());
			arrival_minute[i] = atoi(get_minute_from_str(tmp).c_str());
        }

        for(int i = 0; i < FLIGHT_SIZE; i++){
            std::string tmp;
            file >> tmp;

            flight_day[i] = atoi(get_day_from_str(tmp).c_str());
			flight_hour[i] = atoi(get_hour_from_str(tmp).c_str());
			flight_minute[i] = atoi(get_minute_from_str(tmp).c_str());
        }
        

        for(int i = 0; i < NOTES_SIZE; i++){
            std::string tmp;
            file >> tmp;

            flightplan_day[i] = atoi(get_day_from_str(tmp).c_str());
			flightplan_hour[i] = atoi(get_hour_from_str(tmp).c_str());
			flightplan_minute[i] = atoi(get_minute_from_str(tmp).c_str());
        }

    }
    file.close();

    //We use two files, because it is too much information
    freopen("arrival_info2", "r", stdin);

    for(int i = 0; i < FLIGHT_SIZE; i++){
        scanf("%lf%lf", &flight_array[i].first, &flight_array[i].second);
    }
    
    for(int i = 0; i < NOTES_SIZE; i++){
        scanf("%lf%lf", &flightplan_array[i].first, &flightplan_array[i].second);
    }

    for(int i = 0; i < FLIGHT_SIZE; i++){
        scanf("%lf", &speed_array[i]);
    }

    
    //Open file to write remaining_time results
    //freopen("find_arrival_info/remaining_time", "w", stdout);
	
	for (int i = 0; i < FLIGHT_SIZE; i++) {
		int nearest_historyid = -1;
		int time = -1;
		double distance = -1;

		for (int j = 0; j < NOTES_SIZE; j++) {

			if (flight_history[i] == flightplan_history[j]) {
				if ((flight_day[i] > flightplan_day[j]) || 
					((flight_day[i] == flightplan_day[j]) && (flight_hour[i] > flightplan_hour[j])) || 
					((flight_day[i] == flightplan_day[j]) && (flight_hour[i] == flightplan_hour[j]) && (flight_minute[i] >= flightplan_minute[j]))){
					nearest_historyid = j;
					continue;
				}

				if (nearest_historyid == -1) {
					nearest_historyid = j;
				}

				//It is a first flightplan date value that is bigger than current flight date
				double plane_lat = flight_array[i].first;
				double plane_long = flight_array[i].second;
				double airport_lat = flightplan_array[nearest_historyid].first;
				double airport_long = flightplan_array[nearest_historyid].second;

				time = (arrival_day[nearest_historyid] * 24 * 60 + arrival_hour[nearest_historyid] * 60 + arrival_minute[nearest_historyid]) - (flight_day[i] * 24 * 60 + 
					flight_hour[i] * 60 + flight_minute[i]); 
				
				distance = sqrt(getSquareDistance(plane_lat, plane_long, airport_lat, airport_long));

				//Average speed to overcome remaining distance having remaining_time
				double avg_speed = distance / (time / 60);
				double current_speed = speed_array[i];
				current_speed *= 1.609;
				
				//We want to know, if the average speed is bigger than our current speed or not. If it is bigger we need to increase speed and if it is smaller - we need to decrease it
				if (avg_speed > current_speed){
					is_avg_speed_bigger_array[i] = 1;
				} else {
					is_avg_speed_bigger_array[i] = -1;
				}

				remaining_time_array[i] = time;
				remaining_distance_array[i] = distance;
				 

				break;
			} else {
				//It can be a situation when all flightplans were updated before we get information about plane, so we need to get las as a right flightplan
				if (nearest_historyid != -1) {

				double plane_lat = flight_array[i].first;
				double plane_long = flight_array[i].second;
				double airport_lat = flightplan_array[nearest_historyid].first;
				double airport_long = flightplan_array[nearest_historyid].second;

				time = (arrival_day[nearest_historyid] * 24 * 60 + arrival_hour[nearest_historyid] * 60 + arrival_minute[nearest_historyid]) - (flight_day[i] * 24 * 60 + 
					flight_hour[i] * 60 + flight_minute[i]); 
				
				distance = sqrt(getSquareDistance(plane_lat, plane_long, airport_lat, airport_long));

				//Average speed to overcome remaining distance having remaining_time
				double avg_speed = distance / (time / 60);
				double current_speed = speed_array[i];
				current_speed *= 1.609;

				//We want to know, if the average speed is bigger than our current speed or not. If it is bigger we need to increase speed and if it is smaller - we need to decrease it
				if (avg_speed > current_speed){
					is_avg_speed_bigger_array[i] = 1;
				} else {
					is_avg_speed_bigger_array[i] = -1;
				}

				remaining_time_array[i] = time;
				remaining_distance_array[i] = distance;
				}
			}
		}
		//printf("%d ", remaining_time_array[i]);
	}
	//fclose(stdout);

	freopen("remaining_time", "w", stdout);

	for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%d ", remaining_time_array[i]);
	}
	fclose(stdout);

	freopen("remaining_distance", "w", stdout);

	for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%lf ", remaining_distance_array[i]);
	}
	fclose(stdout);

	freopen("speed_indicator", "w", stdout);
	for (int i = 0; i < FLIGHT_SIZE; i++) {
		printf("%d ", is_avg_speed_bigger_array[i]);
	}
	fclose(stdout);
}