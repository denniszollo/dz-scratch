import sys
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv(sys.argv[1])
print df.columns
subdf = df[[u'TOW [s]', u'SOG [m/s]', u'COG [deg]', u'Fix Mode', 'SVs Used']].head(5000)
print subdf.describe()
m1 = subdf[subdf['Fix Mode'] == 1]
m2 = subdf[subdf['Fix Mode'] == 2]
m3 = subdf[subdf['Fix Mode'] == 3]
m4 = subdf[subdf['Fix Mode'] == 4]
m5 = subdf[subdf['Fix Mode'] == 5]
m6 = subdf[subdf['Fix Mode'] == 6]

dfs = [m1, m2, m3, m4]
labels = ["spp", "dgps", 'float', 'fixed', 'DR', 'SBAS']
colors = ["rx", "cx", "bx", "gx", 'kx', 'ox']

plt.figure(figsize=[20,8])
plt.subplot(2,1,1)
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'SOG [m/s]'], colors[i])
plt.ylabel("3d Error")
plt.legend(labels)  
plt.subplot(2,1,2)
for i,each in enumerate(dfs): 
  plt.plot(each[u'TOW [s]'], each[u'COG [deg]'], colors[i])
plt.ylabel("num_sats")
plt.show()
plt.savefig("vel_mode.png")
