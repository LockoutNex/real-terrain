# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import re
import requests
import sys
import subprocess

GDAL_INFO_BIN = 'bin/gdalinfo.exe'
GDAL_TRANSLATE_BIN = 'bin/gdal_translate.exe'

input_file = 'input/arcgrid_test'
output_tif = 'output/arcgrid_test.tif'
output_png = 'output/arcgrid_test.png'
# input_file = 'input/img_test.img'
# output_file = 'output/img_test.tif'

class HeightMap(object):
    def __init__(self):
        self.min_value = '432.098'
        self.max_value = '713.806'

    def raster_to_geotiff(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-co', 'COMPRESS=LZW', '-co', 
                                'PREDICTOR=3', '-co', 'TFW=YES', '-of', 'GTiff', 
                                input_file, output_tif]
        subprocess.call(gdal_translate_cmd)

    def gdal_info(self):
        gdal_info_cmd = [GDAL_INFO_BIN, '-stats', output_tif]
        try:
            raster_info = subprocess.check_output(gdal_info_cmd)
        except subprocess.CalledProcessError as e:
            print("Failed to retrieve raster information:\n", e.output)
        return raster_info

    def geotiff_to_png(self, res='2048'):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-outsize', res, res, 
                                '-of', 'PNG', '-ot', 'UInt16', '-scale', 
                                self.min_value, self.max_value, '0', '65535', 
                                input_file, output_png]
        subprocess.call(gdal_translate_cmd)


def find_limits(raster_info):
    re.compile()
    re.findall()

h = HeightMap()

h.raster_to_geotiff()
raster_info = h.gdal_info()
h.geotiff_to_png()