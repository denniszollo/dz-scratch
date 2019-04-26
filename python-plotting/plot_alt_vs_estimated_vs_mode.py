import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.68, 0.95, 0.99]
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'GPS TOW [s]', u'Alt Ellips [m]', u'EVPE [m]', 'Pos Mode' ]]
print subdf.describe()
m1 = subdf[subdf['Pos Mode'] == 1]
m2 = subdf[subdf['Pos Mode'] == 2]
m3 = subdf[subdf['Pos Mode'] == 3]
m4 = subdf[subdf['Pos Mode'] == 4]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed']
colors = ["rx", "cx", "bx", "gx"]

fig = plt.figure(figsize=[20,8])
plt.subplot(2,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'GPS TOW [s]'], each[u'Alt Ellips [m]'], colors[i])
plt.ylabel("Alt")
plt.legend(labels + ['EVPE'])  

plt.subplot(2,1,2)
for i,each in enumerate(dfs): 
   plt.plot(each[u'GPS TOW [s]'], each[u'EVPE [m]'], colors[i])
plt.legend(labels)  
plt.ylabel('EVPE')  

fig.savefig('test.png')
