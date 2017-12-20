#include <iostream>
#include <cstdio>
#include <stdlib.h>
#include <vector>
#include <cmath>

/**
 * This file contains algorythm for finding id of the weather station that is nearest to the plane at the moment
 **/

const int FLIGHT_SIZE = 246547;
const int STATIONS_SIZE = 4470;
const double earth_radius = 6372797.560856;
const double degrees_to_rad = 0.017453292519943295769236907684886;
const double INF = 1e7;

//Vector for stations ids from flight_array file
std::vector<double> ids_array(STATIONS_SIZE);

//Vectors for data from flight_array file
std::vector< std::pair<double, double> > flight_array(FLIGHT_SIZE);
std::vector< std::pair<double, double> > stations_array(STATIONS_SIZE);

//Vector for result values of the nearest stations ids
std::vector<int> nearest_stations(FLIGHT_SIZE);
//Supporting vector for distance values between plane and weather station
std::vector<double> nearest_distance(FLIGHT_SIZE);

//Supporting function to get distance frome two points with geographic coordinates
double getSquareDistance(double lat1, double long1, double lat2, double long2) {
	double d_theta = (lat1 - lat2) * degrees_to_rad;
	double d_lambda = (long1 - long2) * degrees_to_rad;
	double mean_t = (lat1 + lat2) * degrees_to_rad / 2.0;
	double cos_meant = cos(mean_t);

	return (earth_radius * sqrt(d_theta * d_theta + cos_meant * cos_meant * d_lambda * d_lambda));
}

int main() {
	//Open file with preparing coordinates
	freopen("find_nearest_station/flight_array", "r", stdin);
	//Open file for writing the result ids
	freopen("find_nearest_station/result_nearest", "w", stdout);

	//Read data
	for (int i = 0; i < STATIONS_SIZE; i++) {
		scanf("%lf", &ids_array[i]);
	}

	for (int i = 0; i < FLIGHT_SIZE; i++) {
		scanf("%lf%lf", &flight_array[i].first, &flight_array[i].second);
	}

	for (int i = 0; i < STATIONS_SIZE; i++) {
		scanf("%lf%lf", &stations_array[i].first, &stations_array[i].second);
	}
	
	//Find nearest stations
	for (int i = 0; i < FLIGHT_SIZE; i++) {
		nearest_distance[i] = INF;
		
		for (int j = 0; j < STATIONS_SIZE; j++) {

			double distance = getSquareDistance(flight_array[i].first, flight_array[i].second, stations_array[j].first, stations_array[j].second);

			if (nearest_distance[i] > distance) {
				nearest_distance[i] = distance;
				nearest_stations[i] = ids_array[j];
			}
		}
		//Write result to the output file
		printf("%d ", nearest_stations[i]);
	}

	//Close input and output files
	fclose(stdin);
	fclose(stdout);
}