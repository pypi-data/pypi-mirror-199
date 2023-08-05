import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import json_normalize
from math import sin, cos, sqrt, atan2, radians

# Universal file saving path
cwd = os.getcwd()

# SINGLE GRAPH
def Monograph(dataset, x_col, y_col, width, height, x_max, y_max, x_label, y_label, graph_title):

  # Pre-set style
  plt.style.use("fivethirtyeight")

  # File saving preps
  file_path = os.path.join(cwd,graph_title + '.svg')

  # Metric
  x = dataset[x_col]
  y = dataset[y_col]

  # Assign graph settings

  plt.figure(figsize=(width,height))

  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(graph_title)

  if x_max != '':
    plt.xlim(0,int(x_max))
  else:
    pass
  
  if y_max != '':
    plt.ylim(0,int(y_max))
  else:
    pass

  plt.plot(x,y)

  plt.savefig(file_path, format="svg")

# MULTI GRAPH
def Multigraph(dataset, x_col, y_col_1, y_col_2, width, height, x_label, y_label_1, y_label_2, graph_title):

  line_1 = 'steelblue'
  line_2 = 'red'

  # File saving preps
  file_path = os.path.join(cwd,graph_title + '.svg')

  # Metric
  x = dataset[x_col]
  y1 = dataset[y_col_1]
  y2 = dataset[y_col_2]


  fig,ax = plt.subplots(figsize=(width, height))

  ax.plot(x, y1, color=line_1, linewidth=3)
  ax.set_xlabel(x_label, fontsize=14)
  ax.set_ylabel(y_label_1, color=line_1, fontsize=16)

  ax2 = ax.twinx()

  ax2.plot(x, y2, color=line_2, linewidth=2)
  ax2.set_ylabel(y_label_2, color=line_2, fontsize=16)

  plt.savefig(file_path, format="svg")