## SPBU, 3-rd year. Semester bachelor's course work.
***

This repository contains preparing data for speed prediction and running random forest algorythm on this data. In this part the main task was to predict for each moment of flight, whether pilot will increase/decrease or leave the same plane's speed.

Original dataset:
https://www.kaggle.com/c/flight2-final/data

There are three types of attributes that can affect speed changing: location attributes (f.e. altitude, geographic coordinates, groundspeed, ...); weather attributes (especially wind direction, wind speed, visibility, ...) and attributes related to the flightplan (estimated arrival time, estimated distance, ...).

* Folder `weather_data` contains Python scrypt for preparing primary weather data
* Folder `find_nearest_station` contains algorithm for finding nearest station to the each plane in each moment of flight and scrypts for preparing data to this algorythm and for adding information about nearest stations to our object-attribute matrix
* Folder `find_forecast` contains algorithm for extracting actual forecast from the nearest station and scrypts for preparing data to this algorythm and for adding information about weather forecast to our object-attribute matrix and filling gapes
* Folder `pressure` contains Python scrypt for calculating real pressure values for the planes
* Folder `find_arrival_info` contains algorithm for calculating estimated time and distance for each plane according to it's actual flight plan and and scrypts for preparing data to this algorythm and for adding information about arrival_info attributes to our object-attribute matrix

Scripts in main folder:
* `prepare_data.py` script prepare waypoint info matrix for future algorithms
* `prepare_for_rf.py` script prepares data for Random Forest algorithm
* `random_forest.py` script runs Random Forest algorithm on prepared data and return the result

***

### How to work with this repository

* First you need to clone repository
* Then you can run `prepare_data.sh` script to get training or test matrix with all necessary attributes and get result (it takes approx. 45 minutes)
