#!/bin/bash

export PATH=/home/gabellani/Library_Collection/gdal-2.1.0/bin:${PATH}
export PATH=/home/gabellani/Library_Collection/grib_api-1.15.0/bin:${PATH}
export PATH=/home/gabellani/Library_Collection/netcdf-4.1.2/bin:${PATH}
export PATH=/home/gabellani/Library_Collection/hdf5-1.8.17/bin:${PATH}
export PATH=/home/gabellani/Library_Collection/hdf4-4.2.10/bin:${PATH}

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/gdal-2.1.0/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/proj-4.9.2/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/netcdf-4.1.2/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/hdf4-4.2.10/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/hdf5-1.8.17/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/geos-3.5.0//lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/zlib-1.2.8/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/gabellani/Library_Collection/grib_api-1.15.0/lib/


cd /home/gabellani/HSAF_Data_Processing/Product_Snow/

# ITALY
python HSAF_Project_Snow_ProductH10_Ver3.py settings_snow_product_h10_italy.txt &

# SERBIA
#python HSAF_Project_Snow_ProductH10_Ver3.py settings_snow_product_h10_serbia.txt &

# LEBANON
python HSAF_Project_Snow_ProductH10_Ver3.py settings_snow_product_h10_lebanon.txt
