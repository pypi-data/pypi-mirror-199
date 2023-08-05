import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import json_normalize
from math import sin, cos, sqrt, atan2, radians
from Gaiatri import Load # Previously "FileProcessor"

def Querystring(dataset,col,value):
   
  # Query the rows with the name
  results = dataset[dataset[col].str.contains(value)]

  return results

# Find the Lat Lon of velocity of interest
def Querynumeric(dataset,col,min,max):

  v1 = str(min)[:3]

  v2 = str(max)[:3]

  try:
    results = dataset.loc[
        (dataset[col].astype(str).str[:3] >= v1)
        &
        (dataset[col].astype(str).str[:3] <= v2)]
  except ValueError:
    print("Error: Non-numeric values found in 'values' column.")

  return results

def Queryradius(dataset, lat, lon, radius):

  # Define a function to calculate the distance between two points using the Haversine formula
  def haversine(lat1, lon1, lat2, lon2):
      R = 6371  # Earth's radius in kilometers
      d_lat = radians(lat2 - lat1)
      d_lon = radians(lon2 - lon1)
      a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
      c = 2 * atan2(sqrt(a), sqrt(1-a))
      distance = R * c
      return distance

  # Query the rows where the distance to the center point is less than the radius
  dataset['distance'] = dataset.apply(lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1)
  result = dataset[dataset['distance'] <= radius]

  # Display the result
  results = dataset.loc[dataset['distance'] <= radius]

  return results