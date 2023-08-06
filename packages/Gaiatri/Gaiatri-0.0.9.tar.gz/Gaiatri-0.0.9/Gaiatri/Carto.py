import ipyleaflet
from ipyleaflet import *
from ipyleaflet import Map, basemaps, basemap_to_tiles, Marker
from ipywidgets import Layout
from Gaiatri import Load

satellite = basemaps.Esri.WorldImagery
vector = basemaps.OpenStreetMap.Mapnik
topo = basemaps.OpenTopoMap

def Monocarto(dataset,zoom,basemap,width,height):
  
  m = Map(center=[dataset['latitude'].mean(), dataset['longitude'].mean()], zoom=zoom, basemap=basemap, layout=Layout(width=width, height=height))

  # Add a marker for each location to the layer group
  for i, row in dataset.iterrows():
    marker = Marker(location=[row['latitude'], row['longitude']])
    m.add_layer(marker)
    
    return m
