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
import shapely.geometry

pd.options.mode.chained_assignment = None  # default='warn'

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

with fiona.open("C:\\Users\\Abhinav\\Desktop\\IIRS_work\\FINN_txt_for_Punjab\\Punjab_shapefile\\Punjab.shp") as fiona_collection:
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


# running all the points for a check is computationally expensive task,
# we will run check only on points within Punjab bounds

# Punjab bounds NS -> 29N, 33N
# Punjab bounds WE -> 72E, 84E

# poisoning with known pts. for testing
sample_fn['LONGI'][8] = 75.26074
sample_fn['LATI'][8] = 30.4763

sample_fn['LONGI'][341] = 74.98074
sample_fn['LATI'][341] = 30.7763

sample_fn['LONGI'][211] = 75.36074
sample_fn['LATI'][211] = 30.2763


check_return1 = []
check_retbnds = []

for i in range(0,sample_fn.shape[0]):
    if ((29.0<sample_fn['LATI'][i]<33.0) & (72.0<sample_fn['LONGI'][i]<84.0)):
        check_retbnds.append(i)
        checky = check(sample_fn["LONGI"][i],sample_fn["LATI"][i],shape)
        check_return1.append(checky)
    # check_return.appned(checky)

# returns 2 lists of check_retbnds telling whether the index is in defined bounds
# second list check_return1 gives 1 (true) and 0 (false) for pt. within shapefile


# inserting new column for co_punj
sample_fn.insert(len(sample_fn.columns),'co_firep',np.zeros((len(sample_fn))))

index_1 = []

for i in range(0,len(check_return1)):
    if check_return1[i]==1:
        index_1.append(check_retbnds[i])
    
index_1 = np.array(index_1)

# replacing those values in sample_fn from above indices
sample_fn['co_firep'][index_1] = sample_fn['CO'][index_1]

# making them again as a string
to_exclude = ['DAY', 'TIME', 'GENVEG']
for column in sample_fn:
    if column not in to_exclude:
        sample_fn[column] = sample_fn[column].apply(lambda x: (str(x).replace("E", "D")))

# conversion to string and subsequent dataframe can be problematic for utility,
# therefore we can make a zero string column in actual dataframe and replace with indices found above

txt_fn.insert(len(txt_fn.columns),'CO_FIREP','    0.0000000000D+06')

txt_fn['CO_FIREP'][index_1] = txt_fn['CO'][index_1]

txt_fn.to_csv("test.txt", header=txt_fn.columns, index=None, sep=',', mode='w')
