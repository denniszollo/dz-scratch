import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.68, 0.95, 0.99]
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'TOW [s]', u'3D Error [m]', u'2D Error [m]', u'EHPE [m]', u'Fix Mode', 'SVs Used', 'Lat [deg]', 'Lon [deg]']]
print subdf.describe()
m1 = subdf[subdf['Fix Mode'] == 1]
m2 = subdf[subdf['Fix Mode'] == 2]
m3 = subdf[subdf['Fix Mode'] == 3]
m4 = subdf[subdf['Fix Mode'] == 4]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed']
colors = ["rx", "cx", "bx", "gx"]

plt.figure(figsize=[20,8])
plt.subplot(3,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'2D Error [m]'], colors[i])
plt.ylabel("2D Error")
plt.plot(subdf[u'TOW [s]'], subdf[u'EHPE [m]'], colors[i])
plt.legend(labels + ['EHPE'])  

plt.subplot(3,1,2)
for i,each in enumerate(dfs):
  each['diff'] = - each[u'2D Error [m]'] +  each['EHPE [m]']
  plt.plot(each[u'TOW [s]'], each['diff'], colors[i])
for i,each in enumerate(dfs):
  each['diff'] = - each[u'2D Error [m]'] +  each['EHPE [m]']
  plt.plot(each[u'TOW [s]'], each['diff'], colors[i])


plt.subplot(3,1,3)
for i,each in enumerate(dfs):
  plt.figtext(0.15 * i + 0.05 ,0.1, labels[i] + " estimated - actual 2D error:\n" + 
              str((each['2D Error [m]'] - each['EHPE [m]']).describe(percentiles=PERCENTILES)))
plt.savefig("error_vs_estimated.png")
  
plt.figure(figsize=[20,8])
for i,each in enumerate(dfs):
  ax = plt.subplot(4,1,i+1)
  each['diff'].hist(ax=ax)
  plt.title(labels[i])
  plt.xlabel("Estimated minus actual 2D Error")
  plt.ylabel("Number")
plt.savefig("error_est_vs_mode_hist.png")

plt.figure(figsize=[20,8])
ax = plt.subplot(3,1,1)
plt.title("Latitude")
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'Lat [deg]'], colors[i])
plt.plot(df['TOW [s]'], np.ones(len(df['TOW [s]'])) * 37.773367, 'k')
plt.legend(labels + ['actual'])
ax = plt.subplot(3,1,2)
plt.title("Latitude")
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'Lon [deg]'], colors[i])
plt.plot(df['TOW [s]'], np.ones(len(df['TOW [s]'])) * -122.417746, 'k')
plt.legend(labels + ['actual'])
ax = plt.subplot(3,1,3)
plt.title("position")
for i,each in enumerate(dfs): 
  plt.plot(each[u'Lat [deg]'], each[u'Lon [deg]'], colors[i])
plt.plot(37.773367, -122.417746, 'x', markersize=10)
plt.legend(labels + ['actual'])
plt.savefig("time_history.png")
