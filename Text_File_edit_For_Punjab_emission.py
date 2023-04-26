# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Abhinav)s

email: abhinavsharma@iirs.gov.in, abhinaviirs@gmail.com  (official)
       abhiinav.18@gmail.com (personal)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import fiona
import shapely

txt_filename = 'C:\\Users\\Abhinav\\Desktop\\IIRS_work\\FINN_txt_for_Punjab\\GLOB_MOZ4_2021001.txt'

txt_fn = pd.read_csv(txt_filename, delimiter = ',', index_col = False)

# sample_fn defined here for limited columns for visualization and testing purpose
sample_fn = txt_fn.loc[0:100, ['DAY', 'TIME', 'GENVEG', 'LATI', 'LONGI', 'AREA', 'CO2', 'CO', 'H2', 'NO', 'NO2', 'SO2']]

# sample_fn converted to copy of original textfile dataframe for conversion to floaty dataframe
sample_fn = txt_fn.copy(deep=True)

to_exclude = ['DAY', 'TIME', 'GENVEG']
for column in sample_fn:
    if column not in to_exclude:
        sample_fn[column] = sample_fn[column].apply(lambda x: float(x.replace("D", "E")))


# Punjab shapefile did not exist, so we made one
# import geopandas
# st = geopandas.read_file("India_State_Boundary\\India_State_Boundary.shp")
# punj = st[st["Name"]=="Punjab"]

# filepath = "Punjab_shapefile\\"
# punj.to_file(f"{filepath}\\Punjab.shp", driver = 'ESRI Shapefile')

# reading shapefile from fiona

with fiona.open("Punjab_shapefile\\Punjab.shp") as fiona_collection:
    shapefile_record = fiona_collection.next()
    shape = shapely.geometry.asShape(shapefile_record['geometry'])


def check(lon,lat,shape):
    point = shapely.geometry.Point(lon,lat) # longitude, latitude
    if shape.contains(point) == True:
        return 1
    else:
        return 0

check(75.26074,30.4763,shape)
# after extensive testing of shapefile polygon code section using manual lat-lon pair from earthdata search,
# it was found to be working correctly

# running all the points in the text file dataframe

check_return = []

sample_fn['LONGI'][8] = 75.26074
sample_fn['LATI'][8] = 30.4763

for i in range(0,sample_fn.shape[0]):
    checky = check(sample_fn["LONGI"][i],sample_fn["LATI"][i],shape)
    check_return.append(checky)







