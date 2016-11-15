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


cd /home/gabellani/HSAF_Data_Processing/Product_Precipitation/H05/

# Italy
python HSAF_Project_Precipitation_ProductH05_Ver2.py settings_precipitation_product_h05_italy.txt &

# Serbia
#python HSAF_Project_Precipitation_ProductH05_Ver2.py settings_precipitation_product_h05_serbia.txt &

# Lebanon
python HSAF_Project_Precipitation_ProductH05_Ver2.py settings_precipitation_product_h05_lebanon.txt
