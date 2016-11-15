#!/bin/bash

# Libraries
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/libpng-1.5.11/lib/
export PATH=/home/gabellani/Library_Collection/gdal-2.1.0/bin:${PATH}

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/gdal-2.1.0/lib/


# Enter to script folder
cd /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/

# Run algorithm --> soil moisture raw product
python Satellite_DynamicData_HSAF_SoilMoisture_H16_Raw.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_algorithm/satellite_dynamicdata_hsaf-sm-h16-raw_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_logs/satellite_dynamicdata_hsaf-sm-h16-raw_logging_server_realtime.config

# Run algorithm --> swi raw product
python Satellite_DynamicData_HSAF_SWI_H16_Raw.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_algorithm/satellite_dynamicdata_hsaf-swi-h16-raw_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_logs/satellite_dynamicdata_hsaf-swi-h16-raw_logging_server_realtime.config

# Run algorithm --> swi star product
python Satellite_DynamicData_HSAF_SWI_H16_Star.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_algorithm/satellite_dynamicdata_hsaf-swi-h16-star_algorithm_server_realtime.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_logs/satellite_dynamicdata_hsaf-swi-h16-star_logging_server_realtime.config

