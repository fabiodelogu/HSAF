#!/bin/bash

# Libraries
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/zlib-1.2.8/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/hdf5-1.8.17/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/hdf4-4.2.10/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/netcdf-4.1.2/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/geos-3.5.0/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/proj-4.9.2/lib/
#export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/fabio/Documents/Working_Area/Code_Development/Library/gdal-2.1.0/lib/

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/libpng-1.5.11/lib/


# BUFR tables
#export BUFR_TABLES=/home/fabio/Documents/Working_Area/Code_Development/Library/bufrdc_000405/bufrtables/

# Enter to script folder
cd /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/

# Run algorithm 
python Satellite_DynamicData_HSAF_SoilMoisture_H16_Raw.py -settingfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_algorithm/satellite_dynamicdata_hsaf-sm-h16-raw_algorithm_server_history.config -logfile /home/gabellani/HSAF_Data_Processing/Product_SoilMoisture/H16/config_logs/satellite_dynamicdata_hsaf-sm-h16-raw_logging_server_history.config


