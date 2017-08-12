# USGS elevation data: https://viewer.nationalmap.gov/basic/

import argparse
import datetime
import re
import sys
import subprocess

GDAL_INFO_BIN = 'bin/gdalinfo.exe'
GDAL_TRANSLATE_BIN = 'bin/gdal_translate.exe'
INPUT_DIR = 'input/'
OUTPUT_DIR = 'output/'

parser = argparse.ArgumentParser(description='Generate a 16-bit PNG' \
                                             'heightmap from USGS data')
parser.add_argument('data', metavar='input_data', 
                    help='Name of the input data (IMG or ArcGrid)')
parser.add_argument('-r', metavar='output_resolution', type=str,
                    help='Resolution of the final output (default 4096x4096)')
args = parser.parse_args()

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
input_data = INPUT_DIR + args.data
output_tif = OUTPUT_DIR + ts + '_geotiff.tif'
output_png = OUTPUT_DIR + ts + '_heightmap.png'
res = args.r

class HeightMap(object):
    def __init__(self, resolution):
        self.res = resolution
        if self.res is None:
            self.res = '4096'
        else:
            self.res = resolution
        self.raster_info = ''
        self.min_elevation = ''
        self.max_elevation = ''

    def generate(self):
        self.raster_to_geotiff()
        self.gdal_info()
        self.find_elevation_range()
        self.geotiff_to_png()

    def raster_to_geotiff(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-co', 'COMPRESS=LZW', '-co', 
                                'PREDICTOR=3', '-co', 'TFW=YES', '-of', 'GTiff', 
                                input_data, output_tif]
        print('>>> Translating raster data to GeoTIFF')
        subprocess.call(gdal_translate_cmd)
        
    def gdal_info(self):
        gdal_info_cmd = [GDAL_INFO_BIN, '-stats', output_tif]
        try:
            print('\n>>> Converting elevation information')
            self.raster_info = str(subprocess.check_output(gdal_info_cmd))
        except subprocess.CalledProcessError as e:
            print("Failed to retrieve raster information:\n", e.output)
            sys.exit(1)
        
    def find_elevation_range(self):
        self.min_elevation = re.findall(r'(?<=STATISTICS_MINIMUM=)\d{1,}', 
                                        self.raster_info)[0]
        self.max_elevation = re.findall(r'(?<=STATISTICS_MAXIMUM=)\d{1,}', 
                                        self.raster_info)[0]
        print('-------------------------------------------------------')
        print('Minimum elevation: {}m'.format(self.min_elevation))
        print('Maximum elevation: {}m'.format(self.max_elevation))
        print('Elevation range: {}m'.format(int(self.max_elevation) - 
                                           int(self.min_elevation)))
        print('-------------------------------------------------------')
        
    def geotiff_to_png(self):
        gdal_translate_cmd = [GDAL_TRANSLATE_BIN, '-outsize', self.res, self.res, 
                                '-of', 'PNG', '-ot', 'UInt16', '-scale', 
                                self.min_elevation, self.max_elevation, 
                                '0', '65535', input_data, output_png]
        print('\n>>> Converting GeoTiff to 16-bit PNG')
        subprocess.call(gdal_translate_cmd)

h = HeightMap(resolution=res)
h.generate()

print('\n>>> Completed')