#!/bin/bash

# Libraries
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/libpng-1.5.11/lib/

# Enter to script folder
cd /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/

# Run algorithm 
python Model_DynamicData_HSAF_SoilMoisture_H14_Raw_Stats.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_algorithm/model_dynamicdata_hsaf-sm-h14-raw-stats_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_logs/model_dynamicdata_hsaf-sm-h14-raw-stats_logging_server_realtime.config


