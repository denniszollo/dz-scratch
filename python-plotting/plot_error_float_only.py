import sys
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'TOW [s]', u'3D Error [m]', u'Fix Mode', 'SVs Used']]
print subdf.describe()
print subdf.groupby('Fix Mode').describe()
PERCENTILES = [0.01, 0.05, 0.25, 0.5, 0.68, 0.95, 0.99]                                                       
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
  if i == 2:
    plt.plot(each[u'TOW [s]'], each[u'3D Error [m]'], colors[i])
plt.ylabel("3d Error")
plt.legend(labels)  
plt.subplot(3,1,2)
for i,each in enumerate(dfs): 
   if i == 2: 
     plt.plot(each[u'TOW [s]'], each[u'SVs Used'], colors[i])
plt.ylabel("num_sats")

plt.subplot(3,1,3)
plt.figtext(0.25,0.1, "Statistics\n " + str(m3.describe(percentiles=PERCENTILES)))
import os
plt.savefig(os.path.join(os.path.split(sys.argv[1])[0], 'figures/float_error.png'))
print m1.describe()
print m2.describe()
print m3.describe()
print m4.describe()

