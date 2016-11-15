#!/bin/bash

# Libraries
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/libpng-1.5.11/lib/

# Enter to script folder
cd /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/

# Run algorithm 
python Satellite_DynamicData_HSAF_SWI_H16_Raw_Stats.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_algorithm/satellite_dynamicdata_hsaf-swi-h16-raw-stats_algorithm_server_history.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_logs/satellite_dynamicdata_hsaf-swi-h16-raw-stats_logging_server_history.config


