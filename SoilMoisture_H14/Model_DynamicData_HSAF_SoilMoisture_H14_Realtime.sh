#!/bin/bash

# Libraries
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/libpng-1.5.11/lib/


# Enter to script folder
cd /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/

# Run algorithm --> raw product
python Model_DynamicData_HSAF_SoilMoisture_H14_Raw.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_algorithm/model_dynamicdata_hsaf-sm-h14-raw_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_logs/model_dynamicdata_hsaf-sm-h14-raw_logging_server_realtime.config

# Run algorithm --> soil moisture star product
python Model_DynamicData_HSAF_SoilMoisture_H14_Star.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_algorithm/model_dynamicdata_hsaf-sm-h14-star_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H14/config_logs/model_dynamicdata_hsaf-sm-h14-star_logging_server_realtime.config

