import sys
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'TOW [s]', u'3D Error [m]', u'Fix Mode', 'SVs Used']]
print subdf.describe()
m1 = subdf[subdf['Fix Mode'] == 1]
m2 = subdf[subdf['Fix Mode'] == 2]
m3 = subdf[subdf['Fix Mode'] == 3]
m4 = subdf[subdf['Fix Mode'] == 4]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed']
colors = ["rx", "cx", "bx", "gx"]

plt.figure(figsize=[20,8])
plt.subplot(2,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'3D Error [m]'], colors[i])
plt.ylabel("3d Error")
plt.legend(labels)  
plt.subplot(2,1,2)
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'SVs Used'], colors[i])
plt.ylabel("num_sats")
plt.show()
