# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 10:56:53 2017

@author: Vempati's
"""

import matplotlib.pyplot as plt
import matplotlib.cm
 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import pandas as pd
import os	


fig, ax = plt.subplots(figsize=(10,20))

m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=25, lon_0=-4.36,
            llcrnrlon=-127.3, llcrnrlat= 26.1, urcrnrlon=-60.5, urcrnrlat=49.4)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
m.drawcoastlines()

#m.readshapefile('data/us_postcode_bounds/Areas', 'areas')
os.chdir("E:/Opex")
excel_file=pd.ExcelFile("Network Planning Case Study - Opex Analytics.xlsx")
#print df.sheet_names
df=excel_file.parse('Customers')

    
for index,rows in df.iterrows():
    x,y=m(rows[7],rows[6])
    m.plot(x, y, 'o', color='#444444', alpha=0.8)
    
cities =[[41.883993,-87.619706],[32.786330,-96.796253],[39.750000,-104.990000],[33.760001,-84.389996]]
i=1
for rows in cities:
    x,y=m(rows[1],rows[0])
    m.plot(x, y, 's', color='#711919', alpha=0.9)
    plt.annotate('Plant %s'%i, xy=(x, y), xytext=(x+1, y+1),arrowprops=dict(facecolor='black', shrink=0.05))
    i=i+1
    
warehouses=[[43.580123,-116.219041],[42.287672,-74.561318],[33.128095,-95.598595],[34.049002,-117.979948]]

i=1
for rows in warehouses:
    x,y=m(rows[1],rows[0])
    m.plot(x, y, 'o', color='Red', alpha=0.9)
    plt.annotate('warehouse %s'%i, xy=(x, y), xytext=(x+1, y+1),arrowprops=dict(facecolor='blue', shrink=0.05))
    i=i+1

    