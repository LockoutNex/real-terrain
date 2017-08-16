# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import datetime
import random
import re
import string
import sys
import subprocess

GDAL_INFO_BIN = 'bin/gdalinfo.exe'
GDAL_TRANSLATE_BIN = 'bin/gdal_translate.exe'
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

parser = argparse.ArgumentParser(description='Generate a 16-bit PNG ' \
                                             'heightmap from USGS data')
parser.add_argument('data', metavar='input_data', 
                    help='Name of the input data (IMG, ArcGrid or GeoTiff format)')
parser.add_argument('-r', metavar='output_resolution', type=str, default='4096',
                    help='Resolution of the final heightmap (default 4096x4096)')
args = parser.parse_args()
res = args.r
input_data = args.data

ts = datetime.datetime.now().strftime('%Y%m%dT%H%M%S_')

class HeightMap(object):
    def __init__(self, resolution):
        self.res = resolution
        self.raster_info = ''
        self.min_elevation = ''
        self.max_elevation = ''
        self.uid = ''.join(random.choice(string.ascii_lowercase) for i in range(4)) 
        self.input_data = INPUT_DIR + input_data
        self.output_png = OUTPUT_DIR + ts + self.uid + '_heightmap.png'

    def generate(self):
        self.gdal_info()
        self.find_elevation_range()
        self.raster_to_png()

    def gdal_info(self):
        gdal_info_cmd = [GDAL_INFO_BIN, '-stats', self.input_data]
        try:
            print('\n>>> Extracting elevation information from input data')
            self.raster_info = str(subprocess.check_output(gdal_info_cmd))
        except subprocess.CalledProcessError as e:
            print("Failed to retrieve raster information:\n", e.output)
            sys.exit(1)
        
    def find_elevation_range(self):
        self.min_elevation = re.findall(r'(?<=STATISTICS_MINIMUM=)\-?\d{1,}', 
                                        self.raster_info)[0]
        self.max_elevation = re.findall(r'(?<=STATISTICS_MAXIMUM=)\-?\d{1,}', 
                                        self.raster_info)[0]
        print('Minimum elevation: {}m'.format(self.min_elevation))
        print('Maximum elevation: {}m'.format(self.max_elevation))
        print('Elevation range: {}m'.format(int(self.max_elevation) - 
                                           int(self.min_elevation)))
        
    def raster_to_png(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-outsize', self.res, 
                              self.res, '-of', 'PNG', '-ot', 'UInt16', '-scale', 
                              self.min_elevation, self.max_elevation, '0', '65535', 
                              self.input_data, self.output_png]
        print('\n>>> Converting input data to 16-bit PNG')
        subprocess.call(gdal_translate_cmd)

h = HeightMap(resolution=res)
h.generate()

print('\n>>> Completed')