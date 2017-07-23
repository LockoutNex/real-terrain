# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import requests
import sys
import subprocess

GDAL_INFO_BIN = 'bin/gdalinfo.exe'
GDAL_TRANSLATE_BIN = 'bin/gdal_translate.exe'

input_file = 'input/arcgrid_test'
output_file = 'output/arcgrid_test.tif'
# input_file = 'input/img_test.img'
# output_file = 'output/img_test.tif'

def translate_to_geotiff():
    gdal_translate_geotiff = [GDAL_TRANSLATE_BIN, '-co', 'COMPRESS=LZW', '-co', 
                              'PREDICTOR=3', '-co', 'TFW=YES', '-of', 'GTiff', 
                              input_file, output_file]
    subprocess.call(gdal_translate_geotiff)

# gdal_info_ = [GDAL_INFO_BIN, '-stats', 'input/img_test.img']
# subprocess.call(gdal_info_cmd)

translate_to_geotiff()